from NextBusAPIParser import global_vars
from NextBusAPIParser.Containers.Route import Route

route_config_command = global_vars.add_query_to_nextbus({"command": "routeConfig"})


class RouteConfig:
    def __init__(self, agency, route_tag):
        self.agency_tag = agency
        self.route_tag = route_tag
        self._route = None

    @property
    def route(self):
        if self._route is None:
            self._route = self._set_route_details()
        return self._route

    @route.setter
    def route(self, value):
        self._route = value

    def _set_route_details(self):
        if self.agency_tag and self.route_tag:
            return RouteConfig.get_data_route_and_agency_tag(self.agency_tag, self.route_tag)
        else:
            return None

    @staticmethod
    def get_data_route_and_agency_tag(agency_tag, route_tag):
        final_url = global_vars.update_query_to_url_result(route_config_command,
                                                           {"a": agency_tag, "r": route_tag})
        xml_data = global_vars.read_xml_url(final_url)
        route_details = xml_data.find("route")
        if route_details is None:
            raise Exception("The xml url built up is bad")
        route_ele = Route(element=route_details)
        return route_ele


if __name__ == '__main__':
    route_conf = RouteConfig(agency="umd", route_tag="108")
    route = route_conf.route
    stops = route.stops
    for stop in stops:
        print("{} towards {}".format(stop.stop_title, stop.direction.get('title')))
