from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, base_url: str):
        self.driver.get(base_url)

    # Locators
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(., 'Call a taxi')]")
    SUPPORTIVE_TARIFF = (By.XPATH, "//div[contains(@class,'tariff-card')][.//*[contains(text(),'Supportive')]]")
    ACTIVE_TARIFF = (By.XPATH, "//div[contains(@class,'tariff-card') and contains(@class,'active')]")
    PHONE_INPUT = (By.ID, "phone")
    PHONE_CONFIRM_CODE_INPUT = (By.ID, "phone-confirm-code")
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "payment-method")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "add-card")
    CARD_NUMBER_INPUT = (By.ID, "card-number")
    CARD_CODE_INPUT = (By.ID, "code")
    LINK_CARD_BUTTON = (By.XPATH, "//button[contains(., 'Link')]")
    COMMENT_TEXTAREA = (By.ID, "comment")
    BLANKET_TOGGLE = (By.ID, "blanket")
    ICE_CREAM_PLUS = (By.CLASS_NAME, "ice-cream-plus")
    ICE_CREAM_COUNT = (By.CLASS_NAME, "ice-cream-count")
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Order')]")
    CAR_SEARCH_MODAL = (By.ID, "car-search")

    # Methods
    def set_addresses(self, from_address, to_address):
        self.driver.find_element(*self.FROM_INPUT).send_keys(from_address)
        self.driver.find_element(*self.TO_INPUT).send_keys(to_address)

    def click_call_taxi(self):
        self.driver.find_element(*self.CALL_TAXI_BUTTON).click()

    def select_supportive_tariff_if_not_active(self):
        active = self.driver.find_elements(*self.ACTIVE_TARIFF)
        if active and "Supportive" in active[0].text:
            return
        self.driver.find_element(*self.SUPPORTIVE_TARIFF).click()

    def enter_phone_and_confirm(self, phone_number, confirmation_code):
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone_number)
        self.driver.find_element(*self.PHONE_CONFIRM_CODE_INPUT).send_keys(confirmation_code)

    def open_payment_and_add_card(self, card_number, card_code):
        self.driver.find_element(*self.PAYMENT_METHOD_BUTTON).click()
        self.driver.find_element(*self.ADD_CARD_BUTTON).click()
        self.driver.find_element(*self.CARD_NUMBER_INPUT).send_keys(card_number)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(card_code)
        self.driver.find_element(*self.CARD_CODE_INPUT).send_keys(Keys.TAB)
        self.driver.find_element(*self.LINK_CARD_BUTTON).click()

    def write_driver_comment(self, text):
        self.driver.find_element(*self.COMMENT_TEXTAREA).send_keys(text)

    def toggle_blanket_and_verify(self):
        checkbox = self.driver.find_element(*self.BLANKET_TOGGLE)
        before = checkbox.get_property("checked")
        checkbox.click()
        after = checkbox.get_property("checked")
        return before, after

    def add_ice_creams(self, count):
        for _ in range(count):
            self.driver.find_element(*self.ICE_CREAM_PLUS).click()
        return self.driver.find_element(*self.ICE_CREAM_COUNT).text

    def order_and_wait_for_car_search(self, message_for_driver):
        self.write_driver_comment(message_for_driver)
        self.driver.find_element(*self.ORDER_BUTTON).click()
        return self.driver.find_element(*self.CAR_SEARCH_MODAL).is_displayed()
