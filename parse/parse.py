import requests
import shutil
import re
from random import randint
from time import sleep
from tqdm import tqdm
import json
from bs4 import BeautifulSoup

def parse_branches(base):
    store_info = {}

    main_page = requests.get(base)
    main = BeautifulSoup(main_page.text, 'html.parser')

    title = main.title.text

    print('\r' + title, end='', flush=True)

    if title == "404 Not Found":
        return title, -1
    else:
        store_info["url"] = base
        store_info["title"] = title
        address = main.find("p", 'branch-address').text
        store_info["address"] = address
        meta = main.find_all('meta')
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == "description":
                store_info["description"] = tag.attrs['content']

            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() == "keywords":
                store_info["keywords"] = tag.attrs['content']

        return title, store_info

stores = []

for i in range(10000):
    base_url = "https://www.myfunnow.com/zh-tw/branches/" + str(i)
    title, store_info = parse_branches(base_url)

    print('\r' + f"{i}/10000 = {title}", end='', flush=True)
    
    if title != "404 Not Found":
        stores.append(store_info)
    
    if (i+1) % 100 == 0:
        with open('./stores.json', 'w', encoding='utf-8') as f:
            json.dump(stores, f, ensure_ascii=False, indent=4)
