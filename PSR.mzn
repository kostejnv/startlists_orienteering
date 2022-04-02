% minizinc definition of model of PSR solver
%includes
include "global_cardinality_low_up_closed.mzn";
include "disjunctive.mzn";


% data
enum Categories = {H21,D21,H16};

array[Categories] of int: idxs = 1..length(Categories); % for ordering the categories
array[Categories] of int: gs = [2,2,3]; % minimal periods
array[Categories] of int: ps = [30,30,10]; % number of athletes
%array[Categories] of string: rs = ["31","31"]; % first controls of categories
array[Categories] of string: cs = ["HE","DE","HE"]; % courses of categories
int: capacity = 1;

int: upperBoundLength = 500;
int: lowerBoundLength = 0;
int: maxG = upperBoundLength div max(ps);

% variables
array[Categories] of var 0..upperBoundLength-1: Ss; %starts
array[Categories] of var 0..maxG: Gs; %periods
var lowerBoundLength..upperBoundLength: cmax; %end of schedule

%functions
function var int: finish(var Categories: cat_idx) = (ps[cat_idx]-1) * Gs[cat_idx] + Ss[cat_idx];

%function array[int] of int: all_start_times(var Categories: i) = [Ss[i] + Gs[i]*t| t in 0..ps[i]-1];

% constraints
%-----------------------------------------------
% cmax definition
constraint cmax = max([finish(i) | i in Categories]);

% G is at least g
constraint forall([gs[i] <= Gs[i] | i in Categories]);

% Gs posibilities based on cmax and start of category
constraint forall([Gs[i] <= ((cmax - Ss[i]) div (ps[i] - 1)) | i in Categories]);

% gap between categories with same courses
constraint forall([ if Ss[i] > finish(j)
                        then Ss[i]-finish(j) >= max([Gs[i], Gs[j]])
                    elseif Ss[j] > finish(j)
                        then Ss[j]-finish(i) >= max([Gs[i], Gs[j]])
                    else false endif
                    | i,j in Categories where idxs[j] > idxs[i] /\ cs[i] == cs[j]]);

% capacity contraint
constraint global_cardinality_low_up_closed([Ss[H21] + Gs[H21]*t| t in 0..ps[H21]-1] ++ [Ss[D21] + Gs[D21]*t| t in 0..ps[D21]-1] ++ [Ss[H16] + Gs[H16]*t| t in 0..ps[H16]-1],
                                            [i| i in 0..upperBoundLength],
                                            [0| i in 0..upperBoundLength],
                                            [capacity|i in 0..upperBoundLength]);

% resources constraint - atheltes of categories with same 1st control cannot start at the same time
%it must be define for all resources
constraint disjunctive([Ss[H21] + Gs[H21]*t| t in 0..ps[H21]-1] ++ [Ss[D21] + Gs[D21]*t| t in 0..ps[D21]-1],
                        [1| i in 1..sum([ps[H21],ps[D21]])]);
% ----------------------------------------------
% solve
solve minimize cmax;

output ["Cmax: \(cmax)\n"] ++ ["\(i)\tstart: \(Ss[i])\tperiod: \(Gs[i]) \n" | i in Categories];