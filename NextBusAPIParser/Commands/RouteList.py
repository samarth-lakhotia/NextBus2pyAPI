from functools import reduce
import global_vars
from NextBusAPIParser.Commands.RouteConfig import RouteConfig

command_url = global_vars.add_query_to_nextbus({"command": "routeList"})


class RouteList:

    def __init__(self, agency_tag):
        self.agency_tag = agency_tag
        self._route_list = None

    @property
    def route_list(self):
        if self._route_list is None:
            self._route_list = RouteList.get_routelist_by_agency_tag(self.agency_tag)
        return self._route_list

    @route_list.setter
    def route_list(self, value):
        self._route_list = value

    @staticmethod
    def get_routelist_by_agency_tag(agency_tag):
        xml_parsed = global_vars.read_xml_url(
            global_vars.update_query_to_url_result(command_url, {"a": agency_tag}))
        route_list = xml_parsed.findall(".//route")
        return route_list

    def get_all_stops(self):
        # expensive
        route_list = self.route_list
        stops = reduce(lambda y, x: y.union(set(RouteConfig(self.agency_tag, x.attrib['tag']).route.stops)), route_list,
                       set())
        return list(stops)

    def get_route_by_keyword(self, name):
        result = list(filter(lambda x: name.lower() in x.attrib['title'].lower(), self.route_list))
        final_result = map(lambda x: RouteConfig(self.agency_tag, x.attrib['tag']), result)
        return list(final_result)


if __name__ == '__main__':
    a = RouteList('umd')
    print(a.get_route_by_keyword('enclave'))
