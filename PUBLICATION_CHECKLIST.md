# Publicatiechecklist

Repository: `https://github.com/thqm10/tata-steel-shift-calendar`
Release: `v2.1.5`

## Klaar in dit pakket

- Eén custom integration onder `custom_components/tata_steel_shift_calendar`.
- `manifest.json` bevat domain, name, version, documentation, issue tracker en codeowner.
- `hacs.json` bevat de HACS-naam, `country: NL` en minimum Home Assistant `2026.8.0`.
- Brandmap met minimaal `brand/icon.png`.
- Nederlandse README, changelog en MIT-licentie.
- GitHub Actions voor Tests, Hassfest en HACS validation.
- `CODEOWNERS` ingesteld op `@thqm10`.
- Cache-, bytecode- en tijdelijke bestanden uitgesloten.
- Releaseversie in `manifest.json` en `const.py`: `2.1.5`.

## Op GitHub instellen na upload

1. Repository moet **Public** zijn.
2. Description: `Tata Steel 5-ploegenrooster voor Home Assistant, volledig lokaal en offline.`
3. Zet **Issues** aan.
4. Voeg topics toe, bijvoorbeeld: `home-assistant`, `hacs`, `custom-integration`, `tata-steel`, `shift-calendar`, `ploegendienst`, `netherlands`.
5. Controleer onder **Actions** dat **Tests**, **Hassfest** en **HACS validation** allemaal groen zijn.
6. Test de repository eerst als aangepaste HACS-repository: installeren, herstarten, configureren, updaten en verwijderen.
7. Maak daarna een echte GitHub Release `v2.1.5` aan; alleen een Git-tag is niet genoeg voor de HACS-default-aanvraag.
8. Controleer na de release opnieuw de HACS validation.
9. Dien daarna desgewenst als eigenaar een PR in bij `hacs/default` onder de integratielijst om opname in de standaard HACS-community store aan te vragen.

## Nog inhoudelijk open

- Externe validatie van 29 februari 2028 zodra een geschikte referentie-export beschikbaar is. De interne schrikkeljaarlogica is wel regressie-getest.
