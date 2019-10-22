#Dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from format_number import format_number
from return_mentions import return_mentions
from return_profile_visits import return_profile_visits
from return_new_followers import return_new_followers
from return_followers import return_followers
import time, os, csv

#TwitterBot
class TwitterBot:
  
  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.driver = webdriver.Chrome()
    self.page_urls = []
    self.data = []
    self.current_date = date.today().strftime('%b %Y')

  #create new folder to store data
  def create_new_folder(self):
    #calculcate previous month
    #tweet bot needs to collect data for previous month for monthly retrospective/presentations so folder for data should be named after previous month
    current_date = date.today()
    current_month = current_date.month
    current_year = current_date.year

    if current_month == 1:
      month_year = current_date.replace(month = 12, year = current_year-1).strftime('%b %Y')
    else:
      month_year = current_date.replace(month = current_month-1).strftime('%b %Y')

    #destination folder path / use this to store csv file
    self.new_folder_path = os.path.join(os.getcwd(), f"{month_year} Tweet Data")
    
    try:
      if not os.path.exists(self.new_folder_path):
        os.mkdir(self.new_folder_path)
        print("=> New folder created")
      else:
        print("=> Folder already exists")
    except Exception as e:
      print(e)

  #construct page urls for scraper using twitter handles
  def construct_page_urls(self):
    print('=> Constructing page urls')

    #this list should contain all twitter handles. placeholders used here
    twitter_handles = ['twitterhandle1', 'twitterhandle2', 'twitterhandle3']
    
    self.page_urls = [f"https://analytics.twitter.com/user/{item}/home" for item in twitter_handles]

  #login 
  def login(self):
    print("=> Visiting twitter.com")
    try:
      login_url = 'https://twitter.com'
      driver = self.driver
      driver.get(login_url)
      #using sleep to make sure page loads and 'NoSuchElement' exceptions are avoided
      time.sleep(3)
    except Exception as e:
      print(e)
    else:
      print('=> Logging into Twitter')
      time.sleep(3)
      #target username and password fiels and login
      username_field = driver.find_element_by_class_name('email-input')
      password_field = driver.find_element_by_name('session[password]')
      username_field.clear()
      password_field.clear()
      username_field.send_keys(self.username)
      password_field.send_keys(self.password)
      driver.find_element_by_class_name('js-submit').click()
      time.sleep(5)
  
  #switch to account overview page. This gives access to all individual twitter accounts
  def go_to_account_overview(self):  
    print("=> Switching to account overview page")
    driver = self.driver
    try:
      driver.find_elements_by_xpath('//div[@class="css-1dbjc4n"]')[8].click()
      time.sleep(3)
      driver.find_element_by_xpath('//div[@title="Analytics"]').click()
      time.sleep(3)
      #switch to new window and check window title
      driver.switch_to.window(driver.window_handles[1])
      assert "Twitter Analytics account overview" in driver.title
    except AssertionError:
      print("Error: This is not the account overview page")
    except Exception as e:
      print(e)
    else:
      time.sleep(2)
      #click on dropdown and select 'switch accounts'
      driver.find_element_by_link_text('link text').click()
      driver.find_element_by_id('switch-account-link').click()
      time.sleep(2)
      try:
        #making sure we're on the correct page
        assert "Select an account" in driver.title
      except AssertionError:
        print("Error: This is not the account selection page")
      else:    
        pass

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

  #write to csv and move csv in the output folder
  def write_to_csv(self):
    print("=> Putting everything in a cute csv your data analyst will love")
    try:
      with open('twitter-data.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, lineterminator = '\n')
        csv_writer.writerow(['Committee Name', 'Followers', 'Profile visits', 'Mentions', 'New followers'])
        for item in self.data:
          csv_writer.writerow([item[0], item[1], item[2], item[3], item[4]])
    except Exception as e:
      print(e)
    #move csv into folder
    current_path = os.getcwd()+f"\\twitter-data.csv"
    new_path = f"{self.new_folder_path}\\twitter-data.csv"
    os.rename(current_path, new_path)
    
  #close driver
  def close_driver(self):
    print("=> Closing driver...")
    self.driver.close()

#run sequence
wpu_bot = TwitterBot('username', 'password')
wpu_bot.create_new_folder()
wpu_bot.construct_page_urls()
wpu_bot.login()
wpu_bot.go_to_account_overview()
wpu_bot.collect_data()
wpu_bot.write_to_csv()
wpu_bot.close_driver()