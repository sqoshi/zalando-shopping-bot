# login piotrpopisgames@gmail.com
# testertest
import smtplib
import sys
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, \
    StaleElementReferenceException


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


def choose_species_path(jeans, underwear, upper_part):
    if upper_part:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[1]/div/span/span"
    elif jeans:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[2]/div/span/span"
    elif underwear:
        return "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/div[3]/div[3]/div/span/span"
    else:
        raise ValueError


# TODO: something better than sleep, exceptions handling upgrade needed.
class ShoppingBot:
    def turn_off_banner(self):
        try:
            self.driver.find_element_by_xpath(
                "//*[@id=\"uc-btn-accept-banner\"]").click()
        except NoSuchElementException:
            sys.stderr.write("Happily banner has not shown on....\n")

    def set_brands(self, wanted_brands):
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/section/div[2]/nav/a[3]/div/span/span')))
        except TimeoutException:
            print("Timed out waiting for page to load")
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/nav/a[3]/div/span").click()
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/li[" + str(i) + "]/span")
                for brand in wanted_brands:
                    brand_web = sample.text.lower()
                    if brand.lower() in brand_web and brand_web not in already_selected:
                        print(brand_web)
                        already_selected.append(brand_web)
                        sample.click()

                i += 1
            except NoSuchElementException:
                break

    def set_sizes(self, wanted_sizes):
        path = choose_species_path(False, False, upper_part=True)
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div/div/section/div[2]/nav/a[2]/div/span/span')))
        except TimeoutException:
            print("Timed out waiting for page to load")
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/section/div[2]/nav/a[2]/div/span/span").click()
        self.driver.find_element_by_xpath(path).click()
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/button[" + str(i) + "]")
                for given_size in wanted_sizes:
                    size_web = sample.text.upper()
                    if given_size == size_web and size_web not in already_selected:
                        print(size_web)
                        already_selected.append(size_web)
                        sample.click()
                i += 1
            except NoSuchElementException:
                break

    def set_categories(self, wanted_categories):
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
        options = Options()
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Firefox(options=options)
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
            except StaleElementReferenceException:
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
        while 1:
            try:
                self.driver.get('https://www.zalando-lounge.pl/campaigns/' + campaign_ID)
                break
            except WebDriverException:
                pass
        # we have to remove  last char in string
        # for example if someone input bluza or bluzy.
        # bluz is preffix that occurs in both single and multiple form.
        selected_categories = adjust_categories(['koszule', 'koszulki'])
        # TODO: function to decide what is in catergories [ SPODNIE, GORNE CZESCI GARDEROBY, BIELIZNA]
        selected_sizes = ['M', 'L']
        selected_brands = ['GAP', 'Fila', 'Kappa', 'Lee']
        # sometimes banner pop up
        self.turn_off_banner()
        self.set_categories(selected_categories)
        self.set_sizes(selected_sizes)
        self.set_brands(selected_brands)


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
