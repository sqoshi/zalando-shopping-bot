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


def sendMail(to, file):
    """
   Function to inform user about founded products by e-mail.
   :param to:
   :param file:
   :return:
   """
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('info.xxxxxx.bot@gmail.com', 'xxxxxxxxxxx')
    from_mail = 'info.xxxxxx.bot@gmail.com'
    body = (open(file, "r").read())
    message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % '' + "\r\n" + body)
    server.sendmail(from_mail, to, message)


def check_size_availability(parent):
    """
    Checks if button is avaible to click.
    :param parent:
    :return:
    """
    is_clickable = parent.value_of_css_property("color")
    if is_clickable == 'rgb(53, 53, 53)':
        return True
    return False


class ShoppingBot:

    def __init__(self, acc, cats, sizs, brds, cid, mpi, maa, mail, is_mail_checked, ite):
        options = Options()
        # options.add_argument("--disable-notifications")
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

    def wait_for_popup(self, attempt, size):
        """
       Waits for popup and tries to close it.
       :return:
       """
        try:
            WebDriverWait(self.driver, 3).until(
                ec.presence_of_element_located((By.XPATH, '//div[contains(@class,"sizeOverlayDialog")]')))
            WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Mimo to zamawiam oba rozmiary"]'))).click()
            WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Potwierdź"]'))).click()
            return True
        except TimeoutException:
            action = ActionChains(self.driver)
            if attempt % 3 == 2:
                self.deal_with_bug(action, size)
                return self.wait_for_popup(attempt + 1, size)
            else:
                if attempt == 3:
                    return False
                WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
                if self.driver.find_element_by_xpath(
                        '//*[@id="addToCartButton"]/div[1]/div[2]/span').text != 'Proszę wybrać rozmiar':
                    return False
                return self.wait_for_popup(attempt + 1, size)

    def wait_for_popup_single(self):
        """
       Waits for popup and tries to close it.
       :return:
       """
        try:
            WebDriverWait(self.driver, 3).until(
                ec.presence_of_element_located((By.XPATH, '//div[contains(@class,"sizeOverlayDialog")]')))
            WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Mimo to zamawiam oba rozmiary"]'))).click()
            WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable((By.XPATH, '//span[text() = "Potwierdź"]'))).click()
            return True
        except TimeoutException:
            return False

    def deal_with_bug(self, action, size):
        """
        Trying to click with action chain to deal with bug
        :param action:
        :param size:
        :return:
        """
        self.driver.refresh()
        button = WebDriverWait(self.driver, 3).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]')))
        cart = WebDriverWait(self.driver, 4).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="header-cart"]')))
        WebDriverWait(self.driver, 4).until(ec.element_to_be_clickable(
            (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]'))).click()
        action.move_to_element(cart)
        action.click(cart)
        action.perform()
        action.move_to_element(button)
        action.click(button)
        action.perform()

    def wait_acceptance_button(self, attempt, size, var):
        """
       Waiting till animation of adding item to shopping cart is finished or leaves error.
        :param var:
       :param attempt:
       :param size:
       :return:
       """
        try:
            WebDriverWait(self.driver, 3).until(ec.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "transf") ]')))
            WebDriverWait(self.driver, 3).until(ec.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "animation-ball") and starts-with(@style, "display: none;") ]')))
            return True
        except TimeoutException:
            print('atcBtn except:', attempt)
            action = ActionChains(self.driver)
            if attempt % 3 == 2:
                self.deal_with_bug(action, size)
                if var:
                    if self.wait_for_popup_single():
                        return True
                return self.wait_acceptance_button(attempt + 1, size, var)
            else:
                if attempt == 3:
                    return False
                WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]'))).click()
                if var:
                    if self.wait_for_popup_single():
                        return True
                if self.driver.find_element_by_xpath(
                        '//*[@id="addToCartButton"]/div[1]/div[2]/span').text != 'Proszę wybrać rozmiar':
                    return False
                return self.wait_acceptance_button(attempt + 1, size, var)

    def wait_login_error(self):
        """
       Tries to click log_in button after error in loging
       :return:
       """
        sleep(2)
        if len(self.driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button')) != 0:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/form/button').click()
            self.wait_login_error()

    def relog(self, href, size):
        """
        relog to next account
        :param href:
        :param size:
        :return:
        """
        WebDriverWait(self.driver, 15).until(
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

    def change_account(self, href, size):
        """
        Changing account after reaching max shopping cart
        :param href:
        :param size:
        :return:
        """
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
        sleep(1)
        self.relog(href, size)
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
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, '//*[@id=\"uc-btn-accept-banner\"]'))).click()
                break
            except StaleElementReferenceException:
                pass
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/button").click()
        element = WebDriverWait(self.driver, 25).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="form-email"]')))
        element.send_keys(self.email)
        element = WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="form-password"]')))
        element.send_keys(self.password)
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

    def check_amount(self, parent):
        """
        Setup amount for late operations.
        :param parent:
        :return:
        """
        amount = -1
        try:
            amount_span = parent.find_element_by_xpath('./span[2]')
            amount = int(amount_span.text[-1:])
            if amount > self.max_ammount:
                amount = self.max_ammount
        except NoSuchElementException:
            amount = self.max_ammount
        return amount

    def should_send_mail(self):
        """
        Check if should sen mail
        :return:
        """
        if self.inform_email is not None:
            sendMail(self.inform_email, 'messages/normally_finished')

    def break_barrier(self, size, total_items, cur_items):
        """
        Check condition wait acceptance
        :param size:
        :param total_items:
        :param cur_items:
        :return:
        """
        WebDriverWait(self.driver, 20).until(ec.invisibility_of_element_located(
            (By.XPATH, '//div[contains(@class,"styles___backdrop")]')))
        if self.wait_acceptance_button(0, size, True):
            total_items, cur_items = total_items + 1, cur_items + 1
        return total_items, cur_items

    def click_add_button(self):
        """
        Trying to click addCCartButton
        :return:
        """
        button = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.XPATH, '//*[@id="addToCartButton"]')))
        button.click()

    def iterate_amount(self, amount, selected, size, total_items, href, size_shopping_cart=5):
        """
        operated on opened href - checking bugs,adding amount times "same" item
        :param amount:
        :param selected:
        :param size:
        :param total_items:
        :param href:
        :param size_shopping_cart:
        :return:
        """
        for x in range(int(amount)):
            cur_items = 0
            self.click_add_button()

            if selected == 2 and x == 0:
                if self.wait_for_popup(0, size) is True:
                    total_items, cur_items = self.break_barrier(size, total_items, cur_items)
                else:
                    break
            else:
                if self.wait_acceptance_button(0, size, False) is True:
                    total_items, cur_items = total_items + 1, cur_items + 1
                else:
                    if x + 1 == amount and cur_items == 0 and selected == 1:
                        selected = 0
                    break
            if total_items == size_shopping_cart:
                total_items = 0
                if x + 1 == int(amount):
                    selected = 0
                if self.change_account(href, size):
                    self.should_send_mail()
                    return amount, selected, size, total_items, True
            if x + 1 == amount and cur_items == 0:
                selected -= 1
        return amount, selected, size, total_items, False

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
            if self.driver.find_element_by_xpath(
                    '//*[@id="addToCartButton"]/div[1]/div[2]/span').text != 'Proszę wybrać rozmiar':
                continue
            for size in selected_sizes:
                if selected == 2:
                    break
                try:
                    element = WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable(
                        (By.XPATH, '//span[contains(@class, "Size") and text()="' + size + '"]')))
                except TimeoutException:
                    continue
                parent = element.find_element_by_xpath("./..")
                if check_size_availability(parent):
                    amount = self.check_amount(parent)
                    element.click()
                    selected = selected + 1
                    amount, selected, size, total_items, flag = self.iterate_amount(amount, selected, size, total_items,
                                                                                    href)
                    if flag:
                        return True
        self.should_send_mail()
        return True

    def work(self):
        """
       Starting bot job
       //main loop
       :return:
       """
        self.driver.get("https://www.zalando-lounge.pl")
        self.perform_login()
        self.scroll_to_event()
        self.filter_event()
        self.scroll_down()
        self.iterate_over_items(self.get_filtered_hrefs(), self.sizes_list)
