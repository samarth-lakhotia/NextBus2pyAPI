from NextBusAPIParser import global_vars
from NextBusAPIParser.Commands.RouteList import RouteList
from NextBusAPIParser.Containers.Predictions import Predictions

prediction_command = global_vars.add_query_to_nextbus({"command": "predictions"})


class PredictionCommand:
    def __init__(self, agency_tag):
        self.agency_tag = agency_tag

    def get_predictions_stop_id(self, stop_id):
        final_command = global_vars.update_query_to_url_result(prediction_command,
                                                               {"a": self.agency_tag, "stopId": stop_id})
        xml_root = global_vars.read_xml_url(final_command)
        predictions = list(map(lambda x: Predictions(x, final_command), xml_root.findall("predictions")))
        return predictions

    def get_predictions_by_route_and_stop_id(self, route_tag, stop_id):
        final_command = global_vars.update_query_to_url_result(prediction_command,
                                                               {"a": self.agency_tag, "r": route_tag,
                                                                "stopId": stop_id})
        xml_root = global_vars.read_xml_url(final_command)
        res = xml_root.findall("./predictions")
        predictions = list(map(lambda x: Predictions(x, final_command), res))
        return predictions

    def get_predictions_by_route_stop_keyword(self, route_keyword, stop_keyword):
        route_list = RouteList(self.agency_tag)
        matches = route_list.get_route_by_keyword(route_keyword)
        if matches:
            stop_results = [match.get_stop_by_keyword(stop_keyword) for match in matches]
            if stop_results:
                return [self.get_predictions_by_route_and_stop_id(match.route_tag, stop.stop_id) for
                        match, stop_result in zip(matches, stop_results) for stop in stop_result]
            else:
                raise LookupError("No stop matches for the given route found")
        else:
            raise LookupError("No routes with the given name found")

    def get_predictions_by_stop_title(self, stop_title):
        # expensive
        route_list = RouteList(self.agency_tag)
        all_stops = route_list.get_all_stops()
        results = list(filter(lambda x: stop_title.lower() in x.stop_title.lower(), all_stops))
        if results:
            all_predictions = [self.get_predictions_stop_id(x.stop_id) for x in results]
            return all_predictions
        else:
            raise LookupError("Cannot find any stops with the given title")


if __name__ == '__main__':
    a = PredictionCommand('umd')
    b = a.get_predictions_by_route_stop_keyword("enclave", "enclave")
    print(b)
    c = a.get_predictions_by_stop_title("stamp")
    print(c)
