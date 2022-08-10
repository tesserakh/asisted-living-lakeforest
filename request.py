import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_name_datastore = 'data.csv'
npage = round(373/25)

def get_place(url):
    baseurl = 'https://www.aplaceformom.com'
    page = BeautifulSoup(requests.get(url).text, 'lxml')
    data = []
    items = page.find_all('section', {'data-au-id':'community-card'})
    for item in items:
        name = item.find('h3').text
        distance = float(item.find('p').find('span').find('span').text.replace(' miles', '').strip())
        link = baseurl+item.find('a', href = True)['href']
        data.append({
            'Name': name,
            'Distance': distance,
            'Link': link
        })

    for i in range(len(data)):
        profile = BeautifulSoup(requests.get(data[i]['Link']).text, 'lxml')
        address = profile.find('span', {'data-au-id':'community-subheading'}).text.strip()
        phone = profile.find('div', {'id':'community-sub-header'}).find_all('div')[3].find('a').text
        data[i].update({
            'Address': address,
            'Phone Number': phone
        })

    return data


alldata = []
for page in range(1, npage+1):
    url = f'https://www.aplaceformom.com/assisted-living/illinois/lake-forest/recommended/distance-50?destination-page={page}'
    print(f'Get from {url}')
    place = get_place(url)
    alldata += place

print(alldata)

df = pd.DataFrame(alldata)
df.to_csv(csv_name_datastore, index = False)
print(f'Data saved to {csv_name_datastore}')
