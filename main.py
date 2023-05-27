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
    test.select_country()
    test.click_proceed_without_checkbox()
    test.check_the_box_and_proceed()
    test.navigate_to_new_tab()
    test.scrolling_and_clicking_actions()
    test.back_second_tab()
    test.drag_n_drop()
    test.link_should_not_visible()
    test.link_should_be_visible()
    test.click_on_link_one()
    test.closing_tabs()
    test.open_contact_us_and_enter_a_comment()
