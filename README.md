# Tata Steel ploegendienstkalender

[![Open HACS Repository on My Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=thqm10&repository=tata-steel-shift-calendar&category=integration)

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/thqm10/tata-steel-shift-calendar)
[![GitHub Issues](https://img.shields.io/github/issues/thqm10/tata-steel-shift-calendar?logo=github&label=Issues)](https://github.com/thqm10/tata-steel-shift-calendar/issues)
[![GitHub Release](https://img.shields.io/github/v/release/thqm10/tata-steel-shift-calendar?logo=github&label=Release)](https://github.com/thqm10/tata-steel-shift-calendar/releases/latest)

Een Home Assistant-integratie voor het Tata Steel 5-ploegenrooster.

De integratie berekent het rooster volledig lokaal in Home Assistant op basis van de gekozen ploegkleur. Voor de roosterberekening wordt geen verbinding gemaakt met een Tata Steel-account, website of intern Tata Steel-systeem.

> **Onofficieel:** dit is een communityproject en is niet verbonden aan, goedgekeurd door of ondersteund door Tata Steel. Tata Steel en bijbehorende merknamen en logo's zijn eigendom van hun respectieve rechthebbenden.

## Functies

- Volledig lokale en offline roosterberekening
- Ondersteuning voor de ploegen **Blauw, Geel, Groen, Rood en Wit**
- Vaste roostertijdzone `Europe/Amsterdam`
- Correcte verwerking van zomer- en wintertijd
- Home Assistant-agenda met diensten
- Sensor voor de eerstvolgende daadwerkelijke dienst
- Timestamp-sensor voor de start van de volgende dienst
- Aan/Uit-entiteiten voor **Werken vandaag** en **Aan het werk**

## Vereisten

- Home Assistant **2026.8.0 of nieuwer**
- HACS wordt aanbevolen voor installatie en updates

## Installatie

### Via HACS

Klik bovenaan op **Open HACS Repository on My Home Assistant** om de integratie rechtstreeks in HACS te openen.

Je kunt ook in **HACS → Integraties** zoeken naar **Tata Steel ploegendienstkalender**.

1. Kies **Downloaden**.
2. Herstart Home Assistant wanneer HACS daarom vraagt.
3. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**.
4. Zoek naar **Tata Steel ploegendienstkalender**.
5. Kies je ploegkleur.

Updates van de integratie worden daarna via HACS aangeboden.

### Handmatige installatie

Download of kopieer de map:

```text
custom_components/tata_steel_shift_calendar
```

naar:

```text
/config/custom_components/tata_steel_shift_calendar
```

Herstart Home Assistant en voeg daarna de integratie toe via:

**Instellingen → Apparaten & diensten → Integratie toevoegen → Tata Steel ploegendienstkalender**

## Configuratie

Bij het toevoegen van de integratie kies je één ploegkleur:

- Blauw
- Geel
- Groen
- Rood
- Wit

De ploegkleur kan later via **Configureren** worden gewijzigd.

Meerdere ploegkleuren kunnen als aparte configuraties worden toegevoegd. Dezelfde ploegkleur kan niet meerdere keren worden toegevoegd.

## Diensttijden

| Dienst | Tijd |
|---|---|
| **Ochtenddienst** | 06:00 – 14:00 |
| **Middagdienst** | 14:00 – 22:00 |
| **Nachtdienst** | 22:00 – 06:00 |

De nachtdienst begint op de geplande kalenderdag om 22:00 en eindigt de volgende ochtend om 06:00.

De integratie gebruikt altijd de tijdzone:

```text
Europe/Amsterdam
```

Hierdoor worden zomer- en wintertijd automatisch correct verwerkt.

## Entiteiten

Na het toevoegen van een ploeg worden de volgende entiteiten aangemaakt.

| Entiteit | Type | Betekenis |
|---|---|---|
| **Dienst vandaag** | Enum-sensor | Geplande dienst op de huidige kalenderdag |
| **Dienst morgen** | Enum-sensor | Geplande dienst voor morgen |
| **Huidige dienst** | Enum-sensor | Dienst die op dit exacte moment actief is, anders Vrij |
| **Volgende dienst** | Enum-sensor | Eerstvolgende daadwerkelijke werkdienst die na nu begint |
| **Start volgende dienst** | Timestamp-sensor | Starttijd van exact dezelfde dienst als **Volgende dienst** |
| **Werken vandaag** | Binary sensor | Aan wanneer de gekozen ploeg vandaag een werkdag heeft |
| **Aan het werk** | Binary sensor | Aan wanneer de gekozen ploeg op dit exacte moment aan het werk is |
| **Agenda** | Kalender | Home Assistant-agenda met alle berekende diensten |

## Dienststatussen

### Dienst vandaag, Dienst morgen en Huidige dienst

Deze entiteiten kunnen de volgende daadwerkelijke states hebben:

```text
ochtenddienst
middagdienst
nachtdienst
vrij
```

In de Home Assistant-interface worden deze weergegeven als:

- **Ochtenddienst**
- **Middagdienst**
- **Nachtdienst**
- **Vrij**

### Volgende dienst

**Volgende dienst** verwijst altijd naar een daadwerkelijke toekomstige werkdienst en gebruikt daarom alleen:

```text
ochtenddienst
middagdienst
nachtdienst
```

`vrij` is voor deze entiteit geen mogelijke waarde.

## Verschil tussen de dienstsensoren

### Dienst vandaag

Geeft de geplande dienst voor de huidige kalenderdag weer.

### Dienst morgen

Geeft de geplande dienst voor de volgende kalenderdag weer.

### Huidige dienst

Geeft alleen een dienst weer wanneer die op dit exacte moment actief is.

Buiten een actieve dienst is de waarde:

```text
vrij
```

Dit is vooral handig voor automatiseringen die alleen tijdens werktijd actief mogen zijn.

### Volgende dienst

Zoekt vanaf het huidige moment naar de eerstvolgende daadwerkelijke werkdienst.

Vrije dagen worden hierbij automatisch overgeslagen.

### Start volgende dienst

Bevat de starttijd van exact dezelfde dienst die door **Volgende dienst** wordt weergegeven.

Hierdoor kunnen **Volgende dienst** en **Start volgende dienst** samen betrouwbaar worden gebruikt in automatiseringen.

## Agenda

De integratie maakt een Home Assistant-kalender aan met de berekende diensten.

Een agenda-item bevat:

- de naam van de dienst
- de begin- en eindtijd
- de gekozen ploegkleur

Voorbeeld:

```text
Ochtenddienst · 06:00–14:00
Ploeg Geel
```

De agenda kan onder andere worden gebruikt voor:

- weergave op dashboards
- kalenderkaarten
- kalendertriggers
- automatiseringen bij het begin van een dienst
- automatiseringen bij het einde van een dienst

## Automatiseringen

De entiteiten zijn ingericht voor gebruik met de visuele Home Assistant automation-editor.

Voor normale automatiseringen zijn geen technische attributen nodig.

### Dienststatus gebruiken

In de visuele automation-editor kun je bijvoorbeeld kiezen:

**Dienst vandaag → Ochtenddienst**

De daadwerkelijke state die Home Assistant gebruikt is:

```text
ochtenddienst
```

Wanneer je YAML gebruikt, ziet een statusvoorwaarde er bijvoorbeeld zo uit:

```yaml
condition:
  - condition: state
    entity_id: <jouw_entiteit_dienst_vandaag>
    state: "ochtenddienst"
```

Vervang `<jouw_entiteit_dienst_vandaag>` door de daadwerkelijke entity-ID uit jouw Home Assistant-installatie.

Entity-ID's kunnen per installatie verschillen. Selecteer daarom bij voorkeur de entiteit via de visuele automation-editor.

### Werken vandaag

**Werken vandaag** is een Aan/Uit-entiteit.

Gebruik deze wanneer alleen van belang is of de gekozen ploeg die kalenderdag moet werken, ongeacht het soort dienst.

### Aan het werk

**Aan het werk** is alleen **Aan** wanneer op het huidige exacte tijdstip daadwerkelijk een dienst actief is.

Dit houdt ook correct rekening met een nachtdienst die na middernacht nog actief is.

### Start volgende dienst

**Start volgende dienst** is een timestamp-sensor.

Hiermee zijn bijvoorbeeld automatiseringen mogelijk:

- exact bij de start van de volgende dienst
- een bepaalde tijd vóór de volgende dienst
- een bepaalde tijd na de start van de volgende dienst

### Agenda

De entiteit **Agenda** kan worden gebruikt met Home Assistant-kalendertriggers voor het begin en einde van diensten.

## Roosterberekening

Het rooster wordt lokaal berekend en niet opgehaald van een externe website.

De integratie houdt onder andere rekening met:

- de vaste cyclus van het 5-ploegenrooster
- de gekozen ploegkleur
- de tijdzone `Europe/Amsterdam`
- zomer- en wintertijd
- nachtdiensten die over middernacht lopen
- de gevalideerde februari/maart-correctie voor niet-schrikkeljaren

## Diagnostics

De integratie ondersteunt **Home Assistant Diagnostics**.

De diagnostics bevatten technische informatie over onder andere:

- integratieversie
- gebruikte tijdzone
- geselecteerde ploegkleur
- huidige berekening
- volgende dienst
- start en einde van de volgende dienst
- volgende geplande refresh

Gebruik diagnostics bij voorkeur wanneer je een reproduceerbaar probleem meldt.

## Beperkingen

De integratie berekent het standaard Tata Steel 5-ploegenrooster.

De volgende zaken worden niet automatisch verwerkt:

- verlof
- vakantie
- ziekte
- overwerk
- geruilde diensten
- persoonlijke roosterwijzigingen
- tijdelijke afwijkingen van het standaardrooster

## Problemen oplossen

### De integratie verschijnt niet bij Integratie toevoegen

Controleer of:

1. de integratie via HACS is gedownload;
2. Home Assistant na installatie opnieuw is gestart;
3. je Home Assistant-versie minimaal **2026.8.0** is.

### Het berekende rooster lijkt niet te kloppen

Controleer eerst:

- of de juiste ploegkleur is ingesteld;
- of Home Assistant de correcte datum en tijd heeft;
- of het probleem ook zichtbaar is in **Agenda**.

Maak vervolgens Home Assistant Diagnostics aan en voeg deze toe aan een GitHub Issue.

## Ondersteuning

Gebruik de **GitHub Issues**-knop bovenaan om problemen, fouten en reproduceerbare afwijkingen te melden.

Vermeld bij een probleem bij voorkeur:

- wat je verwachtte;
- wat er daadwerkelijk gebeurde;
- je Home Assistant-versie;
- de gebruikte versie van deze integratie;
- de ingestelde ploegkleur wanneer dat relevant is;
- Home Assistant Diagnostics wanneer mogelijk.

Plaats geen wachtwoorden, tokens of andere gevoelige gegevens in een issue.

## Changelog

Alle wijzigingen per versie staan in:

[`CHANGELOG.md`](./CHANGELOG.md)

## Licentie

Dit project wordt uitgebracht onder de MIT-licentie.

Zie:

[`LICENSE`](./LICENSE)

## Disclaimer

Dit project is een onafhankelijk communityproject.

Het is niet verbonden aan, goedgekeurd door of ondersteund door Tata Steel. De integratie geeft een lokaal berekend standaardrooster weer en vormt geen officiële bron voor werktijden, personeelsplanning of roosterwijzigingen.

Controleer bij twijfel altijd je officiële rooster of de daarvoor bestemde officiële informatiebronnen.
