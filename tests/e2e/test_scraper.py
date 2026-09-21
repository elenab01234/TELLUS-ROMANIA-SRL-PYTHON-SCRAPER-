"""End-to-end test: scrape the real eJobs employer page for CALLPOINT NEW EUROPE SRL.

The scraper reads the TELUS Digital (CALLPOINT NEW EUROPE SRL) employer page on
eJobs.ro (company id 45016). Skips (rather than fails) when the board is
unreachable, so CI does not break on transient network issues.
"""

import socket

import pytest

from scraper import index

# The employer page currently lists a few open positions and also occasionally
# foreign relocation roles that are filtered out. A sane lower bound protects
# against board restructures without being brittle.
EXPECTED_MIN_JOBS = 1


def _board_reachable():
    try:
        with socket.create_connection(("www.ejobs.ro", 443), timeout=5):
            return True
    except OSError:
        return False


def test_scrape_real_board():
    if not _board_reachable():
        pytest.skip("eJobs not reachable")
    html = index.fetch_listing()
    jobs = index.parse_api_jobs(html)
    assert len(jobs) >= EXPECTED_MIN_JOBS, f"Expected >= {EXPECTED_MIN_JOBS} jobs, got {len(jobs)}"
    for job in jobs:
        assert job["url"].startswith("https://www.ejobs.ro/user/locuri-de-munca/")
        assert job["title"]
    urls = {j["url"] for j in jobs}
    assert len(urls) == len(jobs), "duplicate job URLs found"