import os
import allure
import urllib3
from selenium.common.exceptions import WebDriverException
from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.safari.options import Options as SafariOptions

import pytest
from .webdriver_augmented import WebDriverAugmented
from .settings import config

CHROME_BROWSER_NAME = 'Chrome'
FIREFOX_BROWSER_NAME = 'Firefox'
EDGE_BROWSER_NAME = 'MicrosoftEdge'
SAFARI_BROWSER_NAME = 'Safari'
OPERA_BROWSER_NAME = 'Opera'

test_browsers = [CHROME_BROWSER_NAME, EDGE_BROWSER_NAME, FIREFOX_BROWSER_NAME, SAFARI_BROWSER_NAME]

browser_options = {
    CHROME_BROWSER_NAME: ChromeOptions,
    FIREFOX_BROWSER_NAME: FirefoxOptions,
    EDGE_BROWSER_NAME: EdgeOptions,
    SAFARI_BROWSER_NAME: SafariOptions,
    OPERA_BROWSER_NAME: OperaOptions
}

def desired_caps(browser: str):
    options = browser_options[browser]()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument('--window-size=1920,1080')
    caps = options
    return caps

def get_web_driver(browser_name: str) -> WebDriverAugmented:
    browser = None
    try:
        browser = WebDriverAugmented(
            command_executor=config.webdriver_host,
            options=desired_caps(browser_name)
        )
        browser.browser_name = browser_name
        browser.page_timer.start()
    except WebDriverException as e:
        pytest.exit(print(e))
    except (urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError) as e:
        pytest.exit(print(e))
    return browser

@pytest.fixture(scope='session', params=test_browsers, ids=lambda x: 'Browser: {}'.format(x))
def browser(request):
    browser = get_web_driver(request.param)
    request.addfinalizer(lambda *args: allure.attach(browser.get_screenshot_as_png(), name='name', attachment_type=AttachmentType.PNG) and browser.quit())
    return browser

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed or 'call' and rep.passed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'browser' in item.fixturenames:
                    web_driver = item.funcargs['browser']
                else:
                    print('Fail to take screen-shot')
                    return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
            if web_driver.browser_name != FIREFOX_BROWSER_NAME:
                # Firefox do not support js logs: https://github.com/SeleniumHQ/selenium/issues/2972
                allure.attach(
                    '\n'.join(web_driver.get_log('browser')),
                    web_driver.get_screenshot_as_png(),
                    name='console log:',
                    attachment_type=allure.attachment_type.TEXT and allure.attachment_type.PNG

                )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))