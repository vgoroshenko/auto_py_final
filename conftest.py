import time
import pytest
import os
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.safari.options import Options as SafariOptions
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


@pytest.fixture(scope='session', params=test_browsers, ids=lambda x: 'Browser: {}'.format(x))
def browser(request):
    browser = get_web_driver(request.param)
    request.addfinalizer(lambda *args: allure.attach(browser.get_screenshot_as_png(), name='name',
                                                     attachment_type=AttachmentType.PNG) and browser.quit())
    return browser


def desired_caps(browser: str):
    options = browser_options[browser]()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    caps = options
    return caps


def get_web_driver(browser_name: str):
    browser = None
    try:
        browser = webdriver.Remote(
            command_executor=config.webdriver_host,
            options=desired_caps(browser_name)
        )
    except WebDriverException as e:
        pytest.exit(print(e))
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
                    allure.attach(
                        web_driver.get_screenshot_as_png(),
                        name='step_screenshot_' + f'{time.asctime().split()[-2]}',
                        attachment_type=allure.attachment_type.PNG
                    )
                else:
                    print('Fail to take screen-shot')
                    return
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
