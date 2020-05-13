# login piotrpopisgames@gmail.com
# testertest
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumrequests import Firefox


class ShoppingBot:

    def waitForNonStaleElement(self, type, element):
        strategy = {
            "id":           self.driver.find_element_by_id,
            "link_text":    self.driver.find_element_by_link_text,
            "name":         self.driver.find_element_by_name,
            "xpath":        self.driver.find_element_by_xpath
            }

        lhsType, rhsType = type.split(".", 1)
        find_element = strategy.get(rhsType.lower())

        try:
            find_element(element)
        except StaleElementReferenceException as Exception:
            self.waitForNonStaleElement(type, element)
        except TypeError:
            raise TypeError("ERROR : CODE TO HANDLE \""+element+"\" TYPE NEEDS TO BE CREATED")

    def waitForNonStaleElementClick(self, type, element):
        strategy = {
                "id":           self.driver.find_element_by_id,
                "link_text":    self.driver.find_element_by_link_text,
                "name":         self.driver.find_element_by_name,
                "xpath":        self.driver.find_element_by_xpath
                }
        lhsType, rhsType = type.split(".", 1)
        find_element = strategy.get(rhsType.lower())

        try:
            self.waitForNonStaleElement(type, element)
            find_element(element).click()
        except StaleElementReferenceException as Exception:
            self.waitForNonStaleElementClick( type, element)
        except TypeError:
            raise TypeError("ERROR : CODE TO HANDLE \""+element+"\" TYPE NEEDS TO BE CREATED")
    
    def scroll_shim(self, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        self.driver.execute_script(scroll_by_coord)
        self.driver.execute_script(scroll_nav_out_of_way)

    def scroll_down(self):
        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            sleep(1)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:

                break

            last_height = new_height


    def __init__(self, email, password):

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        # Open website
        self.driver.get("https://www.zalando-lounge.pl")

        # Off annoying banner
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]')))
        element.click()
        #self.waitForNonStaleElementClick("By.XPATH","//*[@id=\"uc-btn-accept-banner\"]")
         # self.driver.find_element_by_xpath("//*[@id=\"uc-btn-accept-banner\"]").click()

        # Open loggin panel
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()

        # email
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(email)

        # password
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(password)

        #loggin

        element.submit()



       
        # self.driver.find_element_by_id('form-email').send_keys(email)
        # self.driver.find_element_by_id('form-password').send_keys(email)
        # self.driver.find_element_by_xpath("//*[@id=\"form-email\"]").send_keys(email)
        # self.driver.find_element_by_xpath("//*[@id=\"form-password\"]").send_keys(password)
        # self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button").click()

        campaign_id = 'campaign-ZZO105N'
        action = ActionChains(self.driver)
        first_compaing = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="'+campaign_id+'"]/div')))
        self.scroll_shim(first_compaing)
        # first_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div')
        action.move_to_element(first_compaing).perform()
        second_compaing = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')))
        # second_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')
        action.move_to_element(second_compaing).perform()
        second_compaing.click()


        price = '100'
        self.driver.find_element_by_xpath('//*[@id="inner-wrapper"]/section/div[2]/nav/a[5]/div/span').click()
        sleep(1)
        price_max=self.driver.find_element_by_xpath('//*[@id="price-max"]')
        sleep(1)
        self.driver.execute_script('document.getElementById("price-max").value = "'+price+'";')
        price_max.send_keys(Keys.ENTER)

        self.scroll_down()
        
        #Store all href for availables items
        hrefs = []

        all_items = self.driver.find_elements_by_xpath("//div[starts-with(@id, 'article-')]/a")
        for item in all_items:
            href = item.get_attribute("href")
            if (len(self.driver.find_elements_by_xpath('//a[@href="' + href[29:] + '"]/div[3]')) == 0):
                hrefs.append(href)


        # Add all items from hrefs to cart
        for href in hrefs:
            self.driver.get(href)
            element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]/div[1]/div[1]/span'))).click()
            self.driver.back()
            sleep(1)
        

        print('finished')




ShoppingBot("piotrpopisgames@gmail.com", 'testertest')
