# balloon-ranking-data

Nightly snapshot of the normalized event data and computed rating
state for the [Global Balloon Pilot Ranking System](https://github.com/zerekw/balloon-ranking-glicko).

## Layout

- `meta.json` — engine version, last update timestamp, parameter values.
- `pilots.json` — all canonical pilots.
- `events/{event_id}.json` — one file per event with tasks + results.
- `ratings/snapshots.jsonl` — one line per (pilot, event) snapshot.
- `current/rankings.json` — current public ranking, denormalized.

## Reproducing the ratings

```
pip install balloon-ranking-glicko
python verify.py
```

## License

CC-BY 4.0. Attribution required, commercial use permitted.
