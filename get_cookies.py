from selenium import webdriver
import pickle
import time

# Nhập tài khoản mật khẩu ở đây để tạo cookies
USERNAME = ""
PASSWORD = ""


def get_cookies():
    driver = webdriver.Chrome()

    driver.get("https://facebook.com/")

    email_element = driver.find_element_by_id("email")
    email_element.send_keys(USERNAME)

    password_element = driver.find_element_by_id("pass")
    password_element.send_keys(PASSWORD)

    login_button = driver.find_element_by_name("login")
    login_button.click()

    time.sleep(2)

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    driver.quit()


if __name__ == "__main__":
    get_cookies()
