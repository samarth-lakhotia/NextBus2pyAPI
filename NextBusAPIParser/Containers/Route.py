from global_vars import LOOP, TWO_DIRECTIONS, read_xml_url
from NextBusAPIParser.Containers.Stop import Stop


class Route:
    def __init__(self, element=None, url=None):
        if element is None:
            self.route_config_url = url
            self.xml_element = read_xml_url(self.route_config_url).find("route")
        else:
            self.xml_element = element
        self.route_tag, self.route_title, self.route_short_title, self.color = self.unpack_element(element)
        self._stops = None
        self.direction_elements = self.xml_element.findall("./direction")
        self.direction_type = self.__set_direction_type()

    def __set_direction_type(self):
        if len(self.direction_elements) == 2:
            return TWO_DIRECTIONS
        else:
            return LOOP

    @property
    def stops(self):
        if self._stops is None:
            self._stops = self.__extract_stops()
        return self._stops

    @stops.setter
    def stops(self, value):
        self._stops = value

    def unpack_element(self, element):
        return element.attrib['tag'], element.attrib['title'], element.attrib['shortTitle'] if hasattr(
            element.attrib, "shortTitle") else None, element.attrib['color'] if hasattr(element.attrib,
                                                                                        'color') else None

    def __extract_stops(self):
        stops = self.xml_element.findall("./stop[@stopId]")
        return list(
            set(map(lambda x: Stop(x, self.xml_element.find("./direction/stop[@tag='%s'].." % x.get('tag'))), stops)))

    def get_stop_by_keyword(self, stop_keyword):
        results = list(filter(lambda x: stop_keyword.lower() in x.stop_title.lower(), self.stops))
        return results

    def __repr__(self):
        return self.route_title

    def __str__(self):
        return self.route_title
