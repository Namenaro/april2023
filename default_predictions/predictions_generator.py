from common_utils import IdsGenerator, Point
from picture_wrapper import Pic
from region_of_pic import Region

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
from copy import deepcopy


class DefaultPredictionsGenerator:
    def __init__(self, pic):
        self.pic = pic
        self.regions_dict = {}
        self.ids_generation = IdsGenerator()
        initial_reg_id = self.ids_generation.generate_id()
        self.regions_dict[initial_reg_id] = Region(pic.get_coords_list(), pic.get_mean())

    def get_points_vals_predictions(self, points_list):
        vals = []
        for point in points_list:
            for reg_id, region in self.regions_dict.items():
                if region.has_point(point):
                    vals.append(region.mean)
        return vals

    def add_fact(self, fact_points, fact_mean):
        while True:
            old_region_id, points_in_intersection, points_not_in_intersection = self._find_some_intersection(fact_points)

            if old_region_id is None:
                break

            self._divide_old_region(old_region_id, points_in_intersection, points_not_in_intersection, fact_mean)

    def print_regions_info(self):
        str_means = ""
        for reg_id, region in self.regions_dict.items():
            str_means += str(reg_id) + ": " + str(region.mean) + ", "
        return str_means

    def draw_to_ax(self, ax):
        numpy_pic = np.zeros(shape=self.pic.img.shape)
        new_pic = Pic(numpy_pic)
        for _, region in self.regions_dict.items():
            region.send_to_pic(new_pic)
        new_pic.draw_to_ax(ax)

        # фоном показать саму цифру:
        cm = plt.get_cmap('Greens')
        ax.imshow(self.pic.img, cmap=cm, alpha=0.07)

    def _find_some_intersection(self, fact_points):
        for old_region_id, region in self.regions_dict.items():
            points_in_intersection, points_not_in_intersection = self._get_AandB_AnoB(point_cloudA_to_divide=region.points,
                                                      point_cloudB=fact_points)
            if len(points_in_intersection) != 0:
                return old_region_id, points_in_intersection, points_not_in_intersection
        return None, None, None

    def _divide_old_region(self, old_region_id, points_in_intersection, points_not_in_intersection, fact_mean):
            mean_of_old_region = self.regions_dict[old_region_id].mean
            del self.regions_dict[old_region_id]

            mean_of_intersection = (fact_mean + mean_of_old_region)/2
            self._add_new_region(mean=mean_of_intersection, points=points_in_intersection)
            self._add_new_region(mean=mean_of_old_region, points=points_not_in_intersection)

    def _add_new_region(self, mean, points):
        reg_id = self.ids_generation.generate_id()
        new_region = Region(points=points, mean=mean)
        self.regions_dict[reg_id] = new_region

    def _get_AandB_AnoB(self, point_cloudA_to_divide, point_cloudB):
        intersecton = []
        outer = []
        for point_a in point_cloudA_to_divide:
            if point_a in point_cloudB:
                intersecton.append(deepcopy(point_a))
            else:
                outer.append(deepcopy(point_a))
        return intersecton, outer


if __name__ == '__main__':
    pic = Pic()




