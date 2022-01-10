# This file is very heavily commented for instructional purposes. 
# We will get rid of these comments when they are no longer 
# necessary.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys


# Import the IScrapeServiceInterface
from iscrapeservice import IScrapeService

# This is how we create concrete classes from the IScraperService 
# interface (a Python Abstract Base Class).
class FrReqScrapeService(IScrapeService):

    # This method is required as part of the interface
    def scrape(self, user_dto, browser):
        
        browser.get("https://www.facebook.com/friends/requests")
        time.sleep(3)
        
        # frBlock = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]')
        # divs = frBlock.find_elements_by_tag_name('div')
        # i = 0
        # for div in divs:
        #     try:
        #         div.send_keys(Keys.DOWN)
        #         print("Worked on div " + str(i))
        #     except:
        #         pass
        #     i = i + 1

        # print("Should have scrolled down, now wait 3 sec")
        # time.sleep(3)
        
        allFriendRequests = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]')
        friendRequestPhotos = allFriendRequests.find_elements_by_tag_name('image')
        friendRequestPhotosFinal = []
        for j in range(len(friendRequestPhotos)):
            if (friendRequestPhotos[j].get_attribute('style') == "height: 60px; width: 60px;"):
                friendRequestPhotosFinal.append(friendRequestPhotos[j].get_attribute('xlink:href'))
        
        # friendRequestPhotos = [a.get_attribute('xlink:href') for a in friendRequestPhotos]
        # print("Friend Request Photos = ")
        # print(friendRequestPhotosFinal)
        # #get the parent div of the 2 spans

        
        friendRequestNamesFinal = []
        friendRequestNames = allFriendRequests.find_elements_by_xpath("//span[contains(@class, 'lrazzd5p') and contains(@class, 'oo9gr5id')]")
        friendRequestNames = [name.text for name in friendRequestNames]
        for i in range(len(friendRequestNames)):
            # print("Name is = " + friendRequestNames[i])
            if friendRequestNames[i] == '' or friendRequestNames[i][:1].isdigit():
                pass
            else:
                friendRequestNamesFinal.append(friendRequestNames[i])

        # print(friendRequestNamesFinal)
        
        

        # # gets 2nd span's text and append to new array
        # for j in range(len(friendRequestNames)):
        #     tempArray = friendRequestNames[j].find_elements_by_tag_name('span')
        #     friendRequestNamesFinal.append(tempArray[1].text)

        # friendRequestPhotos = allFriendRequests.find_elements_by_tag_name('img')
        # friendRequestPhotos = [a.get_attribute('src') for a in friendRequestPhotos]

        user_dto.fr_name_list = friendRequestNamesFinal
        user_dto.fr_photo_list = friendRequestPhotosFinal
        