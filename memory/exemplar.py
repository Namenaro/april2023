from common_utils import Point

class  Exemplar:
    def __init__(self):
        self.global_ids_to_points = {} # global_id: Point
        self.global_ids_to_vals_clouds = {} # global_id : [val1, val_2,....]