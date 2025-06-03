# Create4Care App

Een cross-platform applicatie voor het meten en visualiseren van lichaamsgroei bij kinderen. De applicatie is ontwikkeld als onderdeel van een project in semester 6 van de opleiding Informatica aan de Hogeschool Rotterdam.

## 📦 Projectstructuur

```
├── create4care_app       # MAUI Blazor client-app
├── create4care_docker    # FastAPI backend met Docker ondersteuning
├── pose_decection        # Pose detection scripts en testafbeeldingen
└── sensor_meter          # Arduino-code voor de sensor
````

## 🌐 Frontend: `create4care_app`

Een .NET MAUI Blazor-applicatie met ondersteuning voor Android, iOS, Windows, MacCatalyst en Tizen. Bevat:

- Pagina’s: `Home`, `Bluetooth`, `Instruction`, `Measuring`, `Settings`
- Bluetooth-integratie via `Plugin.BLE`
- Data-opslag via `Preferences`
- Visualisaties met Chart.js
- 3D walkthrough-instructies met animaties

### Starten (voor developers)

```bash
cd create4care_app
dotnet build
dotnet run
````

## 🔧 Backend: `create4care_docker/api`

Een FastAPI-backend met:

* Authenticatie
* Gebruikersbeheer
* Pose detectie via base64-afbeeldingen
* Meting-opslag
* Dockerfile beschikbaar

### Starten (met Docker)

```bash
cd create4care_docker/api
docker build -t create4care-api .
docker run -p 8000:8000 create4care-api
```

## 🧠 Pose Detection: `pose_decection`

Scripts om pose-detectie lokaal te testen.

### Bestand

* `mian.py`: hoofdscript voor het uitvoeren van detectie
* `dummy_correct.jpg` / `dummy_wrong.jpg`: testafbeeldingen

## 🔌 Sensor: `sensor_meter`

Arduino `.ino` bestand dat op de sensor wordt geïnstalleerd om afstandsmetingen te verrichten (bijv. via een ultrasone sensor).

---

## 📚 Benodigdheden

* .NET MAUI workload
* Docker
* Python 3.10+
* Arduino IDE (voor `sensor_meter.ino`)
* BLE-compatibele Arduino (bijv. Arduino R4 WiFi)

## 👥 Team

* INF: Ardit, Ayoeb
* CMGT: Salma
* ADS & AI: Narjiss, Jesse

---

## 📃 Licentie

MIT License – vrij te gebruiken voor educatieve doeleinden.

```
MIT License

Copyright (c) 2025 The Blokk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      
copies of the Software, and to permit persons to whom the Software is         
furnished to do so, subject to the following conditions:                       

The above copyright notice and this permission notice shall be included in    
all copies or substantial portions of the Software.                           

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN     
THE SOFTWARE.
```