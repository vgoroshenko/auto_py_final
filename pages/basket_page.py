from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):

    def should_be_empty_basket(self):
        assert self.is_not_element_present(*BasketPageLocators.BASKET_PRODUCT), "Should not present product"
        empty_basket_text = self.browser.find_element(*BasketPageLocators.BASKET_EMPTY_TEXT)
        assert 'Your basket is empty. Continue shopping' == empty_basket_text.text, "Should be present 'empty basket' text"