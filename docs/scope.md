# **Scope: Meetapparaat voor Lichaamslengte Bepaling**

## **1. Inleiding**
Dit project richt zich op het ontwikkelen van een meetapparaat dat de lichaamslengte van een persoon kan meten met behulp van een **Arduino-gebaseerd systeem** met een **ultrasone sensor** en **Bluetooth-verbinding**. De gegevens worden opgeslagen in een **PostgreSQL database** en kunnen worden weergegeven via een **Next.js webapplicatie**.

## **2. Doelstelling**
- Een **draagbaar meetapparaat** ontwerpen dat eenvoudig te gebruiken is.
- **Accurate metingen** van lichaamslengte (PL) uitvoeren zonder handmatige invoer.
- **Bluetooth-verbinding** gebruiken om de meetgegevens naar een mobiele app (iOS/Android) te sturen.
- Data opslaan en progressie tonen via een **webinterface**.

## **3. Technologieën**
| Component | Technologie |
|-----------|------------|
| Embedded System | **Arduino** met ultrasone sensor |
| Communicatie | **Bluetooth** |
| Mobiele app | **.NET MAUI (iOS/Android)** |
| Backend | **PostgreSQL database** |
| Webinterface | **Next.js** |

## **4. Functionaliteiten**
### **4.1 Meetapparaat**
- Ultrasone sensor meet **Ground Distance (GD)** en **Target Distance (TD)**.
- Formule: **PL = TD - GD**
- Behuizing geprint met een **3D-printer**.

### **4.2 Mobiele App**
- **Onboarding-scherm** met uitleg over de meting.
- **Bluetooth-verbinding** met het meetapparaat.
- **Meetproces**:
  1. Scan de **Ground Distance (GD)**.
  2. Gebruiker staat onder het apparaat en maakt een foto.
  3. Scan de **Target Distance (TD)**.
  4. De lichaamslengte (PL) wordt berekend en opgeslagen.

### **4.3 Webinterface (Next.js)**
- **Weergave van meetresultaten** en progressie.
- **Gebruikersbeheer** en mogelijkheid om oude metingen te bekijken.

## **5. Hardware Componenten**
- **Arduino**
- **Grove - Ultrasonic Distance Sensor**
  - Meetbereik: **3 cm – 350 cm** met **2 mm nauwkeurigheid**.
  - Werkt op **3.3V & 5V** (compatibel met Raspberry Pi en Arduino).
- **Bluetooth-module**
- **3D-geprinte behuizing**

## **6. Waarom Eigen Meetapparaat?**
- **Volledige controle** over software en hardware.
- **Geen internet nodig** → Bluetooth is eenvoudiger en sneller.
- **Minder setup-complexiteit** dan WiFi-gebaseerde oplossingen.
- **Beter aanpasbaar** voor specifieke behoeften.
