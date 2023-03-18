import requests
import json
import logging
import math
import time
import numpy
from fake_useragent import UserAgent
import csv
import datetime


def login():
    request_login = requests.post(tree_locate_graph, data=raw_login, headers=headers)

    if (request_login.status_code != 200):
        logging.info(f'Login ERROR, status code {request_login.status_code}')
        exit()
    else:
        bearer_token = json.loads(request_login.text)['data']['profile']['login']['token']['value']
        headers['Authorization'] = f'Bearer {bearer_token}'
        logging.info(f'Login successful')


def search_more_images(original_image):
    image_counter = 1
    images_found = []

    if original_image:
        original_image = "https://store.treelocate.com" + original_image
        while True:
            image = original_image.replace("_1", f"_{image_counter}")
            if (requests.head(image, headers=headers, timeout=10).status_code == 200):
                images_found.append(image)
                image_counter += 1
            else:
                break

    return images_found


def split_dict(input_dict: dict, num_parts: int) -> list:
    list_len: int = len(input_dict)
    return [dict(list(input_dict.items())[i * list_len // num_parts:(i + 1) * list_len // num_parts])
        for i in range(num_parts)]


if __name__ == '__main__':
    start_time = time.time()
    ua = UserAgent()
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    tree_locate_graph = 'https://store.treelocate.com/api/graph'
    products_per_page = 18
    run_every_x_hours = 6
    sleep_interval = 15
    categories = [
        "c4830e60-65ec-4d2a-84bf-90d01f03c5a5",
        "b0d74de4-8274-4e8c-bc3a-6b6d159cc7df",
        "a9c6043d-28e8-41fb-a639-d231047468c4",
        "084f614d-9786-4542-bca2-1eafb75f7338",
        "366508ba-84c1-4bab-8c46-f3b3c0735781",
        "fb2162ea-71d2-4200-b18f-82fa4eab9a71",
        "50b4457d-9f7c-4f0b-bb41-b4580382a784",
        "2fd200e4-d507-4e8d-bb32-ee05a253c6bd",
        "20bd32e6-a757-40e7-a71d-350f97f2d45e",
        "028d1118-6cff-4ae6-8066-a3c01059a570",
        "40d063a2-4917-4522-9dc9-97ad3b7d97b2",
        "d493cb80-0ed0-4543-b1dd-1367114a0e43",
        "ec520d06-6bad-4bb4-bfac-94072051f0a3",
        "e3337897-d75f-4edf-a4d9-38a462de3c39",
        "13f0cc99-d47d-4db8-8a4b-f2916300097b",
        "607c8b76-a53c-4a86-9789-e16c39566be3",
    ]

    while True:
        products = {}
        random_user_agent = ua.random
        logging.info(f'User agent {random_user_agent}')
        headers = {
            'Host': 'store.treelocate.com',
            'Content-Type': 'text/plain',
            'User-Agent': random_user_agent
        }

        raw_login = "{\"query\":\" mutation Login($input:LoginInput!,$keys:[UserAbilityKey!]!){ profile{ login(input:$input){ token{value expiration:sessionExpiration}failureText @toVariable(name:\\\"failTxt\\\") } }viewer{  id name shopAccountType referenceId:accountReferenceId oneToMany role customerType isImpersonating currencyId pricesInclTax  customer{ id email name phone isValid }  abilities(keys:$keys) @whenEquals(variable:\\\"failTxt\\\", value: null){ key state } } }\",\"variables\":{\"input\":{\"email\":\"support@green4life.co.uk\",\"password\":\"TreeC05153\",\"persistent\":false},\"keys\":[\"VIEW_CATALOG\",\"VIEW_PRICES\",\"VIEW_STOCK\",\"VIEW_UNIT_OF_MEASURE\",\"VIEW_PRODUCT_SUGGESTIONS\",\"VIEW_MY_ACCOUNT_PAGE\",\"ORDER_PRODUCTS\",\"SUBMIT_ORDER\",\"CREATE_QUOTE\",\"COMPARE_PRODUCTS\",\"SUBSCRIBE_TO_NEWSLETTER\",\"USE_ORDER_TEMPLATES\"]}}\n"
        raw_category_list = "{\"query\":\" query ProductListPage( $id:ID!, $options:ProductListPageProductsLoadOptions!, $loadLargeImages:Boolean!, $loadCategories:Boolean=false, ){ pages{ productList(id:$id){ metaTitle metaDescription pageTitle description preset@toVariable(name:\\\"preset\\\") products(options:$options){ products{  id title image{ small mediumSmall large @include(if:$loadLargeImages) } url hasVariants uom{id} uoms{ id description@requireAbility(ability:VIEW_UNIT_OF_MEASURE) minimumQuantity maximumQuantity defaultQuantity quantityStep } stockLevels{ outOfStock lowStock maxStockNumber } specifications(filter:FOR_LIST){ key value  } categoriesPaths @include(if:$loadCategories){ categories{name} }  variantComponentGroups@whenEquals(variable:\\\"preset\\\",value:\\\"ListB2B\\\"){ id } }  facets{ items{ name title displayType ... on RangeFacet{ fieldType minValue maxValue } ... on ListFacet{ sortDescending crawlable values{ title textTitle count value selected } } } multiSelect } totalCount } defaultSorting{ field ascending } sortingEnabled defaultViewMode viewModeSwitchEnabled showThumbnails pagingType backgroundColor backgroundImage headerContent{...rows} footerContent{...rows} } } }fragment rows on RowContentElement{ id fullWidth background{ color desktopImage mobileImage imageAltText video fullWidth hideImageOnMobile alignment } border{ color radius style width } spacing{ margin padding hideSpaces } rowAnimation verticalAlignment attributes{ id className } minHeight{ desktop mobile tablet } heroEffect{ altLogo altSmallLogo headerOnTop headerTextColor showScrolldownIcon mutedSound imageEffect } columns{ id colspan{sm md lg} background{ color desktopImage mobileImage imageAltText video hideImageOnMobile alignment } border{ color radius style width } padding columnAnimation contentOrientation verticalAlignment horizontalAlignment attributes{ id className } minHeight{ desktop mobile tablet } contentBlocks{ id name packId model horizontalAlignment verticalSelfAlignment stretchHeight stretchWidth spacing{ margin padding } minHeight{ desktop mobile tablet } minWidth{ desktop mobile tablet } } } }\",\"variables\":{\"id\":\"$CATEGORY_ID$\",\"options\":{\"page\":{\"index\":$PAGE_INDEX$}},\"specificationFilter\":\"FOR_LIST\",\"loadLargeImages\":true,\"loadCategories\":true}}"
        raw_product_check = "{\"query\":\" query CalculatedProducts($options:ProductsLoadOptions!){ catalog{ products(options:$options){ products{ id price listPrice priceExtraFields{ ...priceInfoExtraField } inventory isOrderable@requireAbility(ability:ORDER_PRODUCTS) uom{id} variantComponentGroups{ id }  productConfiguratorInfo{isProductConfigurable}  } } } } fragment priceInfoExtraField on PriceInfoExtraField{ name ...on PricePriceInfoExtraField{price} ...on PercentagePriceInfoExtraField{percentage} }\",\"variables\":{\"options\":{\"ids\": $PRODUCT_ID_LIST$ ,\"page\":{\"size\":2000,\"index\":0}}}}"


        # proxies = {
        #     "http": "venksta:wifisky10@geo.iproyal.com:12321"
        # }
        #
        # print(requests.get("https://api.ipify.org/?format=json", proxies=proxies).text)
        # exit()
        #
        # curl 'https://api.ipify.org?format=json' -x http://venksta:wifisky10@geo.iproyal.com:12321

        login()

        for category in categories:
            page_iterator = 0
            products_in_category_count = 0
            logging.info(f'Enter {category} category')
            while True:
                category_request = raw_category_list.replace("$CATEGORY_ID$", category).replace("$PAGE_INDEX$", str(page_iterator))
                request_category = requests.post(tree_locate_graph, data=category_request, headers=headers, timeout=10)
                category_data = json.loads(request_category.text)
                total_category_pages = math.ceil(category_data['data']['pages']['productList']['products']['totalCount'] / products_per_page)
                logging.info(f'Scraping {page_iterator+1}/{total_category_pages} pages')
                found_products = category_data['data']['pages']['productList']['products']['products']
                products_in_category_count = products_in_category_count + len(found_products)
                category_name = category_data['data']['pages']['productList']['pageTitle']
                for i in range(len(found_products)):
                    found_products[i]['pageTitle'] = category_data['data']['pages']['productList']['pageTitle']
                    products[found_products[i]['id']] = found_products[i]

                page_iterator += 1
                if page_iterator == total_category_pages:
                    break

            logging.info(f'Products found in {category_name} {category} : {products_in_category_count}')
            time.sleep(sleep_interval)

        product_list_data = []
        logging.info(f'Getting detail product info for {len(products.keys())} items')
        for products_split in split_dict(products, 5):
            product_list_request = raw_product_check.replace("$PRODUCT_ID_LIST$", json.dumps(list(products_split.keys())))
            request_product_list = requests.post(tree_locate_graph, data=product_list_request, headers=headers, timeout=10)
            product_list_data.extend(json.loads(request_product_list.text)['data']['catalog']['products']['products'])
            time.sleep(sleep_interval)
        logging.info(f'Received detail product info for {len(product_list_data)} items')
        logging.info(f'Searching for all product images. Takes time!')
        for i in range(len(product_list_data)):
            logging.info(f'{i+1}/{len(product_list_data)}')
            products[product_list_data[i]['id']]['price'] = product_list_data[i]['price']
            products[product_list_data[i]['id']]['inventory'] = product_list_data[i]['inventory']

            if products[product_list_data[i]['id']]['image']:
                products[product_list_data[i]['id']]['images'] = search_more_images(products[product_list_data[i]['id']]['image']['large'])
            else:
                products[product_list_data[i]['id']]['images'] = []

        f = open(f'archives/{datetime.datetime.now()}.csv', 'w+')
        writer = csv.writer(f)
        for product_id, product in products.items():
            writer.writerow([
                products[product_id]['url'][1:],
                products[product_id]['title'],
                "", #desc
                "","","",
                products[product_id]['pageTitle'],
                "",
                "","","","","","",
                product_id,
                "","",
                products[product_id]['inventory'],
                "", "",
                products[product_id]['price'],
                ' ; '.join(products[product_id]['images']),
            ])
        f.close()

        logging.info(f'Going to sleep for {run_every_x_hours} hours, then restart')
        time.sleep(run_every_x_hours * 60 * 60)
        exit()

