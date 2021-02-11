import itertools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from explicit import waiter, XPATH
import pandas as pd
from time import sleep


def login(driver):
    driver.maximize_window()

    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)

    print('login Process Started')
    sleep(3)

    email = 'Your Email'
    email_xpath = """//*[@id="loginForm"]/div/div[1]/div/label/input"""
    find_email_element = driver.find_element_by_xpath(email_xpath)
    find_email_element.send_keys(email)

    sleep(3)

    password = 'Your Password'
    password_xpath = """//*[@id="loginForm"]/div/div[2]/div/label/input"""
    find_password_element = driver.find_element_by_xpath(password_xpath)
    find_password_element.send_keys(password)
    sleep(3)
    find_password_element.send_keys(Keys.ENTER)
    print('Logged In Successfuly')

    sleep(6)


def insta_scrape(driver, account):
    print('Started Scraping URLs')
    for profile in account:
        href_list = []
        driver.get("https://www.instagram.com/{0}/".format(profile))
        sleep(10)
        driver.find_element_by_partial_link_text("follower").click()
        waiter.find_element(driver, "//div[@role='dialog']", by=XPATH)

        try:
            follower_css = "ul div li:nth-child({}) a.notranslate"
            for group in itertools.count(start=1, step=12):
                for follower_index in range(group, group + 12):
                    get_href = waiter.find_element(
                        driver, follower_css.format(follower_index)).text
                    name = get_href.replace('_', ' ')
                    href_list.append('/'+name+'/')
                    data = {'Links': href_list}
                    df = pd.DataFrame(data)
                    df.to_csv('href_list.csv', index=False)
                    yield name
                last_follower = waiter.find_element(
                    driver, follower_css.format(group + 11))
                driver.execute_script(
                    "arguments[0].scrollIntoView();", last_follower)
        except:
            print('Scraping Done')


if __name__ == "__main__":
    account = []

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument(
        "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'")
    driver = webdriver.Chrome(
        options=opts, executable_path='C:/WebDrivers/chromedriver.exe')

    try:
        login(driver)
        print('Followers of the "{}" account'.format(account))
        for count, follower in enumerate(insta_scrape(driver, account=account), 1):
            print("\t{:>3}: {}".format(count, follower))
    finally:
        driver.quit()
