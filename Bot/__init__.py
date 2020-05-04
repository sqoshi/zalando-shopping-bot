# login piotrpopisgames@gmail.com
# testertest
import smtplib
import sys
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def sendMail(to, file):
    """Function to inform user about founded products by e-mail."""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(open('/home/piotr/Music/music/email', 'r').read(), open('/home/piotr/Music/music/mp3.txt', 'r').read())
    from_mail = open('/home/piotr/Music/music/email', 'r').read()
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


def adjust_categories(categories):
    return [cat[:len(cat) - 1] for cat in categories]


class ShoppingBot:
    def select_categories(self, campaign_ID, wanted_categories):
        while 1:
            try:
                self.driver.get('https://www.zalando-lounge.pl/campaigns/' + campaign_ID)
                break
            except WebDriverException:
                pass
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/section/div[2]/nav/a[1]/div/span/span')))
        except TimeoutException:
            print("Timed out waiting for page to load")
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/nav/a[1]/div/span").click()
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul[2]/li/ul/li[" + str(
                        i) + "]/div/span/span")
                for existence_cat in wanted_categories:
                    cat_web = sample.text.lower()
                    if existence_cat in cat_web and cat_web not in already_selected:
                        print(cat_web)
                        already_selected.append(cat_web)
                        sample.click()

                i += 1
            except NoSuchElementException:
                break

    def __init__(self, email, password):
        self.man = True
        self.driver = webdriver.Firefox()
        # Open website
        self.driver.get("https://www.zalando-lounge.pl")
        while 1:
            try:
                self.driver.get("https://www.zalando-lounge.pl")
                break
            except WebDriverException:
                sys.stderr.write("Could not open website, retrying...\n")
        # Open loggin panel
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
                break
            except NoSuchElementException:
                sys.stderr.write("Could not open login panel, retrying...\n")

        # Off annoying banner
        while 1:
            try:
                element_present = EC.presence_of_element_located(
                    (By.XPATH, "//*[@id=\"uc-btn-accept-banner\"]"))
                WebDriverWait(self.driver, 5).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
            try:
                self.driver.find_element_by_xpath(
                    "//*[@id=\"uc-btn-accept-banner\"]").click()
                break
            except NoSuchElementException:
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

        sleep(2)
        campaign_ID = 'ZZO116V'
        # we have to remove  last char in string
        # for example if someone input bluza or bluzy.
        # bluz is preffix that occurs in both single and multiple form.
        selected_categories = ['koszule',
                               'koszulki']
        selected_categories = adjust_categories(selected_categories)
        self.select_categories(campaign_ID, selected_categories)


# elem = self.driver.find_element_by_xpath("//*")
# source_code = elem.get_attribute("innerHTML")
# filename = open('zalando.html', 'w')
# filename.write(source_code)
# filename.close()


ShoppingBot("piotrpopisgames@gmail.com", 'testertest')

"""
    def research(self):
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[2]/span") \
                    .click()
                sleep(1)
                elems3 = self.driver.find_elements_by_xpath("//a[@href]")
                break
            except:
                sys.stderr.write("Could not find man section, retrying...\n")
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[3]/span") \
                    .click()
                sleep(1)
                elems2 = self.driver.find_elements_by_xpath("//a[@href]")
                break
            except:
                sys.stderr.write("Could not find man section, retrying...\n")
        while 1:
            try:
                self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div/ul/li[4]/span") \
                    .click()
                sleep(1)
                elems1 = self.driver.find_elements_by_xpath("//a[@href]")
                break
            except:
                sys.stderr.write("Could not find man section, retrying...\n")
        print(elems1)
        print(elems2)
        print(elems3)
        print(len(elems1))
        print(len(elems2))
        print(len(elems3))
        print("asd")
        results = []
        for elem in elems1:
            try:
                href = elem.get_attribute("href")
                text = str(elem.get_attribute("text"))
                if "Rek" not in text:
                    results.append((href, text))
            except:
                pass
        for elem in elems2:
            try:
                href = elem.get_attribute("href")
                text = str(elem.get_attribute("text"))
                if "Rek" not in text:
                    results.append((href, text))
            except:
                pass
        for elem in elems3:
            try:
                href = elem.get_attribute("href")
                text = str(elem.get_attribute("text"))
                if "Rek" not in text:
                    results.append((href, text))
            except:
                pass
        for x in results:
            print(x)
            """
