# This class is responsible for get all the friends associated with a certain event on Facebook.
# It scrapes recent events as well as some of the friends that went to those recent events


import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the IScrapeServiceInterface
from .iscrapeservice import IScrapeService

class EventFriendsScrapeService(IScrapeService):
    def scrape(self, user_dto, browser):
        MAXIMUM_WAIT_TIME = 12 # maximum time to wait for necessary elements to appear, in seconds
        browser.implicitly_wait(MAXIMUM_WAIT_TIME)
        browser.get("https://www.facebook.com/events")

        def clickParentUntilNoError(element): # If clicking on the item directly doesn't work, try clicking on its parent until it works!
            try:
                element.click()
            except:
                clickParentUntilNoError(element.find_element(By.XPATH, "./.."))
        
        def getSpanByText(text):
            return browser.find_element(By.XPATH, "//span[text()='" + text + "']")

        def clickBySpanText(text):
            # WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, "//span[text()='" + text + "']")))
            clickParentUntilNoError(getSpanByText(text))
        
        # For testing purposes only
        totalNumberOfFriends = 786

        # ENSURE DEPENDENCIES ARE MET:
        # totalNumberOfFriends = None
        # try:
        #     totalNumberOfFriends = user_dto.user_data["user"]["total_number_of_friends"]
        # except:
        #     raise Exception("EventFriendsScrapeService cannot run unless ProfScrapeService has run first, to scrape the total number of friends.")

        def createEvent():
            logging.debug("Entering createEvent")
            # Click the Create new event button:
            browser.find_element(By.XPATH, "//span[text()='Create new event']").click()

            # Click the "In Person" button for EventType
            browser.find_element(By.XPATH, "//span[text()='In Person']").click()

            # Add some text for the evnet name. This works by finding the Event name span (which appears right above the text box), and then getting the input right after it
            eventNameTextBox = browser.find_element(By.XPATH, "//span[text()='Event name']/following-sibling::input")
            eventNameTextBox.send_keys("a")

            # Click the privacy Options
            privacySpan = browser.find_element(By.XPATH, "//span[text()='Privacy']")
            #privacyButton = WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.presence_of_element_located(privacySpan.find_element(By.XPATH, "../.."))) # Get the grandparent
            privacyButton = privacySpan.find_element(By.XPATH, "../..")
            #privacyButton = browser.find_element(By.XPATH, "//*[@id='mount_0_0_T3']/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[3]/div/div/div/label/div/div[3]/div/i")
            privacyButton.click()
            #WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.presence_of_element_located(By.XPATH, "//span[text()='Private'")).click()
            browser.find_element(By.XPATH, "//span[text()='Private']").click()

            # CLICK NEXT UNTIL DONE
            def xpathExists(xpath):
                try:
                    browser.find_element(By.XPATH, xpath)
                except NoSuchElementException:
                    return False
                return True

            # Keep clicking next until the Create event button appears. The following is intelligent and works great, but it's slow.
            # while not(xpathExists("//span[text()='Create event']")):
            #     browser.find_element(By.XPATH, "//span[text()='Next']").click()

            # Click next 3 times
            # nextButton = WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
            # nextButton.click()
            # nextButton.click()
            # nextButton.click()
            def pushButtonsToFinish():
                browser.find_element(By.XPATH, "//span[text()='Next']").click()
                browser.find_element(By.XPATH, "//span[text()='Next']").click()
                browser.find_element(By.XPATH, "//span[text()='Next']").click()
                try:
                    browser.find_element(By.XPATH, "//span[text()='Next']").click()
                    browser.find_element(By.XPATH, "//span[text()='Create event']").click()
                except:
                    browser.find_element(By.XPATH, "//span[text()='Create event']").click()
            
            pushButtonsToFinish()
            logging.debug("Exiting createEvent")


        
        def getFriends(friendGroupType, friendContainer):
            # Add a conditional such that if friendGroupType is all, then simply scroll down in that div until the number of elements is equal to the number of friends that you have
            print(friendGroupType)
            friendElements = friendContainer.find_elements(By.XPATH, "./div") #friendContainer.find_elements(By.XPATH, ".//*")[2:] # Start at 1 because the 0th element is the "select all" button


            # If we are getting all the friends, scroll until all of the friends are present.
            if friendGroupType == "all":
                numberOfTimesLengthIsSame = 0
                SCROLL_NO_UPDATE_LIMIT = 4 # This is the number of times it will scroll down without the number of elements changing before moving on to the next item
                # while len(friendElements) <= totalNumberOfFriends: # This is interesting. We could use totalNumberOfFriends, however it seems like some friends don't can't be invited to events (e.g. I have 786 friends, but only 777 show up on this list)
                while numberOfTimesLengthIsSame < SCROLL_NO_UPDATE_LIMIT:
                    lengthBeforeScrolling = len(friendElements)
                    # Set the distance to scroll to to be the location of the last element in the friendElements list
                    lastElement = friendElements[len(friendElements) - 2]
                    lastElement.click()
                    html = browser.find_element(By.TAG_NAME, 'html')
                    html.send_keys(Keys.PAGE_DOWN)
                    time.sleep(1)
                    friendElements = friendContainer.find_elements(By.XPATH, "./div") #friendContainer.find_elements(By.XPATH, ".//*")[2:] # Start at 1 because the 0th element is the "select all" button
                    lengthAfterScrolling = len(friendElements)
                    if lengthBeforeScrolling == lengthAfterScrolling:
                        numberOfTimesLengthIsSame += 1
                    else:
                        numberOfTimesLengthIsSame = 0
            
            friends = []
            for friendElement in friendElements: # if you have a friend whose name is "Select," you're out of luck
                elementText = friendElement.text # Only call this once because it's a very expensive opperation that checks styles and visibility of each of the descendants
                if elementText.startswith("Select") or elementText == "" or elementText == None:
                    continue
                print(elementText)
                image = friendElement.find_element(By.TAG_NAME, "image")
                
                # image = friendElement.find_element(By.XPATH, "./div/div/div[1]/div/div/svg/g/image") # It's possible that some kind of code like this could show performance improvements
                
                print(image.get_attribute('xlink:href'))
                friends.append({
                    "name" : elementText,
                    "imageSource": image.get_attribute('xlink:href')
                })
            return friends
        
        def openPopup():
            # CLICK INVITE BUTTON
            # Wait until the event is created. It will be created when the span described below appears.
            WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add a Few Final Details']")))

            inviteButton = browser.find_element(By.CSS_SELECTOR, "[aria-label='Invite']")
            inviteButton.click()

            # Wait for popup to appear
            WebDriverWait(browser, MAXIMUM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Select all']")))
            print("We found the Select All thing!")

        def scrapeFriends():
            sideBar = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/div")
            sideBarChildren = sideBar.find_elements(By.XPATH, ".//*")
            logging.info(len(sideBarChildren))
            print("We found the sidebar!")
            currentElementText = ""
            friendGroupType = "" # Suggested is the first friend group type
            friendsByGroup = []
            friendsByEvent = []
            suggestedFriends = []
            allFriends = []
            for child in sideBarChildren:
                # Continue looping through the children until the children's text is differnet
                # logging.debug("Currently scraping " + currentElementText)
                print("Currently scraping " + currentElementText)
                if child.text == "More...": # No need to click on the more button, that just gives us more stuff to scrape.
                    logging.info("Don't click the More... button")
                    continue
                if child.text == currentElementText:
                    logging.info("Not scraping duplicate element, " + currentElementText)
                    continue
                else:
                    currentElementText = child.text
                    try: # The more button causes an exception on click, so wrap in try except block
                        child.click()
                        time.sleep(1) # Wait one second for everything to update. TODO: update this with something intelligent if you can think of it.
                    except:
                        continue
                    # Get the container surrounding the friends
                    #friendContainer = browser.find_element(By.XPATH, "//div[@class='j83agx80 cbu4d94t buofh1pr l9j0dhe7']")
                    friendContainer = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/div/div/div")

                    if currentElementText == "Suggested":
                        friendGroupType = "suggested"
                    elif currentElementText == "All Friends":
                        friendGroupType = "all"
                    elif currentElementText == "EVENTS I ATTENDED":
                        friendGroupType = "events"
                        continue # Continue because this text represents a header, not a button
                    elif currentElementText == "MY GROUPS":
                        friendGroupType = "groups"
                        continue
                    
                    friends = getFriends(friendGroupType, friendContainer)
                    if friendGroupType == "events":
                        friendsByEvent.append(
                            {
                                "eventName": currentElementText,
                                "friends": friends
                            }
                        )
                    elif friendGroupType == "groups":
                        friendsByGroup.append(
                            {
                                "groupName": currentElementText,
                                "friends": friends
                            }
                        )
                    elif friendGroupType == "all":
                        allFriends = friends
                    elif friendGroupType == "suggested":
                        suggestedFriends = friends
                    else:
                        print(friendGroupType + " is not in the approved list!")
            user_dto.add_data("friendsByEvent", friendsByEvent)
            user_dto.add_data("friendsByGroup", friendsByGroup)
            user_dto.add_data("friends", allFriends)
            user_dto.add_data("suggestedFriends", suggestedFriends)

        def closePopup():
            # Perform a shift tab to unfocus from the text that's selected
            a = webdriver.ActionChains(browser)
            a.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT) # shift tab
            a.perform()

            # Press the escape key
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()


            
        def deleteEvent():
            # Find the three dots option menu
            logging.debug("Attempting to delete event")
            #clickParentUntilNoError(browser.find_element(By.CSS_SELECTOR, "[aria-label='More']")) # Three dots option menu
            clickParentUntilNoError(browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div"))
            time.sleep(5) # Wait 5 seconds to see if the cancel event button will appear
            clickBySpanText("Cancel Event")
            clickBySpanText("Delete Event")
            #clickBySpanText("Confirm")
            # Sadly, it seems there are multiple spans with 'Confirm', so we click the Confirm button by xpath:
            clickParentUntilNoError(browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[4]/div/div[1]/div[1]/div/div[1]/div/span/span"))
            logging.debug("Event deleted")
        
        createEvent()
        openPopup()
        # scrapeFriends()
        closePopup()
        deleteEvent()

        # try:
        #     closePopup()
        #     deleteEvent()
        # except:
        #     print("Oh well, some weird error happend when trying to delete the event. Too bad, so sad.")

        time.sleep(3) # Just let it sleep for a little while so you can see what's on screen before it closes.