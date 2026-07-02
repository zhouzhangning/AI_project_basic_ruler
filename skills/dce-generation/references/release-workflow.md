# DCE Release Workflow

Use this reference for build, package, official release, and Gitee update tasks.

## Versioning

- The app version lives in `src/excel_report_editor/app_info.py`.
- Official releases must bump `APP_VERSION` before building.
- The build folder and EXE name derive from `APP_EXE_BASENAME = f"DCE_v{APP_VERSION}"`.

## Local Test Build

For local EXE testing without publishing:

```powershell
$env:PYTHONPATH='D:\test\DCE_V1.1_clean\.build_deps'
python src\excel_report_editor\build_exe.py --clean
python tools\package_release.py
```

If clean build fails with `PermissionError` inside `DCE_v...`, check for a running old EXE and stop it before retrying.

## Official Release

Use the official script for formal releases:

```powershell
$env:PYTHONPATH='D:\test\DCE_V1.1_clean\.build_deps'
python tools\official_build_release.py
```

The script should generate:

- `DCE_vVERSION` build folder,
- `releases/DCE_vVERSION.zip` local full zip,
- `releases/DCE_vVERSION.zip.part001...` full split parts for Gitee,
- `releases/patch_BASE_to_VERSION.zip`,
- `releases/update.json`,
- update/rollback scripts,
- an entry in `打包发布记录.md`.

Do not upload or track the full zip in Gitee. Track split parts, patch zip, update scripts, `update.json`, version/source changes, and release record.

## Git/Gitee Notes

- Check `git status --short` before staging.
- Do not stage unrelated untracked local development folders unless the user explicitly requests it.
- New release parts may be ignored by `.gitignore`; add them with `git add -f`.
- If Gitee rejects push due to remote changes, fetch and rebase only the release commit(s) onto latest `origin/main`. Avoid replaying old duplicate history after forced remote cleanup.
- After push, confirm `HEAD -> main, origin/main` points to the release commit.

## Baseline Rules

- `release_baseline.json` controls the patch base.
- Do not promote a new baseline unless the user explicitly asks and coworkers are known to be on the new version.
- If older versions were cleaned, ensure `update.json` does not advertise unavailable old patch routes.
