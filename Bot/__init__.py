# login piotrpopisgames@gmail.com
# testertest
from time import sleep
from selenium import webdriver


class Bot:
    def __init__(self, username, password):
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.zalando-lounge.pl")
        sleep(3)


Bot("trash", 'lol')
