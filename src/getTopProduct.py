# Market size: >1000 per month of top 10 seller


# direct generate from postman
import json
import requests
import pandas as pd

import pdb

def main():
    search_items = [
        "airpods%20pro%20case"
    ]

    dfs = []
    for search_item in search_items:
        df = search_bar(search_item)
        dfs.append(df)
    
    results = pd.concat(dfs)
    results.to_csv('../results/first_page_results.csv')
    return results

def search_bar(search_item):

    url = f"https://shopee.sg/api/v4/search/search_items?by=relevancy&keyword={search_item}&limit=50&newest=0&order=desc&page_type=search&version=2"

    payload={}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://shopee.sg/search?keyword=airpods%20pro%20case&trackingId=searchhint-1619268926-56ed35dc-a4fc-11eb-b9bc-d094668303d8',
    'X-Shopee-Language': 'en',
    'X-Requested-With': 'XMLHttpRequest',
    'X-API-SOURCE': 'pc',
    'If-None-Match-': '55b03-2ff39563c299cbdc937f8ab86ef322ab',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Cookie': '_gcl_au=1.1.1541528277.1619268921; csrftoken=BDEnCqVSn3exML2Tx3OpBmd1JXYVlaLN; REC_T_ID=53dee72f-a4fc-11eb-a268-b4969132e9d2; SPC_SI=bfftocsg4.E6fvwqs9IjIwnGK0tn99PLhrLlYmToRd; _ga_4572B3WZ33=GS1.1.1619268921.1.1.1619269033.60; _ga=GA1.1.1007393196.1619268921; SPC_F=34pe4M2981UtC6mes4Xx5V51wDJvpAQu; SPC_R_T_ID="n800gn4Iy7G27T+AriKFTAoYoobSollx1WmzujS0hmLGFh/5tzRm1+Oymy7MPYf9MAUoboi6jBr+fH4gbGZgRklK4YoA62tItp04b5x4wpg="; SPC_IA=-1; SPC_EC=-; SPC_T_ID="n800gn4Iy7G27T+AriKFTAoYoobSollx1WmzujS0hmLGFh/5tzRm1+Oymy7MPYf9MAUoboi6jBr+fH4gbGZgRklK4YoA62tItp04b5x4wpg="; SPC_R_T_IV="b3i2bXUt1wUhKzY2QncjAA=="; SPC_U=-; SPC_T_IV="b3i2bXUt1wUhKzY2QncjAA=="; welcomePkgShown=true; SPC_SI=bfftocsg4.E6fvwqs9IjIwnGK0tn99PLhrLlYmToRd',
    'TE': 'Trailers'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.text

    df = search_bar_resposne_parse(response)

    return df

def search_bar_resposne_parse(res):
    """
    A function to extract what we want
    """
    res = json.loads(res)
    items = res['items']

    df = pd.json_normalize(items)
    pdb.set_trace()

    return df

if __name__ == "__main__":
    main()