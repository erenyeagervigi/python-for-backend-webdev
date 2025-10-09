from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://en.wikipedia.org/wiki/Main_Page")

# Click the search icon (minimized search)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="p-search"]/a'))
).click()

# Wait for the final search bar to be visible & ready
search_bar = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, "search"))
)

# Type and press Enter
search_bar.send_keys("attack on titan")
search_bar.send_keys(Keys.ENTER)
