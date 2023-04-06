
import pytest
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import random
import string

@pytest.fixture(scope='session')
def basic_auth():
    return HTTPBasicAuth('1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL', '')

# test_1_get_products
def test_get_products(basic_auth):
    url_products = 'http://164.92.218.36:8080/api/products'
    response_get = requests.get(url_products, auth=basic_auth)
    assert response_get.status_code == 200

# test_2_post_new_address
@pytest.mark.usefixtures("basic_auth")
def test_create_address(basic_auth):
    url_addresses = 'http://164.92.218.36:8080/api/addresses'
    xml_data_addresses = """
        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
            <address>
                <id_country>12</id_country>
                <alias>Lion</alias>
                <lastname>Melnew</lastname>
                <firstname>Lion</firstname>
                <address1>Firststreet</address1>
                <city>Madrid</city>
            </address>
        </prestashop>
    """
    xml_data_addresses = xml_data_addresses.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}
    response_add_address = requests.post(url_addresses, data=xml_data_addresses, headers=headers, auth=basic_auth)
    assert response_add_address.status_code == 201
    
    added_element = ET.fromstring(response_add_address.text)
    assert added_element.find(".//id").text is not None

# test3, create new currency

@pytest.mark.usefixtures("basic_auth")
def test_create_currency(basic_auth):
    url_currency = 'http://164.92.218.36:8080/api/currencies'
    iso_code = "".join(random.choices(string.ascii_uppercase,k=3))
    length= random.randint(4,10)
    name = "".join(random.choices(string.ascii_letters, k=length))
    conversion_rate = round(random.uniform(0.1,50.0),3)
    xml_data_currency = f"""
        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
            <currency>
                <names>
                    <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1" format="isUnsignedId"></language>
                </names>
                <name notFilterable="true" required="true" maxSize="255" format="isGenericName">{name}</name>
                <symbol maxSize="255">
                    <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1" format="isUnsignedId"></language>
                </symbol> 
                <iso_code required="true" maxSize="3" format="isLanguageIsoCode">{iso_code}</iso_code>
                <conversion_rate required="true" format="isUnsignedFloat">{conversion_rate}</conversion_rate>
            </currency>
        </prestashop>
    """
    xml_data_currency = xml_data_currency.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}

    response_add_currency = requests.post(url_currency, data=xml_data_currency, headers=headers, auth=basic_auth)
    assert response_add_currency.status_code == 201

 # test4_put_product
def test_update_product_new():
    url = "http://164.92.218.36:8080/api/products"
    auth = ("1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL", "")
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
    <order>
        <id>2</id>
        <price>99.999</price>
        
    <associations></associations>
    </order>
    </prestashop>"""

    response = requests.put(url, auth=auth, data=xml_content)

    assert response.status_code == 200 

# test_5_delete_сurrency

@pytest.fixture 
def url_addresses():
    return 'http://164.92.218.36:8080/api/addresses'

def test_create_address_to_be_deleted(basic_auth, url_addresses):
    xml_data_addresses = """
        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
            <address>
                <id_country>525</id_country>
                <alias>Maria</alias>
                <lastname>Longreih</lastname>
                <firstname>Maria</firstname>
                <address1>Richkova15</address1>
                <city>Madrid</city>
            </address>
        </prestashop>
    """
    xml_data_addresses = xml_data_addresses.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}
    response_add_address_to_be_deleted = requests.post(url_addresses, data=xml_data_addresses, headers=headers, auth=basic_auth)
    assert response_add_address_to_be_deleted.status_code == 201
    
    added_element = ET.fromstring(response_add_address_to_be_deleted.text)
    added_element_id = added_element.find(".//id").text
    assert added_element_id is not None
    
    url_address_delete = url_addresses + "/" + added_element_id
    response_delete = requests.delete(url_address_delete, auth=basic_auth)
    assert response_delete.status_code == 200










    

