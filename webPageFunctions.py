from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from datetime import datetime, timedelta
import math
import json

def create_poll(event):
    try:
        with open('links.json', 'r') as file:
            TOKENL = json.load(file)
            TOKENl=TOKENL[0]
            TOKEN=TOKENl['token']
        


        return public_link, admin_link


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
