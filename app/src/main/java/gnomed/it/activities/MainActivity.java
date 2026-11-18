package gnomed.it.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.drawerlayout.widget.DrawerLayout;

import com.google.android.material.navigation.NavigationView;

import candybar.lib.activities.CandyBarMainActivity;

import gnomed.it.R;
import gnomed.it.licenses.License;
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
}
