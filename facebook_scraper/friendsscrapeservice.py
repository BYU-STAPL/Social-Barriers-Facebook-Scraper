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

# This is how we create concrete classes from the IScraperService 
# interface (a Python Abstract Base Class).
class FriendScrapeService(IScrapeService):
    # This method is required as part of the interface
    def scrape(self, user_dto, browser):
        MAXIMUM_WAIT_TIME = 7 # maximum time to wait for necessary elements to appear, in seconds
        browser.implicitly_wait(MAXIMUM_WAIT_TIME)
        startTime = time.time()
        # Go to user's Facebook profile and wait for page to load
        browser.get("https://www.facebook.com/profile")
        friends_url = browser.current_url + "&sk=friends" # This is the url that represents their friends page
        browser.get(friends_url) # Go to their friends page

        
        friendNamesBeforeScrolling = None
        friendNamesAfterScrolling = []
        totalNumberOfFriends = None
        try:
            friendCountElement = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a")
            totalNumberOfFriends = int(friendCountElement.text.replace(" Friends", ""))
        except:
            print("Your thing broke.")
        print("Your total number of friends is: " + str(totalNumberOfFriends))

        friendElements = []
        # Main scrolling loop
        #while len(friendElements) + 1 < totalNumberOfFriends: # The reason we are doing friendElements - 1 is because the last friend element is a div that shows "Loading" until everything is loaded
        while (len(friendElements)) < 30:
            time.sleep(3) # By experimentation, I've found that this is a nice way to do it; Facebook doesn't freeze up from spamming the scroll bar
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            friendParentDiv = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]")
            friendElements = friendParentDiv.find_elements(By.XPATH, "*")
            logging.debug("Number of friends scraped: " + str(len(friendElements) - 1))
            #friendNamesAfterScrolling = browser.find_elements_by_xpath("//div[@class='buofh1pr hv4rvrfc']/div[1]/a/span")
            #print(len(friendNamesAfterScrolling))

        friends = [] # This will be a list that holds the friend name and a link to the friend image.
        for friendElement in friendElements:
            try:
                friends.append(
                    {
                        "imageSource" : friendElement.find_element(By.TAG_NAME, "img").get_attribute("src"),
                        "name": friendElement.find_element(By.XPATH, ".//div[2]/div[1]/a/span").text,
                    }
                )
            except: # This is the last div, where there is no image tag.
                pass
        endTime = time.time()
        logging.info("The total time for the friendsscraperservice to run is")
        logging.info(str(endTime - startTime))
        user_dto.add_data("friends", friends)