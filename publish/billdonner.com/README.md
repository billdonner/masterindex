# billdonner.com publication bundle

`apps/` is generated from `current/index.json` by:

```sh
python3 tools/generate_billdonner_apps.py
```

Publish the generated `apps/` directory to the existing IONOS document root
with the SFTP account recorded in the portfolio inventory. The password is not
stored in this repository. Upload only this subtree; the rest of
`billdonner.com` remains owned by the existing site.

After publication, verify:

```sh
curl -fsS https://billdonner.com/apps/ | grep "19 active apps"
curl -fsSI https://billdonner.com/apps/pfoliolio/
curl -fsSI https://billdonner.com/apps/oliopfolio/
```
