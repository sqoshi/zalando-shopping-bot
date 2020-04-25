# login piotrpopisgames@gmail.com
# testertest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


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

        #self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/form/fieldset/button/span").click()
        #self.driver.find_element_by_class_name('sc-bxivhb kMEQZP')
        self.driver.find_element_by_tag_name('button').click()

        sleep(3)

        try:
            campaign_id = 'campaign-ZZO119M'
            action = ActionChains(self.driver)
            first_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div')
            action.move_to_element(first_compaing).perform()
            second_compaing = self.driver.find_element_by_xpath('//*[@id="'+campaign_id+'"]/div/div[1]/div/button/span')
            action.move_to_element(second_compaing).perform()
            second_compaing.click()
        except Exception as e:
            print('błąd '+ str(e))
            self.driver.quit


        # size_select = 'M'
        # click_size = self.driver.find_element_by_xpath('//*[@id="inner-wrapper"]/section/div[2]/nav/a[2]/span')
        # if size_select != '':
        #     click_size.click()
        #     sleep(1)
        #     set_size = self.driver.find_element_by_xpath('//*[@id="'+size_select+'"]').click()
        #     sleep(1)


Bot("piotrpopisgames@gmail.com", 'testertest')
