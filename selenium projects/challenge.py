from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options= chrome_options)
driver.get("https://www.python.org")

events_date = driver.find_elements(By.CSS_SELECTOR, value=(".event-widget time"))
event_date = [i.text for i in events_date]

events_name = driver.find_elements(By.CSS_SELECTOR, value=(".event-widget ul li a"))
event_name = [i.text for i in events_name]

dictionary = {}

for i in range(len(event_name)):
    dictionary.update({i:{"time": event_date[i], "name": event_name[i]}})

print(dictionary)

driver.quit()