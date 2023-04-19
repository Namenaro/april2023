from w_disent import W_Dis_Evaluator
from picture_wrapper import Pic
from common_utils import HtmlLogger, Point
from default_predictions import DefaultPredictionsGeneratorNaive

import matplotlib.pyplot as plt
import math

# правая кропка закрыть
class Tester:
    def __init__(self, logname):
        self.pic = Pic()
        self.default_generator = DefaultPredictionsGeneratorNaive(self.pic)
        self.w_dis_evaluator = W_Dis_Evaluator(self.pic, self.default_generator)
        self.logger = HtmlLogger(logname)

        self.fig = plt.figure(logname)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        if event.button != 1: # правая кропка закрыть
            plt.close()
            return
        # получаем данные клика
        x = math.ceil(event.xdata)
        y = math.ceil(event.ydata)
        point = Point(x=x, y=y)
        radius = int(input("Enter radius: "))

        # отрисовываем рез-ты клика красным
        rect = plt.Rectangle((x - radius / 2, y - radius / 2), width=radius, height=radius, fc='red', alpha=0.4)
        plt.gca().add_patch(rect)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # проводим оценку w_dis в текущем констексте
        point_cloud = self.pic.get_point_cloud(point, radius)
        predicted_mean = self.pic.get_mean_val_in_point_cloud(point_cloud)
        w = self.w_dis_evaluator.w_for_vicinity(center_point=point, radius=radius, predicted_mean=predicted_mean)
        print("w_dis = " + str(w))

        # добавляем новый факт из этого клика в контекст
        self.default_generator.add_fact(fact_points=point_cloud, fact_mean=predicted_mean)

        # отрисовываем изменившийся конекст в хтмл-логгер
        fig, ax = plt.subplots()
        self.default_generator.draw_to_ax(ax)
        self.logger.add_fig(fig)


    def run_test(self):
        plt.imshow(self.pic.img, cmap='gray')
        plt.show()

if __name__ == '__main__':
    tester = Tester("momental_w_dis_test")
    tester.run_test()
