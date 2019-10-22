#check to see if the data we're after exists on the page and retrieve it. if the container element doesn't exist then return '0' instead of raising an exception. An exception costs us the rest of the data on the page we want.
def return_profile_visits(self):
  try:
    profile_visits = self.driver.find_elements_by_xpath('//h5[text()="%s Summary"]/following-sibling::div//div//div[@class="DataPoint-info metric-profile-views"]'%self.current_date)
    if profile_visits:
      return profile_visits[0].text
    else:
      return '0'
  except Exception as e:
    print(e)