from selenium import webdriver

browser = webdriver.Firefox()

browser.get('http://0.0.0.0:5000/')
assert browser.title == 'Hacker Brunch'

myButton1 = browser.find_element_by_id('14').find_element_by_class_name('try-button')
myButton1.click()

