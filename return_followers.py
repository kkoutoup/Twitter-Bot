#check to see if the data we're after exists on the page and retrieve it. if the container element doesn't exist then return 0 instead of raising an exception. An exception costs us the rest of the data on the page we want.
def return_followers(self):
  try:
    followers = self.driver.find_element_by_xpath('//div[text()="Followers"]/following-sibling::div')
    if followers:
      return followers.text.split(" ")[0]
    else:
      return '0'
  except Exception as e:
    print(e)