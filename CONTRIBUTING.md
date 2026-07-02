# Contributing to RiftPilot

RiftPilot is an early-stage, local-first League of Legends item recommendation prototype. Contributions are welcome, especially when they make the project more accurate, easier to run, or easier to understand.

## Ways to Contribute

- Bug reports: include your OS, how you started the app, which mode you used, and the steps needed to reproduce the issue.
- Feature suggestions: explain the player problem, the data source needed, and whether the feature is a current implementation idea or future roadmap item.
- Documentation improvements: clarify setup, replay workflow, recommendation logic, limitations, or examples.
- Pull Requests: keep changes focused and describe what was tested.

## Pull Request Guidelines

- Keep Current Features factual and based on code that exists in the repository.
- Do not describe planned work as implemented.
- Avoid claims such as automatic item buying, direct `.rofl` parsing, exact full damage simulation, or complete champion coverage unless those features are actually implemented.
- Run the regression tests before opening a PR:

```bash
python -B test_overlay_logic.py
```

- If you change JavaScript files, also run syntax checks when Node.js is available:

```bash
node --check server.js
node --check app.js
```

- Update `CHANGELOG.md` for user-visible changes.
- Update `ROADMAP.md` when a planned feature becomes implemented.

## Local Development

Start the local server:

```bash
node server.js
```

Run the desktop overlay:

```bash
python overlay.py
```

Collecting Master+ build statistics is optional and requires a Riot API key. The core app should remain usable without a bundled API key or generated production dataset.

## Project Tone

RiftPilot should stay honest about its stage: local-first, explainable, and heuristic-based. Clear limitations are better than inflated claims.
