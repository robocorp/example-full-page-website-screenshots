import csv
import os
import time
from pathlib import Path
from urllib.parse import urlparse

from robocorp import browser, log
from robocorp.tasks import task

OUTPUT_DIR = Path(os.environ.get("ROBOT_ARTIFACTS", "output"))
DEVDATA = Path("devdata")

ACCEPT_COOKIES_SELECTOR = "accept_cookies_selector"
DATA_CONSENT_SELECTOR = "data_consent_selector"


@task
def take_website_screenshots():
    """Take screenshots of all websites found in websites.csv file."""
    with open(str(DEVDATA / "websites.csv")) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        websites = list(csv_reader)

    for website in websites:
        browser.goto(website["url"])
        page = browser.page()

        accept_cookies_and_consents(website)

        # Some websites have animations on cookies and consents so wait for that to
        #  disappear.
        time.sleep(1)

        domain = urlparse(website["url"]).netloc.replace(".", "_")
        page.screenshot(path=str(OUTPUT_DIR / f"{domain}.png"), full_page=True)


def accept_cookies_and_consents(website: dict):
    """
    Accept cookies and data consents on every page before taking a screenshot.

    Args:
        website (dict): A dictionary with website related info, including the locators
            to find the consent elements with.
    """
    page = browser.page()

    cookie_selector = website.get(ACCEPT_COOKIES_SELECTOR)
    if cookie_selector:
        try:
            page.locator(cookie_selector).click()
        except Exception as exc:
            log.warn(f"An error occurred during the cookies accept: {exc}")

    data_consent_selector = website.get(DATA_CONSENT_SELECTOR)
    if data_consent_selector:
        try:
            if "frame" in data_consent_selector:
                locator = page.frames[len(page.frames) - 1].locator(
                    data_consent_selector.split(":")[1]
                )
            else:
                locator = page.locator(data_consent_selector)

            locator.click()
        except Exception as exc:
            log.warn(f"An error occurred during the data consent: {exc}")
