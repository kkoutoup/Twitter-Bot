#data formatting function
#the way Twitter displays numbers will break excel calculations so numbers need to converted to the right format
#18.5K => 18500
#6,543 => 6543
#Currently unavailable => 0
#etc.
def format_number(data):
  if data == None or data == '':
    data = 'N/A'
  elif data == 'Currently unavailable':
    data = '0'
  elif data == '1K':
    data = '1000'
  elif data.endswith('K'):
    if'.' in data:
      data = (data[:-1].replace('.' , ''))+'00'
    else:
      data = data[:-1]+'000'
  elif ',' in data:
    data = data.replace(',' , '')
  else:
    data = data
  return data