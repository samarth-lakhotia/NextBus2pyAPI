class Stop:
    def __init__(self, element, direction):
        self.xml_element = element
        self.stop_tag = element.attrib['tag']
        self.stop_id = element.get('stopId').strip()
        self.stop_title = element.attrib['title'].strip()
        self.direction = direction

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, Stop):
            return self.stop_title == other.stop_title
        else:
            return False

    def __hash__(self):
        return str.__hash__(self.stop_title)

    def __str__(self):
        return self.stop_title
