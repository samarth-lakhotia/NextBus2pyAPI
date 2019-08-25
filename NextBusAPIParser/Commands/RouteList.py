import os
import time
from datetime import timedelta
from functools import reduce
import global_vars
from NextBusAPIParser.Commands.RouteConfig import RouteConfig
from cachetools import cached, TTLCache
import pickle

command_url = global_vars.add_query_to_nextbus({"command": "routeList"})

cache = TTLCache(maxsize=500, ttl=2000)


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

    @cached(cache)
    def get_all_stops(self):
        # expensive
        route_list = self.route_list
        try:
            with open("stops.pickle", "rb") as f:
                stops_pickle = pickle.load(f)
            if time.time() - stops_pickle.time_when_initialized > stops_pickle.time_to_reset:
                stops_pickle = PickleWrapper(
                    reduce(lambda y, x: y.union(set(RouteConfig(self.agency_tag, x.attrib['tag']).route.stops)),
                           route_list, set()), stops_pickle.time_to_reset)
                with open("stops.pickle", "wb") as f:
                    pickle.dump(stops_pickle, f)
        except FileNotFoundError:
            stops_pickle = PickleWrapper(
                reduce(lambda y, x: y.union(set(RouteConfig(self.agency_tag, x.attrib['tag']).route.stops)),
                       route_list, set()), timedelta(days=1).total_seconds())
            with open("stops.pickle", "wb") as f:
                pickle.dump(stops_pickle, f)
        stops = stops_pickle.object_to_be_pickled
        return list(stops)

    def get_route_by_keyword(self, name):
        result = list(filter(lambda x: name.lower() in x.attrib['title'].lower(), self.route_list))
        final_result = map(lambda x: RouteConfig(self.agency_tag, x.attrib['tag']), result)
        return list(final_result)


class PickleWrapper:
    def __init__(self, obj, time_to_reset):
        self.object_to_be_pickled = obj
        self.time_when_initialized = time.time()
        self.time_to_reset = time_to_reset


if __name__ == '__main__':
    a = RouteList('umd')
    print(a.get_all_stops())
