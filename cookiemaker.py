from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time


class Cookiemake:
    def __init__(self):
        self.driver = None
        self.naver = "https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/"
        self.data = None


    def wait_for(self, el_type, element):
        while True:
            try:
                if el_type == "ID":
                    self.driver.find_element(By.ID, element)
                elif el_type == "XPATH":
                    self.driver.find_element(By.XPATH, element)
                elif el_type == "NAME":
                    self.driver.find_element(By.NAME, element)
                elif el_type == "CLASS_NAME":
                    self.driver.find_element(By.CLASS_NAME, element)
                time.sleep(0.1)
            except:
                break

    def wait_for_second(self, el_type, element):
        num = 0
        while True:
            try:
                if el_type == "ID":
                    self.driver.find_element(By.ID, element)
                elif el_type == "XPATH":
                    self.driver.find_element(By.XPATH, element)
                elif el_type == "NAME":
                    self.driver.find_element(By.NAME, element)
                elif el_type == "CLASS_NAME":
                    self.driver.find_element(By.CLASS_NAME, element)
                return False
            except:
                if num == 100:
                    return True
                else:
                    num=num+1
                    time.sleep(0.1)
                    pass

    def save(self, data, type):
        pickle.dump(data, open(f'{type}.pv', 'wb'), pickle.HIGHEST_PROTOCOL)

    def load(self, type):
        return pickle.load(open(f'{type}.pv', 'rb'))

    def driver_setting(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def naver_cookie(self):
        try:
            cookie = self.load("N")
        except:
            self.driver = self.driver_setting()
            self.driver.get("https://www.naver.com")
            self.driver.maximize_window()
            self.driver.delete_all_cookies()
            self.driver.get(self.naver)
            self.driver.find_element(By.CLASS_NAME, "keep_text").click()
            while True:
                if self.driver.current_url == "https://www.naver.com" or self.driver.current_url == "https://www.naver.com/":
                    while True:
                        if "my-iframe" in self.driver.page_source:
                            break
                        else:
                            pass
                    break
                else:
                    pass
            time.sleep(1)
            cookie = self.driver.get_cookies()
            # print(cookie)

            self.driver.close()
            self.driver.quit()


            self.save(cookie, "N")
        return cookie

