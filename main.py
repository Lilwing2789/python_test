def in_autotests_we_trust(a, b):
    if a == b:
        print('PASSED')
    else:
        print('FAILED')


in_autotests_we_trust(10, '10')

in_autotests_we_trust(0, False)

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options  # <--- THIS WAS MISSING
from selenium.common.exceptions import WebDriverException
import time
import helpers
import data
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Task 1: Add setup class
        # UPDATED: Use ChromeOptions instead of DesiredCapabilities (Selenium 4 fix)
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        # Initialize driver with options
        cls.driver = webdriver.Chrome(options=options)
        cls.page = UrbanRoutesPage(cls.driver)

        # Task 1: Move URL check inside setup_class and use pytest.skip
        try:
            # Check server reachability
            if not helpers.is_url_reachable(data.BASE_URL):
                # Raise an exception that Pytest can catch and skip the class
                raise WebDriverException(f"The server address {data.BASE_URL} is not reachable.")
        except Exception as e:
            pytest.skip(f"Skipping tests because the server is unreachable: {e}")

    # Setup method to ensure a fresh page is loaded before EACH test
    def setup_method(self):
        self.page.open(data.BASE_URL)
        time.sleep(1)  # Allow page to fully load

    # Helper method to fulfill common prerequisites
    def _fulfill_prerequisites(self):
        """Sets the route, clicks call taxi, and selects supportive plan."""
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

    # --- Test Cases ---

    def test_set_route(self):
        """Task: Setting the Address (To & From Fields)"""
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert self.page.get_from() == data.ADDRESS_FROM
        assert self.page.get_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        """Task: Selecting Supportive plan"""
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Correct assertion using the page object method
        assert "Supportive" in self.page.get_active_tariff_text()

    def test_fill_phone_number(self):
        """Task: Filling in the phone number and confirming login"""
        self._fulfill_prerequisites()

        # 1. Enter phone number FIRST to trigger the SMS
        self.page.input_phone_number(data.PHONE_NUMBER)

        # 2. Retrieve the code (now that it has been sent)
        sms_code = helpers.retrieve_phone_code(self.driver)

        # 3. Enter the code and confirm
        self.page.enter_sms_code_and_confirm(sms_code)

        # Assertion: If the comment box is displayed, it means phone auth was successful
        assert self.driver.find_element(*self.page.COMMENT_TEXTAREA).is_displayed()

    def test_add_credit_card(self):
        """Task: Adding a credit card"""
        self._fulfill_prerequisites()

        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(1)  # Wait for modal to close and payment method to update

        assert "Card" in self.page.get_payment_method_text()

    def test_write_comment(self):
        """Task: Writing a comment for the driver"""
        self._fulfill_prerequisites()

        self.page.write_driver_comment(data.DRIVER_COMMENT)

        assert self.page.get_driver_comment() == data.DRIVER_COMMENT

    def test_order_blanket_and_handkerchiefs(self):
        """Task: Ordering a Blanket and handkerchiefs"""
        self._fulfill_prerequisites()

        before, after = self.page.toggle_blanket_and_verify()
        assert before is False and after is True

    def test_order_two_ice_creams(self):
        """Task: Ordering 2 Ice creams"""
        self._fulfill_prerequisites()

        count_text = self.page.add_ice_creams(data.ICE_CREAM_COUNT_TO_ORDER)

        assert count_text.strip() == str(data.ICE_CREAM_COUNT_TO_ORDER)

    def test_order_supportive_shows_car_search_modal(self):
        """Task: Order a taxi with the 'Supportive' tariff and check for the car search modal."""
        self._fulfill_prerequisites()

        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)
        time.sleep(1)

        # 1. Enter phone number FIRST
        self.page.input_phone_number(data.PHONE_NUMBER)

        # 2. Retrieve the code
        sms_code = helpers.retrieve_phone_code(self.driver)

        # 3. Enter the code
        self.page.enter_sms_code_and_confirm(sms_code)

        # Add extras/message as requested
        self.page.add_ice_creams(1)
        self.page.write_driver_comment(data.DRIVER_MESSAGE_FOR_ORDER)

        # Click Order and verify Modal
        self.page.click_order_button()

        assert self.page.is_car_search_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        # Task 1: Add teardown class
        cls.driver.quit()