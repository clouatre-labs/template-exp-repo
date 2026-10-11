# Experiments

One directory per pre-registered experiment: `experiments/<slug>/`.

## Required Layout

```text
experiments/<slug>/
  protocol.md        # pre-registered design: task, groups, sample size, statistical test
  runner-prompt.md   # exact prompt given to the runner/agent
  scorer-prompt.md   # exact prompt given to the scorer
  analysis.json      # run metadata and scores (schema in DATA_DICTIONARY.md)
  scores.json        # per-criterion rubric scores with justifications
  sessions/          # raw session logs or database exports
```

## Workflow

1. Commit `protocol.md`, `runner-prompt.md`, and `scorer-prompt.md` BEFORE running anything.
2. Run the experiment; store raw artifacts under `sessions/`.
3. Score blind against the rubric; write `scores.json`.
4. Summarize into `analysis.json` and validate: `uv run python validate_schema.py`. Validation iterates every `experiments/*/` directory; one missing `analysis.json` is a validation error (exit 1).
5. Update the experiment index table in the repository README.
