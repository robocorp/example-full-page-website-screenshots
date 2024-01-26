# A robot that takes full page screenshots of given websites

[![YouTube video](https://img.youtube.com/vi/aQkXTHP3Xxw/0.jpg)](http://www.youtube.com/watch?v=aQkXTHP3Xxw)

- Reads the website data (URL, accept cookies and consent selectors) from a `.csv` using the python csv built in library.

- Uses the [Playwright](https://playwright.dev/)-based [Python Framework Browser](https://robocorp.com/docs/python/robocorp/robocorp-browser) library to take full page screenshots of the websites.

## Example csv file

`websites.csv`:

```
url,accept_cookies_selector,data_consent_selector
https://www.nytimes.com/,"xpath=//div[contains(@class, 'fides-banner-button-group')]//button[text()='Accept all']",
https://www.themoscowtimes.com/,,"frame:css=.sp_choice_type_11"
https://www.japantimes.co.jp/,,"css=.fc-cta-consent > .fc-button-label"
```

## Example screenshot

BBC - Homepage

<img src="images/bbc.png" style="margin-bottom:20px">
