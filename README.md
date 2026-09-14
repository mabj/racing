# Racing

A personal training and race log for triathlon and endurance racing.

Each race gets its own folder, organized by year and month, containing:

- **`README.md`** — race details (distance, date, location), results breakdown, training plan and volume statistics, sleep analysis, and "What Went Wrong" / "What Went Well" retrospectives;
- **`data/`** — raw training data (activities, sleep) exported from tracking tools, plus the scripts used to generate charts from it;
- **`image/`** — generated charts (training volume, sport distribution, sleep trends, etc.) embedded in the race `README.md`.

## Structure

```
<year>/<month>_<race_name>/
├── README.md
├── data/
└── image/
```

## Goal

Track training cycles and race outcomes over time, and use each race's retrospective to inform preparation for the next one.
