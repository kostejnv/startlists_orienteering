import datetime

from solvers.solver import Solver
from minizinc import Instance, Model
from minizinc import Solver as MZNSolver
from copy import deepcopy


from solvers.power_2_more_capacity_wrapper import Power2SolverMoreCapacityWrapper
from solvers.best_interval_chooser import BestIntervalChooser
from solvers.power_2_algorithm import Power2Solver
from solvers.greedy_long_at_first_solver import GreedyLongFirstSolver
from solvers.greedy_algorithm_be_resources import GreedyByResouresSolver
from solvers.lower_bound_solver import LowerBoundSolver


class Minizinc(Solver):
    def __init__(self):
        pass

    def solve(self, event):
        gecode = MZNSolver.lookup("gecode")
        instance = self.__get_instance(event, gecode)
        result = instance.solve(timeout=datetime.timedelta(minutes=20))
        solved_categories, schedule_length = self.__convert_result(result, event)
        return solved_categories, schedule_length

    def get_name(self):
        return 'Minizinc'

    def __get_instance(self, event, solver):
        model = self.__generate_model(event)
        instance = self.__generate_instance(model, solver, event)
        return instance

    def __convert_result(self, result, event):
        solved_cats = event.get_not_empty_categories_with_interval_start()
        for idx, cat in enumerate(solved_cats.values()):
            cat.final_start = result["Ss"][idx]
            cat.final_interval = result["Gs"][idx]
        schedule_length = result["cmax"] + 1
        return solved_cats, schedule_length

    def __generate_model(self, event):
        model = Model()
        model_definition = f'''
                % minizinc definition of model of PSR solver
                %includes
                include "global_cardinality_low_up_closed.mzn";
                include "alldifferent.mzn";
                
                
                % data
                enum Categories = {self.__generate_categories(event)};
                
                array[Categories] of int: idxs = 1..length(Categories); % for ordering the categories
                array[Categories] of int: gs; % minimal periods
                array[Categories] of int: ps; % number of athletes
                array[Categories] of string: cs; % courses of categories
                int: capacity;
                
                int: upperBoundLength;
                int: lowerBoundLength;
                int: maxG = (upperBoundLength+1) div (max(ps));
                
                % variables
                array[Categories] of var 0..upperBoundLength: Ss; %starts
                array[Categories] of var 0..upperBoundLength: Gs; %periods
                var lowerBoundLength..upperBoundLength: cmax; %end of schedule
                
                %functions
                function var int: finish(var Categories: cat_idx) = (ps[cat_idx]-1) * Gs[cat_idx] + Ss[cat_idx];
                
                
                % constraints
                %-----------------------------------------------
                % cmax definition
                constraint cmax = max([finish(i) | i in Categories]);
                
                % G is at least g
                constraint forall([gs[i] <= Gs[i] | i in Categories]);
                
                % Gs posibilities based on cmax and start of category
                %constraint forall([cmax >= (ps[i]-1)*Gs[i]+Ss[i] | i in Categories]);
                
                % gap between categories with same courses
                constraint forall([ if Ss[i] > finish(j)
                                        then Ss[i]-finish(j) >= max([Gs[i], Gs[j]])
                                    elseif Ss[j] > finish(j)
                                        then Ss[j]-finish(i) >= max([Gs[i], Gs[j]])
                                    else false endif
                                    | i,j in Categories where idxs[j] > idxs[i] /\ cs[i] == cs[j]]);
                
                % capacity contraint    
                {self.__generate_capacity_constraint(event)}
        
                
                % resources constraint - atheltes of categories with same 1st control cannot start at the same time
                %it must be define for all resources
                {self.__generate_resources_constraint(event)}
                
                % ----------------------------------------------
                % solve
                solve minimize cmax;
                
                output ["Cmax: \(cmax)\\n"] ++ ["\(i)\\tstart: \(Ss[i])\\tperiod: \(Gs[i]) \\n" | i in Categories];
            '''

        model.add_string(model_definition)
        return model

    def __generate_instance(self, model, solver, event):
        instance = Instance(solver, model)

        # add variables
        cats = event.get_not_empty_categories_with_interval_start()
        instance["gs"] = [cat.min_interval for cat in cats.values()]
        instance["ps"] = [cat.get_category_count() for cat in cats.values()]
        instance["cs"] = [cat.course for cat in cats.values()]
        instance["upperBoundLength"] = self.__get_upperBound(deepcopy(event)) - 1
        instance["lowerBoundLength"] = self.__get_lowerBound(deepcopy(event)) - 1
        instance['capacity'] = event.capacity

        return instance

    def __generate_capacity_constraint(self, event):
        cats = event.get_not_empty_categories_with_interval_start()
        return f'''
            constraint global_cardinality_low_up_closed({self.__generate_all_athletes_starts_query(cats.values())},
                                            [i| i in 0..upperBoundLength],
                                            [0| i in 0..upperBoundLength],
                                            [capacity|i in 0..upperBoundLength]);
        '''

    def __generate_resources_constraint(self, event):
        cats = event.get_not_empty_categories_with_interval_start()
        resources = set([cat.first_control for cat in cats.values()])
        return '\n\n'.join([self.__generate_constraint_for_given_resources(res, cats.values()) for res in resources])



    def __get_upperBound(self, event):
        _, power2_result = Power2SolverMoreCapacityWrapper(Power2Solver(improved=True)).solve(deepcopy(event))
        _, greedy_long_result = BestIntervalChooser(GreedyLongFirstSolver()).solve(deepcopy(event))
        _, greedy_resources_result = BestIntervalChooser(GreedyByResouresSolver()).solve(deepcopy(event))
        return min([power2_result,greedy_long_result, greedy_resources_result])

    def __get_lowerBound(self, event):
        _, lower_bound = LowerBoundSolver().solve(deepcopy(event))
        return lower_bound

# [self.__generate_category_all_starts_query(cat) + (" ++ " if idx < len(cats) - 1 else "") for idx, cat in enumerate(cats.values())] #TODO: check it

    def __generate_all_athletes_starts_query(self, cats):
        query = ""
        for idx, cat in enumerate(cats):
            query += self.__generate_category_all_starts_query(cat)
            query += " ++ " if idx < len(cats) - 1 else ""
        return query

    def __generate_constraint_for_given_resources(self, res, cats):
        res_cats = [cat for cat in cats if cat.first_control == res]
        constraint = f'''
                        constraint alldifferent({self.__generate_all_athletes_starts_query(res_cats)});
        ''' if len(res_cats) > 1 else ""
        return constraint

    def __generate_category_all_starts_query(self, cat):
        cat_name = cat.name.replace("-", "")
        return f"[Ss[{cat_name}] + Gs[{cat_name}]*t| t in 0..ps[{cat_name}]-1]"

    def __generate_categories(self, event):
        cats = event.get_not_empty_categories_with_interval_start()
        cat_str = "{"
        for idx, cat in enumerate(cats.values()):
            cat_str += cat.name.replace("-", "")
            cat_str += ", " if idx < len(cats) - 1 else ""
        return cat_str + '}'

            
            