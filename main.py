import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import helpers
from pages import UrbanRoutesPage

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # 1. Setup Chrome Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        # 2. Initialize Driver
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(5)

        # 3. Initialize Page Object
        cls.page = UrbanRoutesPage(cls.driver)

        # 4. Check Server Reachability
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert self.page.get_from() == data.ADDRESS_FROM
        assert self.page.get_to() == data.ADDRESS_TO

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        assert "Supportive" in self.page.get_active_tariff_text()

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Test Logic
        self.page.input_phone_number(data.PHONE_NUMBER)
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_sms_code_and_confirm(sms_code)

        assert self.driver.find_element(*self.page.COMMENT_TEXTAREA).is_displayed()

    def test_add_credit_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Test Logic
        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)

        assert "Card" in self.page.get_payment_method_text()

    def test_write_comment(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Test Logic
        self.page.write_driver_comment(data.DRIVER_COMMENT)

        assert self.page.get_driver_comment() == data.DRIVER_COMMENT

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Test Logic
        before, after = self.page.toggle_blanket_and_verify()
        assert before is False and after is True

    def test_order_two_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Test Logic
        count_text = self.page.add_ice_creams(data.ICE_CREAM_COUNT_TO_ORDER)

        assert count_text.strip() == str(data.ICE_CREAM_COUNT_TO_ORDER)

    def test_order_supportive_shows_car_search_modal(self):
        self.driver.get(data.URBAN_ROUTES_URL)

        # Prerequisites
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_supportive_tariff_if_not_active()

        # Flow
        self.page.input_phone_number(data.PHONE_NUMBER)
        sms_code = helpers.retrieve_phone_code(self.driver)
        self.page.enter_sms_code_and_confirm(sms_code)

        self.page.open_payment_and_add_card(data.CARD_NUMBER, data.CARD_CODE)

        self.page.write_driver_comment(data.DRIVER_COMMENT)
        self.page.add_ice_creams(1)

        self.page.click_order_button()

        assert self.page.is_car_search_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()