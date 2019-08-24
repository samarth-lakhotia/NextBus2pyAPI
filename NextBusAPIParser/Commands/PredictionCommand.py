import global_vars
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
            if len(matches) > 1:
                raise Exception("Multiple matches found, please have a good keyword")
            stop_results = matches[0].route.get_stop_by_keyword(stop_keyword)
            if stop_results:
                if len(stop_results) > 1:
                    raise Exception("Multiple stop names with the keyword %s found " % stop_keyword)
                return self.get_predictions_by_route_and_stop_id(matches[0].route_tag, stop_results[0].stop_id)
            else:
                raise LookupError("No stop matches found")
        else:
            raise LookupError("No routes with the given name found")


if __name__ == '__main__':
    a = PredictionCommand('umd')
    b = a.get_predictions_by_route_and_stop_id('122', '10001')
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
    print(str(b[0].directions['Loop'][0]))
