from bs4 import BeautifulSoup
import requests

product_page = requests.get("https://store.treelocate.com/grass-reed-180cm-fr-uv-s4-tl2851")
if product_page.status_code != 200:
    print('error')

soup = BeautifulSoup(product_page.content, 'html.parser')
description = soup.find('dl', {'class': 'Details_table-list'}).get_text()
