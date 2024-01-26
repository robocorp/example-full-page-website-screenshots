import csv
import time
from urllib.parse import urlparse
from robocorp.tasks import task
from robocorp import browser


@task
def take_website_screenshots():
    """Take screenshots of all websites found in websites.csv file."""
    with open("websites.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        websites = list(csv_reader)

    for website in websites:
        browser.goto(website["url"])
        page = browser.page()

        accept_cookies_and_consents(website)

        # some websites have animations on cookies and consents so wait for that to disappear
        time.sleep(1)

        domain = get_domain_name(website["url"])
        page.screenshot(path=f"output/{domain}.png", full_page=True)


def get_domain_name(url) -> str:
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")

    # Check if the domain has subdomains and extract the second-to-last part
    if len(domain_parts) >= 2:
        return domain_parts[-2]

    return domain_parts[0]


def accept_cookies_and_consents(website):
    page = browser.page()

    if website["accept_cookies_selector"]:
        try:
            page.locator(website["accept_cookies_selector"]).click()
        except Exception:
            pass

    data_consent_selector = website["data_consent_selector"]
    if website["data_consent_selector"]:
        try:
            if "frame" in data_consent_selector:
                locator = page.frames[len(page.frames) - 1].locator(
                    data_consent_selector.split(":")[1]
                )
            else:
                locator = page.locator(data_consent_selector)

            locator.click()
        except Exception:
            pass
