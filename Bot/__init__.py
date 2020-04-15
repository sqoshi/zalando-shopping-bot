# login piotrpopisgames@gmail.com
# testertest
from time import sleep
from selenium import webdriver


class Bot:
    def __init__(self, email, password):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.zalando-lounge.pl")
        sleep(3)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
        self.driver.find_element_by_xpath(
            "//*[@id=\"uc-btn-accept-banner\"]").click()
        self.driver.find_element_by_xpath("//*[@id=\"form-email\"]").send_keys(email)
        self.driver.find_element_by_xpath("//*[@id=\"form-password\"]").send_keys(password)
        sleep(2)
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/form/fieldset/button/span").click()


Bot("piotrpopisgames@gmail.com", 'testertest')
