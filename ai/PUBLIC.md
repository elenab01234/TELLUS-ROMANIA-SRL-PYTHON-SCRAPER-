# PUBLIC.md — Repository Must Be PUBLIC

All scrapers derived from the template **MUST** be **PUBLIC** repositories.

## Why?

- Peviitor is an open-source platform
- Job data should be accessible to everyone
- Transparency builds trust

## Enforcement

Keep the repository public. The repo is public and hosted at:

- Repository: https://github.com/elenab01234/TELLUS-ROMANIA-SRL-PYTHON-SCRAPER-
- GitHub Pages: https://elenab01234.github.io/TELLUS-ROMANIA-SRL-PYTHON-SCRAPER-/ (`docs/` on `main`, built automatically)
- Scraper workflow: https://github.com/elenab01234/TELLUS-ROMANIA-SRL-PYTHON-SCRAPER-/actions/workflows/job-seeker-ro-spider.yml
- Jobs page: `docs/jobs.md` (generated, committed, served on GitHub Pages)
- Peviitor search: https://peviitor.ro (CIF `21147668`)

## How to check

```bash
gh repo view elenab01234/TELLUS-ROMANIA-SRL-PYTHON-SCRAPER- --json visibility
```
