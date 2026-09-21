[![Oportunitati si Cariere](https://github.com/ale23yfm/e-infra-sa-python-scraper/actions/workflows/job-seeker-ro-spider.yml/badge.svg)](https://github.com/ale23yfm/e-infra-sa-python-scraper/actions/workflows/job-seeker-ro-spider.yml)
[![Automation Tests](https://github.com/ale23yfm/e-infra-sa-python-scraper/actions/workflows/automation-testing.yml/badge.svg)](https://github.com/ale23yfm/e-infra-sa-python-scraper/actions/workflows/automation-testing.yml)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fpeviitor.ro&label=peviitor.ro)](https://peviitor.ro)
[![API](https://img.shields.io/website?url=https%3A%2F%2Fapi.peviitor.ro%2F&label=api.peviitor.ro)](https://api.peviitor.ro/)
[![GitHub Pages](https://img.shields.io/github/deployments/ale23yfm/e-infra-sa-python-scraper/github-pages?label=GitHub%20Pages)](https://ale23yfm.github.io/e-infra-sa-python-scraper/)

# job_seeker_ro_spider — E-INFRA S.A. Scraper

**job_seeker_ro_spider** — a scraper for E-INFRA S.A. jobs in Romania. It collects the announcements published by the [E-INFRA](https://e-infra.ro/ro/cariere/) department on the group's applytojob board and publishes them to [peviitor.ro](https://peviitor.ro) through the Peviitor API.

> **🌱 Derived scraper.** This repository is derived from [electrogrup-sa-python-scraper](https://github.com/peviitor-scrapers/electrogrup-sa-python-scraper), the reference implementation for Python scrapers in the peviitor.ro ecosystem.

## Overview

The project automates the daily collection of E-INFRA jobs in Romania, keeping the peviitor.ro board up to date with the latest career opportunities.

## Features

- Extracts jobs from the E-INFRA group applytojob board (`?department=E-INFRA` filter)
- Additional ANOFM jobs via CIF
- Validates the company via ANAF (CUI, active/inactive status, full address) with CUIScan fallback
- **ANAF cache** — does not hit the APIs on every scrape
- **Stale cache / config fallback** when ANAF is unavailable
- Cross-validates against the Peviitor API
- Deletes stale jobs (present on the site but not in Peviitor)
- Stores to the Peviitor API (job core + company core)
- Generates `docs/jobs.md` automatically — accessible on GitHub Pages
- **Company identity in a single file** (`scraper/config/company.json`)
- GitHub Actions: daily scrape + automated testing (unit, integration, e2e, consistency)
- Identifies itself through the User-Agent: `job_seeker_ro_spider`

## License

Copyright (c) 2026 Alexandra Ifrim

Licensed under the [MIT License](LICENSE).

## Managed By

This project is managed by [ASOCIATIA OPORTUNITATI SI CARIERE](https://oportunitatisicariere.ro) and used as a web scraper for the [peviitor.ro](https://peviitor.ro) job board project.

## Disclaimer

This scraper is designed for educational purposes and legitimate job data aggregation for the Romanian job market.
