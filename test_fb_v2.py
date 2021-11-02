from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import pickle
import time


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

    def test_gui_loi_moi_ket_ban_KB1(self):
        self.driver.get(
            "https://www.facebook.com/profile.php?id=100057086702583")

        ket_ban_btn = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Thêm bạn bè')]")

        ket_ban_btn.click()
        time.sleep(2)

        self.assertEqual(ket_ban_btn.text, "Hủy lời mời")

    def test_gui_loi_moi_ket_ban_KB4(self):
        self.driver.get(
            "https://www.facebook.com/profile.php?id=100074136751652")

        # Nếu đã kết bạn rồi thì sẽ không tìm thấy button "Thêm bạn bè"
        ket_ban_elements = self.driver.find_elements_by_xpath(
            "*//span[contains(text(), 'Thêm bạn bè')]")

        self.assertEqual(len(ket_ban_elements), 0)

    def test_huy_ket_ban_HKB1(self):
        self.driver.get(
            "https://www.facebook.com/profile.php?id=100072606127810")

        # Nếu đã kết bạn rồi thì sẽ không tìm thấy button "Thêm bạn bè"
        ban_be_btn = self.driver.find_element_by_xpath(
            "*//span/span[contains(text(), 'Bạn bè')]")
        ban_be_btn.click()

        time.sleep(1)
        huy_ket_ban_btn = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Hủy kết bạn')]")

        time.sleep(2)
        huy_ket_ban_btn.click()

        time.sleep(2)
        xac_nhan_btn = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Xác nhận')]")
        xac_nhan_btn.click()

        time.sleep(1)
        ket_ban_elements = self.driver.find_elements_by_xpath(
            "*//span[contains(text(), 'Thêm bạn bè')]")  # tìm tất cả các element có "Thêm bạn bè"
        self.assertGreater(len(ket_ban_elements), 0)  # Có button Thêm bạn bè

    def test_huy_ket_ban_HKB2(self):
        self.driver.get(
            "https://www.facebook.com/ly.em.9250")

        ket_ban_elements = self.driver.find_elements_by_xpath(
            "*//span[contains(text(), 'Thêm bạn bè')]")
        self.assertEqual(len(ket_ban_elements), 2)  # Có 2 button Thêm bạn bè

    def test_chan_nguoi_dung_C1(self):
        self.driver.get(
            "https://www.facebook.com/profile.php?id=100054531253847")

        ho_ten = self.driver.find_element_by_xpath(
            "*//div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/div/div/span/h1").text

        xem_them = self.driver.find_element_by_css_selector(
            'div[aria-label="Xem thêm"]')
        xem_them.click()

        time.sleep(3)
        chan_btn = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Chặn')]")
        chan_btn.click()

        time.sleep(2)
        xac_nhan_btn = self.driver.find_element_by_xpath(
            "*//span[contains(text(), 'Xác nhận')]")
        xac_nhan_btn.click()

        self.driver.get("https://www.facebook.com/settings?tab=blocking")

        oh_my_iframe = self.driver.find_element_by_xpath(
            "*//iframe[contains(@src,'https://www.facebook.com/settings?tab=blocking')]")
        self.driver.switch_to.frame(oh_my_iframe)

        list_blocked_friends = self.driver.find_elements_by_css_selector(
            "span.fcb")

        last_blocked_friend = list_blocked_friends[0].text

        self.assertEqual(ho_ten, last_blocked_friend)

    def test_chan_nguoi_dung_C2(self):
        self.driver.get(
            "https://www.facebook.com/profile.php?id=100054531253847")

        dem = len(self.driver.find_elements_by_xpath(
            "*//span[contains(text(), 'Bạn hiện không xem được nội dung này')]"))

        self.assertGreater(dem, 0)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
