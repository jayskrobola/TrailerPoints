from ebaysdk.shopping import Connection as shopping
from bs4 import BeautifulSoup

Keywords = input('Enter an item ID to search: ')
api = shopping(appid='JaySkrob-TrailerP-PRD-0e65090ee-840b0c33', config_file=None)
api_request = {'ItemID':Keywords}

response = api.execute('GetSingleItem', api_request)
soup = BeautifulSoup(response.content, 'lxml')

#print(soup)

#totalentries = int(soup.find('totalentries').text)
item = soup.find('item')

#print(item)

itemid = item.itemid.string
title = item.title.string.strip()
price = item.convertedcurrentprice.string
pic = item.pictureurl.string

print(itemid)
print(title)
print('$'+price)
print(pic)