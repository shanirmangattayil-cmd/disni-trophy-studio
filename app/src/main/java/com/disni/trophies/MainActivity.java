package com.disni.trophies;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.ContactsContract;
import android.provider.MediaStore;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.core.content.FileProvider;
import androidx.webkit.WebViewAssetLoader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;

/** Disni Trophy Studio: the design app runs as a web page inside this WebView; this class adds the phone features. */
public class MainActivity extends Activity {
    static final String HOME = "https://appassets.androidplatform.net/assets/index.html";
    static final String AUTH = "com.disni.trophies.files";
    static final int PICK = 41, VOICE = 43, CONTACT = 44;
    /** The app's screens are also published here; newer copies are downloaded and used without reinstalling. */
    static final String LIVE_URL = "https://shanirmangattayil-cmd.github.io/disni-trophy-studio/app/index.html";
    static final Pattern VER = Pattern.compile("name=\"disni-web-version\" content=\"(\\d+)\"");
    long lastCheck = 0;
    WebView web;
    ValueCallback<Uri[]> pending;
    File cameraFile;
    Uri cameraUri;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        web = new WebView(this);
        web.setBackgroundColor(0xFF7A0716);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this)).build();
        web.setWebViewClient(new WebViewClient() {
            @Override public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest r) {
                Uri u = r.getUrl();
                if ("appassets.androidplatform.net".equals(u.getHost()) && "/assets/index.html".equals(u.getPath())) {
                    File live = liveFile();
                    if (live.exists() && versionOf(live) > bundledVersion()) {
                        try {
                            WebResourceResponse res = new WebResourceResponse("text/html", "utf-8", new FileInputStream(live));
                            HashMap<String, String> h = new HashMap<>(); h.put("Cache-Control", "no-store"); res.setResponseHeaders(h);
                            return res;
                        } catch (Exception ignored) { }
                    }
                }
                return loader.shouldInterceptRequest(u);
            }
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                Uri u = r.getUrl();
                if ("appassets.androidplatform.net".equals(u.getHost())) return false;
                openExternal(u.toString());
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {
            @Override public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (pending != null) pending.onReceiveValue(null);
                pending = cb;
                boolean images = false, anyType = false;
                String[] acc = p.getAcceptTypes();
                if (acc != null) for (String a : acc) { if (a == null) continue; for (String part : a.split(",")) { String t = part.trim(); if (t.startsWith("image/")) images = true; else if (!t.isEmpty()) anyType = true; } }
                if (!images && !anyType) anyType = true;
                Intent cam = images ? cameraIntent() : null;
                try {
                    if (p.isCaptureEnabled() && cam != null) { startActivityForResult(cam, PICK); return true; }
                    Intent i = new Intent(Intent.ACTION_GET_CONTENT);
                    i.addCategory(Intent.CATEGORY_OPENABLE);
                    i.setType(images && !anyType ? "image/*" : "*/*");
                    Intent chooser = Intent.createChooser(i, images ? "Photo തിരഞ്ഞെടുക്കൂ" : "File തിരഞ്ഞെടുക്കൂ");
                    if (cam != null) chooser.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Intent[]{cam});
                    startActivityForResult(chooser, PICK);
                } catch (ActivityNotFoundException e) { pending = null; return false; }
                return true;
            }
        });
        web.addJavascriptInterface(new Bridge(), "DisniNative");
        if (b != null) web.restoreState(b); else web.loadUrl(HOME);
    }

    File liveFile() { return new File(new File(getFilesDir(), "live"), "index.html"); }

    static long parseVersion(String head) { Matcher m = VER.matcher(head); return m.find() ? Long.parseLong(m.group(1)) : 0; }

    long versionOf(File f) {
        try (InputStream in = new FileInputStream(f)) { byte[] b = new byte[4096]; int n = in.read(b); return n > 0 ? parseVersion(new String(b, 0, n, "UTF-8")) : 0; }
        catch (Exception e) { return 0; }
    }

    long bundled = -1;
    long bundledVersion() {
        if (bundled >= 0) return bundled;
        try (InputStream in = getAssets().open("index.html")) { byte[] b = new byte[4096]; int n = in.read(b); bundled = n > 0 ? parseVersion(new String(b, 0, n, "UTF-8")) : 0; }
        catch (Exception e) { bundled = 0; }
        return bundled;
    }

    long currentVersion() { File live = liveFile(); long lv = live.exists() ? versionOf(live) : 0; return Math.max(lv, bundledVersion()); }

    /** Downloads the newest published screens in the background; the page offers to reload when one arrives. */
    void checkLive() {
        long now = System.currentTimeMillis();
        if (now - lastCheck < 5 * 60 * 1000) return;
        lastCheck = now;
        new Thread(() -> {
            HttpURLConnection c = null;
            try {
                c = (HttpURLConnection) new URL(LIVE_URL + "?t=" + now).openConnection();
                c.setConnectTimeout(10000); c.setReadTimeout(30000); c.setUseCaches(false);
                if (c.getResponseCode() != 200) return;
                ByteArrayOutputStream bo = new ByteArrayOutputStream();
                try (InputStream in = c.getInputStream()) { byte[] buf = new byte[16384]; int n; while ((n = in.read(buf)) > 0) bo.write(buf, 0, n); }
                byte[] data = bo.toByteArray();
                String text = new String(data, "UTF-8");
                long v = parseVersion(text.length() > 4096 ? text.substring(0, 4096) : text);
                if (v <= currentVersion() || !text.contains("DisniNative") || !text.trim().endsWith("</html>")) return;
                File dir = liveFile().getParentFile(); dir.mkdirs();
                File tmp = new File(dir, "index.html.tmp");
                try (FileOutputStream o = new FileOutputStream(tmp)) { o.write(data); }
                if (!tmp.renameTo(liveFile())) { liveFile().delete(); tmp.renameTo(liveFile()); }
                final long nv = v;
                runOnUiThread(() -> js("disniWebUpdated", String.valueOf(nv)));
            } catch (Exception ignored) {
            } finally { if (c != null) c.disconnect(); }
        }).start();
    }

    @Override protected void onResume() { super.onResume(); checkLive(); }

    Intent cameraIntent() {
        try {
            File dir = new File(getCacheDir(), "camera"); dir.mkdirs();
            cameraFile = new File(dir, "disni-" + System.currentTimeMillis() + ".jpg");
            cameraUri = FileProvider.getUriForFile(this, AUTH, cameraFile);
            Intent c = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            c.putExtra(MediaStore.EXTRA_OUTPUT, cameraUri);
            c.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION);
            c.setClipData(ClipData.newRawUri("photo", cameraUri));
            return c;
        } catch (Exception e) { cameraFile = null; cameraUri = null; return null; }
    }

    void openExternal(String url) {
        try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); }
        catch (Exception e) { Toast.makeText(this, "ഈ link തുറക്കാൻ app ഇല്ല", Toast.LENGTH_SHORT).show(); }
    }

    void js(String fn, String arg) { web.evaluateJavascript("window." + fn + "&&" + fn + "(" + arg + ")", null); }

    @Override protected void onActivityResult(int req, int res, Intent data) {
        if (req == VOICE) {
            String said = null;
            if (res == RESULT_OK && data != null) {
                java.util.ArrayList<String> r = data.getStringArrayListExtra(android.speech.RecognizerIntent.EXTRA_RESULTS);
                if (r != null && !r.isEmpty()) said = r.get(0);
            }
            js("disniVoice", said == null ? "null" : JSONObject.quote(said));
            return;
        }
        if (req == CONTACT) {
            String out = "null";
            if (res == RESULT_OK && data != null && data.getData() != null) {
                try (Cursor c = getContentResolver().query(data.getData(), new String[]{
                        ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER}, null, null, null)) {
                    if (c != null && c.moveToFirst()) {
                        JSONObject o = new JSONObject(); o.put("name", c.getString(0)); o.put("num", c.getString(1)); out = JSONObject.quote(o.toString());
                    }
                } catch (Exception ignored) { }
            }
            js("disniContact", out);
            return;
        }
        if (req != PICK || pending == null) { super.onActivityResult(req, res, data); return; }
        Uri[] out = null;
        if (res == RESULT_OK) {
            if (data != null && data.getData() != null && !data.getData().equals(cameraUri)) out = new Uri[]{data.getData()};
            else if (cameraFile != null && cameraFile.exists() && cameraFile.length() > 0) out = new Uri[]{cameraUri};
        }
        cameraFile = null;
        pending.onReceiveValue(out);
        pending = null;
    }

    @Override public void onBackPressed() {
        web.evaluateJavascript("window.disniBack?window.disniBack():false", v -> { if (!"true".equals(v)) MainActivity.super.onBackPressed(); });
    }

    @Override protected void onSaveInstanceState(Bundle b) { super.onSaveInstanceState(b); web.saveState(b); }

    boolean installed(String pkg) {
        try { getPackageManager().getPackageInfo(pkg, 0); return true; } catch (PackageManager.NameNotFoundException e) { return false; }
    }

    Uri cacheFile(String name, byte[] bytes) throws Exception {
        File dir = new File(getCacheDir(), "share"); dir.mkdirs();
        File f = new File(dir, name.replaceAll("[^\\w.\\- ]", "_"));
        try (FileOutputStream o = new FileOutputStream(f)) { o.write(bytes); }
        return FileProvider.getUriForFile(this, AUTH, f);
    }

    /** Writes a file into the phone's shared Pictures or Download folder under "Disni Trophies". */
    boolean saveShared(String name, String mime, byte[] bytes, boolean picture, boolean overwrite) {
        try {
            if (Build.VERSION.SDK_INT >= 29) {
                ContentResolver cr = getContentResolver();
                Uri coll = picture ? MediaStore.Images.Media.EXTERNAL_CONTENT_URI : MediaStore.Downloads.EXTERNAL_CONTENT_URI;
                String rel = (picture ? Environment.DIRECTORY_PICTURES : Environment.DIRECTORY_DOWNLOADS) + "/Disni Trophies/";
                Uri target = null;
                if (overwrite) try (Cursor c = cr.query(coll, new String[]{MediaStore.MediaColumns._ID},
                        MediaStore.MediaColumns.DISPLAY_NAME + "=? AND " + MediaStore.MediaColumns.RELATIVE_PATH + "=?", new String[]{name, rel}, null)) {
                    if (c != null && c.moveToFirst()) target = Uri.withAppendedPath(coll, String.valueOf(c.getLong(0)));
                }
                if (target == null) {
                    ContentValues v = new ContentValues();
                    v.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
                    v.put(MediaStore.MediaColumns.MIME_TYPE, mime);
                    v.put(MediaStore.MediaColumns.RELATIVE_PATH, rel);
                    target = cr.insert(coll, v);
                }
                if (target == null) return false;
                try (OutputStream o = cr.openOutputStream(target, "wt")) { o.write(bytes); }
                return true;
            }
            File d = new File(getExternalFilesDir(picture ? Environment.DIRECTORY_PICTURES : null), "Disni Trophies"); d.mkdirs();
            try (FileOutputStream o = new FileOutputStream(new File(d, name))) { o.write(bytes); }
            return true;
        } catch (Exception e) { return false; }
    }

    class Bridge {
        @JavascriptInterface public int versionCode() { return BuildConfig.VERSION_CODE; }
        @JavascriptInterface public String webVersion() { return String.valueOf(currentVersion()); }
        @JavascriptInterface public void open(String url) { runOnUiThread(() -> openExternal(url)); }
        @JavascriptInterface public void copy(String text) {
            runOnUiThread(() -> { ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE); if (cm != null) cm.setPrimaryClip(ClipData.newPlainText("Disni", text)); });
        }
        @JavascriptInterface public void voice(String lang) {
            runOnUiThread(() -> {
                Intent i = new Intent(android.speech.RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                i.putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE_MODEL, android.speech.RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                String l = (lang == null || lang.isEmpty()) ? "ml-IN" : lang;
                i.putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE, l);
                i.putExtra(android.speech.RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, l);
                i.putExtra(android.speech.RecognizerIntent.EXTRA_PROMPT, l.startsWith("ml") ? "പറയൂ…" : "Speak now…");
                try { startActivityForResult(i, VOICE); } catch (Exception e) { js("disniVoice", "null"); }
            });
        }
        @JavascriptInterface public void pickContact() {
            runOnUiThread(() -> {
                try { startActivityForResult(new Intent(Intent.ACTION_PICK, ContactsContract.CommonDataKinds.Phone.CONTENT_URI), CONTACT); }
                catch (Exception e) { js("disniContact", "null"); }
            });
        }
        @JavascriptInterface public String waApps() {
            StringBuilder sb = new StringBuilder();
            if (installed("com.whatsapp.w4b")) sb.append("w4b");
            if (installed("com.whatsapp")) { if (sb.length() > 0) sb.append(','); sb.append("wa"); }
            return sb.toString();
        }
        /** Opens WhatsApp with the design image and message attached; with a number it goes straight to that chat. */
        @JavascriptInterface public boolean shareWhatsApp(String app, String number, String text, String name, String b64) {
            try {
                Uri u = cacheFile(name, Base64.decode(b64, Base64.DEFAULT));
                Intent i = new Intent(Intent.ACTION_SEND);
                i.setType("image/png");
                i.putExtra(Intent.EXTRA_STREAM, u);
                i.putExtra(Intent.EXTRA_TEXT, text);
                i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                String pkg = "w4b".equals(app) ? "com.whatsapp.w4b" : "wa".equals(app) ? "com.whatsapp" : null;
                if (pkg != null && installed(pkg)) {
                    i.setPackage(pkg);
                    if (number != null && !number.isEmpty()) i.putExtra("jid", number + "@s.whatsapp.net");
                    runOnUiThread(() -> startActivity(i));
                } else runOnUiThread(() -> startActivity(Intent.createChooser(i, "Share")));
                return true;
            } catch (Exception e) { return false; }
        }
        @JavascriptInterface public boolean shareImage(String name, String b64) {
            try {
                Uri u = cacheFile(name, Base64.decode(b64, Base64.DEFAULT));
                Intent i = new Intent(Intent.ACTION_SEND); i.setType("image/png"); i.putExtra(Intent.EXTRA_STREAM, u);
                i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                runOnUiThread(() -> startActivity(Intent.createChooser(i, "Share")));
                return true;
            } catch (Exception e) { return false; }
        }
        @JavascriptInterface public boolean saveImage(String name, String b64) { return saveShared(name, "image/png", Base64.decode(b64, Base64.DEFAULT), true, false); }
        @JavascriptInterface public boolean saveText(String name, String text) { return saveShared(name, "application/json", text.getBytes(StandardCharsets.UTF_8), false, true); }
    }
}
