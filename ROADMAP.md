# Roadmap

RiftPilot is an early-stage, local-first, explainable item recommendation prototype. This roadmap separates current implemented work from planned features.

## Currently Implemented

- Local web dashboard for demo, live, sample replay, and local replay-style workflows.
- Desktop overlay built with Python/Tkinter.
- Local Node.js server for static files and proxy endpoints.
- Riot Live Client Data API proxy.
- Local replay endpoint support and playback controls where Riot local replay APIs are available.
- Riot Data Dragon proxy for item and champion metadata.
- Explainable, heuristic-based item recommendation logic.
- Threat-aware item scoring for damage type, healing, shielding, crowd control, burst risk, and purchase timing.
- Optional Master+ build statistics collector.
- 1-core, 2-core, and 3-core build path comparison when local stats are available.
- Latest recommendation snapshot output.
- Regression tests for selected recommendation logic.

## Planned

These items are not implemented yet.

- Champion recommendation during Ban/Pick.
- Player history analysis.
- Team composition analysis.
- Replay workflow documentation with screenshots or GIFs.
- Test coverage expansion.

## Not Current Features

The following should not be described as implemented until the code supports them:

- Direct `.rofl` file parsing.
- Automatic item buying.
- Exact full champion damage simulation.
- Complete champion-specific coverage.
- Production-grade recommendation accuracy validation.
