import time

from selenium import webdriver


def testCase1():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
    time.sleep(5)
    driver.close()
