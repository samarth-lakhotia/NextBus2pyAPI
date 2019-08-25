from urllib.parse import urlsplit, urlencode, parse_qs, parse_qsl
from xml.etree import ElementTree as ET
import urllib.request as url_utils

nextbus_base_url = urlsplit("http://webservices.nextbus.com/service/publicXMLFeed")

MULTIPLE_DIRECTIONS = 0
LOOP = 1


def update_query_to_url_result(url_result, query_dict={}):
    existing_dict = parse_qs(url_result.query)
    existing_dict.update(query_dict)
    return url_result._replace(query=urlencode(existing_dict, doseq=True))


def add_query_to_nextbus(query_dict={}):
    return update_query_to_url_result(nextbus_base_url, query_dict)


def read_xml_url(complete_url):
    complete_url = complete_url.geturl()
    xml_file = url_utils.urlopen(complete_url)
    data = xml_file.read()
    xml_parsed = ET.fromstring(data)
    xml_file.close()
    return xml_parsed
