from .userdto import UserDTO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class Scraper():

    def __init__(self, phone_number, password):
        self.backend = None
        self.scrape_services = []
        self.user_dto = UserDTO({})
        self.user_dto.user_data["password"] = password
        self.user_dto.user_data["phone_number"] = phone_number

    def scrape(self):
        username = self.user_dto.user_data["phone_number"]
        password = self.user_dto.user_data["password"]
        
        # DISABLE NOTIFICATION POPUPS
        option = Options()
        option.add_argument('--disable-notifications')
        option.add_argument("--window-size=1920,1080")
        option.add_argument("--start-maximized")
        option.add_argument("--headless")


        # OPEN FACEBOOK
        browser = webdriver.Chrome(options=option)
        browser.get('https://www.facebook.com/')
        
        # LOG USER IN
        phone_input = browser.find_element_by_name('email')
        password_input = browser.find_element_by_name('pass')
        login_button = browser.find_element_by_name('login')

        # notice we are using username here but it will be phone number eventually
        phone_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(3) #TODO: see if you can elminate this sleep(3) thing.

        # SCRAPE ALL SERVICES
        for service in self.scrape_services:
            service.scrape(self.user_dto, browser)
        
        # STORE DATA IN THE BACKEND
        self.backend.store_data(self.user_dto)
        browser.quit()

    def attach_scraper(self, scrape_service):
        self.scrape_services.append(scrape_service)

    def attach_backend(self, backend):
        self.backend = backend