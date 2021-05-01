# Market size: >1000 per month of top 10 seller


# direct generate from postman
import json
import requests
from datetime import datetime
import pandas as pd
from items import search_items, search_item_monitoring

import pdb

def main(search_items, page_start, page_end):

    search_by = 'relevancy' #'sales'


    for search_item in search_items:
        dfs_searchbar = []
        grass_time = datetime.now()
        for page_num in range(page_start, page_end*50, 50):
            df_searchbar = search_bar(grass_time, search_by, search_item, page_num)
            dfs_searchbar.append(df_searchbar)

        dfs_searchbar = pd.concat(dfs_searchbar)

        shop_ids = dfs_searchbar['shopid'].unique()

        dfs_shop_info = []
        for shop_id in shop_ids:
            df_shop_info = shop_info(grass_time,shop_id)
            dfs_shop_info.append(df_shop_info)

        dfs_shop_info = pd.concat(dfs_shop_info)

        dfs_searchbar.to_csv(f'../results/{search_item}.csv', index=False)
        dfs_shop_info.to_csv(f'../results/{search_item}_shop_info.csv', index=False)

    return 

def search_bar(grass_time, search_by, search_item, page_num):

    url = f"https://shopee.my/api/v4/search/search_items?by={search_by}&keyword={search_item}&limit=50&newest={page_num}&order=desc&page_type=search&version=2"

    payload={}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Shopee-Language': 'en',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc',
    'If-None-Match-': '55b03-2ff39563c299cbdc937f8ab86ef322ab',
    'DNT': '1',
    'Connection': 'keep-alive',
    'TE': 'Trailers'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.text

    df = search_bar_resposne_parse(response)
    df['created_on'] = datetime.now()
    df['grass_time'] = grass_time
    df['searsch_keywords'] = search_item
    df['search_type'] = search_by
    df['page_num'] = (page_num/50) + 1

    return df

def search_bar_resposne_parse(res):
    """
    A function to extract what we want
    """
    res = json.loads(res)
    items = res['items']

    df = pd.json_normalize(items)

    return df

def product_details(grass_time,item_id, shop_id):
    url = f"https://shopee.com.my/api/v2/item/get?itemid={item_id}&shopid={shop_id}"

    payload={}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Shopee-Language': 'en',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc',
    'If-None-Match-': '55b03-c6966dfc1b32ac0420c7aa87b0de1a61',
    'Connection': 'keep-alive',
    'Sec-GPC': '1',
    'If-None-Match': '771fe9e4fabafcd3c06808ebe640ad56',
    'TE': 'Trailers',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.text

    df = product_details_parse(response)
    df['created_on'] = datetime.now()
    df['grass_time'] = grass_time   

    return df

def product_details_parse(res):
    res = json.loads(res)
    items = res['item']

    df = pd.json_normalize(items)

    return df

def shop_info(grass_time, shop_id):
    url = f"https://shopee.com.my/api/v4/product/get_shop_info?shopid={shop_id}"

    payload={}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Shopee-Language': 'en',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc',
    'If-None-Match-': '55b03-37bbce88409985e577c12c337391ce3e',
    'Connection': 'keep-alive',
    'Sec-GPC': '1',
    'TE': 'Trailers',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.text

    df = shop_info_parse(response)
    df['created_on'] = datetime.now()
    df['grass_time'] = grass_time

    return df

def shop_info_parse(res):
    res = json.loads(res)
    data = res['data']

    try:
        df = pd.json_normalize(data)
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()


if __name__ == "__main__":
    main(search_item_monitoring, 0, 100)