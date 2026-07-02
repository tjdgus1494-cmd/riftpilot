# Changelog

All notable project changes should be documented in this file.

## [0.1.0] - 2026-07-03

### Initial Public Release

- Added a local web dashboard for demo, live, sample replay, and local replay-style workflows.
- Added a Python/Tkinter desktop overlay for viewing item recommendations while watching gameplay or replay data.
- Added a local Node.js server for static files and local proxy endpoints.
- Added Riot Live Client Data API proxy support.
- Added local replay endpoint support and replay playback controls where Riot local replay APIs are available.
- Added Riot Data Dragon proxy support for item and champion metadata.
- Added an explainable, heuristic-based item recommendation engine.
- Added threat-aware recommendation factors for damage type, healing, shielding, crowd control, burst risk, and item timing.
- Added optional Master+ build statistics collection through `collect_master_build_stats.py`.
- Added support for 1-core, 2-core, and 3-core build path comparison when local Master+ stats are available.
- Added latest recommendation snapshot output at `data/latest_recommendation.json`.
- Added regression tests for selected overlay recommendation logic in `test_overlay_logic.py`.
- Added `DEVELOPMENT_LOG.md` for implementation notes and iteration history.

### Notes

- This release does not include direct `.rofl` file parsing.
- This release does not include automatic item purchasing or gameplay automation.
- Master+ build statistics require a user-provided Riot API key and generated local data.
