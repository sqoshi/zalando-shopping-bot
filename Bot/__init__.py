import smtplib
import sys
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import PyQt5
from PyQt5.QtWidgets import QMessageBox, QApplication


def sendMail(to, file):
    """
   Function to inform user about founded products by e-mail.
   :param to:
   :param file:
   :return:
   """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('info.shopping.bot@gmail.com', 'shopping123bot')
    from_mail = 'info.shopping.bot@gmail.com'
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)
    print('\'' + body + '\' to', to)


class ShoppingBot:

    def __init__(self, acc, cats, sizs, brds, cid, mpi, maa, mail, is_mail_checked, ite):
        options = Options()
        # options.add_argument("--disable-notifications")
        # print(acc, cats, sizs, brds, cid, mpi, maa, mail, is_mail_checked, ite)
        self.driver = webdriver.Firefox(options=options)
        self.inform_email = None
        if is_mail_checked:
            self.inform_email = mail
        self.email = acc[ite].split()[0]
        self.password = acc[ite].split()[1]
        self.categories_list = cats
        self.sizes_list = sizs
        self.brands_list = brds
        self.campaign_id = cid
        self.max_per_item = mpi
        self.accounts_list = acc
        self.max_ammount = maa
        self.iteration = ite

    def scroll_shim(self, obj):
        """
       Scrolling down to needed event

       :param obj:
       :return:
       """
        x = obj.location['x']
        y = obj.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        self.driver.execute_script(scroll_by_coord)
        self.driver.execute_script(scroll_nav_out_of_way)

    def scroll_down(self):
        """
       Scrolling down all items on list
       :return:
       """
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
        """
       Turn off cookie acceptance banner
       :return:
       """
        try:
            self.driver.find_element_by_xpath(
                "//*[@id=\"uc-btn-accept-banner\"]").click()
        except NoSuchElementException:
            sys.stderr.write("Happily banner has not shown on....\n")

    def set_max_per_item(self, max_cost_per_item):
        """
       Setting max price per item in filtering
       :param max_cost_per_item:
       :return:
       """

        WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="price-max"]'))).click()
        if max_cost_per_item != 0:
            self.driver.execute_script('document.getElementById("price-max").value = "' + str(max_cost_per_item) + '";')
            self.driver.find_element_by_xpath('//*[@id="price-max"]').send_keys(Keys.ENTER)

    def set_brands(self, wanted_brands):
        """
       Choosing brand in filtering as on the list.
       :param wanted_brands:
       :return:
       """
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/li[" + str(i) + "]/span")
                for brand in wanted_brands:
                    brand_web = sample.text.lower()
                    if brand.lower() in brand_web and brand_web not in already_selected:
                        # print(brand_web)
                        already_selected.append(brand_web)
                        try:
                            sample.click()
                        except ElementClickInterceptedException:
                            pass
                i += 1
            except NoSuchElementException:
                break

    def set_sizes(self, wanted_sizes):
        """
       Setting sizes in filtering as in the given list.
       :param wanted_sizes:
       :return:
       """
        i = 1
        already_selected = []
        while i:
            try:
                sample = self.driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/button[" + str(i) + "]")
                for given_size in wanted_sizes:
                    size_web = sample.text.upper()
                    if given_size == size_web and size_web not in already_selected:
                        # print(size_web)
                        already_selected.append(size_web)
                        sample.click()
                i += 1
            except NoSuchElementException:
                break

    def wait_for_popup(self):
        """
       Waits for popup and tries to close it.
       :return:
       """
        try:
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//div[contains(@class,"sizeOverlayDialog")]')))

            WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Mimo to zamawiam oba rozmiary"]'))).click()

            WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Potwierdź"]'))).click()
        except TimeoutException:

            WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
            self.wait_for_popup()

    def wait_for_atcButton(self, attempt, size):
        """
       Waiting till animation of adding item to shopping cart is finished or leaves error.
       :param attempt:
       :param size:
       :return:
       """
        try:
            WebDriverWait(self.driver, 2).until(ec.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
            WebDriverWait(self.driver, 2).until(ec.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))

            return True

        except TimeoutException:
            pass
            # print('Attempt: ', attempt)

            if attempt == 5:
                return False

            if attempt % 3 == 2:
                self.driver.refresh()
                WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]'))).click()

            # WebDriverWait(self.driver, 5).until(
            #     ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()

            button = WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]/div[1]/div[1]')))
            self.driver.execute_script("arguments[0].click();", button)

            if self.driver.find_element_by_xpath(
                    '//*[@id="addToCartButton"]/div[1]/div[2]/span').text != 'Proszę wybrać rozmiar':
                return False

            self.wait_for_atcButton(attempt + 1, size)

    def wait_login_error(self):
        """
       Tries to click log_in button after error in loging
       :return:
       """
        sleep(2)
        if len(self.driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button')) != 0:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button').click()
            self.wait_login_error()

    def change_acc(self, href, size):
        """
        Changing account after reaching max shopping cart
        :param href:
        :param size:
        :return:
        """
        print(self.iteration)
        print(len(self.accounts_list))
        self.iteration += 1
        if self.iteration == len(self.accounts_list):
            return True
        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//span[text() = "Konto"]'))).click()
        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Wyloguj")]'))).click()

        while True:
            if len(self.driver.find_elements_by_xpath('//span[contains(text(), "Zaloguj")]')) == 0:
                 sleep(2)
            else:
                break 

        WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Zaloguj")]'))).click()

        element = WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        cred = self.accounts_list[self.iteration].split()
        element.send_keys(cred[0])

        element = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(cred[1])

        element.submit()

        self.wait_login_error()

        self.driver.get(href)

        WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(
            (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]'))).click()
        return False

    def filter_event(self):
        """
       Filtering event in filters( categories, sizes , maxprice...)
       :return:
       """
        WebDriverWait(self.driver, 20).until(
            ec.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "filters")]')))
        i = 1
        WebDriverWait(self.driver, 15).until(
            ec.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/section/div[2]/nav/a[" + str(1) + "]")))
        while i:
            try:
                element = "/html/body/div[2]/div/div/section/div[2]/nav/a[" + str(i) + "]"
                sample = self.driver.find_element_by_xpath(element)
                i += 1
                if sample.text == 'ROZMIAR':
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

    def perform_login(self):
        """
       Logging to account, checks error, sends login,pwd
       :return:
       """
        # Wait for cookies banner and close it
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]'))).click()
                break
            except StaleElementReferenceException:
                pass
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
        # email
        element = WebDriverWait(self.driver, 25).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(self.email)
        # password
        element = WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(self.password)
        # logging in
        element.submit()
        self.wait_login_error()

    def get_filtered_hrefs(self, ind=29):
        """
       Gets all items as hrefs and filtering them with categories(given)
       :param ind:
       :return:
       """
        hrefs = []
        all_items = self.driver.find_elements_by_xpath("//div[starts-with(@id, 'article-')]/a")
        for item in all_items:
            href = item.get_attribute("href")
            item_parent = item.find_element_by_xpath("./..")
            item_description = item_parent.find_element_by_xpath('./div/div[1]').text
            if len(self.driver.find_elements_by_xpath('//a[@href="' + href[ind:] + '"]/div[3]')) == 0:
                if self.categories_list:
                    if any(category_name.lower() in item_description.lower() for category_name in self.categories_list):
                        hrefs.append(href)
                else:
                    hrefs.append(href)
        return hrefs

    def scroll_to_event(self):
        """
        Scroll down to selected event, move corsor on it and click 'go to'
        """
        self.campaign_id = 'campaign-' + self.campaign_id
        action = ActionChains(self.driver)
        first_campaign = WebDriverWait(self.driver, 120).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="' + self.campaign_id + '"]/div')))
        self.scroll_shim(first_campaign)
        action.move_to_element(first_campaign).perform()
        second_campaign = WebDriverWait(self.driver, 20).until(
            ec.presence_of_element_located(
                (By.XPATH, '//*[@id="' + self.campaign_id + '"]/div/div[1]/div/button/span')))
        action.move_to_element(second_campaign).perform()
        second_campaign.click()

    def iterate_over_items(self, hrefs, selected_sizes, total_items=0):
        """
       Went trough filtered hrefs and adding items to shopping cart
       :param hrefs:
       :param selected_sizes:
       :param total_items:
       :return:
       """
        for href in hrefs:
            self.driver.get(href)

            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.XPATH, "//div[starts-with(@class, 'ArticleSizestyles')]")))

            selected = 0

            if self.driver.find_element_by_xpath('//*[@id="addToCartButton"]/div[1]/div[2]/span').text != 'Proszę wybrać rozmiar':
                continue
               

            for size in selected_sizes:
                try:
                    element = WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable(
                        (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]')))
                except TimeoutException:
                    continue

                parent = element.find_element_by_xpath("./..")
                is_clickable = parent.value_of_css_property("color")
                amount = -1
                if is_clickable == 'rgb(53, 53, 53)':
                    try:
                        amount_span = parent.find_element_by_xpath('./span[2]')
                        amount = int(amount_span.text[-1:])
                        if amount > self.max_ammount:
                            amount = self.max_ammount
                    except NoSuchElementException:
                        amount = self.max_ammount

                    element.click()
                    selected = selected + 1

                    for x in range(int(amount)):
                        cur_items = 0
                        button = WebDriverWait(self.driver, 5).until(
                            ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]')))
                        button.click()

                        if selected == 2 and x == 0:
                            self.wait_for_popup()
                            WebDriverWait(self.driver, 20).until(ec.invisibility_of_element_located(
                                (By.XPATH, '//div[contains(@class,"styles___backdrop")]')))

                        if self.wait_for_atcButton(0, size):
                            total_items += 1
                            cur_items += 1
                            if total_items == 3:
                                total_items = 0
                                if x+1 == int(amount):
                                    selected = 0
                                if self.change_acc(href, size):
                                    print('KONIEC')
                                    if self.inform_email is not None:
                                       sendMail(self.inform_email, 'messages/normally_finished')
                                    return True # Koniec dodawania
                        
                        if(x+1 == amount and cur_items == 0 and selected ==1):
                            selected = 0
                        
                        

                       
        print('KONIEC')
        if self.inform_email is not None:
            sendMail(self.inform_email, 'messages/normally_finished')
        return True # Koniec dodawania

    def popup_finished(self):
        """
        Informs when bot finishing job.
        :return:
        """
        app = QApplication([])
        w = QWidget()
        w.setWindowTitle("Finish dialog")

        msg = QMessageBox()
        msg.setText("Bot finished job, checkout items in your shopping cart")
        msg.show()
        
        app.exec_()
        
    def work(self):
        """
       Starting bot job
       :return:
       """
        self.driver.get("https://www.zalando-lounge.pl")
        self.perform_login()
        self.scroll_to_event()
        self.filter_event()
        self.scroll_down()
        if (self.iterate_over_items(self.get_filtered_hrefs(), self.sizes_list)):
            self.popup_finished()


ShoppingBot(['piotrpopisgames@gmail.com testertest'], ['Koszula', 't-shirt'],
            ['M', 'L'], [], 'ZZO11GQ', 300, 1, 'piotrpopis@icloud.com', True, 0).work()
# ShoppingBot(['piotrpopisgames@gmail.com testertest', 'mtarka1337@gmail.com Azexs1998'], ['bluza'],
#       ['M', 'L'], [], 'ZZO0ZBU', 300, 2, 'piotrpopis@icloud.com', True, 0).work()
# ShoppingBot(["piotrpopisgames@gmail.com
# testertest", "mtarka1337@gmail.com Azexs1998"], ['koszula'], ['M','L'
# ], [], 'ZZO11GQ', 200, 2,'regqerg',False, 0).work()
# sample = self.driver.find_element_by_
# xpath("/html/body/div[2]/div/div/section/div[2]/div[1]/div/div/ul/li[" + str(i) + "]/span")
