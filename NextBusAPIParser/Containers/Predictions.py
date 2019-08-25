import global_vars
from NextBusAPIParser.Containers.Prediction import Prediction
import time

class Predictions:
    def __init__(self, element, xml_url):
        self.xml_url = xml_url
        self._xml_element = element
        self.has_predictions = True if not self._xml_element.get("dirTitleBecauseNoPredictions") else False
        self._directions = self.__set_direction()
        self.time_since_directions_updated = time.time()

    @property
    def directions(self):
        if self.time_since_directions_updated - time.time() > 10:
            self.time_since_directions_updated = time.time()
            return self.__set_direction()
        else:
            return self._directions

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
        if not self.has_predictions:
            return None
        for ele in self.xml_element.findall("./direction"):
            title = ele.get('title')
            directions[title] = list(
                map(lambda x: Prediction(x), ele.findall("./prediction")))
        return directions

    def __repr__(self):
        initial_string = "Route %s: " % self._xml_element.get('routeTitle')
        if self.has_predictions is False:
            return "%s No Predictions available" % initial_string
        direction_string = "Direction towards "
        if self.directions.get("Loop"):
            return "{}{}".format(initial_string, self._directions['Loop'])
        return initial_string + "\n".join(
            ["{}{}: {}".format(direction_string, direction, predictions) for direction, predictions in
             self._directions.items()])
