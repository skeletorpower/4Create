from test.testcases import TestCases

# using context manager
with TestCases(teardown=False) as test:
    test.land_on_page()
    test.increase_three_times_and_add_to_cart()
    test.add_three_random_items_to_cart()
    test.proceed_to_checkout()
    test.enter_a_promo_code()
    test.click_apply()
    test.click_place_order()