# Changelog

## 2.1.6

- Ploegkleuren in de configuratie worden nu alfabetisch gesorteerd op de zichtbare vertaalde naam.
- In het Nederlands wordt de volgorde: Blauw, Geel, Groen, Rood en Wit.
- In het Engels wordt de volgorde automatisch alfabetisch op de Engelse kleurnamen bepaald.
- De interne ploegwaarden en roosterberekening zijn ongewijzigd gebleven.

## 2.1.5

- Kalenderentity zichtbaar hernoemd van `Rooster` naar `Agenda`.
- Nieuwe installaties gebruiken `agenda` als voorgestelde kalender entity-ID.
- Pre-release kalender entity-ID's die eindigen op `_rooster` of `_roster` worden bij het laden veilig naar `_agenda` gemigreerd wanneer de doel-ID vrij is.
- Roosterberekening, dienstsensoren en automation-interface verder ongewijzigd gelaten.

## 2.1.4

- Dienstsensoren zijn nu echte Home Assistant enum-sensoren voor een nette keuzelijst in automations.
- `Dienst vandaag`, `Dienst morgen` en `Huidige dienst` bieden Ochtenddienst, Middagdienst, Nachtdienst en Vrij als statuskeuze.
- `Volgende dienst` biedt alleen de drie werkdiensten; Vrij is daar geen geldige volgende dienst.
- Overbodige entity-attributen verwijderd zodat de automation-editor niet meer wordt gevuld met technische roosterinformatie.
- `Werken vandaag` en `Aan het werk` blijven eenvoudige binary sensors voor Aan/Uit-voorwaarden en triggers.
- `Start volgende dienst` blijft een timestamp-sensor en kan rechtstreeks als tijdtrigger (ook met offset) worden gebruikt.
- `Rooster` blijft een calendar entity voor kalender-start/einde triggers.
- Minimum Home Assistant-versie in HACS aangepast naar 2026.8.0, passend bij de geteste installatie.

## 2.1.3

- Zichtbare entity-attributen vertaald naar Nederlandse, stabiele attribuutnamen voor gebruiksgemak in automations en templates.
- Voorbeelden: `date` → `datum`, `shift` → `dienst`, `team_color` → `ploegkleur`, `morning_team` → `ochtendploeg`, `afternoon_team` → `middagploeg`, `night_team` → `nachtploeg`, `end` → `einde` en `active` → `actief`.
- Interne roosterlogica en sensorstates blijven taalneutraal; alleen de publieke state-attributen zijn aangepast.

## 2.1.2

- Definitieve Nederlandse en Engelse interface-teksten toegepast.
- Integratienaam gewijzigd naar `Tata Steel ploegendienstkalender`.
- Configuratie vereenvoudigd naar `Kies je ploegkleur.` / `Choose your team color.`.
- Nederlandse shiftstatussen tonen nu `Ochtenddienst`, `Middagdienst`, `Nachtdienst` en `Vrij`.
- `Volgende dienst start` hernoemd naar `Start volgende dienst`.
- Engelse config-entry/device-titel aangepast naar `Shift roster <color>`.
- Config-flow typehint gemoderniseerd naar `ConfigFlowResult`.

## 2.1.1

- De experimentele entiteit `Volgende vrije periode` verwijderd.
- Upgrade-cleanup toegevoegd zodat de verwijderde entity niet als oude registry-entry achterblijft.
- `shift` toegevoegd aan de attributen van `Huidige dienst` wanneer er geen dienst actief is.
- `shift` toegevoegd aan de attributen van `Aan het werk` wanneer er geen dienst actief is.

## 2.1.0

- Voorspelbare, taalneutrale entity-ID-suggesties voor schone installaties.
- Uitgebreidere dienstattributen, inclusief gelokaliseerde ploegkleurnaam.
- Kalender-events tonen het geplande tijdsbereik.
- Timestamp-entiteiten gebruiken Home Assistant voor relatieve tijdweergave zonder minuutpolling.

## 2.0.0

- Definitieve domainnaam: `tata_steel_shift_calendar`.
- Persoonsnaam volledig uit de configuratie verwijderd.
- Automatische config/device-naam: `Ploegendienst rooster <kleur>`.
- Ploegkleur opgeslagen als stabiele interne waarde (`red`, `green`, `blue`, `yellow`, `white`).
- Vertaalbare ploegkleur-selector voor Nederlands en Engels.
- Taalneutrale shift states: `morning`, `afternoon`, `night`, `off`.
- Vertaalde sensorstates in Nederlands en Engels.
- Nederlandse technische attributen vervangen door stabiele Engelse machinekeys.
- Dubbele configuraties per ploegkleur geblokkeerd.
- Diagnostiek toegevoegd zonder persoonsgegevens.
- Eén gedeelde refresh-timer per config entry in plaats van één timer per entity.
- `Volgende dienst` en `Start volgende dienst` verwijzen naar dezelfde eerstvolgende dienst vanaf nu.
- HACS repositorystructuur, README en CI-workflows toegevoegd.
- Minimum Home Assistant-versie voor HACS ingesteld op 2026.9.0.
