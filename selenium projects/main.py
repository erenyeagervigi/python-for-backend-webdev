from selenium import webdriver
from selenium.webdriver.common.by import By
#to keep the chrome tab open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options = chrome_options)
# driver.get("https://www.amazon.in/Apple-MacBook-13-inch-10-core-Unified/dp/B0DZDDV7GC/ref=sr_1_1_sspa?crid=2LXBA2Y54U0XE&dib=eyJ2IjoiMSJ9.L2Hu7nsAw269fTBuFKBbdqcWN4STbO4e5t8RPOfyswAT0DzglHEA19yGY1dngXs8yPaSvHFeDvMuFW_HlLBv9AFqWWcriCw-0TiQxEGCbV5rbXPMAcMnMH_b2AnIdDU6Po4yyTubFT56dVkiHc3Mf8Mc8D-QLDoq5K5ACG41F2KGm7C3UEY3yS685LyENSjWZ8Fx0eBQvA68yb8FRdQgFBDiyP9YJR4R_zTTnnAkZY0.W3RO13flqiVYNGIKM0Rr0QD1dS0gg0MafPWkpPqsB0k&dib_tag=se&keywords=macbook%2Bair%2Bm4&qid=1753934076&sprefix=mac%2Caps%2C384&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1")
# prices = driver.find_elements(By.CLASS_NAME, 'a-price-whole')
# for price in prices:
#     if price.text.strip() != "":
#         print(f"The price is {price.text}")
#         break
# #to close the current tab
# driver.close()

driver.get("https://www.python.org/")

search_bar = driver.find_element(By.NAME, "q")

#to get the name of a specific selenium attributes .attribute name
print(search_bar.tag_name)

#or you can use the get_attribute method
print(search_bar.get_attribute("placeholder"))

#to find an element inside a nested statements
documentation_widget = driver.find_element(By.CSS_SELECTOR, value=".documentation-widget a")
print(documentation_widget.text)

#to find element via xpath
search_bug = driver.find_element(By.XPATH,value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
print(search_bug.text)

downloads = driver.find_element(By.XPATH,value='//*[@id="container"]/li[2]/a')
print(downloads.text)

#to click on a element by the specified path
# random_number.click()

# #to click on a element using link
# link = driver.find_element(By.LINK_TEXT, "Bots")
# link.click()

#to search on the search bar
# search_bar = driver.find_element(By.NAME, value="search")


# search_bar.send_keys("attack on titan", Keys.ENTER)




#to close the software
driver.quit()