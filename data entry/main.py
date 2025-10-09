from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
data = response.text

google_sheets_link = "https://docs.google.com/forms/d/e/1FAIpQLScdPa4yomSntm1-sE88L3ufOo6JwmsIbB1tt2C85YSha1GXFQ/viewform?usp=sharing&ouid=117224782894654986562"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(google_sheets_link)

wait = WebDriverWait(driver, 13)


# sumbit_again_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')

soup = BeautifulSoup(data, "html.parser")
price = [i.getText().split("/")[0] for i in soup.find_all(class_ = "PropertyCardWrapper__StyledPriceLine")]
filtered_price = [i.split("+")[0] for i in price]
links= [i.get("href") for i in soup.find_all(name="a", class_ ="StyledPropertyCardDataArea-anchor")]
address = [i.getText().strip() for i in soup.find_all(name="a", class_ ="StyledPropertyCardDataArea-anchor")]

for i in range(len(price)):

    check_condition = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[1]/div/div[2]/div[1]/div').text
    if check_condition == "SF RENTING SEARCH":
        address_button = driver.find_element(By.XPATH,
                                             '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_button = driver.find_element(By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_button = driver.find_element(By.XPATH,
                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        sumbit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')

        price_button.click()
        price_button.send_keys(filtered_price[i])

        link_button.click()
        link_button.send_keys(links[i])

        address_button.click()
        address_button.send_keys(address[i])

        sumbit_button.click()
        sumbit_again = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        sumbit_again.click()

