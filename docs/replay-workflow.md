# Replay Workflow

This guide explains the replay-style workflow currently supported by RiftPilot.

RiftPilot does not parse `.rofl` files directly. It works with the local League of Legends client and the local endpoints that are available while a game or replay is running.

## Requirements

- League of Legends client installed
- A live game or replay opened in the League client
- RiftPilot local server running at `http://127.0.0.1:5177/`
- Optional desktop overlay running with `python overlay.py`

## Start the Local Server

```powershell
node server.js
```

Open the web dashboard:

```text
http://127.0.0.1:5177/
```

## Use Replay-Style Mode

1. Open a replay in the League client.
2. Start RiftPilot with `node server.js`.
3. Open the RiftPilot web dashboard.
4. Select the replay-style workflow in the dashboard.
5. If Riot local replay endpoints are available, RiftPilot can read playback-style data and expose replay controls.
6. If live-style participant data is available, the recommendation logic can use visible champion, item, and game-state information.

Availability can vary depending on the League client state and what Riot's local endpoints expose at that moment.

## Use the Desktop Overlay

```powershell
python overlay.py
```

The overlay polls the local RiftPilot server and displays recommendation cards in a small desktop window. It can show connection states such as waiting for replay data or server connection errors.

## What This Workflow Supports

- Local replay-style endpoint polling
- Replay playback controls when Riot local replay APIs are available
- Recommendation updates from available local game data
- Desktop overlay display while watching gameplay or replay data
- Automatic gold estimation when exact gold is not available

## Current Limitations

- Direct `.rofl` file parsing is not implemented.
- Replay support depends on local endpoints exposed by the League client.
- Some values are estimated because replay/local APIs do not expose every detail needed for exact simulation.
- RiftPilot does not buy items or automate gameplay.
- Recommendation logic is heuristic-based and inspectable, not a production-grade prediction model.
