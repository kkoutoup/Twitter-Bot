# Dependencies
import time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import date

# Local Dependencies
from format_number import format_number
from return_mentions import return_mentions
from return_profile_visits import return_profile_visits
from return_new_followers import return_new_followers
from return_followers import return_followers
from create_csv import create_csv

# TwitterBot
class TwitterBot:
  
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.chrome_options = Options()
    self.chrome_options.add_argument("--start-maximized")
    self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
    self.page_urls = []
    self.data = []

  # create new folder to store data
  def create_new_folder(self):
    # calculcate previous month
    # tweet bot needs to collect data for previous month for monthly retrospective/presentations so folder for data should be named after previous month
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year

    if current_month == 1:
      self.month_year = current_date.replace(month = 12, year = current_year-1).strftime('%b %Y')
      self.full_month_year = current_date.replace(month = 12, year = current_year-1).strftime('%B %Y')
    else:
      self.month_year = current_date.replace(month = current_month-1).strftime('%b %Y')
      self.full_month_year = current_date.replace(month = current_month-1).strftime('%B %Y')

    # destination folder path / use this to store csv file
    self.new_folder_path = os.path.join(os.getcwd(), f"{self.month_year} Tweet Data")
    
    try:
      if not os.path.exists(self.new_folder_path):
        os.mkdir(self.new_folder_path)
        print("=> New folder created")
      else:
        print("=> Folder already exists")
    except Exception as e:
      print(e)

  # construct page urls for scraper using twitter handles
  def construct_page_urls(self):
    print('=> Constructing page urls')

    # this list should contain all twitter handles. placeholders used here
    twitter_handles = ['twitterhandle1','twitterhandle2','twitterhandle3']
    
    self.page_urls = [f"https://analytics.twitter.com/user/{item}/home" for item in twitter_handles]

  # login 
  def login(self):
    print("=> Visiting twitter.com")
    try:
      login_url = 'https://twitter.com'
      driver = self.driver
      driver.get(login_url)
      # using sleep to make sure page loads and 'NoSuchElement' exceptions are avoided
      time.sleep(3)
    except Exception as e:
      print(e)
    else:
      print('=> Logging into Twitter')
      time.sleep(3)
      # target username and password fiels and login
      username_field = driver.find_element_by_class_name('email-input')
      password_field = driver.find_element_by_name('session[password]')
      username_field.clear()
      password_field.clear()
      username_field.send_keys(self.username)
      password_field.send_keys(self.password)
      driver.find_element_by_class_name('js-submit').click()
      time.sleep(5)

  #loop through accounts and collect data
  def collect_data(self):
    #uses return_mentions, return_profile_visits, return_new_followers, return_followers imports
    print("=> Collecting data")
    for item in self.page_urls:
      driver = self.driver
      driver.get(item)
      time.sleep(4)
      #data container
      committee_data_list = []
      #collect and format data  
      try:
        committee_name = driver.find_element_by_class_name('ProfileHeader-screenName').text[1:]

        #if the script is run on the 1st of the month the stats appear at the top of the page. if not the browser needs to scroll down a bit for dynamic loading of data to happen.
        self.driver.execute_script("window.scrollBy(0,1800)")
        time.sleep(4)

        followers = return_followers(self)
        formatted_followers = format_number(followers)
        
        profile_visits = return_profile_visits(self)
        formatted_profile_visits = format_number(profile_visits)

        mentions = return_mentions(self)
        formatted_mentions = format_number(mentions)        

        new_followers = return_new_followers(self)
        formatted_new_followers = format_number(new_followers)
        
        committee_data_list.extend([committee_name, formatted_followers, formatted_profile_visits, formatted_mentions, formatted_new_followers])
      except Exception as e:
        print(e)
        pass
      else:
        self.data.append(committee_data_list)

  # write to csv and move csv in the output folder
  def write_to_csv(self):
    # checks if file exists and asks for user input
    current_path = os.getcwd()+f"\\twitter-data.csv"
    new_path = f"{self.new_folder_path}\\twitter-data.csv"
    if os.path.exists(new_path):
      while True:
        user_input = input("The file already exists. Would you like to replace it? Y/N: ")
        if user_input.lower() == 'n':
          print("=> Didn\'t produce new csv file. Exiting now...")
          return
        elif user_input.lower() == 'y':
          os.remove(new_path)
          new_csv = create_csv(self)
          os.rename(current_path, new_path)
          print("=> File replaced")
          break
    else:
      new_csv = create_csv(self)
      os.rename(current_path, new_path)
      print("=> csv file saved")

    # switch to main window  
    time.sleep(2)

  # collect video data
  def collect_video_data(self):
    print("=> Downloading video data")
    for item in self.page_urls:
      try:
        self.driver.get(item)
        time.sleep(4)
        # click on dropdown and select videos page link
        self.driver.find_elements_by_xpath('//ul[@class = "SharedNavBar-navGroup"]//li')[4].click()
        self.driver.find_elements_by_xpath('//ul[@class = "SharedNavBar-navGroup"]//li')[5].click()
        time.sleep(4)
        # set date_range
        self.driver.find_element_by_id('daterange-button').click() 
        time.sleep(4)
        self.driver.find_element_by_xpath('//li[text() = "%s"]'%self.full_month_year).click()
        time.sleep(4)
        download_csv_button = self.driver.find_element_by_xpath('//button[@class = "btn btn-default ladda-button"]')
        # if element is clickable download video data .csv
        if download_csv_button.is_enabled():
          try:
            download_csv_button.click()
            time.sleep(2)
            self.driver.find_element_by_xpath('//button[@data-type = "by_video"]').click()
            time.sleep(2)
            # give the operation a 15" window to complete, otherwise throw timeout exception
            wait = WebDriverWait(self.driver, 15)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "btn btn-default ladda-button"]')))
          except TimeoutException:
            print(f"Operation timed out at {self.driver.current_url}. Moving to next page.")
          finally:
            pass
        else:
          print(f"No video data for {self.driver.current_url}")
      except Exception as e:
        print(e)
    
  # collect tweet data
  def collect_tweet_data(self):
    print("=> Downloading tweet data")
    for item in self.page_urls:
      try:
        driver = self.driver
        driver.get(item)
        time.sleep(4)
        # click on dropdown and select tweets page link
        driver.find_elements_by_xpath('//ul[@class="SharedNavBar-navGroup"]//li')[1].click()
        time.sleep(4)
        # set date_range
        driver.find_element_by_id('daterange-button').click() 
        time.sleep(4)
        driver.find_element_by_xpath('//li[text() = "%s"]'%self.full_month_year).click()
        time.sleep(4)
        download_csv_button = driver.find_element_by_xpath('//button[@class = "btn btn-default ladda-button"]')
        # if element is clickable download tweet data .csv
        if download_csv_button.is_enabled():
          try:
            download_csv_button.click()
            time.sleep(2)
            driver.find_element_by_xpath('//button[@data-type = "by_tweet"]').click()
            time.sleep(2)
            # give the operation a 30" window to complete, otherwise throw timeout exception
            wait = WebDriverWait(driver, 30)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "btn btn-default ladda-button"]')))
          except TimeoutException:
            print(f"Operation timed out at {self.driver.current_url}. Moving to next page.")
          finally:
            pass
        else:
          print(f"No tweet data for {self.driver.current_url}")
      except Exception as e:
        print(e)

# run sequence
wpu_bot = TwitterBot('username', 'password')
wpu_bot.create_new_folder()
wpu_bot.construct_page_urls()
wpu_bot.login()
wpu_bot.collect_data()
wpu_bot.write_to_csv()
wpu_bot.collect_video_data()
wpu_bot.collect_tweet_data()
