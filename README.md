# WayRemote 🚀

**WayRemote** è un'applicazione autonoma in formato **AppImage** per l'accesso e controllo desktop remoto nativo in ambienti Linux **Wayland** (come Niri, GNOME, Sway, Labwc, Wayfire), senza intermediari cloud/proprietari e senza protocolli obsoleti come VNC.

Utilizza il forwarding nativo Wayland tramite **`waypipe`** incapsulato in un tunnel **`SSH`** sicuro con compressione video hardware.

---

## 🌟 Funzionalità Principali

1. **Gestione Connessioni Multi-Server (Stile GNOME Connections / Remmina)**:
   - Rubrica profili memorizzati in `~/.config/wayremote/connections.json`.
   - Aggiunta, modifica, eliminazione e connessione rapida con un clic.
   - Memorizzazione host, utente e sessione preferita per ciascun server.

2. **Client Desktop Remoto Nativo Wayland**:
   - Connessione diretta LAN/VPN ad alta velocità via SSH + `waypipe`.
   - Supporto nativo per **Desktop Completo Niri** (con avvio automatico della shell DMS / Waybar e terminale).
   - Inoltro nativo scorciatoie da tastiera con `mod-key-nested "Super"`, garantendo che i tasti `Super+Return`, `Super+Space`, `Super+E`, ecc. funzionino esattamente come sul PC remoto.
   - Opzioni di fallback affidabili con rilevamento automatico del socket grafico Wayland e modalità sicura `--no-gpu` contro i crash dei driver video.

3. **Configuratore Server One-Click**:
   - Rilevamento automatico della distribuzione (`Arch/CachyOS/EndeavourOS`, `Debian/Ubuntu/Mint`, `Fedora/RHEL`, `openSUSE`).
   - Installazione assistita e abilitazione immediata del demone `sshd` e `waypipe`.
   - Configurazione automatica `IPQoS none` per prevenire il blocco del traffico su reti Wi-Fi domestiche.

4. **Integrazione Desktop Automatica**:
   - Installazione in `~/.local/bin/wayremote`.
   - Creazione della desktop entry XDG e associazione icone di sistema.

---

## 📁 Struttura del Progetto

```text
wayremote/
├── WayRemote.AppDir/
│   ├── AppRun              # Script Bash principale con gestione GUI Zenity
│   ├── connections.py      # Gestore profili di connessione (~/.config/wayremote/connections.json)
│   ├── wayremote.desktop   # Desktop Entry conforme a XDG
│   ├── wayremote.png       # Icona dell'applicazione (128x128)
│   └── .DirIcon            # Icona per AppImage
├── build.sh                # Script automatizzato di compilazione AppImage
├── wayremote.svg           # Sorgente vettoriale dell'icona
└── WayRemote-x86_64.AppImage # Eseguibile finale generato
```

---

## 🛠️ Requisiti

- **Zenity** (per i dialoghi grafici):
  - Arch/CachyOS: `sudo pacman -S zenity`
  - Debian/Ubuntu: `sudo apt install zenity`
  - Fedora: `sudo dnf install zenity`
- **SSH** e **Waypipe** (installati automaticamente tramite la funzione Server).

---

## 🔨 Compilazione

Per ricompilare l'AppImage partendo dalla directory `WayRemote.AppDir`:

```bash
chmod +x build.sh
./build.sh
```

Lo script scaricherà automaticamente `appimagetool` se non presente nel sistema e produrrà il binario `WayRemote-x86_64.AppImage`.

---

## 🚀 Utilizzo

### Modalità Grafica (Doppio clic o da terminale)
```bash
./WayRemote-x86_64.AppImage
```

### Parametri da riga di comando
- **Client (Connessione Diretta)**:
  ```bash
  ./WayRemote-x86_64.AppImage --client
  ```
- **Configuratore Server**:
  ```bash
  ./WayRemote-x86_64.AppImage --server
  ```
- **Integrazione Desktop**:
  ```bash
  ./WayRemote-x86_64.AppImage --install
  ```
- **Guida**:
  ```bash
  ./WayRemote-x86_64.AppImage --help
  ```
