# login piotrpopisgames@gmail.com
# testertest
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class ShoppingBot:
    def __init__(self, email, password):
        self.driver = webdriver.Firefox()
        # Open website
        self.driver.get("https://www.zalando-lounge.pl")
        while 1:
            try:
                self.driver.get("https://www.zalando-lounge.pl")
                break
            except:
                sys.stderr.write("Could not open website, retrying...\n")
        # Open loggin panel
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
                break
            except:
                sys.stderr.write("Could not open login panel, retrying...\n")

        # Off annoying banner
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "//*[@id=\"uc-btn-accept-banner\"]").click()
                break
            except:
                sys.stderr.write("Could not accept cookies acceptance, retrying...\n")

            # Log into shop.
        while 1:
            try:
                self.driver.find_element_by_xpath("//*[@id=\"form-email\"]").send_keys(email)
                self.driver.find_element_by_xpath("//*[@id=\"form-password\"]").send_keys(password)
                self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button").click()
                break
            except:
                self.driver.find_element_by_xpath("//*[@id=\"form-email\"]").clear()
                self.driver.find_element_by_xpath("//*[@id=\"form-password\"]").clear()
                sys.stderr.write("Login failed, retrying...\n")

                # select Man
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[4]/span") \
                    .click()
                sleep(1)
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[4]/span") \
                    .click()
                break
            except:
                sleep(2)
                sys.stderr.write("Could not find man section, retrying...\n")

        elems = self.driver.find_elements_by_xpath("//a[@href]")
        while 1:
            print("asd")
            for elem in elems:
                # if "Puma" in elem.get_attribute("text") and "Rek" not in elem.get_attribute("text"):
                href = elem.get_attribute("href")
                text = str(elem.get_attribute("text"))
                clas = str(elem.get_attribute("class"))
                if "Armani" in text and "Rek" not in text:
                    print(href, text, 'cls', clas)
                    self.driver.get(href)
                    sleep(7)
                    price = '400'
                    self.driver.find_element_by_xpath('//*[@id="inner-wrapper"]/section/div[2]/nav/a[5]/div/span').click()
                    price_max=self.driver.find_element_by_xpath('//*[@id="price-max"]')
                    sleep(1)
                    self.driver.execute_script('document.getElementById("price-max").value = "'+price+'";')
                    price_max.send_keys(Keys.ENTER)
                    break
            break
                   

        print('finished')
        # elem = self.driver.find_element_by_xpath("//*")
        # source_code = elem.get_attribute("innerHTML")
        # filename = open('zalando.html', 'w')
        # filename.write(source_code)
        # filename.close()




ShoppingBot("piotrpopisgames@gmail.com", 'testertest')
