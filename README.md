# Tata Steel ploegendienstkalender

Home Assistant-integratie voor het Tata Steel 5-ploegenrooster. Het rooster wordt volledig lokaal berekend en werkt zonder internetverbinding.

> **Onofficieel:** dit communityproject is niet verbonden aan, goedgekeurd door of ondersteund door Tata Steel. Tata Steel en bijbehorende merknamen/logo's zijn eigendom van hun respectieve rechthebbenden.

## Eigenschappen

- Volledig lokale roosterberekening; internet is na installatie niet nodig voor de roosterberekening.
- Ondersteunt de ploegkleuren **Rood, Groen, Blauw, Geel en Wit**.
- Gebruikt de vaste roostertijdzone `Europe/Amsterdam`, inclusief zomer- en wintertijd.
- Houdt rekening met de gevalideerde februari/maart-correctie in niet-schrikkeljaren.
- Nederlandse en Engelse interface.
- Eén configuratie per ploegkleur; dubbele roosters worden geblokkeerd.
- Geschikt voor gebruik in dashboards, agenda's en automatiseringen.

## Vereisten

- Home Assistant **2026.8.0 of nieuwer**
- HACS is aanbevolen voor installatie en updates, maar niet verplicht.

## Installatie

### Via HACS

Zolang de integratie nog niet in de standaard HACS-community store is opgenomen:

1. Voeg `https://github.com/thqm10/tata-steel-shift-calendar` in HACS toe als **Aangepaste repository** van het type **Integratie**.
2. Installeer **Tata Steel ploegendienstkalender** via HACS.
3. Herstart Home Assistant.
4. Ga naar **Instellingen → Apparaten & diensten → Integratie toevoegen**.
5. Zoek naar **Tata Steel ploegendienstkalender** en kies je ploegkleur.

Na opname in de standaard HACS-community store is stap 1 niet meer nodig en kan de integratie direct in HACS worden gevonden.

### Handmatig

Kopieer:

```text
custom_components/tata_steel_shift_calendar
```

naar:

```text
/config/custom_components/tata_steel_shift_calendar
```

Herstart daarna Home Assistant.

## Configuratie

Bij het toevoegen van de integratie kies je alleen je ploegkleur:

- Rood
- Groen
- Blauw
- Geel
- Wit

De ploegkleur kan later via **Configureren** worden gewijzigd.

## Entiteiten

| Entiteit | Betekenis |
|---|---|
| **Dienst vandaag** | Geplande dienst op de huidige kalenderdag |
| **Dienst morgen** | Geplande dienst voor morgen |
| **Huidige dienst** | Dienst die op dit exacte moment actief is, anders Vrij |
| **Volgende dienst** | Eerstvolgende daadwerkelijke dienst die na nu begint |
| **Start volgende dienst** | Starttijd van exact dezelfde eerstvolgende dienst |
| **Werken vandaag** | Aan als deze kalenderdag een werkdag is |
| **Aan het werk** | Aan als de ploeg op dit exacte moment dienst heeft |
| **Agenda** | Home Assistant-kalender met alle berekende diensten |

## Automatiseringen

De entiteiten zijn ingericht voor de visuele Home Assistant automation-editor:

- **Dienst vandaag**, **Dienst morgen** en **Huidige dienst** hebben de keuzes **Ochtenddienst**, **Middagdienst**, **Nachtdienst** en **Vrij**.
- **Volgende dienst** heeft de keuzes **Ochtenddienst**, **Middagdienst** en **Nachtdienst**.
- **Werken vandaag** en **Aan het werk** zijn Aan/Uit-entiteiten en kunnen direct als trigger of voorwaarde worden gebruikt.
- **Start volgende dienst** is een timestamp-sensor en kan als tijdtrigger worden gebruikt, inclusief een offset.
- **Agenda** kan worden gebruikt met Home Assistant-kalendertriggers voor het begin of einde van een dienst.

Voor normale automatiseringen hoef je geen technische attributen te gebruiken.

## Ondersteuning

Problemen of fouten kunnen worden gemeld via:

`https://github.com/thqm10/tata-steel-shift-calendar/issues`

Voeg bij een probleem waar mogelijk Home Assistant Diagnostics toe.

## Beperkingen

- De integratie berekent het standaard Tata Steel 5-ploegenrooster.
- Verlof, overwerk en geruilde diensten worden niet automatisch verwerkt.
- De integratie maakt geen verbinding met een Tata Steel-account of interne Tata Steel-systemen.

## Broncode en releases

Broncode, changelog en releases:

`https://github.com/thqm10/tata-steel-shift-calendar`

## Licentie

Dit project wordt uitgebracht onder de MIT-licentie.
