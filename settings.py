class Config:
    host = 'localhost'
    api_host = 'https://localhost/api'
    webdriver_host = 'http://{}:4444/wd/hub'.format(host)
    local_screenshot_folder = 'screenshots'


config = Config()