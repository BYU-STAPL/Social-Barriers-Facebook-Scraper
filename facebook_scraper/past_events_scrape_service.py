import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the IScrapeServiceInterface
from .iscrapeservice import IScrapeService

class PastEventsScrapeService(IScrapeService):
    def scrape(self, user_dto, browser):
        MAXIMUM_WAIT_TIME = 7 # maximum time to wait for necessary elements to appear, in seconds
        browser.implicitly_wait(MAXIMUM_WAIT_TIME)
        browser.get("https://www.facebook.com/events/past")

        # The following xpath is all the spans that contain the name of previous events you've attended
        eventNameElements = browser.find_elements(By.XPATH, "//div[@class='rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw i1fnvgqd owycx6da btwxx1t3 bp9cbjyn']//div[2]/div[1]/div/div/div/div[2]/span/span/object/a/span")

        eventNames = [] 
        for event in eventNameElements:
            eventNames.append(event.text)
        
        user_dto.add_data("recent_events", eventNames)