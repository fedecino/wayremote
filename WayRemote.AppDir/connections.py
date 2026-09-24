#!/usr/bin/env python3
"""
WayRemote - Connections Manager
Manages saved remote desktop profiles in ~/.config/wayremote/connections.json
"""
import os
import sys
import json
import uuid

CONFIG_DIR = os.path.expanduser("~/.config/wayremote")
CONFIG_FILE = os.path.join(CONFIG_DIR, "connections.json")

SESSION_PRESETS = {
    "auto": "Rilevamento Automatico DE (Consigliato)",
    "niri-desktop": "Niri (Desktop Completo con Barra DMS)",
    "gnome": "GNOME Desktop (Shell Wayland)",
    "plasma": "KDE Plasma (KWin Wayland)",
    "sway": "Sway Compositor",
    "hyprland": "Hyprland Compositor",
    "labwc": "Labwc Compositor",
    "wayfire": "Wayfire Compositor",
    "kitty": "Terminale Kitty Remoto",
    "alacritty": "Terminale Alacritty Remoto",
    "ghostty": "Terminale Ghostty Remoto",
    "foot": "Terminale Foot Remoto",
    "custom": "Comando Personalizzato"
}

def load_connections():
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

def save_connections(conns):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(conns, f, indent=2, ensure_ascii=False)

def init_defaults():
    conns = load_connections()
    if not conns:
        # Pre-popola una voce di default con rilevamento automatico DE
        conns = [
            {
                "id": "1",
                "name": "ThinkPad Ufficio",
                "host": "192.168.4.162",
                "user": "fede",
                "session": "auto",
                "custom_cmd": ""
            }
        ]
        save_connections(conns)
    return conns

def cmd_list():
    conns = init_defaults()
    # Output adatto a zenity --list con colonne: ID, Nome, Host, Utente, Sessione
    for c in conns:
        sess_label = SESSION_PRESETS.get(c.get("session", ""), c.get("session", "Niri"))
        print(c.get("id", ""))
        print(c.get("name", ""))
        print(c.get("host", ""))
        print(c.get("user", ""))
        print(sess_label)

def cmd_get(conn_id):
    conns = load_connections()
    for c in conns:
        if str(c.get("id")) == str(conn_id):
            print(f'CONN_ID="{c.get("id", "")}"')
            print(f'CONN_NAME="{c.get("name", "")}"')
            print(f'CONN_HOST="{c.get("host", "")}"')
            print(f'CONN_USER="{c.get("user", "")}"')
            print(f'CONN_SESSION="{c.get("session", "niri-desktop")}"')
            print(f'CONN_CUSTOM_CMD="{c.get("custom_cmd", "")}"')
            return 0
    return 1

def cmd_add(name, host, user, session="niri-desktop", custom_cmd=""):
    conns = load_connections()
    # Trova il prossimo ID numerico
    max_id = 0
    for c in conns:
        try:
            val = int(c.get("id", 0))
            if val > max_id:
                max_id = val
        except ValueError:
            pass
    new_id = str(max_id + 1)
    new_conn = {
        "id": new_id,
        "name": name,
        "host": host,
        "user": user,
        "session": session,
        "custom_cmd": custom_cmd
    }
    conns.append(new_conn)
    save_connections(conns)
    print(new_id)

def cmd_update(conn_id, name, host, user, session="niri-desktop", custom_cmd=""):
    conns = load_connections()
    found = False
    for c in conns:
        if str(c.get("id")) == str(conn_id):
            c["name"] = name
            c["host"] = host
            c["user"] = user
            c["session"] = session
            c["custom_cmd"] = custom_cmd
            found = True
            break
    if found:
        save_connections(conns)
        return 0
    return 1

def cmd_delete(conn_id):
    conns = load_connections()
    conns = [c for c in conns if str(c.get("id")) != str(conn_id)]
    save_connections(conns)

def cmd_count():
    conns = load_connections()
    print(len(conns))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        cmd_list()
    elif cmd == "get" and len(sys.argv) >= 3:
        sys.exit(cmd_get(sys.argv[2]))
    elif cmd == "add" and len(sys.argv) >= 5:
        sess = sys.argv[5] if len(sys.argv) > 5 else "niri-desktop"
        custom = sys.argv[6] if len(sys.argv) > 6 else ""
        cmd_add(sys.argv[2], sys.argv[3], sys.argv[4], sess, custom)
    elif cmd == "update" and len(sys.argv) >= 6:
        sess = sys.argv[6] if len(sys.argv) > 6 else "niri-desktop"
        custom = sys.argv[7] if len(sys.argv) > 7 else ""
        sys.exit(cmd_update(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sess, custom))
    elif cmd == "delete" and len(sys.argv) >= 3:
        cmd_delete(sys.argv[2])
    elif cmd == "count":
        cmd_count()
    elif cmd == "init":
        init_defaults()
    else:
        sys.exit(1)
