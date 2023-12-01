# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dimod import ConstrainedQuadraticModel, QuadraticModel
from dwave.system import LeapHybridCQMSampler


# Set the solver we're going to use
def set_sampler():
    '''Returns a dimod sampler'''

    sampler = LeapHybridCQMSampler()

    return sampler


# Set employees and preferences
def employee_preferences():
    '''Returns a dictionary of employees with their preferences'''

    preferences = {"Anna": [1, 2, 3, 4],
                   "Bill": [3, 2, 1, 4],
                   "Chris": [4, 2, 3, 1],
                   "Diane": [4, 1, 2, 3],
                   "Erica": [1, 2, 3, 4],
                   "Frank": [3, 2, 1, 4],
                   "George": [4, 2, 3, 1],
                   "Harriet": [4, 1, 2, 3]}

    return preferences


# Create CQM object
def build_cqm():
    '''Builds the CQM for our problem'''

    preferences = employee_preferences()
    num_shifts = 4

    # Initialize the CQM object
    cqm = ConstrainedQuadraticModel()

    # Represent shifts as a set of binary variables
    # for each employee
    for employee, preference in preferences.items():
        # Create labels for binary variables
        labels = [f"x_{employee}_{shift}" for shift in range(num_shifts)]

        # Add a discrete constraint over employee binaries
        cqm.add_discrete(labels, label=f"discrete_{employee}")

        # Incrementally add objective terms as list of (label, bias)
        cqm.objective.add_linear_from([*zip(labels, preference)])

    # TODO: Restrict Anna from working shift 4
    constraint = QuadraticModel()
    constraint.add_variable('BINARY', "x_Anna_4")
    constraint.set_linear("x_Anna_4", 1)
    cqm.add_constraint(constraint, sense="==", rhs=0, label="Anna 4")

    # TODO: Set constraints to reflect the restrictions in the README.
    constraint_EH = QuadraticModel()
    for s in range(num_shifts):
        # Bill and Frank don't want to work together
        constraint_BF = QuadraticModel()
        constraint_BF.add_variable('BINARY', f"x_Bill_{s}")
        constraint_BF.add_variable('BINARY', f"x_Frank_{s}")
        constraint_BF.set_quadratic(f"x_Bill_{s}", f"x_Frank_{s}", 1)
        cqm.add_constraint(constraint_BF, sense="==", rhs=0,
                           label="BF_shift_" + str(s))

        # Erica and Harriet want to work together
        constraint_EH.add_variable('BINARY', f"x_Erica_{s}")
        constraint_EH.add_variable('BINARY', f"x_Harriet_{s}")
        constraint_EH.set_quadratic(f"x_Erica_{s}", f"x_Harriet_{s}", 1)

    cqm.add_constraint(constraint_EH, sense="==", rhs=1, label="E_H")

    # 2 employees per shift
    for s in range(num_shifts):
        constraint_2 = QuadraticModel()

        for employee in preferences.keys():
            constraint_2.add_variable('BINARY', f"x_{employee}_{s}")
            constraint_2.set_linear(f"x_{employee}_{s}", 1)

        cqm.add_constraint(constraint_2, sense="==", rhs=2,
                           label=f"2_shift_{s}")

    print(cqm)

    return cqm


# Solve the problem
def solve_problem(cqm, sampler):
    '''Runs the provided cqm object on the designated sampler'''

    # Initialize the CQM solver
    sampler = set_sampler()

    # Solve the problem using the CQM solver
    sampleset = sampler.sample_cqm(cqm, label='Training - Employee Scheduling')

    # Filter for feasible samples
    feasible_sampleset = sampleset.filter(lambda x: x.is_feasible)

    return feasible_sampleset


# Process solution
def process_sampleset(sampleset):
    '''Processes the best solution found for displaying'''

    # Get the first solution
    sample = sampleset.first.sample

    shift_schedule = [[] for i in range(4)]

    # Interpret according to shifts
    for key, val in sample.items():
        if val == 1.0:
            name = key.split('_')[1]
            shift = int(key.split('_')[2])
            shift_schedule[shift].append(name)

    return shift_schedule


## ------- Main program -------
if __name__ == "__main__":

    # Problem information
    shifts = [1, 2, 3, 4]
    num_shifts = len(shifts)

    cqm = build_cqm()

    sampler = set_sampler()

    sampleset = solve_problem(cqm, sampler)

    shift_schedule = process_sampleset(sampleset)

    for i in range(num_shifts):
        print("Shift:", shifts[i], "\tEmployee(s): ", shift_schedule[i])
