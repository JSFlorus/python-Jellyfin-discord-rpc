# Jellyfin Discord RPC

[![CI/CD](https://github.com/jsflorus/python-jellyfin-discord-rpc/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/jsflorus/python-jellyfin-discord-rpc/actions)

---

Displays your Jellyfin playback status on Discord Rich Presence.

---

## ✨ Features

- Shows currently playing media from Jellyfin  
- Updates Discord Rich Presence in real time  
- Lightweight and Docker-friendly  
- Works with reverse proxy setups  

---

## 📦 Requirements

- Jellyfin server  
- Discord (must be running on the host)  
- Docker (recommended)  

---

## 🎮 Discord Setup (Client ID + Assets)

Before running the app, you need to create a Discord application and configure assets.

### 1. Create a Discord Application

1. Go to https://discord.com/developers/applications  
2. Click **New Application**  
3. Give it a name (e.g., `Jellyfin RPC`)  
4. Click **Create**

---

### 2. Get Your Client ID

1. Inside your application dashboard  
2. Go to **General Information**  
3. Copy the **Application ID**

➡️ This is your `DISCORD_CLIENT_ID`

---

### 3. Add Rich Presence Image Asset

1. Go to **Rich Presence → Art Assets**  
2. Click **Add Image(s)**  
3. Upload an image (e.g., Jellyfin logo)  
4. Set the **Asset Name** (IMPORTANT)

Example:


Asset Name: server


➡️ This must match:


ART_ASSET=server


---

### 4. Notes

- Rich Presence is enabled by default  
- No OAuth setup is required  

---
## 🚀 Quick Start (Docker)

```bash
docker run -d \
  --name jellyfin-rpc \
  --restart unless-stopped \
  -e DISCORD_CLIENT_ID=your_discord_client_id \
  -e JELLYFIN_URL=http://your-jellyfin \
  -e JELLYFIN_API_KEY=your_api_key \
  -e JELLYFIN_USER=your_username \
  -e ART_ASSET=server \
  -e DISCORD_UPDATE_INTERVAL_SECS=10 \
  -e XDG_RUNTIME_DIR=/run/user/1000 \
  -v /run/user/1000/.flatpak/com.discordapp.Discord/xdg-run:/run/user/1000 \
  ghcr.io/jsflorus/python-jellyfin-discord-rpc:latest
```

---

## 🐳 Docker Compose

```yaml
services:
  jellyfin-rpc:
    image: ghcr.io/jsflorus/python-jellyfin-discord-rpc:latest
    container_name: jellyfin-rpc
    restart: unless-stopped

    env_file:
      - .env

    environment:
      XDG_RUNTIME_DIR: /run/user/1000

    volumes:
      - /run/user/1000/.flatpak/com.discordapp.Discord/xdg-run:/run/user/1000

    network_mode: host
    user: "1000:1000"
```

---

## ⚙️ Environment Variables

| Variable | Description |
|----------|------------|
| DISCORD_CLIENT_ID | Discord application client ID |
| JELLYFIN_URL | URL of your Jellyfin server |
| JELLYFIN_API_KEY | Jellyfin API key |
| JELLYFIN_USER | Username to track |
| ART_ASSET | Discord Rich Presence image asset name |
| DISCORD_UPDATE_INTERVAL_SECS | Update interval in seconds |

---

## 📄 Example `.env`

```env
DISCORD_CLIENT_ID=123456789
JELLYFIN_URL=https://jellyfin.example
JELLYFIN_API_KEY=your_api_key_here
JELLYFIN_USER=JohnDoe
ART_ASSET=server
DISCORD_UPDATE_INTERVAL_SECS=10
```

## 🧠 How it works

The app polls the Jellyfin Sessions API and updates Discord via IPC (local socket).

---

## ⚠️ Important (Linux + Flatpak Discord)

If you're using Flatpak Discord, you **must mount the runtime directory**:

```yaml
volumes:
  - /run/user/1000/.flatpak/com.discordapp.Discord/xdg-run:/run/user/1000
```

Otherwise you will get:

```text
Discord RPC unavailable: Could not find Discord installed and running
```

---

## 🛠 Troubleshooting

### Discord not detected

* Make sure Discord is running
* Verify socket exists:

```bash
ls /run/user/1000/.flatpak/com.discordapp.Discord/xdg-run
```

You should see:

```text
discord-ipc-0
```

---

### Container restarts constantly

```bash
docker logs jellyfin-rpc
```

---

### Wrong DNS / cannot reach Jellyfin

* Ensure correct DNS or reverse proxy routing

---

## 📄 License

MIT
