from input_manager.classes_manager import Classes_manager
from input_manager.entries_manager import Entries_manager
from input_manager.courses_manager import Courses_manager
from input_manager.startlists_manager import Startlist_manager
from input_manager.constraints_manager import ConstrainsManager
from input_manager.event_manager import Event_manager
from entities.event import Event


class Input_manager:
    def __init__(self, event_id):
        self.event_id = event_id

    def get_event(self):
        # add categories
        event_path = f'data/{self.event_id}'
        with open(f"{event_path}/event_info.json", "r") as event_f:
            event = Event_manager(event_f).get_event()
        with open(f"{event_path}/event_info.json", "r") as event_f:
            cats = Classes_manager(event_f).get_categories()  # get names of categories from event info
        with open(f"{event_path}/startlists.json", "r") as startlists_f:
            cats = Startlist_manager(startlists_f).add_athletes(cats)  # add entered atheletes to categories
        with open(f"{event_path}/courses.txt", "r") as courses_f:
            cats = Courses_manager(courses_f).add_courses_info_to_cats(cats)  # add info about courses to categories
        with open(f"{event_path}/category_constraints.json", "r") as constraints_f:
            cats = ConstrainsManager(constraints_f).add_constraints_to_cats(cats,
                                                                            event.discipline)  # get organizers preferences
        event.categories = cats

        # add startlist data
        with open(f"{event_path}/startlists.json", "r") as startlists_f:
            startlists_manager = Startlist_manager(startlists_f)
            event.capacity = startlists_manager.get_capacity(event) # capacity from human startlists
            event.categories = startlists_manager.add_vacants(event.categories) # add vacants based on human startlist

        return event
