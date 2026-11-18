package gnomed.it.request;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.FileProvider;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import gnomed.it.R;

/**
 * Icon requests without e-mail and without zip.
 *
 * CandyBar builds a zip (appfilter.xml, appmap.xml, theme_resources.xml, one PNG per app)
 * and hands it to an e-mail app. Many AI agents and chats accept images and text but no
 * zip, so Gnomed keeps a copy of the last request and can also
 *  - share it as separate files: request.txt (app, ComponentInfo, file) + every icon PNG,
 *  - share / save the zip with any app (Files, Drive, Telegram, ...),
 *  - copy the app list as text.
 */
public final class RequestExport {

    /** Folder inside the app cache, see res/xml/gnomed_share_paths.xml. */
    private static final String DIR = "gnomed-request";
    private static final String ZIP = "GnomedRequest.zip";
    private static final Pattern ITEM = Pattern.compile(
            "<!--\\s*(.*?)\\s*-->\\s*<item\\s+component=\"(ComponentInfo\\{[^}]*\\})\"\\s+drawable=\"([^\"]+)\"",
            Pattern.DOTALL);

    private RequestExport() {
    }

    private static String authority(Context c) {
        return c.getPackageName() + ".gnomed.share";
    }

    @NonNull
    private static File dir(Context c) {
        return new File(c.getCacheDir(), DIR);
    }

    /** The kept copy of the last request, or null if there is none. */
    @Nullable
    public static File last(@NonNull Context c) {
        File f = new File(dir(c), ZIP);
        return f.isFile() && f.length() > 0 ? f : null;
    }

    /** Copy CandyBar's request zip into our cache (CandyBar deletes or forgets its own copy). */
    @Nullable
    public static File keep(@NonNull Context c, @Nullable String zipPath) {
        if (zipPath == null) return null;
        File src = new File(zipPath);
        if (!src.isFile()) return null;
        File d = dir(c);
        deleteTree(d);
        //noinspection ResultOfMethodCallIgnored
        d.mkdirs();
        File out = new File(d, ZIP);
        try (InputStream in = new FileInputStream(src); OutputStream os = new FileOutputStream(out)) {
            copy(in, os);
            return out;
        } catch (IOException e) {
            return null;
        }
    }

    /** "Label | ComponentInfo{pkg/activity} | drawable.png" for every app in the request. */
    @NonNull
    public static String summary(@NonNull Context c, @NonNull File zip) throws IOException {
        String appfilter = null;
        int pngs = 0;
        try (ZipInputStream zin = new ZipInputStream(new FileInputStream(zip))) {
            ZipEntry e;
            while ((e = zin.getNextEntry()) != null) {
                String name = new File(e.getName()).getName().toLowerCase(Locale.ROOT);
                if (name.equals("appfilter.xml")) appfilter = readAll(zin);
                else if (name.endsWith(".png")) pngs++;
            }
        }
        if (appfilter == null) throw new IOException("appfilter.xml missing in the request");
        StringBuilder rows = new StringBuilder();
        int n = 0;
        Matcher m = ITEM.matcher(appfilter);
        while (m.find()) {
            rows.append(m.group(1)).append(" | ").append(m.group(2)).append(" | ").append(m.group(3)).append(".png\n");
            n++;
        }
        return c.getString(R.string.gnomed_request_text_header, n, pngs) + "\n" + rows;
    }

    public static void shareZip(@NonNull Activity a, @NonNull File zip) {
        try {
            Uri uri = FileProvider.getUriForFile(a, authority(a), zip);
            Intent send = new Intent(Intent.ACTION_SEND)
                    .setType("application/zip")
                    .putExtra(Intent.EXTRA_STREAM, uri)
                    .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            send.setClipData(ClipData.newRawUri("request", uri));
            a.startActivity(Intent.createChooser(send, a.getString(R.string.gnomed_request_share_zip)));
        } catch (RuntimeException ex) {
            fail(a, ex);
        }
    }

    /** Unpack the zip and share request.txt + every PNG; the list also goes in EXTRA_TEXT. */
    public static void shareFiles(@NonNull Activity a, @NonNull File zip) {
        try {
            File d = new File(dir(a), "files");
            deleteTree(d);
            if (!d.mkdirs() && !d.isDirectory()) throw new IOException("cannot create " + d);
            String text = summary(a, zip);
            ArrayList<Uri> uris = new ArrayList<>();
            File txt = new File(d, "request.txt");
            try (OutputStream os = new FileOutputStream(txt)) {
                os.write(text.getBytes(StandardCharsets.UTF_8));
            }
            uris.add(FileProvider.getUriForFile(a, authority(a), txt));
            try (ZipInputStream zin = new ZipInputStream(new FileInputStream(zip))) {
                ZipEntry e;
                while ((e = zin.getNextEntry()) != null) {
                    if (e.isDirectory()) continue;
                    String name = new File(e.getName()).getName();
                    if (!name.toLowerCase(Locale.ROOT).endsWith(".png")) continue;  // xml files are in request.txt
                    File f = new File(d, name);
                    try (OutputStream os = new FileOutputStream(f)) {
                        copy(zin, os);
                    }
                    uris.add(FileProvider.getUriForFile(a, authority(a), f));
                }
            }
            Intent send = new Intent(Intent.ACTION_SEND_MULTIPLE)
                    .setType("*/*")
                    .putParcelableArrayListExtra(Intent.EXTRA_STREAM, uris)
                    .putExtra(Intent.EXTRA_TEXT, text)
                    .addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            ClipData clip = ClipData.newRawUri("request", uris.get(0));
            for (int i = 1; i < uris.size(); i++) clip.addItem(new ClipData.Item(uris.get(i)));
            send.setClipData(clip);
            a.startActivity(Intent.createChooser(send, a.getString(R.string.gnomed_request_share_files)));
        } catch (IOException | RuntimeException ex) {
            fail(a, ex);
        }
    }

    public static void copyList(@NonNull Activity a, @NonNull File zip) {
        try {
            ClipboardManager cm = (ClipboardManager) a.getSystemService(Context.CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("Gnomed request", summary(a, zip)));
            Toast.makeText(a, R.string.gnomed_request_copied, Toast.LENGTH_SHORT).show();
        } catch (IOException | RuntimeException ex) {
            fail(a, ex);
        }
    }

    private static void fail(Activity a, Exception ex) {
        Toast.makeText(a, a.getString(R.string.gnomed_request_failed, String.valueOf(ex.getMessage())),
                Toast.LENGTH_LONG).show();
    }

    private static String readAll(InputStream in) throws IOException {
        ByteArrayOutputStream bo = new ByteArrayOutputStream();
        copy(in, bo);
        return bo.toString("UTF-8");
    }

    private static void copy(InputStream in, OutputStream out) throws IOException {
        byte[] buf = new byte[64 * 1024];
        int n;
        while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
    }

    private static void deleteTree(File f) {
        if (f.isDirectory()) {
            File[] kids = f.listFiles();
            if (kids != null) for (File k : kids) deleteTree(k);
        }
        //noinspection ResultOfMethodCallIgnored
        f.delete();
    }
}
