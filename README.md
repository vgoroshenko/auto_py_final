[Test link](http://selenium1py.pythonanywhere.com/)

[Link to Allure report after run tests](https://vgoroshenko.github.io/auto_py_final/)

# pytest + selenium + allure

Install deps for test `pip3 install -r requirements.txt`

Run tests  `pytest -v --tb=line --language=en -m need_review --alluredir=reports`


## GitHub Actions + GitHub Pages
Run tests using GitHub Actions and publish Allure results to Github pages. 

2 build options: in Docker or using Python env.
