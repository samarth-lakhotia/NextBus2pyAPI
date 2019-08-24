import global_vars
from NextBusAPIParser.Commands.RouteList import RouteList


class Agency:
    _route_list: RouteList

    def __init__(self, agency_tag, agency_name=None, agency_region=None):
        self.agency_tag = agency_tag
        self.agency_name = agency_name
        self.region = agency_region
        self._route_list = None

    @property
    def route_list(self):
        if self._route_list is None:
            self._route_list = RouteList(self.agency_tag)
        return self._route_list

    @route_list.setter
    def route_list(self, value):
        self._route_list = value


if __name__ == '__main__':
    a = Agency("umd")
    stops = a.route_list.get_all_stops()
    print(stops)
    print(len(stops))
