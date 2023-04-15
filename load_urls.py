import requests
import xmltodict
from bs4 import BeautifulSoup
import csv
import time
import json
import certifi

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://jcrew-app:KICisfROhfIjfOC8@cluster0.9yvvojd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["jcrew_db"]
collection = db["products"]

print(client.list_database_names())


def __main__():
    with open('product_urls.csv', 'w') as csv_file:
        # header_names = ['name', 'id', 'listPrice']
        # writer = csv.DictWriter(csv_file, fieldnames=header_names)
        # writer.writeheader()
        num_products = 0
        products = list()
        # Loop through 6 pages of lists of product urls
        for i in range(1, 6):
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
                    collection.insert_one(product)
                    # writer.writerow(product)
                else:
                    print("Product Not Found")


def findEleById(soup, id):
    ele = soup.find(id=id)
    if ele:
        return ele.text


def createProductObj(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script = soup.find('script', id="__NEXT_DATA__")
    product = {}
    id = url[-5:]
    if script:
        json_data = json.loads(script.text)
        productList = json_data['props']['initialState']['products']['productsByProductCode']
        id_dict_key = list(productList.keys())[0]
        product_info = productList[id_dict_key]
        listPrice = product_info['listPrice']
        if listPrice is not None:
            product['listPrice'] = listPrice['amount']
        else:
            return None

    name = findEleById(soup, 'product-name__p')

    if name is None:
        print("product not found")
        return None
    desc = soup.find('p', attrs={'data-qaid': 'pdpProductDescriptionRomance'})
    if desc:
        print("desc " + desc.getText())
    else:
        print("desc not found")
    _id = url[-5:]
    product['desc'] = desc.getText()
    product['name'] = name
    product['_id'] = id

    return product


__main__()
