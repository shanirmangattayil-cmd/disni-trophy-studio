# Disni Trophies app — how to make changes

The owner (Befil, Disni Trophies shop) asks for changes in chat. Work in Malayalam/English mix in the UI, red-gold Disni look.

- Edit the screens in `src/disni_src.html` (shared design source; `__IMGS__` is filled from `src/images.json`).
  Phone-app-only behaviour (sign-in, Android bridge `DisniNative`, WhatsApp share, voice, background remover, updates) is patched in by `src/make_app.py`.
- Build: `python3 src/make_app.py` — writes `app/src/main/assets/index.html` and `web/app/index.html` with a new `disni-web-version` stamp.
- Publish: commit and push to `main`. The Pages workflow publishes `web/`; installed Android apps download the new screens on next open and show a green "Update" bar. No reinstall needed.
- Only Java/manifest changes need a new APK: the build workflow makes it. Without the `DISNI_KEYSTORE_*` secrets it is unsigned (release `unsigned`); it must be signed with the original Disni key or it will not install over the existing app. Bump `release/version.txt` to the build's run number so old apps show the APK update bar.
- One link for everyone: https://shanirmangattayil-cmd.github.io/disni-trophy-studio/ (Android APK button + iPhone web app).
