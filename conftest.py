import os
import random
import allure
import urllib3
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.events import AbstractEventListener
from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import pytest
from .webdriver_augmented import WebDriverAugmented
from .settings import config

CHROME_BROWSER_NAME = 'Chrome'
FIREFOX_BROWSER_NAME = 'Firefox'

test_browsers = [CHROME_BROWSER_NAME, FIREFOX_BROWSER_NAME]
browser_options = {
    CHROME_BROWSER_NAME: ChromeOptions, # DesiredCapabilities.CHROME,
    FIREFOX_BROWSER_NAME: FirefoxOptions,  # DesiredCapabilities.FIREFOX
}

def desired_caps(browser: str) -> DesiredCapabilities:
    options = browser_options[browser]()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-client-side-phishing-detection")
    caps = options.to_capabilities()
    caps['platform'] = 'Linux'
    return caps

def get_web_driver(browser_name: str) -> WebDriverAugmented:
    """
    Creates remote web driver (located on selenium host) for desired browser.
    """
    FAIL_HELP = f'''
    Fail to connect to selenium webdriver remote host {config.webdriver_host}.
    To run local selenium hub from tests_e2e folder: 
        docker-compose up -d
    To restart freezing local selenium hub:
        restart_selenium.sh
    '''
    browser = None
    try:
        browser = WebDriverAugmented(
            command_executor=config.webdriver_host,
            desired_capabilities=desired_caps(browser_name)
        )
        browser.browser_name = browser_name
        browser.page_timer.start()
    except WebDriverException as e:
        pytest.exit(FAIL_HELP + f':\n\n{e}\n')
    except (urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError) as e:
        pytest.exit(FAIL_HELP + f':\n\n{e}\n')
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
                    name='js console log:',
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))