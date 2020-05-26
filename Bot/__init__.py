# login info.shopping.bot@gmail.com
# shopping123bot
import smtplib
import sys
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
    server.login('info.shopping.bot@gmail.com', 'shopping123bot')
    from_mail = 'info.shopping.bot@gmail.com'
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


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

        WebDriverWait(self.driver, 5).until \
            (EC.element_to_be_clickable((By.XPATH, '//span[.="Cena"]'))).click()
        price_max = self.driver.find_element_by_xpath('//*[@id="price-max"]')
        self.driver.execute_script('document.getElementById("price-max").value = "' + str(max_cost_per_item) + '";')
        price_max.send_keys(Keys.ENTER)

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
                        sample.click()
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

    def wait_for(self):
        try:
            WebDriverWait(self.driver, 1).until \
                (EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"sizeOverlayDialog")]')))

            WebDriverWait(self.driver, 5).until \
                (EC.element_to_be_clickable((By.XPATH, '//span[text() = "Mimo to zamawiam oba rozmiary"]'))).click()

            WebDriverWait(self.driver, 5).until \
                (EC.element_to_be_clickable((By.XPATH, '//span[text() = "Potwierdź"]'))).click()
        except TimeoutException:

            element = WebDriverWait(self.driver, 5).until \
                (EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
            self.wait_for()

    def wait_for_atcButton(self):
        try:
            # WebDriverWait(self.driver, 5).until \
            # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
            WebDriverWait(self.driver, 5).until \
                    (EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
            WebDriverWait(self.driver, 5).until \
                    (EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))

        except TimeoutException:
            print('atcBtn')

    def __init__(self, em, pwd, cats, sizs, brds, cid, mpi):
        options = Options()
        # options.add_argument("--disable-notifications")
        self.driver = webdriver.Firefox(options=options)
        self.email = em
        self.password = pwd
        self.categories_list = cats
        self.sizes_list = sizs
        self.brands_list = brds
        self.campaign_id = cid
        self.max_per_item = mpi

    def start_bot(self):

        # Open website
        self.driver.get("https://www.zalando-lounge.pl")

        # Wait for cookies banner and close it
        WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]'))).click()

        # Open loggin panel
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()

        # email
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(self.email)

        # password
        element = WebDriverWait(self.driver, 20).until \
            (EC.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(self.password)

        # loggin in
        element.submit()

        # Go to selected event
        self.campaign_id = 'campaign-' + self.campaign_id

        action = ActionChains(self.driver)
        first_compaing = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="' + self.campaign_id + '"]/div')))
        self.scroll_shim(first_compaing)
        action.move_to_element(first_compaing).perform()
        second_compaing = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="' + self.campaign_id + '"]/div/div[1]/div/button/span')))
        action.move_to_element(second_compaing).perform()
        second_compaing.click()

        # Wait until filters load
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "filters")]')))

        # sometimes banner pop up
        self.turn_off_banner()
        i = 1

        while i:
            try:
                element = "/html/body/div[2]/div/div/section/div[2]/nav/a[" + str(i) + "]"
                sample = self.driver.find_element_by_xpath(element)
                i += 1
                print(sample)
                if sample.text == 'KATEGORIE':
                    pass
                elif sample.text == 'ROZMIAR':
                    sample.click()
                    self.set_sizes(self.sizes_list)
                elif sample.text == 'MARKA':
                    sample.click()
                    self.set_brands(self.brands_list)
                elif sample.text == 'CENA':
                    sample.click()
                    self.set_max_per_item(self.max_per_item)
            except NoSuchElementException:
                break

        self.scroll_down()

        # Store all href for availables items
        hrefs = []

        all_items = self.driver.find_elements_by_xpath("//div[starts-with(@id, 'article-')]/a")
        for item in all_items:
            href = item.get_attribute("href")
            item_parent = item.find_element_by_xpath("./..")
            item_description = item_parent.find_element_by_xpath('./div/div[1]').text
            # print(item_description)
            if (len(self.driver.find_elements_by_xpath('//a[@href="' + href[29:] + '"]/div[3]')) == 0):
                if any(category_name.lower() in item_description.lower() for category_name in self.categories_list):
                    hrefs.append(href)

        selected_sizes = self.sizes_list
        # Add all items from hrefs to cart
        for href in hrefs:
            self.driver.get(href)

            WebDriverWait(self.driver, 5).until \
                (EC.presence_of_element_located((By.XPATH, "//div[starts-with(@class, 'ArticleSizestyles')]")))

            selected = 0

            for size in selected_sizes:
                element = WebDriverWait(self.driver, 5).until \
                        (EC.element_to_be_clickable(
                        (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]')))
                # addtoCartButton = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]')))
                parent = element.find_element_by_xpath("./..")
                is_clickable = parent.value_of_css_property("color")
                if is_clickable == 'rgb(53, 53, 53)':
                    ammount = -1
                    try:
                        ammount_span = parent.find_element_by_xpath('./span[2]')
                        ammount = int(ammount_span.text[-1:])
                    except NoSuchElementException:
                        ammount = 5

                    element.click()
                    selected = selected + 1
                    for x in range(ammount):
                        WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()

                        if selected == 2 and x == 0:
                            self.wait_for()
                            WebDriverWait(self.driver, 20).until \
                                    (EC.invisibility_of_element_located(
                                    (By.XPATH, '//div[contains(@class,"styles___backdrop")]')))
                        else:
                            self.wait_for_atcButton()  # sleep(1.5)

                # if selected == 1: ZZO125F
                #     sleep(.7)
                # WebDriverWait(self.driver, 5).until \
                # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
                # WebDriverWait(self.driver, 5).until \
                # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
                # WebDriverWait(self.driver, 5).until \
                # (EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
                # if selected==2:
                #     print("no nie dziala")
                #     self.wait_for()
        print('finished')


datetime_str = '24/05/20 15:31:00'
datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')

print(type(datetime_object))
print(datetime_object)  # printed in default format

# ShoppingBot("piotrpopisgames@gmail.com", 'testertest') ZZO0ZLB
