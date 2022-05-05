import string
import time
import random

import pytest
from .pages.product_page import ProductPage
from .pages.login_page import LoginPage
from .pages.basket_page import BasketPage
from .pages.locators import UrlLocators



@pytest.mark.need_review
#@pytest.mark.parametrize('link', UrlLocators.PROMO_URLS)
def test_guest_can_add_product_to_basket(browser):
    link = UrlLocators.PROMO_URLS[0]
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_success_message()

@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()
    page = LoginPage(browser, link)
    page.should_be_login_page()


def test_guest_cant_see_success_message(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()

@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.go_to_basket_page()
    page = BasketPage(browser, link)
    page.should_be_empty_basket()

def test_guest_should_see_login_link_on_product_page(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()

@pytest.mark.xfail #For demo
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.should_not_be_success_message()

@pytest.mark.xfail #For demo
def test_message_disappeared_after_adding_product_to_basket(browser):
    link = UrlLocators.PRODUCT_URL
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.should_wait_not_be_success_message()

@pytest.mark.skip # Register new user dont work
@pytest.mark.new
class TestUserAddToBasketFromProductPage():
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        link = UrlLocators.LOGIN_URL
        browser.delete_all_cookies()
        page = LoginPage(browser, link)
        page.open()
        new_email = str(time.time() + random.randint(1, 1000)) + "@fakemail.org"
        new_password = 'Test221234567'
        page.register_new_user(new_email, new_password)
        page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        link = UrlLocators.PRODUCT_URL
        page = ProductPage(browser, link)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.need_review
    @pytest.mark.xfail
    def test_user_can_add_product_to_basket(self, browser):
        link = UrlLocators.PROMO_URLS[0]
        page = ProductPage(browser, link)
        page.open()
        page.add_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_success_message()
