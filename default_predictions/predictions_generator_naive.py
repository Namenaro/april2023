from common_utils import IdsGenerator, Point
from picture_wrapper import Pic
from region_of_pic import Region

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
from copy import deepcopy


class DefaultPredictionsGeneratorNaive:
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
        old_region_ids, points_in_intersections, points_not_in_intersections = self._find_all_intersections(fact_points)

        for i in range(len(old_region_ids)):
            self._divide_old_region(old_region_ids[i], points_in_intersections[i], points_not_in_intersections[i],
                                    fact_mean=fact_mean)

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

    def _find_all_intersections(self, fact_points):
        old_regions_ids = []
        points_in_intersections = []
        points_not_in_intersections = []

        for old_region_id, region in self.regions_dict.items():
            points_in_intersection, points_not_in_intersection = self._get_AandB_AnoB(
                point_cloudA_to_divide=region.points,
                point_cloudB=fact_points)
            if len(points_in_intersection) == 0:
                continue
            old_regions_ids.append(old_region_id)
            points_in_intersections.append(points_in_intersection)
            points_not_in_intersections.append(points_not_in_intersection)
        return old_regions_ids, points_in_intersections, points_not_in_intersections

    def _divide_old_region(self, old_region_id, points_in_intersection, points_not_in_intersection, fact_mean):
        mean_of_old_region = self.regions_dict[old_region_id].mean
        del self.regions_dict[old_region_id]

        mean_of_intersection = (fact_mean + mean_of_old_region) / 2
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
    prediction_generator = DefaultPredictionsGeneratorNaive(pic)

    # до добавления фактов это выглядит так:
    fig, ax = plt.subplots()
    prediction_generator.draw_to_ax(ax)
    plt.show()

    # добавим один факт (про область вокруг центра изображения):
    point = pic.get_center_point()
    radius = 4
    points_cloud = pic.get_point_cloud(point, radius=radius)
    mean_in_cloud = pic.get_mean_val_in_point_cloud(points_cloud)
    prediction_generator.add_fact(points_cloud, mean_in_cloud)
    fig, ax = plt.subplots()
    prediction_generator.draw_to_ax(ax)
    plt.show()

    # добавим еще один факт (про область ниже центра изображения):
    point = point + Point(0, 3)
    radius = 8
    points_cloud = pic.get_point_cloud(point, radius=radius)
    mean_in_cloud = pic.get_mean_val_in_point_cloud(points_cloud)
    prediction_generator.add_fact(points_cloud, mean_in_cloud)
    fig, ax = plt.subplots()
    prediction_generator.draw_to_ax(ax)
    plt.show()
