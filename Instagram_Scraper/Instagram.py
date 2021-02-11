from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd
from time import sleep
import os


def login(driver):
    driver.maximize_window()

    url = 'https://www.instagram.com/accounts/login/'
    driver.get(url)

    driver.implicitly_wait(10)

    print('login Process Started')

    email = 'Your Email'
    email_xpath = """//*[@id="loginForm"]/div/div[1]/div/label/input"""
    find_email_element = driver.find_element_by_xpath(email_xpath)
    find_email_element.send_keys(email)

    driver.implicitly_wait(10)

    password = 'Your Password'
    password_xpath = """//*[@id="loginForm"]/div/div[2]/div/label/input"""
    find_password_element = driver.find_element_by_xpath(password_xpath)
    find_password_element.send_keys(password)
    find_password_element.send_keys(Keys.ENTER)
    print('Logged in Successfuly')


def insta_scrape(driver, account):

    Username_list = []
    Name_list = []
    Description_list = []
    No_of_followers = []
    No_of_following = []
    No_of_post = []

    print('Started Scraping Profiles Data')

    sleep(4)

    for profile in account:

        driver.get(profile)
        print()
        print(f"Collecting Data of {profile}")

        try:
            following = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span""")
            if following is None:
                No_of_following.append('No following')
            else:
                following_text = following.text
                No_of_following.append(following_text)
                print(following_text)

        except:
            following = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span""")
            if following is None:
                No_of_following.append('No following')
            else:
                following_text = following.text
                No_of_following.append(following_text)
                print(following_text)

        try:
            username2 = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/div[1]/h1""")
            if username2 is None:
                Username_list.append('No Username')
            else:
                username2_text = username2.text
                Username_list.append(username2_text)
                print(username2_text)
        except:
            username = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/div[1]/h2""")
            if username is None:
                Username_list.append('No Username')
            else:
                username_text = username.text
                Username_list.append(username_text)
                print(username_text)

        try:
            name = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/div[2]/h1""")
            name_text = name.text
            Name_list.append(name_text)
            print(name_text)
        except:
            Name_list.append('No Name Found')

        try:
            description = driver.find_element_by_xpath(
                """//*[@id="react-root"]/section/main/div/header/section/div[2]/span""")
            description_text = description.text
            Description_list.append(description_text)
            print(description_text)
        except:
            Description_list.append('No Description Found')

        try:
            followers_xpath = """//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/span/span"""
            followers = driver.find_element_by_xpath(followers_xpath)
            if followers is None:
                No_of_followers.append('No followers')
            else:
                followers_text = followers.text
                No_of_followers.append(followers_text)
                print(followers_text)
        except:
            followers_xpath = """//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span"""
            followers = driver.find_element_by_xpath(followers_xpath)
            if followers is None:
                No_of_followers.append('No followers')
            else:
                followers_text = followers.text
                No_of_followers.append(followers_text)
                print(followers_text)

        posts_xpath = """//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span"""
        posts = driver.find_element_by_xpath(posts_xpath)
        if posts is None:
            No_of_post.append('No Posts')
        else:
            posts_text = posts.text
            No_of_post.append(posts_text)
            print(posts_text)

        print('All Data Has Been Scraped of this User, Jumping to the Next User')

    curr_dir = os.getcwd()
    # in path replace \ with / (important)
    path = "path(folder) where you want to store the scraped data"
    os.chdir(path)
    data = {
        'Username': Username_list,
        'Name': Name_list,
        'Description': Description_list,
        'No_of_Followers': No_of_followers,
        'No_of_Following': No_of_following,
        'No_of_Posts': No_of_post
    }
    df = pd.DataFrame(data)
    df.to_csv("write here the name of master csv file with(.csv)", index=False)

    os.chdir(curr_dir)


if __name__ == "__main__":
    account = []

    # in path replace \ with / (important)
    with open("F:/CODE/Liz's Scripts/href_list.csv", 'r')as f:
        link_data = csv.reader(f)
        for row in link_data:
            for link in row:
                account.append(
                    ('https://www.instagram.com' + link).replace(" ", "_"))

    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument(
        "--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'")
    # in path replace \ with / (important)
    driver = webdriver.Chrome(
        options=opts, executable_path='C:/WebDrivers/chromedriver.exe')
    try:
        login(driver)
        insta_scrape(driver, account=account)
    finally:
        driver.quit()
