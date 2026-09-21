"""Unit tests for the eJobs employer-page listing parser."""

import json

from scraper import index

SAMPLE_HTML = """
<html><body>
<li class="job-card-wrapper job-card-wrapper--visible">
  <div class="job-card">
    <div class="job-card-content">
      <div class="job-card-content-middle">
        <h2 class="job-card-content-middle__title">
          <a href="/user/locuri-de-munca/level-2-customer-support-agent/111"><span>Level 2 Customer Support Agent</span></a>
        </h2>
        <h3 class="job-card-content-middle__info job-card-content-middle__info--darker">TELUS Digital</h3>
        <div class="job-card-content-middle__info">București</div>
      </div>
    </div>
  </div>
</li>
<li class="job-card-wrapper job-card-wrapper--visible">
  <div class="job-card">
    <div class="job-card-content">
      <div class="job-card-content-middle">
        <h2 class="job-card-content-middle__title">
          <a href="/user/locuri-de-munca/danish-customer-support/222"><span>Danish Customer Support Representative</span></a>
        </h2>
        <h3 class="job-card-content-middle__info job-card-content-middle__info--darker">TELUS Digital</h3>
        <div class="job-card-content-middle__info">București</div>
      </div>
    </div>
  </div>
</li>
</body></html>
"""

FOREIGN_HTML = """
<html><body>
<li class="job-card-wrapper">
  <div class="job-card-content-middle">
    <h2 class="job-card-content-middle__title">
      <a href="/user/locuri-de-munca/relocation-sofia/333"><span>Player Support with German - Relocation to Sofia, Bulgaria</span></a>
    </h2>
    <h3 class="job-card-content-middle__info job-card-content-middle__info--darker">TELUS Digital</h3>
    <div class="job-card-content-middle__info">Străinătate, Bulgaria</div>
  </div>
</li>
</body></html>
"""

REMOTE_HTML = """
<html><body>
<li class="job-card-wrapper">
  <div class="job-card-content-middle">
    <h2 class="job-card-content-middle__title">
      <a href="/user/locuri-de-munca/csr-french-remote/444"><span>French Customer Support Representative</span></a>
    </h2>
    <h3 class="job-card-content-middle__info job-card-content-middle__info--darker">TELUS Digital</h3>
    <div class="job-card-content-middle__info">Lucru de acasă</div>
  </div>
</li>
</body></html>
"""


def test_build_listing_url(scraper_config):
    url = index.build_listing_url()
    assert url.startswith("https://")
    assert "ejobs.ro" in url
    assert "/company/" in url


def test_make_absolute_absolute_url():
    assert index.make_absolute("https://x/y") == "https://x/y"


def test_make_absolute_relative_url():
    assert index.make_absolute("/user/locuri-de-munca/a/1").startswith("https://www.ejobs.ro/")
    assert index.make_absolute("user/locuri-de-munca/a/1").startswith("https://www.ejobs.ro/")


def test_job_id_from_url():
    assert index.job_id_from_url("https://www.ejobs.ro/user/locuri-de-munca/foo/123") == "123"
    assert index.job_id_from_url("/user/locuri-de-munca/foo/123") == "123"
    assert index.job_id_from_url("https://www.ejobs.ro/company/x/1") is None


def test_extract_location_takes_first_token():
    assert index.extract_location("Bucuresti, Ilfov") == ["Bucuresti"]
    assert index.extract_location("Cluj-Napoca, Cluj") == ["Cluj-Napoca"]


def test_extract_location_country_token():
    assert index.extract_location("România") == ["România"]
    assert index.extract_location("Romania") == ["România"]


def test_extract_location_remote_maps_to_romania():
    assert index.extract_location("Lucru de acasă") == ["România"]
    assert index.extract_location("Work from home") == ["România"]


def test_extract_location_missing():
    assert index.extract_location(None) == []
    assert index.extract_location("") == []
    assert index.extract_location("   ") == []


def test_parse_api_jobs_cards():
    jobs = index.parse_api_jobs(SAMPLE_HTML)
    assert len(jobs) == 2
    assert jobs[0]["title"] == "Level 2 Customer Support Agent"
    assert jobs[0]["url"] == "https://www.ejobs.ro/user/locuri-de-munca/level-2-customer-support-agent/111"
    assert jobs[0]["location"] == ["București"]
    assert jobs[1]["title"] == "Danish Customer Support Representative"


def test_parse_api_jobs_deduplicates():
    html = SAMPLE_HTML + SAMPLE_HTML
    jobs = index.parse_api_jobs(html)
    assert len(jobs) == 2


def test_parse_api_jobs_skips_foreign_relocation():
    jobs = index.parse_api_jobs(FOREIGN_HTML)
    assert jobs == []


def test_parse_api_jobs_remote_maps_to_romania():
    jobs = index.parse_api_jobs(REMOTE_HTML)
    assert len(jobs) == 1
    assert jobs[0]["location"] == ["România"]
    assert jobs[0]["workmode"] == "remote"


def test_parse_api_jobs_skips_cards_without_link():
    jobs = index.parse_api_jobs("<html><li class='job-card-wrapper'><span>no link</span></li></html>")
    assert jobs == []


def test_parse_api_jobs_empty():
    assert index.parse_api_jobs("<html></html>") == []


def test_map_to_job_model_adds_company_and_status():
    raw = {"url": "https://www.ejobs.ro/user/locuri-de-munca/foo/1",
           "title": "Customer Support", "location": ["București"]}
    index.COMPANY_NAME = "CALLPOINT NEW EUROPE SRL"
    job = index.map_to_job_model(raw, "21147668")
    assert job["company"] == "CALLPOINT NEW EUROPE SRL"
    assert job["cif"] == "21147668"
    assert job["status"] == "scraped"
    assert job["location"] == ["București"]


def test_transform_jobs_for_solr_keeps_required_fields():
    jobs = [{"url": "https://x/job", "title": "Test Job", "location": ["Cluj-Napoca"],
             "company": "CALLPOINT NEW EUROPE SRL", "cif": "21147668"}]
    transformed = index.transform_jobs_for_solr({"company": "CALLPOINT NEW EUROPE SRL", "jobs": jobs})
    assert len(transformed["jobs"]) == 1
    t = transformed["jobs"][0]
    assert t["url"]
    assert t["title"]
    assert t["location"] == ["Cluj-Napoca"]
    assert t["company"] == "CALLPOINT NEW EUROPE SRL"


def test_transform_workmode_normalized():
    jobs = [{"url": "https://x/1", "title": "Dev", "location": ["Cluj-Napoca"], "workmode": "Remote"}]
    transformed = index.transform_jobs_for_solr({"company": "CALLPOINT NEW EUROPE SRL", "jobs": jobs})
    assert transformed["jobs"][0]["workmode"] == "remote"


def test_transform_missing_workmode_dropped():
    jobs = [{"url": "https://x/1", "title": "Dev", "location": ["Cluj-Napoca"]}]
    transformed = index.transform_jobs_for_solr({"company": "CALLPOINT NEW EUROPE SRL", "jobs": jobs})
    assert "workmode" not in transformed["jobs"][0]


def test_generate_jobs_markdown(tmp_path, company_config):
    jobs = [{"url": "https://x/job", "title": "Level 2 Customer Support Agent",
             "company": "CALLPOINT NEW EUROPE SRL", "cif": "21147668",
             "location": ["București"], "workmode": "on-site"}]
    md = index.generate_jobs_markdown(company_config, jobs)
    assert f"# {company_config['company']}" in md
    assert "## Jobs (1)" in md
    assert "Level 2 Customer Support Agent" in md
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
        "company": "CALLPOINT NEW EUROPE SRL", "cif": "21147668", "status": "active",
        "address": "MUNICIPIUL BUCURESTI, SECTOR 6"})
    monkeypatch.setattr(index, "search_anofm", lambda cif: [])

    index.main(root=tmp_path)
    out = tmp_path / "scraper" / "jobs.json"
    assert out.exists()
    data = json.loads(out.read_text())
    assert len(data["jobs"]) >= 3