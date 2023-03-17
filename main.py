import requests
import json
import logging
import math
from fake_useragent import UserAgent

ua = UserAgent()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

tree_locate_graph = 'https://store.treelocate.com/api/graph'
random_user_agent = ua.random
products_per_page = 18
categories = ["c4830e60-65ec-4d2a-84bf-90d01f03c5a5", "b0d74de4-8274-4e8c-bc3a-6b6d159cc7df"]
products = {}

headers = {
    'Host': 'store.treelocate.com',
    'Content-Type': 'text/plain',
    'User-Agent': random_user_agent
}

raw_login = "{\"query\":\" mutation Login($input:LoginInput!,$keys:[UserAbilityKey!]!){ profile{ login(input:$input){ token{value expiration:sessionExpiration}failureText @toVariable(name:\\\"failTxt\\\") } }viewer{  id name shopAccountType referenceId:accountReferenceId oneToMany role customerType isImpersonating currencyId pricesInclTax  customer{ id email name phone isValid }  abilities(keys:$keys) @whenEquals(variable:\\\"failTxt\\\", value: null){ key state } } }\",\"variables\":{\"input\":{\"email\":\"support@green4life.co.uk\",\"password\":\"TreeC05153\",\"persistent\":false},\"keys\":[\"VIEW_CATALOG\",\"VIEW_PRICES\",\"VIEW_STOCK\",\"VIEW_UNIT_OF_MEASURE\",\"VIEW_PRODUCT_SUGGESTIONS\",\"VIEW_MY_ACCOUNT_PAGE\",\"ORDER_PRODUCTS\",\"SUBMIT_ORDER\",\"CREATE_QUOTE\",\"COMPARE_PRODUCTS\",\"SUBSCRIBE_TO_NEWSLETTER\",\"USE_ORDER_TEMPLATES\"]}}\n"
raw_category_list = "{\"query\":\" query ProductListPage( $id:ID!, $options:ProductListPageProductsLoadOptions!, $loadLargeImages:Boolean!, $loadCategories:Boolean=false, ){ pages{ productList(id:$id){ metaTitle metaDescription pageTitle description preset@toVariable(name:\\\"preset\\\") products(options:$options){ products{  id title image{ small mediumSmall large @include(if:$loadLargeImages) } url hasVariants uom{id} uoms{ id description@requireAbility(ability:VIEW_UNIT_OF_MEASURE) minimumQuantity maximumQuantity defaultQuantity quantityStep } stockLevels{ outOfStock lowStock maxStockNumber } specifications(filter:FOR_LIST){ key value  } categoriesPaths @include(if:$loadCategories){ categories{name} }  variantComponentGroups@whenEquals(variable:\\\"preset\\\",value:\\\"ListB2B\\\"){ id } }  facets{ items{ name title displayType ... on RangeFacet{ fieldType minValue maxValue } ... on ListFacet{ sortDescending crawlable values{ title textTitle count value selected } } } multiSelect } totalCount } defaultSorting{ field ascending } sortingEnabled defaultViewMode viewModeSwitchEnabled showThumbnails pagingType backgroundColor backgroundImage headerContent{...rows} footerContent{...rows} } } }fragment rows on RowContentElement{ id fullWidth background{ color desktopImage mobileImage imageAltText video fullWidth hideImageOnMobile alignment } border{ color radius style width } spacing{ margin padding hideSpaces } rowAnimation verticalAlignment attributes{ id className } minHeight{ desktop mobile tablet } heroEffect{ altLogo altSmallLogo headerOnTop headerTextColor showScrolldownIcon mutedSound imageEffect } columns{ id colspan{sm md lg} background{ color desktopImage mobileImage imageAltText video hideImageOnMobile alignment } border{ color radius style width } padding columnAnimation contentOrientation verticalAlignment horizontalAlignment attributes{ id className } minHeight{ desktop mobile tablet } contentBlocks{ id name packId model horizontalAlignment verticalSelfAlignment stretchHeight stretchWidth spacing{ margin padding } minHeight{ desktop mobile tablet } minWidth{ desktop mobile tablet } } } }\",\"variables\":{\"id\":\"$CATEGORY_ID$\",\"options\":{\"page\":{\"index\":$PAGE_INDEX$}},\"specificationFilter\":\"FOR_LIST\",\"loadLargeImages\":true,\"loadCategories\":true}}"

request_login = requests.post(tree_locate_graph, data=raw_login, headers=headers)

if(request_login.status_code != 200):
    logging.info(f'Login ERROR, status code {request_login.status_code}')
    exit()
else:
    bearer_token = json.loads(request_login.text)['data']['profile']['login']['token']['value']
    headers['Authorization'] = f'Bearer {bearer_token}'
    logging.info(f'Login successful')

for category in categories:
    page_iterator = 0

    while True:
        print(f'I {page_iterator}')
        category_request = raw_category_list.replace("$CATEGORY_ID$", category).replace("$PAGE_INDEX$", str(page_iterator))
        request_category = requests.post(tree_locate_graph, data=category_request, headers=headers)
        category_data = json.loads(request_category.text)
        total_category_pages = math.ceil(category_data['data']['pages']['productList']['products']['totalCount'] / products_per_page)
        print(f'Total pages {total_category_pages}')
        found_products = category_data['data']['pages']['productList']['products']['products']

        for i in range(len(found_products)):
            found_products[i]['pageTitle'] = category_data['data']['pages']['productList']['pageTitle']
            products[found_products[i]['id']] = found_products[i]

        page_iterator += 1
        if page_iterator >= total_category_pages:
            break

#all product keys
print(list(products.keys()))

for product_id, product in products.items():
    print(product_id)
    print(product)
    products[product_id]['alabala'] = 'venci'


#TODO
add all keys and search with one query for pricing and quantity

