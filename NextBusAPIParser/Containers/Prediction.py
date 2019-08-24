class Prediction:
    def __init__(self, prediction_element):
        self.xml_element = prediction_element
        self._minutes = prediction_element.get('minutes')
        self.isDeparture = prediction_element.get('isDeparture')
        self._seconds = prediction_element.get('seconds')

    @property
    def seconds(self):
        return self.xml_element.get('seconds')

    @seconds.setter
    def seconds(self, value):
        self._seconds = value

    @property
    def minutes(self):
        return self.xml_element.get('minutes')

    @minutes.setter
    def minutes(self, value):
        self._minutes = value

    def __repr__(self):
        return "{} minutes".format(self.minutes)

    def __str__(self):
        return "{} minutes or {} seconds".format(self.minutes, self.seconds)
