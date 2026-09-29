# Tata Steel ploegendienstkalender

Home Assistant-integratie voor het Tata Steel 5-ploegenrooster. Het rooster wordt volledig lokaal berekend en werkt zonder internetverbinding.

> **Onofficieel:** dit communityproject is niet verbonden aan, goedgekeurd door of ondersteund door Tata Steel. Tata Steel en bijbehorende merknamen/logo's zijn eigendom van hun respectieve rechthebbenden.

## Eigenschappen

- Volledig lokale roosterberekening; internet is niet nodig na installatie.
- Ploegkleuren: Rood, Groen, Blauw, Geel en Wit.
- Vaste roostertijdzone `Europe/Amsterdam`, inclusief zomer-/wintertijd.
- Houdt rekening met nachtdiensten over middernacht.
- Houdt rekening met de gevalideerde februari/maart-correctie in niet-schrikkeljaren.
- Nederlandse en Engelse UI-vertalingen.
- Eén configuratie per ploegkleur; dubbele roosters worden geblokkeerd.
- Diagnostiek zonder persoonsnaam, tokens of locatiegegevens.

## Installatie

### HACS

Zolang de integratie nog niet in de standaard HACS-community store is opgenomen:

1. Voeg `https://github.com/thqm10/tata-steel-shift-calendar` in HACS toe als **Aangepaste repository** van het type **Integratie**.
2. Installeer **Tata Steel ploegendienstkalender** via HACS.
3. Herstart Home Assistant.
4. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen** en zoek naar **Tata Steel ploegendienstkalender**.

Na opname in de standaard HACS-community store is stap 1 niet meer nodig en kan de integratie direct in HACS worden gezocht.

### Handmatig

Kopieer `custom_components/tata_steel_shift_calendar` naar `/config/custom_components/tata_steel_shift_calendar` en herstart Home Assistant volledig.

## Configuratie

Je kiest alleen je ploegkleur. De config-entry en het apparaat krijgen automatisch een naam als:

`Ploegendienst rooster Rood`

Er wordt geen persoonsnaam opgeslagen.

## Entiteiten

| Entiteit | Betekenis |
|---|---|
| Dienst vandaag | Geplande dienst op de huidige kalenderdag |
| Dienst morgen | Geplande dienst morgen |
| Huidige dienst | Dienst die op dit exacte moment actief is, anders Vrij/Off |
| Volgende dienst | Eerstvolgende daadwerkelijke dienst die na nu begint |
| Start volgende dienst | Timestamp van exact dezelfde eerstvolgende dienst |
| Werken vandaag | Aan als deze kalenderdag een werkdag is |
| Aan het werk | Aan als de ploeg op dit exacte moment dienst heeft |
| Agenda | Home Assistant-kalender met alle berekende diensten |

De technische states zijn taalneutraal (`morning`, `afternoon`, `night`, `off`). Home Assistant vertaalt die in de interface.

## Automatiseringen

De entiteiten zijn bewust ingericht voor de visuele Home Assistant automation-editor:

- **Dienst vandaag**, **Dienst morgen** en **Huidige dienst** zijn enum-sensoren met de keuzes **Ochtenddienst**, **Middagdienst**, **Nachtdienst** en **Vrij**.
- **Volgende dienst** is een enum-sensor met alleen **Ochtenddienst**, **Middagdienst** en **Nachtdienst**.
- **Werken vandaag** en **Aan het werk** zijn binary sensors en kunnen direct als Aan/Uit-trigger of -voorwaarde worden gebruikt.
- **Start volgende dienst** is een timestamp-sensor. Gebruik die in een **Tijd**-trigger om exact bij de volgende dienst te starten; Home Assistant ondersteunt daar ook een offset voor.
- **Agenda** is een calendar entity en kan met een kalendertrigger reageren op het begin of einde van een dienst.

De normale entities bevatten geen technische roosterattributen meer. Detailinformatie voor foutanalyse blijft beschikbaar via Home Assistant Diagnostics. Hierdoor blijft de automation-editor overzichtelijk.

## Validatie

De standaardcyclus is vergeleken met het aangeleverde `Shifts.ics` over 30 maart 2026 t/m 2 augustus 2027: 491 kalenderdagen en 1.473 diensten zonder roosterafwijking. De regressietests bewaken daarnaast de februari/maart-correctie, schrikkeldag-doorloop, jaarwisseling, nachtdiensten, DST en kalender-overlap.

De aangeleverde referentie bevat geen 29 februari 2028. De schrikkeljaarlogica is daarom wel regressie-getest, maar niet extern tegen een 2028-export gevalideerd.

## Migratie vanaf de oude testversie

Versie 2.1.5 hernoemt de kalenderentity zichtbaar naar **Agenda** en gebruikt voor nieuwe installaties `..._agenda` als entity-ID. Pre-release entity-ID's die eindigen op `_rooster` of `_roster` worden bij het laden automatisch naar `_agenda` gemigreerd zolang de doel-ID nog vrij is.

Versie 2.1.4 verwijdert de tijdelijke publieke roosterattributen uit de entities. Voor normale automations gebruik je voortaan de entity-state zelf, de twee binary sensors, de timestamp-sensor of de kalender. Dit is de definitieve automation-interface vóór de publieke release.

Versie 2.0.0 gebruikt de definitieve domainnaam `tata_steel_shift_calendar` in plaats van `work_shift_calendar`. Home Assistant kan config entries niet automatisch tussen domains verplaatsen. Verwijder daarom de oude testintegratie, verwijder de oude map `custom_components/work_shift_calendar`, herstart Home Assistant en installeer daarna deze versie opnieuw.

## Ondersteuning

Meld problemen via de [GitHub issue tracker](https://github.com/thqm10/tata-steel-shift-calendar/issues). Voeg bij problemen waar mogelijk Home Assistant Diagnostics toe; daarin worden geen persoonsnamen opgeslagen.

## Generatiepact

GP1 en GP2 zijn bewust nog niet opgenomen. Die worden pas toegevoegd nadat hun referentieroosters op dezelfde manier volledig zijn gevalideerd.


## Broncode en releases

De broncode en releases staan op [GitHub](https://github.com/thqm10/tata-steel-shift-calendar).
