from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ozh.github.io/cookieclicker")

driver.implicitly_wait(5)
language_select = driver.find_element(By.CLASS_NAME, "langSelectButton")
language_select.click()

cookie = driver.find_element(By.ID, value="bigCookie")
first_tool = driver.find_element(By.ID, value="product0")
first_tool_price = driver.find_element(By.ID, value="productPrice0")
first_tool_owned = driver.find_element(By.ID, value="productOwned0")

second_tool = driver.find_element(By.ID, value="product1")
second_tool_price = driver.find_element(By.ID, value="productPrice1")
second_tool_owned = driver.find_element(By.ID, value="productOwned1")

while True:
    cookie.click()
    click_scoreboard = driver.find_element(By.ID, value="cookies").text
    click_score = int(click_scoreboard.split(" ")[0])
    if  click_score > int(first_tool_price.text):
        first_tool.click()
    if first_tool_owned.text:
        while int(first_tool_owned.text) > 3:
            cookie.click()
            if click_score > int(second_tool_price.text):
                second_tool.click()
