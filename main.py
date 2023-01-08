

import time

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class TwitterBot:
    """A TwitterBot class to automate login's and tweets unlike

    :param username 'require': your twitter username used to login
    :param password 'require': your twitter password used to login
    :param chromedriver 'require': download the chrome driver online v 108.0.5359.71 and higher

    :param url 'not require': leave default unless twitter home url changes in the future
    """
    def __init__(self, username:str, password:str, url:str = "http://twitter.com/", chromedriver:str = "~/Documents/Programming/chrome-driver/chromedriver"):
        self.username = username
        self.password = password
        self.url = url
        self.chromedriver = chromedriver
        
        # Selenium settings
        self.option = Options()
        self.option.add_experimental_option("detach", True)
        driver_service = Service(executable_path = self.chromedriver)
        self.driver = webdriver.Chrome(service=driver_service, options=self.option)


    def login(self) -> bool:
        """This method login and navigate to the users profile/likes"""
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()
            time.sleep(3)

            login_btn = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Log in")
            login_btn.click()
            self.driver.implicitly_wait(5)

            input_box = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input' )
            input_box.send_keys(self.username)

            next_btn = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
            next_btn.click()

            password_box = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
            password_box.send_keys(self.password)

            login = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
            login.click()
            time.sleep(2)

            profile_link =  self.driver.find_element(By.PARTIAL_LINK_TEXT, 'Profile')
            profile_link.click()

            like_tweets = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/nav/div/div[2]/div/div[4]/a')
            like_tweets.click()

            return True
        except:
            return False


    def unlike_tweets(self, number:int = 10):
        """This method is used to unlike tweets once on the like page and it takes 1 argument

        :number: int 'require: number(s) of tweet(s) to unlike' """
        try:
            for i in range(0, number):
                path_tag = self.driver.find_element(By.CSS_SELECTOR, " path[d='M20.884 13.19c-1.351 2.48-4.001 5.12-8.379 7.67l-.503.3-.504-.3c-4.379-2.55-7.029-5.19-8.382-7.67-1.36-2.5-1.41-4.86-.514-6.67.887-1.79 2.647-2.91 4.601-3.01 1.651-.09 3.368.56 4.798 2.01 1.429-1.45 3.146-2.1 4.796-2.01 1.954.1 3.714 1.22 4.601 3.01.896 1.81.846 4.17-.514 6.67z']  ")
                path_tag.click()
                print(f"Tweet {i + 1} unliked")
                time.sleep(2)
                
            print(f"Sucess {number} tweets unliked.... ") 
        except NoSuchElementException:
            self.driver.quit()           

    def login_and_unlike(self, unlike_number:int = 10):
        """This method logins and unlike tweets
        :unlike_number: int 'require: number(s) of tweet(s) to unlike'
        """
        try:
            if self.login():
                self.unlike_tweets(unlike_number)
            else:
                print("something went wrong, couldn't login")
                self.driver.quit()
        finally:
            self.driver.quit()
        
