# Repo Health Badge

A lightweight GitHub Action that automatically analyzes repository health and generates a score badge.

## Features

- Full analysis from 4 dimensions: Basic Metrics, Activity, Code Quality, Community Health
- Quantified scoring: 0-100 points + A-F grade
- SVG badge for README embedding
- Easy GitHub Action integration

## Scoring Dimensions

| Dimension | Points | What it checks |
|-----------|--------|----------------|
| Basic Metrics | 30 | Stars, Forks, Watchers |
| Activity | 25 | Recent commits, Issue activity |
| Code Quality | 25 | License, README, CONTRIBUTING, SECURITY, FUNDING, Topics |
| Community Health | 20 | Recent Issues/PRs, Issue/PR templates |

## Quick Start

### Method 1: GitHub Action (Recommended)

Create .github/workflows/health-check.yml in your repo:

```yaml
name: Repo Health Check

on:
  schedule:
    - cron: '0 0 * * 0'
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: LIE28-MAX/repo-health-badge@v1
        with:
          output-format: svg
          output-path: health-badge.svg
```

### Method 2: Standalone Script

```bash
GITHUB_REPOSITORY=owner/repo python src/action.py
```

## Grade Scale

- A (80-100): Excellent
- B (60-79): Good
- C (40-59): Fair
- D (20-39): Poor
- F (0-19): Bad

## License

MIT

---

If you find this project useful, please give it a star!
