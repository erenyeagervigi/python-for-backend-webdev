from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")
wait = WebDriverWait(driver, 10)

join_button = driver.find_element(By.CLASS_NAME, "Home_heroButton__3eeI3")
join_button.click()

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Login_pageTitle__j_4ga")))

email_input = driver.find_element(By.ID, "email-input")
email_input.click()
email_input.send_keys("stdent@test.com")

password_input = driver.find_element(By.ID, "password-input")
password_input.click()
password_input.send_keys("password123")

submit = driver.find_element(By.ID, "submit-button")
submit.click()


wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

Classes_booked = 0
Waitlists_joined = 0
Already_booked_waitlisted = 0
processed_class = []
authentication = 0

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text
    if "Tue" in day_title:
        time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time:
            book = card.find_element(By.CSS_SELECTOR, "div button[id^='book-button']")
            class_name = card.find_element(By.CSS_SELECTOR, "div h3[id^='class-name-']").text
            if book.text == "Book Class" :
                book.click()
                print(f"class is booked on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Classes_booked +=1
                processed_class.append(f"[new booking] {class_name} on {day_title}")
            elif book.text == "Join Waitlist":
                book.click()
                print(f"class is waitlisted on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Waitlists_joined +=1
                processed_class.append(f"[new waitlist] {class_name} on {day_title}")
            elif book.text == "Booked" or book.text == "Waitlisted":
                print(f"class is already {book.text} on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Already_booked_waitlisted +=1
                processed_class.append(f"[{book.text}] {class_name} on {day_title}")

    if "Thu" in day_title:
        time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time:
            book = card.find_element(By.CSS_SELECTOR, "div button[id^='book-button']")
            class_name = card.find_element(By.CSS_SELECTOR, "div h3[id^='class-name-']").text
            if book.text == "Book Class" :
                book.click()
                print(f"class is booked on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Classes_booked +=1
                processed_class.append(f"[new booking] {class_name} on {day_title}")
            elif book.text == "Join Waitlist":
                book.click()
                print(f"class is waitlisted on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Waitlists_joined +=1
                processed_class.append(f"[new waitlist] {class_name} on {day_title}")
            elif book.text == "Booked" or book.text == "Waitlisted":
                print(f"class is already {book.text} on {day_title} at {time.split("Time:")[1]} for {class_name}")
                Already_booked_waitlisted +=1
                processed_class.append(f"[{book.text}] {class_name} on {day_title}")


#                 my booking page
my_booking = driver.find_element(By.ID, "my-bookings-link")
my_booking.click()
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MyBookings_pageTitle__i0Jkj")))
booking_class_card = driver.find_elements(By.CSS_SELECTOR, "div[id^='booking-card-']")
waitlist_card = driver.find_elements(By.CSS_SELECTOR, "div[id^='waitlist-card-']")

my_booked_classes = []
my_booked_class_name = []
print("--- Total Tuesday/Thursday 6pm classes: 2 ---")

for card in booking_class_card:
    date = card.find_element(By.TAG_NAME, "p").text
    class_name_booking = card.find_element(By.CSS_SELECTOR, "h3[id^=booking-class-name-]").text
    my_booked_class_name.append(class_name_booking)
    my_booked_classes.append(date)

for card in waitlist_card:
    date = card.find_element(By.TAG_NAME, "p").text
    class_name_booking = card.find_element(By.CSS_SELECTOR, "h3[id^=waitlist-class-name-]").text
    my_booked_class_name.append(class_name_booking)
    my_booked_classes.append(date)

print("--- VERIFYING ON MY BOOKINGS PAGE ---")

for i in my_booked_classes:
    if "Thu" in i and "6:00 PM" in i:
        authentication += 1
        print(f"verified:{my_booked_class_name[0]}")
    if "Tue" in i and "6:00 PM" in i:
        authentication += 1
        print(f"verified:{my_booked_class_name[1]}")

print("Expected: 2 bookings")
print(f"Found: {authentication} bookings")

if authentication == 2:
        print("✅ SUCCESS: All bookings verified! \n")
        print("--- BOOKING SUMMARY ---")
        print(f" Classes booked: {Classes_booked}")
        print(f"Waitlists joined: {Waitlists_joined}")
        print(f"Already booked/waitlisted: {Already_booked_waitlisted}")
        print(f"Total Tuesday & Thursday classes: {Classes_booked + Waitlists_joined + Already_booked_waitlisted}")

        print("=======Detailed summary=======")
        for i in processed_class:
            print(i)
else:
    print("❌ MISMATCH:")
