from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


class UrbanRoutesPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    # --- LOCATORS ---
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, "button.button.round")

    # Tariff'''
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[contains(text(), 'Supportive')]]")
    ACTIVE_TARIFF = (By.CSS_SELECTOR, ".tcard.active")

    # Phone
    PHONE_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_INPUT = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.CSS_SELECTOR, "button.button.full")
    PHONE_CONFIRM_CODE_INPUT = (By.ID, "code")
   #replaced above PHONE_CONFIRM_CODE_INPUT = (By.ID, "phone-confirm-code")
    PHONE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirm')]")

    # Payment
    PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-value-text")
    #replaced w/ above PAYMENT_METHOD_BUTTON = (By.CSS_SELECTOR, ".pp-text")
    ADD_CARD_BUTTON = (By.CSS_SELECTOR, ".pp-plus-container")
    CARD_NUMBER_INPUT = (By.ID, "number")
    #replaced w/ above CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.NAME, "code")
    LINK_CARD_BUTTON = (By.XPATH, "//button[contains(text(), 'Link')]")

    # Extras
    COMMENT_TEXTAREA = (By.ID, "comment")
    BLANKET_SWITCH = (By.CSS_SELECTOR, ".switch")
    BLANKET_CHECKBOX = (By.CSS_SELECTOR, ".switch-input")
    ICE_CREAM_PLUS = (By.CSS_SELECTOR, ".counter-plus")
    ICE_CREAM_COUNT = (By.CSS_SELECTOR, ".counter-value")

    ORDER_BUTTON = (By.CSS_SELECTOR, "button.smart-button")
    CAR_SEARCH_MODAL = (By.CSS_SELECTOR, ".order-body")

    # --- METHODS ---

    def set_route(self, from_address, to_address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.FROM_INPUT)).send_keys(from_address)
        self.driver.find_element(*self.FROM_INPUT).send_keys(Keys.TAB)
        self.driver.find_element(*self.TO_INPUT).send_keys(to_address)
        self.driver.find_element(*self.TO_INPUT).send_keys(Keys.TAB)

    def get_from(self):
        return self.driver.find_element(*self.FROM_INPUT).get_attribute("value")

    def get_to(self):
        return self.driver.find_element(*self.TO_INPUT).get_attribute("value")

    def click_call_taxi(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_tariff_if_not_active(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.SUPPORTIVE_TARIFF))
        supportive_card = self.driver.find_element(*self.SUPPORTIVE_TARIFF)
        if "active" not in supportive_card.get_attribute("class"):
            self.driver.execute_script("arguments[0].click();", supportive_card)

    def input_phone_number(self, phone_number):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.PHONE_INPUT)).send_keys(phone_number)

        # Click background to trigger validation
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".modal").click()
        except:
            self.driver.find_element(By.TAG_NAME, "body").click()

        time.sleep(1)
        next_btn = self.driver.find_element(*self.PHONE_NEXT_BUTTON)
        self.driver.execute_script("arguments[0].click();", next_btn)

    def enter_sms_code_and_confirm(self, confirmation_code):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.PHONE_CONFIRM_CODE_INPUT)).send_keys(
            confirmation_code)
        time.sleep(1)
        confirm_btn = self.driver.find_element(*self.PHONE_CONFIRM_BUTTON)
        self.driver.execute_script("arguments[0].click();", confirm_btn)

    def open_payment_and_add_card(self, card_number, card_code):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ADD_CARD_BUTTON)).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT)).send_keys(
            card_number)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(card_code)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(Keys.TAB)

        time.sleep(1)
        link_btn = self.driver.find_element(*self.LINK_CARD_BUTTON)
        self.driver.execute_script("arguments[0].click();", link_btn)

        # Close payment modal safely
        time.sleep(1)
        try:
            close_btn = self.driver.find_element(By.CSS_SELECTOR, ".payment-picker .close-button")
            self.driver.execute_script("arguments[0].click();", close_btn)
        except:
            pass

    def get_payment_method_text(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_BUTTON).text

    def write_driver_comment(self, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.COMMENT_TEXTAREA)).send_keys(text)

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_TEXTAREA).get_attribute("value")

    def toggle_blanket_and_verify(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.BLANKET_SWITCH))
        checkbox = self.driver.find_element(*self.BLANKET_CHECKBOX)
        before = checkbox.get_property("checked")
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*self.BLANKET_SWITCH))
        after = checkbox.get_property("checked")
        return before, after

    def add_ice_creams(self, count):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS))
        plus_btn = self.driver.find_element(*self.ICE_CREAM_PLUS)
        for _ in range(count):
            self.driver.execute_script("arguments[0].click();", plus_btn)
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def click_order_button(self):
        time.sleep(1)
        order_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.ORDER_BUTTON))
        self.driver.execute_script("arguments[0].click();", order_btn)

    def is_car_search_modal_displayed(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL))
        return self.driver.find_element(*self.CAR_SEARCH_MODAL).is_displayed()

    def get_active_tariff_text(self):
        return self.driver.find_element(*self.ACTIVE_TARIFF).text