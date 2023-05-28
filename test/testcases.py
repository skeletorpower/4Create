import random
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import test.constants as const


class TestCases(webdriver.Firefox):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(TestCases, self).__init__()
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_on_page(self):
        self.get(const.BASE_URL)

    def increase_three_times_and_add_to_cart(self, item=None):
        add_element = self.find_element(By.CSS_SELECTOR,
                                        'div.product:nth-child(4) > div:nth-child(5) > button:nth-child(1)')
        for e in range(4):
            add_element.click()

    def add_three_random_items_to_cart(self):
        items = self.find_elements(By.CLASS_NAME, 'product-action')

        # I tried bonus task in here, but couldn't figure out how to take out most expensive
        # and cheapest items. I got the prices from the elements but not the element itself
        # If I managed to do that the task would be done. We can have a brief discussion about that

        # product_prices = self.find_elements(By.CLASS_NAME, 'product-price')
        # all_prices = [price.get_attribute('textContent') for price in product_prices]

        # most_expensive_item = max(all_prices)
        # cheapest_item = min(all_prices)
        # print(all_prices)
        # print(max(all_prices))

        for i in range(3):
            item = random.choice(items)
            item.click()

    def proceed_to_checkout(self):
        cart = self.find_element(By.CLASS_NAME, 'cart-icon')
        proceed_button = self.find_element(By.CLASS_NAME, 'action-block')
        cart.click()
        proceed_button.click()

    def enter_a_promo_code(self):
        add_promo_code = self.find_element(By.CLASS_NAME, 'promoCode')
        total_amount = self.find_element(By.CLASS_NAME, 'totAmt').text
        add_promo_code.send_keys(total_amount)

    def click_apply(self):
        apply_button = self.find_element(By.CLASS_NAME, 'promoBtn')
        apply_button.click()

        error_code = self.find_element(By.CLASS_NAME, 'promoInfo')

        def error_exists():
            try:
                error_code
            except NoSuchElementException:
                return False
            return True

        error_exists()

    def click_place_order(self):
        place_order_btn = self.find_element(By.CSS_SELECTOR, '.products > div:nth-child(4) > button')
        place_order_btn.click()

        terms = self.find_element(By.CLASS_NAME, 'wrapperTwo')
        try:
            terms
        except NoSuchElementException:
            return False
        return True

    def select_country(self):
        country_dropdown = self.find_element(By.TAG_NAME, 'select')
        option_select = self.find_element(By.CSS_SELECTOR, 'select > option:nth-child(1)')
        countries = self.find_elements(By.XPATH, '//option[@value]')

        random_country = random.choice(countries)

        country_dropdown.click()
        if option_select.get_property('enabled'):
            print('It is enabled o.O')

        random_country.click()

    def click_proceed_without_checkbox(self):
        proceed_btn = self.find_element(By.TAG_NAME, 'button')
        error_message = self.find_element(By.CLASS_NAME, 'errorAlert').get_attribute('textContent')

        proceed_btn.click()

        # ASSERT MI JE OVDE, POGLEDAJ OVO PA URADI SVUDA GDE TREBA
        try:
            assert error_message == 'Please accept Terms & Conditions - Required', 'error message is not the same'
        except AssertionError as msg:
            print(msg)

    def check_the_box_and_proceed(self):
        check_box = self.find_element(By.CLASS_NAME, 'chkAgree')
        proceed_btn = self.find_element(By.TAG_NAME, 'button')

        check_box.click()
        proceed_btn.click()

        order_message = self.find_element(By.CLASS_NAME, 'wrapperTwo').get_attribute('textContent')

        try:
            assert order_message == "Thank you, your order has been placed successfully  You'll be redirected to Home page shortly!!", 'order message is not the same'
        except AssertionError as msg:
            print(msg)

    def navigate_to_new_tab(self):
        self.execute_script("window.open('');")
        time.sleep(2)
        self.switch_to.window(self.window_handles[1])
        self.get(const.NEW_TAB_URL)

    def scrolling_and_clicking_actions(self):
        actions_element = self.find_element(By.ID, 'actions')
        self.execute_script("arguments[0].scrollIntoView()", actions_element)
        self.save_screenshot('screenshots/screenshot.png')
        time.sleep(2)
        self.execute_script("arguments[0].click()", actions_element)

    def back_second_tab(self):
        time.sleep(1)
        self.switch_to.window(self.window_handles[1])
        time.sleep(1)
        self.save_screenshot('screenshots/backScreenshot.png')
        time.sleep(1)
        self.switch_to.window(self.window_handles[2])

        title_action = self.find_element(By.TAG_NAME, 'title').get_attribute('textContent')

        if 'Actions' in title_action:
            print('Title contains Actions')

    def drag_n_drop(self):
        drag = self.find_element(By.ID, 'draggable')
        drop = self.find_element(By.ID, 'droppable')
        time.sleep(2)
        action = ActionChains(self)
        action.drag_and_drop(drag, drop)
        action.perform()

        dropped = self.find_element(By.CSS_SELECTOR, '#droppable > p').text

        try:
            assert dropped == "Dropped!", 'Not dropped!'
        except AssertionError as msg:
            print(msg)

    def link_should_not_visible(self):

        link1 = self.find_element(By.CSS_SELECTOR, 'div.dropdown:nth-child(1) > div > a').text

        if len(link1) > 0:
            print('ELEMENT EXISTS?!')

    def link_should_be_visible(self):

        btn1 = self.find_element(By.CSS_SELECTOR, 'div.dropdown:nth-child(1) > button:nth-child(1)')

        action = ActionChains(self)
        action.move_to_element(btn1)
        action.perform()

        link1 = self.find_element(By.CSS_SELECTOR, 'div.dropdown:nth-child(1) > div > a').text

        try:
            assert link1 == 'Link 1', 'Link 1 is not present!!!'
        except AssertionError as msg:
            print(msg)

    def click_on_link_one(self):

        global alert_text

        link1 = self.find_element(By.CSS_SELECTOR, 'div.dropdown:nth-child(1) > div > a')

        link1.click()

        try:
            WebDriverWait(self, 2).until(EC.alert_is_present())

            alert = self.switch_to.alert
            alert_text = alert.text
            time.sleep(3)
            alert.accept()
            print(alert_text + '--> this text was saved in alert_text variable')
            print("Alert exists!")
        except TimeoutException:
            print("Alert does not exist :( ")

    def closing_tabs(self):

        for handle in self.window_handles:
            self.switch_to.window(handle)
            self.close()

    def open_contact_us_and_enter_a_comment(self):
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(const.CONTACT_US_URL)
        time.sleep(1)
        comment_section = driver.find_element(By.TAG_NAME, 'textarea')

        comment_section.send_keys(alert_text)
