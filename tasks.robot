*** Settings ***
Documentation     Takes full page screenshots of given websites.
Library           RPA.Browser.Playwright
Library           RPA.Tables
Task Setup        Register Keyword To Run On Failure    ${NONE}

*** Variables ***
${WEBSITES_CSV}=    websites.csv

*** Keywords ***
Take full page screenshot
    [Arguments]    ${url}    ${accept_cookies_selector}    ${data_consent_selector}
    New Page    ${url}
    Accept cookies and consents
    ...    ${accept_cookies_selector}
    ...    ${data_consent_selector}
    Scroll the page and wait until network is idle
    ${domain}=    Evaluate    urllib.parse.urlparse('${url}').netloc
    Take Screenshot    ${OUTPUT_DIR}${/}${domain}    fullPage=True

*** Keywords ***
Accept cookies and consents
    [Arguments]    ${accept_cookies_selector}    ${data_consent_selector}
    Run Keyword And Ignore Error    Click    ${accept_cookies_selector}
    Run Keyword And Ignore Error    Click    ${data_consent_selector}

*** Keywords ***
Scroll the page and wait until network is idle
    FOR    ${i}    IN RANGE    10
        Scroll By    vertical=100%
    END
    Run Keyword And Ignore Error    Wait Until Network Is Idle

*** Tasks ***
Take full page screenshots of given websites
    @{websites}=    Read Table From Csv    ${WEBSITES_CSV}    header=True
    FOR    ${website}    IN    @{websites}
        Run Keyword And Ignore Error
        ...    Take full page screenshot
        ...    ${website}[url]
        ...    ${website}[accept_cookies_selector]
        ...    ${website}[data_consent_selector]
    END
