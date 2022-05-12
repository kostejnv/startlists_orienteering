

class Category:
    def __init__(self, name):
        self.name = name
        self.athletes = []
        self.min_interval = 1
        self.vacants_count = 0
        self.categories_w_same_course = []
        self.first_control = "-1"
        self.course = None
        self.near_category = []
        self.far_category = []
        self.final_interval = None
        self.final_start = None
        self.has_interval_start = True

    def get_category_count(self):
        return len(self.athletes) + self.vacants_count