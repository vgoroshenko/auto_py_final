[Stepik Test link](http://selenium1py.pythonanywhere.com/)

[Link to Allure report after run tests](https://vgoroshenko.github.io/auto_py_final/)

# Parallel crossbrowser tests

Used `Pytest + Selenium + Selenoid + Allure`

4 browsers `Chrome, Safari, Firefox, EDGE`


Run selenoid service `docker-compose up -d `, `make pull` 

Install deps for test `pip3 install -r requirements.txt`

Run tests  `pytest -v --tb=line --alluredir=reports -n 5 --clean-alluredir -q`


## GitHub Actions + GitHub Pages
Run tests in GitHub Actions and publish Allure results to Github pages.