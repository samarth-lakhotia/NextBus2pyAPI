import global_vars
from NextBusAPIParser.Containers.Prediction import Prediction


class Predictions:
    def __init__(self, element, xml_url):
        self.xml_url = xml_url
        self._xml_element = element
        self._directions = self.__set_direction()

    @property
    def directions(self):
        return self.__set_direction()

    @directions.setter
    def directions(self, value):
        self._directions = value

    @property
    def xml_element(self):
        return global_vars.read_xml_url(self.xml_url).find(
            "./predictions{}".format(Predictions.xpath_attrib_string_formatter(self._xml_element.attrib)))

    @staticmethod
    def xpath_attrib_string_formatter(attrib_dict):
        return "".join(["[@{}='{}']".format(k, v) for k, v in attrib_dict.items()])

    @xml_element.setter
    def xml_element(self, value):
        self._xml_element = value

    def __set_direction(self):
        directions = dict()
        for ele in self.xml_element.findall("./direction"):
            title = ele.get('title')
            directions[title] = list(
                map(lambda x: Prediction(x), self.xml_element.findall("./direction[@title='%s']/prediction" % title)))
        return directions
