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


db = client["jcrew_db"]
collection = db["products"]


def __main__():
    db.products.delete_many({})
    num_products = 0
    products = list()
    # Loop through 6 pages of lists of product urls
    for i in range(2, 6):
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
                try:
                    collection.insert_one(product)
                except:
                    pass
            else:
                print("Product Not Found")


def findEleById(soup, id):
    ele = soup.find(id=id)
    if ele:
        return ele.text


url = 'https://www.jcrew.com/p/womens/categories/clothing/blazers/lady-jacket/odette-sweater-lady-jacket-in-cotton-blend-boucleacute/BR789?display=standard&fit=Classic&color_name=kelly-green&colorProductCode=BR789'


def createProductObj(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script = soup.find('script', id="__NEXT_DATA__")
    found = soup.find_all('a', attrs={'href': "#BVRRWidgetID"})
    print(found)
    product = {}
    id = url[-5:]
    if script:
        json_data = json.loads(script.text)
        # file.write(json.dumps(json_data, indent=2))
        productList = json_data['props']['initialState']['products']['productsByProductCode']
        id_dict_key = list(productList.keys())[0]
        product_info = productList[id_dict_key]
        listPrice = product_info['listPrice']
        colorsList = product_info['colorsList']
        product['sizesList'] = list(product_info['sizesMap'].keys())
        priceModel = product_info['priceModel']
        if 'now' in priceModel:
            product['sale_price'] = priceModel['now']['amount']
            product['on_sale'] = True
        else:
            product['on_sale'] = False
        if listPrice is not None:
            product['list_price'] = listPrice['amount']
        else:
            return None
        if colorsList is not None:
            product['colors'] = list()
            colors = colorsList[0]['colors']
            for color in colors:
                product['colors'].append(
                    color['name'].lower().capitalize())

    name = findEleById(soup, 'product-name__p')

    if name is None:
        print("product not found")
        return None
    desc = soup.find(
        'p', attrs={'data-qaid': 'pdpProductDescriptionRomance'})
    if desc:
        product['desc'] = desc.getText()
    _id = url[-5:]

    product['name'] = name
    product['_id'] = id
    return product


createProductObj(url)
# __main__()
