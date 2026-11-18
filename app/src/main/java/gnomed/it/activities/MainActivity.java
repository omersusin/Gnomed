package gnomed.it.activities;

import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.material.navigation.NavigationView;

import java.io.File;

import candybar.lib.activities.CandyBarMainActivity;
import candybar.lib.applications.CandyBarApplication;
import candybar.lib.fragments.RequestFragment;
import candybar.lib.fragments.dialog.IntentChooserFragment;

import gnomed.it.R;
import gnomed.it.licenses.License;
import gnomed.it.request.RequestExport;
import gnomed.it.style.StyleSwitcher;

public class MainActivity extends CandyBarMainActivity {

    /** Extra used by the "Icon style" app shortcut (res/xml/shortcuts.xml). */
    private static final String EXTRA_OPEN = "gnomed_open";

    @NonNull
    @Override
    public ActivityConfiguration onInit() {
        return new ActivityConfiguration()
                .setLicenseCheckerEnabled(License.isLicenseCheckerEnabled())
                .setLicenseKey(License.getLicenseKey())
                .setRandomString(License.getRandomString())
                .setDonationProductsId(License.getDonationProductsId())
                .setPremiumRequestProducts(License.getPremiumRequestProductsId(), License.getPremiumRequestProductsCount());
    }

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        addStyleEntries();
        if (savedInstanceState == null) handleOpenExtra(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        handleOpenExtra(intent);
    }

    /**
     * Drawer: an "Icon style" entry, and the style popup on top of the Apply screen
     * (the library still opens Apply; the popup lets the user pick the style first).
     */
    private void addStyleEntries() {
        NavigationView nav = findViewById(candybar.lib.R.id.navigation_view);
        if (nav == null) return;
        DrawerLayout drawer = findViewById(candybar.lib.R.id.drawer_layout);

        MenuItem style = nav.getMenu().add(Menu.NONE, R.id.gnomed_nav_style, Menu.NONE, R.string.gnomed_style_title);
        style.setIcon(R.drawable.ic_gnomed_style);
        style.setOnMenuItemClickListener(item -> {
            if (drawer != null) drawer.closeDrawers();
            StyleSwitcher.showPicker(this);
            return true;   // handled here; the library never sees this item
        });

        MenuItem export = nav.getMenu().add(Menu.NONE, R.id.gnomed_nav_request, Menu.NONE, R.string.gnomed_request_title);
        export.setIcon(candybar.lib.R.drawable.ic_toolbar_share);
        export.setOnMenuItemClickListener(item -> {
            if (drawer != null) drawer.closeDrawers();
            File last = RequestExport.last(this);
            if (last == null) {
                android.widget.Toast.makeText(this, R.string.gnomed_request_none, android.widget.Toast.LENGTH_LONG).show();
            } else {
                showExportChoices(last);
            }
            return true;
        });

        MenuItem apply = nav.getMenu().findItem(candybar.lib.R.id.navigation_view_apply);
        if (apply != null) {
            apply.setOnMenuItemClickListener(item -> {
                StyleSwitcher.showPicker(this);
                return false;  // let the library continue to the Apply screen
            });
        }
    }

    private void handleOpenExtra(@Nullable Intent intent) {
        if (intent != null && "style".equals(intent.getStringExtra(EXTRA_OPEN))) {
            intent.removeExtra(EXTRA_OPEN);
            getWindow().getDecorView().post(() -> StyleSwitcher.showPicker(this));
        }
    }

    /**
     * CandyBar calls this when the request zip is ready, with an e-mail intent. Gnomed keeps a
     * copy of the zip and offers ways that need neither e-mail nor zip support (AI agents,
     * chats): images + text, the zip itself, or the app list as text.
     */
    @Override
    public void onRequestBuilt(Intent intent, int type) {
        if (type != IntentChooserFragment.ICON_REQUEST || intent == null) {
            super.onRequestBuilt(intent, type);
            return;
        }
        File kept = RequestExport.keep(this, CandyBarApplication.sZipPath);
        if (kept == null) {
            super.onRequestBuilt(intent, type);
            return;
        }
        String[] items = {
                getString(R.string.gnomed_request_email, appLabel(intent.getComponent())),
                getString(R.string.gnomed_request_share_files),
                getString(R.string.gnomed_request_share_zip),
                getString(R.string.gnomed_request_copy),
        };
        new AlertDialog.Builder(this)
                .setTitle(R.string.gnomed_request_title)
                .setItems(items, (d, which) -> {
                    if (which == 0) {
                        super.onRequestBuilt(intent, type);          // the library's e-mail draft
                        return;
                    }
                    super.onRequestBuilt(null, type);                // bookkeeping only (marks the apps as requested)
                    runExport(which, kept);
                })
                .setNegativeButton(android.R.string.cancel, (d, w) -> cancelRequest())
                .setOnCancelListener(d -> cancelRequest())
                .show();
    }

    /** Drawer entry: export the last request again (any of the three ways). */
    private void showExportChoices(@NonNull File zip) {
        String[] items = {
                getString(R.string.gnomed_request_share_files),
                getString(R.string.gnomed_request_share_zip),
                getString(R.string.gnomed_request_copy),
        };
        new AlertDialog.Builder(this)
                .setTitle(R.string.gnomed_request_title)
                .setItems(items, (d, which) -> runExport(which + 1, zip))
                .setNegativeButton(android.R.string.cancel, null)
                .show();
    }

    private void runExport(int which, @NonNull File zip) {
        if (which == 1) RequestExport.shareFiles(this, zip);
        else if (which == 2) RequestExport.shareZip(this, zip);
        else RequestExport.copyList(this, zip);
    }

    /** Same as the library's "cancel" in its e-mail chooser: nothing is sent or counted. */
    private void cancelRequest() {
        if (CandyBarApplication.sZipPath != null) {
            //noinspection ResultOfMethodCallIgnored
            new File(CandyBarApplication.sZipPath).delete();
        }
        RequestFragment.sSelectedRequests = null;
        CandyBarApplication.sRequestProperty = null;
        CandyBarApplication.sZipPath = null;
    }

    @NonNull
    private String appLabel(@Nullable ComponentName cn) {
        if (cn == null) return getString(R.string.gnomed_request_email_app);
        try {
            PackageManager pm = getPackageManager();
            return pm.getApplicationInfo(cn.getPackageName(), 0).loadLabel(pm).toString();
        } catch (PackageManager.NameNotFoundException e) {
            return cn.getPackageName();
        }
    }
}
