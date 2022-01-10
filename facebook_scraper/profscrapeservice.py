from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .iscrapeservice import IScrapeService

class ProfScrapeService(IScrapeService):

    def scrape(self, user_dto, browser):
        browser.get("https://www.facebook.com/profile")

        time.sleep(5)

        totalNumberOfFriends = None
        try:
            friendCountElement = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[2]/span/a")
            totalNumberOfFriends = int(friendCountElement.text.replace(" Friends", ""))
        except:
            print("Your thing broke.")
        print("Your total number of friends is: " + str(totalNumberOfFriends))

        
        def xpathWrapper(xpaths):
            for xpath in xpaths:
                try:
                    browser.find_element_by_xpath(xpath)
                except NoSuchElementException:
                    continue
                return browser.find_element_by_xpath(xpath)
            
            
        profNameXpaths = ['/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div/div/span/h1', 
                          '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]/div/div/div[1]/div/div/span/h1']
        profName = xpathWrapper(profNameXpaths)
        
        #For some reason can't get direct svg xpaths, so have to go to parents, note, order of these xpaths 
        # matter since they both exist in the different web pages
        profPicXpaths = [
            '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div/div/div/div', 
            '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div/div/div/div/div']
        profPicHead = xpathWrapper(profPicXpaths)
        profPic = profPicHead.find_element_by_tag_name('image')

        # user_dto.add_data("profile_name", profName.text)
        # user_dto.add_data("profile_image_source", profPic.get_attribute('xlink:href'))
        user_dto.add_data("user", {
            "name": profName.text,
            "imageSource": profPic.get_attribute('xlink:href'),
            "total_number_of_friends": totalNumberOfFriends
        })