from test_platform.solvers.best_interval_chooser import BestIntervalChooser
from test_platform.solvers.greedy_algorithm import GreedySolver
from test_platform.solvers.greedy_algorithm_be_resources import GreedyByResouresSolver
from test_platform.solvers.greedy_long_at_first_solver import GreedyLongFirstSolver
from test_platform.solvers.human_solver import HumanSolver
from test_platform.solvers.minizinc_solver import Minizinc
from test_platform.solvers.power_2_more_capacity_wrapper import Power2SolverMoreCapacityWrapper
from test_platform.solvers.power_2_algorithm import Power2Solver
from test_platform.categories_modificators.courses_joiner_high import CoursesJoinerHigh
from test_platform.categories_modificators.courses_joiner_low import CoursesJoinerLow
from test_platform.evaluator import Evaluator
import datetime

def __test_solver(solver):
    evaluator = Evaluator(solver, solver.get_name())
    evaluator.evaluate_solver(verbose=False)

def test_RealStartlists():
    __test_solver(HumanSolver())

def test_GenGreedyHighInt():
    __test_solver(BestIntervalChooser(GreedySolver(CoursesJoinerHigh()), CoursesJoinerHigh()))

def test_GenGreedyLowInt():
    __test_solver(BestIntervalChooser(GreedySolver(CoursesJoinerLow()), CoursesJoinerLow()))

def test_GreedyLengthHighInt():
    __test_solver(BestIntervalChooser(GreedyLongFirstSolver(CoursesJoinerHigh()), CoursesJoinerHigh()))

def test_GreedyLengthLowInt():
    __test_solver(BestIntervalChooser(GreedyLongFirstSolver(CoursesJoinerLow()), CoursesJoinerLow()))

def test_GreedyResHighInt():
    __test_solver(BestIntervalChooser(GreedyByResouresSolver(CoursesJoinerHigh()), CoursesJoinerHigh()))

def test_GreedyResLowInt():
    __test_solver(BestIntervalChooser(GreedyByResouresSolver(CoursesJoinerHigh()), CoursesJoinerHigh()))

def test_DoublingHighIntFull():
    __test_solver(Power2SolverMoreCapacityWrapper(Power2Solver(CoursesJoinerHigh(),improved=False), CoursesJoinerHigh()))

def test_DoublingHighIntHalf():
    __test_solver(Power2SolverMoreCapacityWrapper(Power2Solver(CoursesJoinerHigh(),improved=True), CoursesJoinerHigh()))


def test_DoublingLowIntFull():
    __test_solver(
        Power2SolverMoreCapacityWrapper(Power2Solver(CoursesJoinerLow(), improved=False), CoursesJoinerLow()))


def test_DoublingLowIntHalf():
    __test_solver(
        Power2SolverMoreCapacityWrapper(Power2Solver(CoursesJoinerLow(), improved=True), CoursesJoinerLow()))

def test_ConsProg(timeout_in_sec):
    __test_solver(Minizinc(timeout=datetime.timedelta(seconds=timeout_in_sec)))

def test_all_methods():
    test_RealStartlists()
    test_GenGreedyHighInt()
    test_GenGreedyLowInt()
    test_GreedyLengthHighInt()
    test_GreedyLengthLowInt()
    test_GreedyResHighInt()
    test_GreedyResLowInt()
    test_DoublingHighIntFull()
    test_DoublingHighIntHalf()
    test_DoublingLowIntFull()
    test_DoublingLowIntHalf()
    test_ConsProg(timeout_in_sec=1)
    test_ConsProg(timeout_in_sec=10)
    test_ConsProg(timeout_in_sec=60)
    test_ConsProg(timeout_in_sec=600)
    test_ConsProg(timeout_in_sec=3600)

if __name__ == "__main__":
    test_all_methods()

