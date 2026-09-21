# Update Repo About

Keep the GitHub repository metadata up to date.

## Description

Scraper automat pentru locurile de muncă E-INFRA S.A. (CIF: 38647188) — extrage
de pe electrogrup.applytojob.com și publică pe peviitor.ro

## Homepage

https://ale23yfm.github.io/e-infra-sa-python-scraper/

## Topics (exactly 2, per TOPICS.md)

- job-seeker-ro-spider
- peviitor-ro

## Workflow file

`.github/workflows/job-seeker-ro-spider.yml`

## How to apply

```bash
gh repo edit ale23yfm/e-infra-sa-python-scraper \
  --description "Scraper automat pentru locurile de muncă E-INFRA S.A. (CIF: 38647188) — extrage de pe electrogrup.applytojob.com și publică pe peviitor.ro" \
  --homepage "https://ale23yfm.github.io/e-infra-sa-python-scraper/"
```

## GitHub Pages

- Source: branch `main`, path `/docs` (static site, no Pages workflow needed).
- Builds automatically on every push to `main` (`build_type: legacy`).
- Site: https://ale23yfm.github.io/e-infra-sa-python-scraper/
- `docs/jobs.md` is regenerated on each scrape and served on the site.
- Homepage on the repo points to the Pages URL (same as the EPAM template).
