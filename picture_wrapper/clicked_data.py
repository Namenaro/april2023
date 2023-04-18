import jsonpickle


class ClickedData:
    def __init__(self):
        self.radiuses = []
        self.points = []

    def set_data(self, radiuses, points):
        self.radiuses = radiuses
        self.points = points

    def save_to_file(self, filename="hand_select.pkl"):
        encoded = jsonpickle.encode(self)

        with open(filename, "w") as write_file:
            write_file.write(encoded)

    def load_from_file(self, filename="hand_select.pkl"):
        with open(filename, "r") as read_file:
            loaded = read_file.read()
            decoded = jsonpickle.decode(loaded)
            self.set_data(decoded.radiuses, decoded.points)