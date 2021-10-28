from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import pickle
import time

# Cần chạy file get_cookies.py để tạo file cookies.pkl trước
# sau đó mới tiến hành chạy test case


class FacebookTest(unittest.TestCase):
    def setUp(self):
        option = Options()
        option.add_argument("start-maximized")

        # Tắt hỏi bật notification của facebook
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.get("https://facebook.com/")

        # Load cookies
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

        # Reload page
        self.driver.get("https://facebook.com/")

        self.driver.implicitly_wait(5)

    def test_gui_loi_moi_ket_ban(self):
        self.driver.get("https://www.facebook.com/friends/suggestions")
        first_add_friend_button = self.driver.find_element_by_css_selector(
            "div[aria-label='Thêm bạn bè']")

        first_add_friend_button.click()

        bodyText = self.driver.find_element_by_tag_name('body').text
        self.assertTrue("Đã gửi lời mời" in bodyText)

    def test_huy_ket_ban(self):
        self.driver.get("https://www.facebook.com/friends/list")

        current_friends_element = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'người bạn')]")

        old_friends = int(current_friends_element.text.split(" ")[0])

        xem_them_button = self.driver.find_element_by_css_selector(
            "div[aria-label='Xem thêm']")
        xem_them_button.click()

        time.sleep(1)
        huy_ket_ban_button = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Hủy kết bạn')]")
        huy_ket_ban_button.click()

        time.sleep(1)
        xac_nhan_button = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Xác nhận')]")
        xac_nhan_button.click()

        time.sleep(1)
        self.driver.get("https://www.facebook.com/friends/list")

        current_friends_element = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'người bạn')]")
        new_friends = int(current_friends_element.text.split(" ")[0])

        self.assertEqual(old_friends - 1, new_friends)

    def test_chan_ban_be(self):
        self.driver.get("https://www.facebook.com/friends/list")

        xem_them_button = self.driver.find_element_by_css_selector(
            "div[aria-label='Xem thêm']")
        time.sleep(2)
        xem_them_button.click()

        time.sleep(1)
        chan_button = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Chặn ')]")
        chan_button.click()

        time.sleep(1)
        friend_name_element = self.driver.find_element_by_xpath(
            "*//span[contains(text(), '?')]")

        blocked_friend = friend_name_element.text[5:-1]

        time.sleep(1)
        xac_nhan_button = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Xác nhận')]")
        xac_nhan_button.click()

        self.driver.get("https://www.facebook.com/settings?tab=blocking")

        oh_my_iframe = self.driver.find_element_by_xpath(
            "*//iframe[contains(@src,'https://www.facebook.com/settings?tab=blocking')]")
        self.driver.switch_to.frame(oh_my_iframe)

        list_blocked_friends = self.driver.find_elements_by_css_selector(
            "span.fcb")

        last_blocked_friend = list_blocked_friends[0].text

        self.assertEqual(blocked_friend, last_blocked_friend)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
