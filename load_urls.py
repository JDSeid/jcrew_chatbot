import requests
import xmltodict
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
import json
import pymongo

# driver = webdriver.Chrome()


# #Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["jcrew_db"]
# collection = db["products"]

# print(client.list_database_names())


def __main__():
    with open('product_urls.csv', 'w') as csv_file:
        header_names = ['name', 'id', 'listPrice', 'isSoldOut']
        writer = csv.DictWriter(csv_file, fieldnames=header_names)
        writer.writeheader()
        num_products = 0
        products = list()
        # Loop through 6 pages of lists of product urls
        for i in range(1, 2):
            product_list_url = "https://www.jcrew.com/sitemap-wex/sitemap-pdp{page_num}.xml".format(
                page_num=i)
            # product_list_url = product_list_url.format(page_num=i)
            response = requests.get(product_list_url)
            page_list = xmltodict.parse(response.content)['urlset']['url']
            for page in page_list:
                product = createProductObj(page['loc'])
                num_products += 1
                print("Num product " + str(num_products))
                if product is not None:
                    # collection.insert_one(product)
                    writer.writerow(product)
                else:
                    print("Product Not Found")


def findEleById(soup, id):
    ele = soup.find(id=id)
    if ele:
        return ele.text


def createProductObj(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    name = findEleById(soup, 'product-name__p')
    if name is None:
        print("product not found")
        return None
    id = url[-5:]
    product = {}
    product['name'] = name
    product['id'] = id
    script = soup.find('script', id="__NEXT_DATA__")
    if script:
        json_data = json.loads(script.text)
        productList = json_data['props']['initialState']['products']['productsByProductCode']
        id_dict_key = list(productList.keys())[0]
        product_info = productList[id_dict_key]
        listPrice = product_info['listPrice']
        if listPrice is not None:
            product['listPrice'] = listPrice
            product['isSoldOut'] = False
        else:
            product['listPrice'] = 'N/A'
            product['isSoldOut'] = True
    return product


__main__()
