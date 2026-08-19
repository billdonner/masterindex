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

## SFTP account

Host `home350968887.1and1-data.host`, user `u61384650`, document root `/`
(so the catalog lives at `/apps/`). The password is in the macOS keychain as an
internet password for that server — read it without printing:

```sh
PW=$(security find-internet-password -s home350968887.1and1-data.host -a u61384650 -w)
sshpass -p "$PW" sftp u61384650@home350968887.1and1-data.host
```

Same account `~/qross/scripts/export-catalog.sh` uses. Recorded here because the
note above ("the SFTP account recorded in the portfolio inventory") pointed at
details the inventory did not actually contain.
