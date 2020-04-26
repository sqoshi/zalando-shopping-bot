# login piotrpopisgames@gmail.com
# testertest
from time import sleep
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException


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
                print("Retrying !!!")
        # Open loggin panel
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
                break
            except:
                print("Retrying !!!")

        # Off annoying banner
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "//*[@id=\"uc-btn-accept-banner\"]").click()
                break
            except:
                print("Retrying !!!")

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

                # select Man
        while 1:
            try:
                sleep(3)
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[3]/span").click()
                break
            except:
                print("cant find Man")

        elems = self.driver.find_elements_by_xpath("//a[@href]")
        while 1:
            try:
                for elem in elems:
                    # if "Puma" in elem.get_attribute("text") and "Rek" not in elem.get_attribute("text"):
                    href = elem.get_attribute("href")
                    text = elem.get_attribute("text")
                    alt = elem.get_attribute("alt")
                    clas = elem.get_attribute("class")
                    print(href, text, alt, clas)
                print("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
                raise Exception
            except Exception as ex:
                break
        self.driver.get("https://www.zalando-lounge.pl/campaigns/ZZO10ZG/gender_134")
        # elem = self.driver.find_element_by_xpath("//*")
        # source_code = elem.get_attribute("innerHTML")
        # filename = open('zalando.html', 'w')
        # filename.write(source_code)
        # filename.close()


ShoppingBot("piotrpopisgames@gmail.com", 'testertest')
