"""Unit tests for the applytojob listing parser."""

import json

from scraper import index

SAMPLE_HTML = """
<html><body>
<div class="row">
  <a class="job_title_link" href="/apply/jobs/details/ABC123?department=E-INFRA">Inginer Ofertare Energetic</a>
</div>
<div class="row">
  <a class="job_title_link" href="/apply/jobs/details/DEF456?department=E-INFRA">SCADA Engineer</a>
</div>
</body></html>
"""

SAMPLE_TABLE_HTML = """
<html><body><table>
  <tr>
    <td><a class="job_title_link" href="/apply/jobs/details/AAA111?department=E-INFRA">Job A</a></td>
    <td>Bucuresti, Bucuresti, Romania</td>
  </tr>
  <tr>
    <td><a class="job_title_link" href="/apply/jobs/details/BBB222?department=E-INFRA">Job B</a></td>
    <td>Cluj-Napoca, Cluj, Romania</td>
  </tr>
</table></body></html>
"""


def test_build_listing_url(scraper_config):
    url = index.build_listing_url()
    assert url.startswith("https://")
    assert "applytojob.com" in url
    assert "department=" in url


def test_build_job_url():
    assert index.build_job_url("ABC123") == "https://electrogrup.applytojob.com/apply/jobs/details/ABC123"


def test_build_job_url_preserves_job_id():
    assert index.build_job_url("ABC123") == "https://electrogrup.applytojob.com/apply/jobs/details/ABC123"


def test_extract_location_takes_first_token():
    assert index.extract_location("Bucuresti, Bucuresti, Romania") == ["Bucuresti"]
    assert index.extract_location("Cluj-Napoca, Cluj, Romania") == ["Cluj-Napoca"]


def test_extract_location_single_token():
    assert index.extract_location("Romania") == ["România"]


def test_extract_location_missing():
    assert index.extract_location(None) == []
    assert index.extract_location("") == []


def test_parse_api_jobs_link_divs():
    jobs = index.parse_api_jobs(SAMPLE_HTML)
    assert len(jobs) == 2
    assert jobs[0]["title"] == "Inginer Ofertare Energetic"
    assert jobs[0]["url"].endswith("/apply/jobs/details/ABC123")
    assert jobs[0]["location"] == ["România"]


def test_parse_api_jobs_table_rows():
    jobs = index.parse_api_jobs(SAMPLE_TABLE_HTML)
    assert len(jobs) == 2
    by_url = {j["url"]: j for j in jobs}
    assert by_url["https://electrogrup.applytojob.com/apply/jobs/details/AAA111"]["location"] == ["Bucuresti"]
    assert by_url["https://electrogrup.applytojob.com/apply/jobs/details/BBB222"]["location"] == ["Cluj-Napoca"]


def test_parse_api_jobs_deduplicates():
    html = SAMPLE_HTML + SAMPLE_HTML
    jobs = index.parse_api_jobs(html)
    assert len(jobs) == 2


def test_parse_api_jobs_empty():
    assert index.parse_api_jobs("<html></html>") == []


def test_map_to_job_model_adds_company_and_status():
    raw = {"url": "https://electrogrup.applytojob.com/apply/jobs/details/ABC123",
           "title": "SCADA Engineer", "location": ["Bucuresti"]}
    index.COMPANY_NAME = "E-INFRA S.A."
    job = index.map_to_job_model(raw, "38647188")
    assert job["company"] == "E-INFRA S.A."
    assert job["cif"] == "38647188"
    assert job["status"] == "scraped"
    assert job["location"] == ["Bucuresti"]


def test_transform_jobs_for_solr_keeps_required_fields():
    jobs = [{"url": "https://x/job", "title": "Test Job", "location": ["Cluj-Napoca"],
             "company": "E-INFRA S.A.", "cif": "38647188"}]
    transformed = index.transform_jobs_for_solr({"company": "E-INFRA S.A.", "jobs": jobs})
    assert len(transformed["jobs"]) == 1
    t = transformed["jobs"][0]
    assert t["url"]
    assert t["title"]
    assert t["location"] == ["Cluj-Napoca"]
    assert t["company"] == "E-INFRA S.A."


def test_transform_workmode_normalized():
    jobs = [{"url": "https://x/1", "title": "Dev", "location": ["Cluj-Napoca"], "workmode": "Remote"}]
    transformed = index.transform_jobs_for_solr({"company": "E-INFRA S.A.", "jobs": jobs})
    assert transformed["jobs"][0]["workmode"] == "remote"


def test_transform_missing_workmode_dropped():
    jobs = [{"url": "https://x/1", "title": "Dev", "location": ["Cluj-Napoca"]}]
    transformed = index.transform_jobs_for_solr({"company": "E-INFRA S.A.", "jobs": jobs})
    assert "workmode" not in transformed["jobs"][0]


def test_generate_jobs_markdown(tmp_path, company_config):
    jobs = [{"url": "https://x/job", "title": "Inginer Ofertare Energetic",
             "company": "E-INFRA S.A.", "cif": "38647188",
             "location": ["Bucuresti"], "workmode": "on-site"}]
    md = index.generate_jobs_markdown(company_config, jobs)
    assert f"# {company_config['company']}" in md
    assert "## Jobs (1)" in md
    assert "Inginer Ofertare Energetic" in md
    assert "](https://x/job)" in md


def test_generate_jobs_markdown_empty():
    md = index.generate_jobs_markdown({}, [])
    assert "## Jobs (0)" in md
    assert "_No jobs found._" in md


def test_main_dry_run_writes_summary(tmp_path, monkeypatch):
    fake_jobs = [{"url": f"https://x/{i}", "title": f"Job {i}", "location": ["Cluj-Napoca"]}
                 for i in range(3)]
    monkeypatch.setattr(index, "parse_api_jobs", lambda html: fake_jobs)
    monkeypatch.setattr(index, "fetch_listing", lambda: "<html>fake</html>")
    monkeypatch.setattr(index, "query_solr", lambda cif: {"numFound": 1, "docs": []})
    monkeypatch.setattr(index, "upsert_jobs", lambda jobs: None)
    monkeypatch.setattr(index, "delete_job_by_url", lambda url: None)
    monkeypatch.setattr(index, "upsert_company", lambda cfg: None)
    monkeypatch.setattr(index, "validate_and_get_company", lambda: {
        "company": "E-INFRA S.A.", "cif": "38647188", "status": "active",
        "address": "CLUJ-NAPOCA"})
    monkeypatch.setattr(index, "search_anofm", lambda cif: [])

    index.main(root=tmp_path)
    out = tmp_path / "scraper" / "jobs.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert len(data["jobs"]) >= 3
