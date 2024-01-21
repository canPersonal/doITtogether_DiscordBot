from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

def create_poll(event):
    # Specify the path to your webdriver (e.g., chromedriver.exe)
    driver_path = '/path/to/chromedriver'

    # Create a new instance of the Chrome driver
    browser = webdriver.Chrome(executable_path=driver_path)

    try:
        # Load the webpage
        browser.get('your_poll_website_url_here')

        # Fill out the form
        fill_out_form(browser, event)

        # Extract and return the admin and public links
        public_link = browser.find_element(By.CLASS_NAME, 'public-link').get_attribute('href')
        admin_link = browser.find_element(By.CLASS_NAME, 'admin-link').get_attribute('href')

        return public_link, admin_link

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser window
        browser.quit()

def fill_out_form(browser, event):
    # Locate form elements and fill them out
    name_field = browser.find_element(By.ID, "poll_title")
    nameyour_field = browser.find_element(By.ID, "yourname")
    email_field = browser.find_element(By.ID, "email")

    name_field.send_keys(event['title'])
    nameyour_field.send_keys(event['organizer'])
    email_field.send_keys(event['email'])

    # Submit the form (you may need to adjust the locator for the submit button)
    submit_button = browser.find_element(By.XPATH, "//button[contains(text(), 'step')]")
    submit_button.click()

    # ... (rest of your form filling logic)

# Example event structure
event_info = {
    'title': 'Your Event Title',
    'organizer': 'Your Name',
    'email': 'your_email@example.com',
    # Add other event details as needed
}

# Call the function with the event information
public_link, admin_link = create_poll(event_info)

# Print the results
print(f"Public Link: {public_link}")
print(f"Admin Link: {admin_link}")
