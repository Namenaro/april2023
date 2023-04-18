from common_utils import Point, Distr
from picture_wrapper import ClickedData
from clicker import CoordSelector

import numpy as np
import random
import torchvision.datasets as datasets
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib
from math import ceil


class Pic:
    def __init__(self, numpy_pic=None):
        if numpy_pic is None:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(dir_path, '../MNIST')
            self.dataset = datasets.MNIST(root=path, train=True, download=True, transform=None)
            class_of_pisc = 3
            for element in self.dataset:
                if element[1] == class_of_pisc:
                    self.img = np.array(element[0])
                    break
        else:
            self.img = numpy_pic

        self.distr = Distr(min=0, max=255, sample=self._gather_bio1_sample())

    def show(self):
        plt.imshow(self.img, cmap='gray', interpolation='none')
        plt.show()

    def get_coords_list(self):
        points_list = []
        for x in range(0, self.img.shape[1]):
            for y in range(0, self.img.shape[0]):
                points_list.append(Point(x=x, y=y))
        return points_list

    def get_mean(self):
        return np.mean(self.img)

    def get_sample_b1(self):
        return self.distr.sample

    def get_val_in_point(self, point):
        return self.img[point.y][point.x]

    def get_center_point(self):
        Y=self.img.shape[0]
        X=self.img.shape[1]
        center_x = ceil(X/2)
        center_y = ceil(Y / 2)
        return Point(x=center_x, y=center_y)

    def draw_to_ax(self, ax):
        norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
        cmap = cm.gray
        rgba = cmap(norm(self.img))
        ax.imshow(rgba, interpolation='none')

    def get_point_cloud(self, center_point, radius):
        points = []

        rect_x = int(center_point.x - radius / 2)
        rect_y = int(center_point.y - radius / 2)

        for y in range(rect_y, rect_y + radius):
            for x in range(rect_x, rect_x + radius):
                points.append(Point(x=x, y=y))
        return points

    def get_num_points_in_vicitiny(self, radius): #TODO ужасно, но с радиусом 0 неочевидно...
        points = self.get_point_cloud(Point(0,0), radius)
        return len(points)

    def _gather_bio1_sample(self, sample_size=None):
        full_sample = self.img.ravel()
        if sample_size is None:
            return full_sample
        S_1 = [random.choice(full_sample) for _ in range(sample_size)]
        return S_1

    def get_max_XY(self):
        Y = self.img.shape[0]
        X = self.img.shape[1]
        return X, Y

    def set_point_val(self, point, val):
        self.img[point.y][point.x] = val

    def get_mean_val_in_point_cloud(self, point_cloud):
        mass = 0
        for point in point_cloud:
            mass += self.get_val_in_point(point)
        return mass/len(point_cloud)

    def get_vals_of_point_cloud(self, point_cloud):
        vals_cloud = []
        for point in point_cloud:
            vals_cloud.append(self.get_val_in_point(point))
        return vals_cloud

    def get_vals_cloud_around_point(self, point, radius):
        point_cloud = self.get_point_cloud(point, radius)
        return self.get_vals_of_point_cloud(point_cloud)

    def select_in_hand_mode_with_radiuses(self):
        devcr = CoordSelector(self.img, need_radiuses=True)
        points, radiuses = devcr.create_device()
        data_from_pic = ClickedData()
        data_from_pic.set_data(points, radiuses)
        return data_from_pic

    def select_in_hand_mode_without_radiuses(self):
        devcr = CoordSelector(self.img, need_radiuses=False)
        points, radiuses = devcr.create_device()
        data_from_pic = ClickedData()
        data_from_pic.set_data(points, radiuses=None)
        return data_from_pic

    def draw_rectangle(self, ax, radius, point, color='red'):
        x = point.x
        y = point.y
        rect = plt.Rectangle((x - radius / 2, y - radius / 2), width=radius, height=radius, fc=color, alpha=0.4)
        ax.add_patch(rect)


    def annotate_point(self, ax, point, text_str):
        ax.annotate(text_str, (point.x, point.y), color='red')

    def connect_two_points_by_arrow(self, ax, point_from, point_to):
        arrow = mpatches.FancyArrowPatch((point_from.x, point_from.y), (point_to.x, point_to.y),
                                         mutation_scale=10, alpha=0.4)
        ax.add_patch(arrow)

    def draw_point(self, ax, point, str_for_point=None, color='green'):
        if str_for_point is None:
            str_for_point='o'
        else:
            str_for_point='$'+str_for_point + '$'
        ax.scatter(point.x, point.y, c=[color], marker=str_for_point, alpha=0.6, s=200)



if __name__ == '__main__':
    pic = Pic()
    #pic.show()

    fig, ax = plt.subplots()
    pic.draw_to_ax(ax)
    center_point = pic.get_center_point()
    next_point = center_point + Point(5, 8)
    pic.draw_point(ax, center_point, '1')
    pic.draw_point(ax, next_point)
    pic.connect_two_points_by_arrow(ax, center_point, next_point)
    pic.annotate_point(ax, next_point, 'bla bla')

    plt.show()
    plt.close(fig)


    print(pic.get_mean())
    sample = pic.get_sample_b1()
    plt.hist(sample)
    plt.show()


