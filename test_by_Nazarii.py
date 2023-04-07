import pytest 
import requests 
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import random
import string


@pytest.fixture(scope='session')
def basic_auth():
    return HTTPBasicAuth('1VQDHXQ8EF73QTHESPT7UHU9AJQPLXXL', '')

def test_get_products(basic_auth):
    url_products = 'http://164.92.218.36:8080/api/countries'
    response_get = requests.get(url_products, auth=basic_auth)
    assert response_get.status_code == 200

@pytest.mark.usefixtures("basic_auth")
def test_create_country(basic_auth):
    url_country = 'http://164.92.218.36:8080/api/countries'
    xml_data_country = """
        <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
            <country>
                <id_zone required="true" format="isUnsignedId">1</id_zone>
                <id_currency format="isUnsignedId"></id_currency>
                <call_prefix format="isInt"></call_prefix>
                <iso_code required="true" maxSize="3" format="isLanguageIsoCode">GBP</iso_code>
                <active format="isBool"></active>
                <contains_states required="true" format="isBool">0</contains_states>
                <need_identification_number required="true" format="isBool">0</need_identification_number>
                <need_zip_code format="isBool"></need_zip_code>
                <zip_code_format format="isZipCodeFormat"></zip_code_format>
                <display_tax_label required="true" format="isBool">0</display_tax_label>
                <name required="true" maxSize="64" format="isGenericName">
                <language id="1" xlink:href="http://164.92.218.36:8080/api/languages/1" format="isUnsignedId" >Ukrainian</language>
                </name>
            </country>
        </prestashop>
    """
    xml_data_country = xml_data_country.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}
    response_add_country = requests.post(url_country, data=xml_data_country, headers=headers, auth=basic_auth)
    assert response_add_country.status_code == 201

@pytest.mark.usefixtures("basic_auth")
def test_create_currency(basic_auth):
    url_currency = 'http://164.92.218.36:8080/api/currencies'
    iso_code = "".join(random.choices(string.ascii_uppercase,k=3))
    length= random.randint(1,5)
    name = "".join(random.choices(string.ascii_letters, k=length))
    conversion_rate = round(random.uniform(0.1,1.0),2)
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

@pytest.mark.usefixtures("basic_auth")
def test_update_order(basic_auth):
    url_order = 'http://164.92.218.36:8080/api/orders/1'

    xml_data_order = """
        <prestashop>
            <order>
                <id>1</id>
                <id_address_delivery>1</id_address_delivery>
                <id_address_invoice>1</id_address_invoice>
                <id_cart>1</id_cart>
                <id_currency>1</id_currency>
                <id_lang>1</id_lang>
                <id_customer>1</id_customer>
                <id_carrier>1</id_carrier>
                <module>cashondelivery</module>
                <payment>OfflinePayment</payment>
                <total_paid>0.00</total_paid>
                <total_paid_real>0.00</total_paid_real>
                <total_products>0.00</total_products>
                <total_products_wt>0.00</total_products_wt>
                <conversion_rate>1</conversion_rate>
            </order>
        </prestashop>
    """
    xml_data_order = xml_data_order.encode('utf-8')
    headers = {'Content-Type': 'application/xml'}

    response_update_order = requests.put(url_order, data=xml_data_order, headers=headers, auth=basic_auth)
    assert response_update_order.status_code == 200

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
                <city>Lviv</city>
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