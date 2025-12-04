def in_autotests_we_trust(a, b):
    if a == b:
        print('PASSED')
    else:
        print('FAILED')

in_autotests_we_trust(10, '10')

in_autotests_we_trust(0, False)


import pytest
from selenium import webdriver
import helpers
import data
from pages import UrbanRoutesPage

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        # Check server reachability
        if not helpers.is_url_reachable(data.BASE_URL):
            raise RuntimeError("Target URL is not reachable. Aborting test setup.")

        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.page = UrbanRoutesPage(cls.driver)
        cls.page.open(data.BASE_URL)

    def test_set_address(self):
        self.page.set_addresses(data.FROM_ADDRESS, data.TO_ADDRESS)
        assert self.driver.find_element(*self.page.FROM_INPUT).get_attribute("value") == data.FROM_ADDRESS
        assert self.driver.find_element(*self.page.TO_INPUT).get_attribute("value") == data.TO_ADDRESS

    def test_select_supportive_plan(self):
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()
        assert "Supportive" in self.driver.find_element(*self.page.ACTIVE_TARIFF).text

    def test_fill_phone_number(self):
        sms_code = helpers.retrieve_phone_code()
        self.page.enter_phone_and_confirm(data.PHONE_NUMBER, sms_code)
        assert data.PHONE_NUMBER in self.driver.find_element(*self.page.PHONE_INPUT).get_attribute("value")

    def test_add_credit_card(self):
        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert "Card" in self.driver.find_element(*self.page.PAYMENT_METHOD_BUTTON).text

    def test_write_comment(self):
        self.page.write_driver_comment(data.DRIVER_COMMENT)
        assert self.driver.find_element(*self.page.COMMENT_TEXTAREA).get_attribute("value") == data.DRIVER_COMMENT

    def test_order_blanket_and_handkerchiefs(self):
        before, after = self.page.toggle_blanket_and_verify()
        assert before != after and after is True

    def test_order_two_ice_creams(self):
        count_text = self.page.add_ice_creams(2)
        assert count_text.strip() == "2"

    def test_order_supportive_shows_car_search_modal(self):
        sms_code = helpers.retrieve_phone_code()
        self.page.enter_phone_and_confirm(data.PHONE_NUMBER, sms_code)
        visible = self.page.order_and_wait_for_car_search(data.DRIVER_MESSAGE_FOR_ORDER)
        assert visible is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
