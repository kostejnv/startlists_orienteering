import json


class ConstrainsManager:
    def __init__(self, file):
        self.constraints = json.load(file)

    def add_constraints_to_cats(self, cats, discipline, apply_JE_rules=True):
        if apply_JE_rules:
            cats = self.__apply_JE_rules(cats, discipline)

        # set default value for final interval
        for cat in cats.values():
            cat.final_interval = cat.min_interval
        return cats

    def __apply_JE_rules(self, cats, discipline):
        # mark categories without interval start
        for cat_name, cat_data in cats.items():
            if cat_name in ['HDR', 'T', 'P', 'T4', 'P2', 'T-FIT', 'T-OPEN', 'T10P',
                            'T10']: cat_data.has_interval_start = False

        if discipline == 'SP':
            cats = self.__apply_JE_rules_for_sprint(cats)
        else:  # 'KT' 'KL'
            cats = self.__apply_JE_rules_for_middle_and_long(cats)
        return cats

    def __apply_JE_rules_for_sprint(self, cats):
        for cat_name, cat_data in cats.items():
            if cat_name in ['H10', 'D10', 'H12', 'D12']:
                cat_data.min_interval = 2
            else:
                cat_data.min_interval = 1
        return cats

    def __apply_JE_rules_for_middle_and_long(self, cats):
        for cat_name, cat_data in cats.items():
            if len(cat_data.athletes) <= 8:
                cat_data.min_interval = 6
            elif len(cat_data.athletes) <= 15:
                cat_data.min_interval = 3
            else:
                if cat_name in ['H10', 'D10', 'H12', 'D12', 'H14', 'D14']:
                    cat_data.min_interval = 3
                else:
                    cat_data.min_interval = 2
        return cats
