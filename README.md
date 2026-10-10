<p align="center">
  <a href="https://conventionalcommits.org"><img alt="Conventional Commits" src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=for-the-badge" height="20"></a>
  <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template"><img alt="GitHub Template" src="https://img.shields.io/badge/GitHub-Template-blue.svg?style=for-the-badge&logo=github" height="20"></a>
</p>

<h1 align="center">{{REPO_NAME}}</h1>

{{TITLE}}. TODO: one-paragraph description of what this repository studies and why.

## Experiment Index

| Slug | Question | Status | Key Result |
|------|----------|--------|------------|
| `<slug>` | TODO | planned \| running \| analyzed | TODO |

## Repository Layout

- `experiments/` - one directory per pre-registered experiment (see [experiments/README.md](experiments/README.md))
- `recipe/` - analysis notebooks and scripts that regenerate figures
- `figures/` - generated figures
- [METHODOLOGY.md](METHODOLOGY.md) - shared experimental design contract
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) - schema for `analysis.json` and `scores.json`
- [CITATION.cff](CITATION.cff) and `.zenodo.json` - citation metadata

## Reproduction

1. Clone the repository and check out the tag matching the release.
2. Install [uv](https://docs.astral.sh/uv/).
3. Validate the dataset schema:

   ```bash
   uv run python validate_schema.py
   ```

4. Regenerate figures from the recipes in `recipe/`.

Each experiment directory under `experiments/` contains its protocol, runner and scorer prompts, raw sessions, and analysis records, so any result can be traced back to its pre-registered design.

## Citing This Work

See [CITATION.cff](CITATION.cff). TODO: fill in authors, version, release date, and DOI before first release.

## Using This Template

Clone or click **Use this template**, then run `bash scripts/bootstrap.sh` to create standard labels and work through the post-clone checklist in [docs/REPO-STANDARDS.md](docs/REPO-STANDARDS.md). Replace all `{{...}}` placeholders in this README, [CITATION.cff](CITATION.cff), `.zenodo.json`, and [CONTRIBUTING.md](CONTRIBUTING.md).
