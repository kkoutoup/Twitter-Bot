# check to see if the data we're after exists on the page and retrieve it. if the container element doesn't exist then return 0 instead of raising an exception. An exception costs us the rest of the data on the page we want.
def return_new_followers(self):
  try:
    new_followers = self.driver.find_elements_by_xpath('//h5[text()="%s Summary"]/../..//div[@class="DataPoint-info metric-followers"]'%self.month_year)
    if new_followers:
      return new_followers[0].text
    else:
      return '0'
  except Exception as e:
    print(e)
