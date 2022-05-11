from entities.event import Event
from entities.category import Category
from solvers.minizinc_solver import Minizinc
import datetime
from categories_modificators.utils import to_dict

def create_event():
    cats = []

    cat1 = Category('C1')
    cat1.course = 'r1'
    cat1.first_control = 'f1'
    cat1.vacants_count = 32
    cat1.min_interval = 2
    cats.append(cat1)

    cat1 = Category('C2')
    cat1.course = 'r2'
    cat1.first_control = 'f1'
    cat1.vacants_count = 5
    cat1.min_interval = 4
    cats.append(cat1)

    cat1 = Category('C3')
    cat1.course = 'r3'
    cat1.first_control = 'f2'
    cat1.vacants_count = 20
    cat1.min_interval = 2
    cats.append(cat1)

    cat1 = Category('C4')
    cat1.course = 'r3'
    cat1.first_control = 'f2'
    cat1.vacants_count = 9
    cat1.min_interval = 3
    cats.append(cat1)

    event = Event(111,'example',None, 'KL', 'PR')
    event.capacity = 6
    event.categories = to_dict(cats)
    return event

event = create_event()

solver = Minizinc(timeout=datetime.timedelta(days=2))
print(solver.get_upperBound(event))
print(solver.get_lowerBound(event))
print(solver.generate_str_model(event))
