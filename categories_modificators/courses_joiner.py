from entity.category import Category

def create_merge_cat(cats, index):
    interval = max([cat.min_interval for cat in cats])
    athletes = sum([cat.get_category_count() for cat in cats])
    category = Category(index)
    category.min_interval = interval
    category.vacants_count = athletes
    category.first_control = cats[0].first_control
    return category


class CoursesJoiner:
    def __init__(self):
        self.was_joined = False

    def join(self, categories):
        self.was_joined = True
        index = 0
        self.groups_of_cats = {}

        cats_indices = {}
        for cat in categories.values():
            if cat.name not in cats_indices:
                cats_indices[cat.name] = index
                for same_course_cat in cat.categories_w_same_course:
                    if same_course_cat in categories:
                        cats_indices[same_course_cat] = index
                index += 1

        for cat_name, index in cats_indices.items():
            if index in self.groups_of_cats:
                self.groups_of_cats[index].append(categories[cat_name])
            else:
                self.groups_of_cats[index] = [categories[cat_name]]

        merged_categories = {}
        for index, cats in self.groups_of_cats.items():
            merged_categories[index] = create_merge_cat(cats, index)
        return merged_categories


    def disjoin(self, solved_merged_categories):
        if not self.was_joined:
            raise "at first join must be ran"

        final_categories = {}
        for solved_merged_cat in solved_merged_categories.values():
            for final_cat in self.__disjoint_cat(solved_merged_cat):
                final_categories[final_cat.name] = final_cat
        return final_categories

    def __disjoint_cat(self, solved_merged_cat):
        act_start = solved_merged_cat.final_start
        for final_cat in self.groups_of_cats[solved_merged_cat.name]:
            final_cat.final_interval = solved_merged_cat.final_interval
            final_cat.final_start = act_start
            act_start += final_cat.get_category_count() * final_cat.final_interval
        return self.groups_of_cats[solved_merged_cat.name]
