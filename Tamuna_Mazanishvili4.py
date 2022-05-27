from bs4 import BeautifulSoup
import requests
import csv
import time
import random

f = open('vinyl.csv', 'w', encoding="utf-8_sig", newline='\n')
f_obj = csv.writer(f)
f_obj.writerow(['Title', 'Condition', 'Price', 'Detailed_shipping', 'Total'])
for page in range(1, 5):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=vinyl&_pgn={page}'
    res = requests.get(url)
    soup_all = BeautifulSoup(res.text, 'html.parser')

    soup = soup_all.find('ul', class_='srp-results srp-list clearfix')

    all_items = soup.find_all('li', class_='s-item s-item__pl-on-bottom s-item--watch-at-corner')
    for item in all_items:
        title = item.find('h3', class_='s-item__title').text
        condition = item.find('span', class_='SECONDARY_INFO').text
        price = item.find('span', class_='s-item__price').text
        shipping = item.find('span', class_='s-item__shipping s-item__logisticsCost').text
        location = item.find('span', class_='s-item__location s-item__itemLocation').text
        pr = price.replace('$', '')
        pr = pr.replace(',', '')
        pr = pr.replace(' ', '')
        if shipping == 'Shipping not specified' or shipping =='Free International Shipping':
            sh = 0
        else:
            sh = shipping.replace('+$', '')
            sh = sh.replace(' shipping', '')
            sh = sh.replace(',', '')

        detailed_shipping = f"+${sh} {location}"

        total = float(pr) + float(sh)
        total = round(total, 2)
        f_obj.writerow([title, condition, price, detailed_shipping, total])
    time.sleep(random.randint(15, 20))

f.close()



