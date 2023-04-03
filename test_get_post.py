
import pytest
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth

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

# test_3_post_new_currency
@pytest.mark.usefixtures("basic_auth")
def test_create_currency(basic_auth):
    url_currency = 'http://164.92.218.36:8080/api/currencies'
    xml_data_currency = """
        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
            <currency>
                <names>
                    <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1" format="isUnsignedId"></language>
                </names>
                <name notFilterable="true" required="true" maxSize="255" format="isGenericName">Ларі</name>
                <symbol maxSize="255">
                    <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1" format="isUnsignedId"></language>
                </symbol> 
                <iso_code required="true" maxSize="3" format="isLanguageIsoCode">GEL</iso_code>
                <conversion_rate required="true" format="isUnsignedFloat">3.10</conversion_rate>
            </currency>
        </prestashop>
    """
    xml_data_currency = xml_data_currency.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}

    response_add_currency = requests.post(url_currency, data=xml_data_currency, headers=headers, auth=basic_auth)
    assert response_add_currency.status_code == 201
    
    added_currency = ET.fromstring(response_add_currency.text)
    new_currency_id = added_currency.find(".//id").text
    assert added_currency.find(".//id").text is not None

# test4 delete_сurrency
@pytest.mark.usefixtures("basic_auth")
def test_delete_currency(basic_auth, url_currency, new_currency_id):
    response_delete_currency = requests.delete(url_currency + '/' + str(new_currency_id), auth=basic_auth)
    assert response_delete_currency.status_code == 204 
    







    

