from selenium.webdriver.common.by import By


class MainPageLocators():
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

class LoginPageLocators():
    LOGIN_EMAIL = (By.CSS_SELECTOR, "#id_login-username")
    LOGIN_PASS = (By.CSS_SELECTOR, "#id_login-password")

    REGISTER_EMAIL = (By.CSS_SELECTOR, "#id_registration-email")
    REGISTER_PASS = (By.CSS_SELECTOR, "#id_registration-password1")
    REGISTER_CONFIRM_PASS = (By.CSS_SELECTOR, "#id_registration-password2")\

    REGISTER_BUTTON = (By.CSS_SELECTOR, ".register_form .btn-primary")

class BasketPageLocators():
    BASKET_EMPTY_TEXT = (By.CSS_SELECTOR, "#content_inner >p")
    BASKET_PRODUCT = (By.CSS_SELECTOR, ".basket-items")

class ProductPageLocators():
    BUTTON_ADD_PRODUCT = (By.CSS_SELECTOR, ".btn-add-to-basket")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product_main h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product_main .price_color")
    PRODUCT_SUCCESS_MESSAGE_NAME = (By.CSS_SELECTOR, ".alert:nth-child(1) strong")
    PRODUCT_MESSAGE_TOTAL_RICE = (By.CSS_SELECTOR, ".alert-info strong")

class BasePageLocators():
    BASKET_BUTTON = (By.CSS_SELECTOR, ".btn-group >a")
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")

