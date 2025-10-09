from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--force-dark-mode")

driver = webdriver.Chrome(options = chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com")

first_name = driver.find_element(By.NAME, value="fName")
first_name.send_keys("Eren")

last_name = driver.find_element(By.NAME, value="lName")
last_name.send_keys("Yeager")

email_name = driver.find_element(By.NAME, value="email")
email_name.send_keys("Vignesh13006@gmail.com")

sign_up_button = driver.find_element(By.CLASS_NAME, value="btn-primary")
sign_up_button.click()