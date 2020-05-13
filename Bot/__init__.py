# login piotrpopisgames@gmail.com
# testertest
import smtplib
import sys
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

    def turn_off_banner(self):
        try:
            self.driver.find_element_by_xpath(
                "//*[@id=\"uc-btn-accept-banner\"]").click()
        except NoSuchElementException:
            sys.stderr.write("Happily banner has not shown on....\n")

    def set_max_per_item(self, max_cost_per_item):
        while 1:
            try:
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").click()
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").clear()
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").send_keys(max_cost_per_item)
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").clear()
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").send_keys(max_cost_per_item)
                self.driver.find_element_by_xpath("//*[@id=\"price-max\"]").send_keys(Keys.ENTER)
                break
            except:
                print('some kind of exception in price inputing max prive')

    def set_brands(self, wanted_brands):
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
                        try:
                            sample.click()
                        except ElementClickInterceptedException:
                            pass
                i += 1
            except NoSuchElementException:
                break

    def set_sizes(self, wanted_sizes):
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

    def __init__(self, email, password, selected_sizes, selected_brands):
        options = Options()
        # options.add_argument("--disable-notifications")
        self.driver = webdriver.Firefox(options=options)

        # Open website
        self.driver.get("https://www.zalando-lounge.pl")

        # Wait for cookies banner and close it
        # WebDriverWait(self.driver, 20).until \
        #     (EC.element_to_be_clickable((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]'))).click()

        # Open loggin panel
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()

        # email
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(email)

        # password
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(password)

        # loggin in
        element.submit()

        # Go to selected event
        campaign_id = 'campaign-ZZO10BY'

        action = ActionChains(self.driver)
        first_compaing = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="' + campaign_id + '"]/div')))
        self.scroll_shim(first_compaing)
        # first_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div')
        action.move_to_element(first_compaing).perform()
        second_compaing = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="' + campaign_id + '"]/div/div[1]/div/button/span')))
        # second_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')
        action.move_to_element(second_compaing).perform()
        second_compaing.click()

        # we have to remove  last char in string
        # for example if someone input bluza or bluzy.
        # bluz is preffix that occurs in both single and multiple form.

        # sometimes banner pop up
        self.turn_off_banner()

        i = 1
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/section/div[2]/nav/a[1]"))
            WebDriverWait(self.driver, 15).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        hrefs = []
        while i:
            try:
                element = "/html/body/div[2]/div/div/section/div[2]/nav/a[" + str(i) + "]"
                sample = self.driver.find_element_by_xpath(element)
                i += 1
                print(sample.text)
                if sample.text == 'KATEGORIE':
                    pass
                elif sample.text == 'ROZMIAR':
                    sample.click()
                    self.set_sizes(selected_sizes)
                elif sample.text == 'MARKA':
                    sample.click()
                    self.set_brands(selected_brands)
                elif sample.text == 'CENA':
                    sample.click()
                    self.set_max_per_item(120)
            except NoSuchElementException:
                break

        all_items = self.driver.find_elements_by_xpath("//div[starts-with(@id, 'article-')]/a")
        for item in all_items:
            hrefs.append(item.get_attribute("href"))
        for href in hrefs:
            self.driver.get(href)
            element = WebDriverWait(self.driver, 20).until \
                (EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]/div[1]/div[1]/span'))).click()
            self.driver.back()
            sleep(1)
        self.scroll_down()


ShoppingBot("piotrpopisgames@gmail.com", 'testertest', ['M', 'L'], ['GAP', 'Fila', 'Kappa', 'Lee'])

"""
    def set_categories_23fgc(self, wanted_categories):
        already_selected = []
        i = 1
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

    def set_categories_2bQSu(self, wanted_categories):
        already_selected = []
        i = 1
        while i:
            try:
                xpath = "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[" + str(i)
                element = self.driver.find_element_by_xpath(xpath + "]/div/span")
                j = 1
                print(i)
                i += 1
                if 'Mężczyźn'.upper() in element.text.upper() or 'UNISE' in element.text.upper():
                    while j:
                        try:
                            print(j)
                            next_cat = xpath + "]/ul/li[" + str(j) + "]/div/span"
                            "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[3]/ul/li[2]/div/span"
                            j += 1
                            sample = self.driver.find_element_by_xpath(next_cat)
                            print(sample.text)
                            for existence_cat in wanted_categories:
                                cat_web = sample.text.lower()
                                if existence_cat in cat_web and cat_web:  # not in already_selected:
                                    already_selected.append(cat_web)
                                    sample.click()
                        except NoSuchElementException:
                            print('no more columns - categories')
                            break
            except NoSuchElementException:
                print('no more rows - categories')
                break

    def set_categories(self, wanted_categories):
        _2bQSu, _23fgc = self.distinct_structure_categories()
        if _2bQSu:
            self.set_categories_2bQSu(wanted_categories)

    def distinct_structure_categories(self):
        _23fgc = False
        _2bQSu = False
        try:
            # 2bq
            element = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[1]/div/span")
            # next : /html/body/div[2]/div/div/section/div[2]/div/div/div/ul/li[2]/div/span
            print(element.text)
            _2bQSu = True
        except NoSuchElementException:
            _2bQSu = False
        try:
            # 2fgc
            element = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/section/div[2]/div/div/div/ul[1]/li[1]/span")
            # next /html/body/div[2]/div/div/section/div[2]/div/div/div/ul[1]/li[2]/span
            print(element.text)
            _23fgc = True
        except NoSuchElementException:
            _23fgc = False
        return _2bQSu, _23fgc
"""
