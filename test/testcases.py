import random
from selenium.common.exceptions import NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By

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
        add_element = self.find_element(By.CSS_SELECTOR, 'div.product:nth-child(4) > div:nth-child(5) > button:nth-child(1)')
        for e in range(4):
            add_element.click()

    def add_three_random_items_to_cart(self):
        items = self.find_elements(By.CLASS_NAME, 'product-action')

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
