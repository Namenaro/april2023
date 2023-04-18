from common_utils import IdsGenerator, Point
from picture_wrapper import Pic


class Region:
    def __init__(self, points, mean):
        self.points = points
        self.mean = mean

    def has_point(self, point):
        if point in self.points:
            return True
        return False

    def get_mass(self):
        return len(self.points) + self.mean

    def send_to_pic(self, pic):
        for point in self.points:
            pic.set_point_val(point, self.mean)
