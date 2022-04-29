class Config:
    # host can be overriden by pytest command line option '--host' (see conftest.py)
    host = 'localhost'  # Use host.docker.internal to go to local host from selenium grid docker
    api_host = 'https://localhost/api'
    webdriver_host = 'http://{}:4444/wd/hub'.format(host)
    local_screenshot_folder = 'screenshots'


config = Config()