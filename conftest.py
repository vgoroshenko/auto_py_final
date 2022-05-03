import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


def pytest_addoption(parser):
    parser.addoption('--language', action='store', default=None,
                     help="Choose browser language")


@pytest.fixture(scope="function")
def browser(request):
    language = request.config.getoption("language")
    browser = None
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1920,1080')
    options.add_experimental_option('prefs', {'intl.accept_languages': f"{language}-us"})
    browser = webdriver.Chrome(options=options)
    # browser = webdriver.Remote(
    #     command_executor='http://localhost:4444/wd/hub',
    #     desired_capabilities={
    #         "browserName": "chrome",
    #         "javascriptEnabled": True,
    #     },
    #     options=options
    #     )
    yield browser
    print("\nquit browser..")
    browser.quit()
