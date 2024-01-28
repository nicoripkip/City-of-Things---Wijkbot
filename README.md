# Project 56: City of Things Prototyping Kit - De Robokast Editie

## Overzicht

In het kader van het City of Things Lab010 project onderzoeken we de impact van autonome objecten in de slimme stad op het dagelijks leven van mensen. Ons doel is om te begrijpen hoe deze objecten, zoals autonome veegmachines of informatieborden, positieve veranderingen kunnen brengen in lokale gemeenschappen, met een focus op buurtniveau in Rotterdam.

Als onderdeel van dit initiatief ontwikkelen we een 'bot kit' voor het snel en eenvoudig creëren van prototypes van autonome objecten. Deze kit is ontworpen om toegankelijk te zijn voor ontwerpers en burgers met beperkte programmeerkennis. Meer informatie en voorbeelden zijn te vinden op [www.wijkbot.nl](http://www.wijkbot.nl).

De huidige opdracht richt zich op het toevoegen van functionaliteiten aan de bot kit om een 'robokast' te creëren. Deze robokast moet in staat zijn om autonoom door het CMI-gebouw te navigeren om workshopmateriaal voor het bouwen van robots aan studenten te leveren. De kast wordt in samenwerking met een stagiair(e) meubelmaker vervaardigd, terwijl de focus van het project ligt op de programmering en elektronica.

## Systeemvereisten

- Ubuntu 20.04
- ROS
- Gehackte 'hoverboard'-hardware

## Installatie

1. **Hoverboard Firmware Flashen**: Voordat u begint, is het noodzakelijk om de firmware van het hoverboard te flashen. Gedetailleerde instructies hiervoor zijn te vinden op de [hoverboard-firmware-hack-FOC GitHub-pagina](https://github.com/EFeru/hoverboard-firmware-hack-FOC).

2. **Code/Functionaliteit Toevoegen**:
   - Maak een nieuwe directory aan in `Documents/Code`.
   - Voor ROS-gerelateerde projecten, voeg een nieuwe directory toe in `Documents/Code/catkin_ws/src`.

3. **ROS Environment Setup**: Voeg de volgende regel toe aan uw `.bashrc` bestand om ROS in elke terminal/shell sessie beschikbaar te maken:
   ```
   source /opt/ros/noetic/setup.bash
   ```
   
4. **Autostart Scripts**: In de directory `.config/autostart` bevinden zich bash scripts die automatisch starten wanneer de Raspberry Pi opstart. Dit maakt het mogelijk voor de robot om zonder aangesloten scherm te functioneren. Overweeg om het wachtwoord van de Raspberry Pi te verwijderen voor een soepeler opstartproces.

## Bekende Problemen

- Het systeem start mogelijk niet correct op zonder een HDMI-kabel aangesloten (weergavefouten).
- Onverwachte onderbrekingen in de seriële communicatie tussen ROS en het hoverboard.
