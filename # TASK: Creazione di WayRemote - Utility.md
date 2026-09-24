# TASK: Creazione di WayRemote - Utility Universale AppImage per Remote Login Wayland

Crea un progetto completo e pronto all'uso denominato **WayRemote** che consenta l'accesso desktop remoto bidirezionale nativo in ambienti Linux Wayland (con supporto specifico a window manager moderni come Niri, GNOME, KDE o Sway), senza usare software cloud/proprietari (come RustDesk, AnyDesk, TeamViewer) e senza ricorrere a server VNC.

L'output finale deve essere una directory `WayRemote.AppDir` e uno script per compilare l'eseguibile autonomo `WayRemote-x86_64.AppImage` tramite `appimagetool`.

---

## 1. Requisiti Funzionali

L'eseguibile AppImage deve svolgere sia da installer/configuratore che da client grafico leggero con finestre di dialogo native (`zenity`):

1. **Primo avvio (Doppio clic sull'AppImage):**
   - Mostrare un menu di scelta:
     - `1. Connettiti a un PC remoto (Client)`
     - `2. Configura questo PC come SERVER (riceve connessioni)`
     - `3. Installa WayRemote nel sistema (Integrazione Desktop per l'utente)`

2. **Flusso SERVER:**
   - Rilevare automaticamente la distribuzione Linux leggendo `/etc/os-release` (supporto per Arch/CachyOS/EndeavourOS, Debian/Ubuntu/Mint, Fedora).
   - Richiedere conferma all'utente per scaricare e installare i pacchetti necessari.
   - Richiedere la password di amministrazione (`sudo`) tramite un prompt grafico con caratteri mascherati (`zenity --password`).
   - Installare i pacchetti:
     - Su Arch/CachyOS: `openssh`, `waypipe` (e verificare dipendenze video/codec).
     - Su Debian/Ubuntu/Mint: `openssh-server`, `waypipe`.
     - Su Fedora: `openssh-server`, `waypipe`.
   - Abilitare e avviare immediatamente il servizio di sistema (`systemctl enable --now ssh` o `sshd`).
   - Al termine, mostrare un messaggio di successo e chiedere se si desidera configurare/integrare anche il Client su questa stessa macchina.

3. **Flusso INSTALLAZIONE CLIENT (Integrazione Desktop):**
   - Se l'utente sceglie l'integrazione o acconsente al termine del setup server:
     - Copiare il binario dell'AppImage in `~/.local/bin/wayremote` (rendendolo eseguibile).
     - Installare l'icona in `~/.local/share/icons/hicolor/128x128/apps/wayremote.png`.
     - Creare il file `~/.local/share/applications/wayremote.desktop` con flag `Exec=wayremote --client`.
     - Aggiornare il database desktop con `update-desktop-database`.

4. **Flusso CLIENT (Connessione Diretta):**
   - Quando invocato con il flag `--client` (o dal file `.desktop`):
     - Mostrare un prompt grafico per inserire l'indirizzo IP del PC target nella LAN (con placeholder `192.168.1.`).
     - Mostrare un prompt per il nome utente remoto (default: `$USER`).
     - Eseguire la sessione grafica remota incapsulata via `waypipe` su SSH (`waypipe --video ssh -X -t "$user@$ip" "niri"` o fallback alla sessione configurata).
     - Rilevare il terminale installato sul sistema per l'autenticazione interattiva (dare precedenza a `ghostty`, `kitty`, `alacritty`, `foot`, o `x-terminal-emulator`).

---

## 2. Struttura dei File da Generare

Genera i seguenti file nella root del workspace:

1. `WayRemote.AppDir/AppRun`:
   - Script Bash robusto, con gestione errori (`set -e`), funzioni modulari per rilevamento distro, prompt grafici zenity, esecuzione comandi con pipe sicura della password sudo, integrazione desktop e avvio della connessione.
2. `WayRemote.AppDir/wayremote.desktop`:
   - Desktop entry standard conforme a XDG.
3. `WayRemote.AppDir/wayremote.png`:
   - Genera uno script o scarica/crea un'icona SVG/PNG valida per l'applicazione.
4. `build.sh`:
   - Script automatizzato che:
     1. Verifica la presenza di `appimagetool` (se assente, lo scarica da GitHub e lo rende eseguibile).
     2. Imposta i permessi corretti su `AppRun`.
     3. Compila l'AppImage finale: `WayRemote-x86_64.AppImage`.

Fornisci il codice completo di ciascun file e le istruzioni esatte per lanciare la compilazione e testare l'eseguibile.