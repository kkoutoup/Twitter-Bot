# create csv
def create_csv(self):
  import csv
  try:
    with open('twitter-data.csv', 'w') as csv_file:
      csv_writer = csv.writer(csv_file, lineterminator = '\n')
      csv_writer.writerow(['Committee Name', 'Followers', 'Profile visits', 'Mentions', 'New followers'])
      for item in self.data:
        csv_writer.writerow([item[0], item[1], item[2], item[3], item[4]])
  except Exception as e:
    print(e)
