# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-08-03

### Added
- Python scraper for the E-INFRA S.A. department on the group's applytojob board (`?department=E-INFRA`).
- Publisher to peviitor v1 API: company upsert, job upload, stale-job delete.
- ANAF company validation with CUIScan fallback and cache.
- ANOFM job search mirroring the Node.js template.
- `validate_jobs.py` CLI for head/content URL validation.
- Unit, integration, e2e, and consistency tests.
- GitHub Actions workflows: `job-seeker-ro-spider`, `automation-testing`, deep-validate, recovery.
- GitHub Pages (`docs/`) with generated `jobs.md` and `company.json`.
- AI documentation under `ai/`.

### Fixed
- Location normalization: common spellings (`Bucuresti`, `Turda`, etc.) and case/diacritic variants are no longer dropped to `România`.
- Stale-job deletion is scoped to this scraper's applytojob board, so jobs published by other peviitor scrapers under the same CIF are never removed.
- E2E `EXPECTED_MIN_JOBS` and integration tests reflect the E-INFRA department and CIF `38647188`.
