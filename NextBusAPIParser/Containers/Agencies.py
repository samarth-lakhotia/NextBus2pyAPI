import global_vars


class Agencies:
    def __init__(self):
        self.complete_url = global_vars.add_query_to_nextbus({"command": "agencyList"})
        self.xml_parsed = global_vars.read_xml_url(self.complete_url)
        self.agencies = self.get_agencies()

    def get_agencies(self):
        agency_list = self.xml_parsed.findall('.//agency')
        return agency_list

    def get_agency_names(self):
        return list(map(lambda x: x.attrib['title'], self.agencies))

    def get_agency_element_by_tag(self, tag_id):
        agency = list(filter(lambda x: x.attrib['tag'] == tag_id, self.agencies))
        return agency

    def get_agency_element_by_title(self, title):
        agency = list(filter(lambda x: x.attrib['title'] == title, self.agencies))
        return agency


if __name__ == '__main__':
    a = Agencies()
    b = a.get_agency_element_by_tag('umd')
    print(b[0].attrib['title'])
