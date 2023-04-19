import numpy as np

from picture_wrapper import Pic
from common_utils import Distr
from default_predictions import DefaultPredictionsGeneratorNaive


class W_Dis_Evaluator:
    def __init__(self, pic, defualt_generator):
        self .pic = pic
        self.default_generator = defualt_generator

    def w_for_vicinity(self, center_point, radius, predicted_mean):
        points_cloud = self.pic.get_point_cloud(center_point, radius)
        cloud_default_vals = self.default_generator.get_points_vals_predictions(points_cloud)
        cloud_real_vals = self.pic.get_vals_of_point_cloud(points_cloud)
        w = w_for_cloudA(self.pic.distr, cloud_real_vals=cloud_real_vals, cloud_default_vals=cloud_default_vals, predicted_mean=predicted_mean)
        return w


#######################################################################
def w_for_1(distr, real_val, predicted_val, default_val):
    curr_profit = 1 - distr.get_p_of_event(real_val, default_val)
    new_profit = 1 - distr.get_p_of_event(real_val, predicted_val)
    w = new_profit - curr_profit
    return w

def w_for_cloudA(distr, cloud_real_vals, cloud_default_vals, predicted_mean):
    w = 0
    for i in range(len(cloud_real_vals)):
        w += w_for_1(distr, real_val=cloud_real_vals[i], predicted_val=predicted_mean, default_val=cloud_default_vals[i])
    return w

def w_for_cloudB(distr, cloud_real_vals, cloud_default_vals, predicted_mean):
    w = 0
    real_mean = np.mean(cloud_real_vals)
    for i in range(len(cloud_real_vals)):
        w += w_for_1(distr, real_val=real_mean, predicted_val=predicted_mean, default_val=cloud_default_vals[i])
    return w
