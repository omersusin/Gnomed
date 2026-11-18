package gnomed.it.style;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageInstaller;
import android.net.Uri;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.widget.FrameLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import gnomed.it.R;

/**
 * In-app icon style switch.
 *
 * Launchers read an icon pack's appfilter.xml and drawables straight from the
 * installed APK, so a style cannot be changed at runtime inside one APK. Every
 * style is therefore built as its own APK with the SAME package name and signing
 * key (Gradle flavors). Choosing a style downloads that APK from the GitHub
 * release and installs it as an update of this app; the launcher then re-reads
 * the pack.
 */
public final class StyleSwitcher {

    /** Must match the Gradle flavors and pack/styles.json. */
    static final String[] STYLES = {"faithful", "disc", "rimmed", "symbol"};

    private static final ExecutorService IO = Executors.newSingleThreadExecutor();

    private StyleSwitcher() {
    }

    @NonNull
    public static String currentStyle(@NonNull Activity activity) {
        return activity.getString(R.string.gnomed_style);
    }

    /** Style list; the current style is pre-selected. */
    public static void showPicker(@NonNull Activity activity) {
        String[] labels = activity.getResources().getStringArray(R.array.gnomed_style_labels);
        int current = Arrays.asList(STYLES).indexOf(currentStyle(activity));
        new AlertDialog.Builder(activity)
                .setTitle(R.string.gnomed_style_title)
                .setSingleChoiceItems(labels, current, (dialog, which) -> {
                    dialog.dismiss();
                    if (which != current) confirm(activity, STYLES[which], labels[which]);
                })
                .setNegativeButton(R.string.gnomed_style_keep, null)
                .show();
    }

    private static void confirm(Activity activity, String style, String label) {
        new AlertDialog.Builder(activity)
                .setTitle(label)
                .setMessage(activity.getString(R.string.gnomed_style_confirm, label))
                .setPositiveButton(R.string.gnomed_style_switch, (d, w) -> download(activity, style))
                .setNegativeButton(android.R.string.cancel, null)
                .show();
    }

    private static void download(Activity activity, String style) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O
                && !activity.getPackageManager().canRequestPackageInstalls()) {
            new AlertDialog.Builder(activity)
                    .setTitle(R.string.gnomed_style_permission_title)
                    .setMessage(R.string.gnomed_style_permission)
                    .setPositiveButton(R.string.gnomed_style_open_settings, (d, w) ->
                            activity.startActivity(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                                    Uri.parse("package:" + activity.getPackageName()))))
                    .setNegativeButton(android.R.string.cancel, null)
                    .show();
            return;
        }

        ProgressBar bar = new ProgressBar(activity, null, android.R.attr.progressBarStyleHorizontal);
        bar.setIndeterminate(true);
        FrameLayout box = new FrameLayout(activity);
        int pad = Math.round(24 * activity.getResources().getDisplayMetrics().density);
        box.setPadding(pad, pad / 2, pad, 0);
        box.addView(bar);
        AlertDialog progress = new AlertDialog.Builder(activity)
                .setTitle(R.string.gnomed_style_downloading)
                .setView(box)
                .setCancelable(false)
                .show();

        Handler main = new Handler(Looper.getMainLooper());
        String url = activity.getString(R.string.gnomed_release_url, style);
        File apk = new File(activity.getCacheDir(), "gnomed-" + style + ".apk");
        IO.execute(() -> {
            try {
                fetch(url, apk, (done, total) -> main.post(() -> {
                    if (total > 0) {
                        bar.setIndeterminate(false);
                        bar.setMax(1000);
                        bar.setProgress((int) (done * 1000 / total));
                    }
                }));
                main.post(() -> {
                    progress.dismiss();
                    install(activity, apk);
                });
            } catch (IOException e) {
                main.post(() -> {
                    progress.dismiss();
                    Toast.makeText(activity, activity.getString(R.string.gnomed_style_failed, e.getMessage()),
                            Toast.LENGTH_LONG).show();
                });
            }
        });
    }

    private interface Progress {
        void update(long done, long total);
    }

    private static void fetch(String url, File target, Progress progress) throws IOException {
        HttpURLConnection c = (HttpURLConnection) new URL(url).openConnection();
        c.setInstanceFollowRedirects(true);   // GitHub release links redirect to the file host
        c.setConnectTimeout(20000);
        c.setReadTimeout(30000);
        try {
            int code = c.getResponseCode();
            if (code != HttpURLConnection.HTTP_OK) throw new IOException("HTTP " + code);
            long total = c.getContentLength();   // int variant: minSdk 21
            try (InputStream in = c.getInputStream(); OutputStream out = new FileOutputStream(target)) {
                byte[] buf = new byte[64 * 1024];
                long done = 0;
                int n;
                while ((n = in.read(buf)) > 0) {
                    out.write(buf, 0, n);
                    done += n;
                    progress.update(done, total);
                }
            }
        } finally {
            c.disconnect();
        }
    }

    private static void install(Activity activity, File apk) {
        try {
            PackageInstaller installer = activity.getPackageManager().getPackageInstaller();
            PackageInstaller.SessionParams params =
                    new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
            params.setAppPackageName(activity.getPackageName());
            int id = installer.createSession(params);
            try (PackageInstaller.Session session = installer.openSession(id)) {
                try (InputStream in = new FileInputStream(apk);
                     OutputStream out = session.openWrite("base.apk", 0, apk.length())) {
                    byte[] buf = new byte[64 * 1024];
                    int n;
                    while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                    session.fsync(out);
                }
                int flags = PendingIntent.FLAG_UPDATE_CURRENT
                        | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ? PendingIntent.FLAG_MUTABLE : 0);
                Intent result = new Intent(activity, StyleInstallReceiver.class);
                PendingIntent pi = PendingIntent.getBroadcast(activity, id, result, flags);
                session.commit(pi.getIntentSender());
            }
        } catch (IOException | RuntimeException e) {
            Toast.makeText(activity, activity.getString(R.string.gnomed_style_failed, e.getMessage()),
                    Toast.LENGTH_LONG).show();
        }
    }
}
