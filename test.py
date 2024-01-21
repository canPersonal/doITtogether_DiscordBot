from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# Get tomorrow's date
start_date = datetime.now() + timedelta(days=1)
# Generate the next five dates
date_list = [start_date + timedelta(days=i) for i in range(5)]
# Format dates as yyyy-mm-dd
formatted_dates = [date.strftime("%Y-%m-%d") for date in date_list]

# Function to fill out the form
def fill_out_form(browser):
    try:
        # Locate form elements and fill them out
        name_field = browser.find_element(By.ID, "poll_title")
        nameyour_field = browser.find_element(By.ID, "yourname")
        email_field = browser.find_element(By.ID, "email")

        name_field.send_keys("title")
        nameyour_field.send_keys("your")
        email_field.send_keys("hscvx@gmail.com")

        # Submit the form (you may need to adjust the locator for the submit button)
        submit_button = browser.find_element(By.XPATH, "//button[contains(text(), 'step')]")
        submit_button.click()
        
        add_a_day_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.ID, "add-a-day"))
        )

        add_a_day_button.click()
        add_a_day_button.click()

        # Locate and input dates into each field using a loop
        for i in range(0, 5):  # Assuming IDs are "dateformat1" to "dateformat5"
            date_field_id = f"day{i}"
            date_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, date_field_id))
            )
            date_field.send_keys(formatted_dates[i])

        # Wait for the "Add a time slot" button to be clickable
        add_an_hour_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.add-an-hour'))
        )

        add_an_hour_button.click()
        add_an_hour_button.click()
        
        # Iterate through the hours (h0 to h4)
        for hour in range(5):
            # Construct the ID of the input field
            field_id = f"d0-h{hour}"

            # Wait for the input field to be present
            input_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )

            # Input some data (replace this with your actual input)
            input_field.send_keys(f"{hour+17}")


        buttoncopy = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'copyhours'))
        )

        buttoncopy.click()


        # Submit the form (you may need to adjust the locator for the submit button)
        submit2_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        submit2_button.click()


        # Submit the form (you may need to adjust the locator for the submit button)
        submit3_button = browser.find_element(By.XPATH, "//button[contains(text(), 'poll')]")
        submit3_button.click()

        public_link = browser.find_element(By.CLASS_NAME, 'public-link').get_attribute('href')
        admin_link = browser.find_element(By.CLASS_NAME, 'admin-link').get_attribute('href')

        print(f"Public Link: {public_link}")
        print(f"Admin Link: {admin_link}")







    except Exception as e:
        print(f"Error: {e}")
    finally:
         #Close the browser
        browser.quit()

# Set up the Chrome webdriver
browser = webdriver.Chrome()

# Open the webpage
browser.get("https://framadate.org/create_poll.php?type=date&lang=en")

# Call the fill_out_form function
fill_out_form(browser)
