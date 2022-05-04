import time

from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):

    def add_to_basket(self):
        add_product = self.browser.find_element(*ProductPageLocators.BUTTON_ADD_PRODUCT)
        add_product.click()

    def should_be_success_message(self):
        time.sleep(2)
        #self.should_be_product_name_in_add_message()
        self.should_be_have_basket_total()

    def should_be_product_name_in_add_message(self):
        product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME)
        added_product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_SUCCESS_MESSAGE_NAME)
        assert product_name.text == added_product_name.text, "Invalid product name in message"

    def should_be_have_basket_total(self):
        product_price = self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE)
        added_product_price_total = self.browser.find_element(*ProductPageLocators.PRODUCT_MESSAGE_TOTAL_RICE)
        assert product_price.text == added_product_price_total.text, "Invalid product total price in message"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.PRODUCT_SUCCESS_MESSAGE_NAME), \
            "Success message is presented, but should not be"

    def should_wait_not_be_success_message(self):
        assert self.is_disappeared(*ProductPageLocators.PRODUCT_SUCCESS_MESSAGE_NAME), \
            "Success message is presented, but should not be"