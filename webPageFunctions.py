from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from datetime import datetime, timedelta
import math

def create_poll(event):
    try:

        BROWSERSTACK_USERNAME="canoluk_698K32"
        BROWSERSTACK_ACCESS_KEY="GzPZ7wLYhKdwdHybZ9PG"
        BROWSERSTACK_URL = 'https://hub-cloud.browserstack.com/wd/hub'

        
        # Define desired capabilities for BrowserStack
        desired_capabilities = {
            'browser': 'Chrome',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '10',
            'name': 'Your Test Name'  # Replace with a descriptive name for your test
        }

        # Set up WebDriver with BrowserStack
        browser = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            desired_capabilities=desired_capabilities,
            username=BROWSERSTACK_USERNAME,
            access_key=BROWSERSTACK_ACCESS_KEY
        )

        # Create a new instance of the Firefox driver
        # browser = webdriver.Firefox()

        # Load the webpage
        browser.get("https://framadate.org/create_poll.php?type=date&lang=en")

        # Fill out the form
        public_link, admin_link = fill_out_form(browser, event)

        return public_link, admin_link

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None

    finally:
        if 'browser' in locals():
            # Close the browser window
            browser.quit()

def fill_out_form(browser, event):
    try:
        # Get tomorrow's date
        start_date = datetime.now() + timedelta(days=1)
        # Generate the next week
        date_list = [start_date + timedelta(days=i) for i in range(7)]
        # Format dates as yyyy-mm-dd
        formatted_dates = [date.strftime("%Y-%m-%d") for date in date_list]

        # Locate form elements and fill them out
        browser.find_element(By.ID, "poll_title").send_keys(event['name'])
        browser.find_element(By.ID, "yourname").send_keys(event['author'])
        browser.find_element(By.ID, "email").send_keys(event['emailAu'])

        # Submit the form
        submit_button = browser.find_element(By.XPATH, "//button[contains(text(), 'step')]")
        submit_button.click()
        
        # Add dates
        add_a_day_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.ID, "add-a-day"))
        )
        for _ in range(4):
            add_a_day_button.click()

        # Input dates
        for i in range(0,6):  # Assuming IDs are "dateformat1" to "dateformat5"
            date_field_id = f"day{i}"
            date_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, date_field_id))
            )
            date_field.send_keys(formatted_dates[i])

        # Add time slots
        add_an_hour_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.add-an-hour'))
        )
        num_of_clicks = math.ceil(18 / float(event['duration']))
        for _ in range(num_of_clicks):
            add_an_hour_button.click()
        
        # Input hours
        hour0=8
        for hourIT in range(num_of_clicks):
            field_id = f"d0-h{hourIT}"
            hour1=hourIT*float(event['duration'])+hour0
            input_field = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )
            input_field.send_keys(f"{hour1}")

        # Copy hours
        buttoncopy = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'copyhours'))
        )
        buttoncopy.click()

        # Navigate to next step
        submit2_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Next')]")
        submit2_button.click()

        # Submit the form
        submit3_button = browser.find_element(By.XPATH, "//button[contains(text(), 'poll')]")
        submit3_button.click()

        # Extract and return the admin and public links
        public_link = browser.find_element(By.CLASS_NAME, 'public-link').get_attribute('href')
        admin_link = browser.find_element(By.CLASS_NAME, 'admin-link').get_attribute('href')
        return public_link, admin_link

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
