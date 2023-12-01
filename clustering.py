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
import math
from collections import defaultdict
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import dwavebinarycsp
import dwave.inspector
from dwave.system import EmbeddingComposite, DWaveSampler


def get_groupings(sample):
    """Grab selected items and group them by color"""
    colored_points = defaultdict(list)

    for label, bool_val in sample.items():
        # Skip over items that were not selected
        if not bool_val:
            continue

        # Parse selected items
        # Note: label look like "<x_coord>,<y_coord>_<color>"
        coord, color = label.split("_")
        coord_tuple = tuple(map(float, coord.split(",")))
        colored_points[color].append(coord_tuple)

    return dict(colored_points)


def visualize_groupings(groupings_dict, filename):
    """
    Args:
        groupings_dict: key is a color, value is a list of x-y coordinate tuples.
          For example, {'r': [(0,1), (2,3)], 'b': [(8,3)]}
        filename: name of the file to save plot in
    """
    for color, points in groupings_dict.items():
        # Ignore items that do not contain any coordinates
        if not points:
            continue

        # Populate plot
        point_style = color + "o"
        plt.plot(*zip(*points), point_style)

    plt.savefig(filename)


def visualize_scatterplot(x_y_tuples_list, filename):
    """Plotting out a list of x-y tuples

    Args:
        x_y_tuples_list: A list of x-y coordinate values. e.g. [(1,4), (3, 2)]
    """
    plt.plot(*zip(*x_y_tuples_list), "o")
    plt.savefig(filename)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # coordinate labels for groups red, green, and blue
        label = "{0},{1}_".format(x, y)
        self.r = label + "r"
        self.g = label + "g"
        self.b = label + "b"


def get_distance(coordinate_0, coordinate_1):
    diff_x = coordinate_0.x - coordinate_1.x
    diff_y = coordinate_0.y - coordinate_1.y

    return math.sqrt(diff_x**2 + diff_y**2)


def get_max_distance(coordinates):
    max_distance = 0
    for i, coord0 in enumerate(coordinates[:-1]):
        for coord1 in coordinates[i+1:]:
            distance = get_distance(coord0, coord1)
            max_distance = max(max_distance, distance)

    return max_distance


def cluster_points(scattered_points, filename, problem_inspector):
    """Perform clustering analysis on given points

    Args:
        scattered_points (list of tuples):
            Points to be clustered
        filename (str):
            Output file for graphic
        problem_inspector (bool):
            Whether to show problem inspector
    """
    # Set up problem
    # Note: max_distance gets used in division later on. Hence, the max(.., 1)
    #   is used to prevent a division by zero
    coordinates = [Coordinate(x, y) for x, y in scattered_points]
    max_distance = max(get_max_distance(coordinates), 1)

    # Build constraints
    csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

    # Apply constraint: coordinate can only be in one colour group
    choose_one_group = {(0, 0, 1), (0, 1, 0), (1, 0, 0)}
    for coord in coordinates:
        csp.add_constraint(choose_one_group, (coord.r, coord.g, coord.b))

    # Build initial BQM
    bqm = dwavebinarycsp.stitch(csp)

    # Edit BQM to bias for close together points to share the same color
    for i, coord0 in enumerate(coordinates[:-1]):
        for coord1 in coordinates[i+1:]:
            # Set up weight
            d = get_distance(coord0, coord1) / max_distance  # rescale distance
            weight = -math.cos(d*math.pi)

            # Apply weights to BQM
            bqm.add_interaction(coord0.r, coord1.r, weight)
            bqm.add_interaction(coord0.g, coord1.g, weight)
            bqm.add_interaction(coord0.b, coord1.b, weight)

    # Edit BQM to bias for far away points to have different colors
    for i, coord0 in enumerate(coordinates[:-1]):
        for coord1 in coordinates[i+1:]:
            # Set up weight
            # Note: rescaled and applied square root so that far off distances
            #   are all weighted approximately the same
            d = math.sqrt(get_distance(coord0, coord1) / max_distance)
            weight = -math.tanh(d) * 0.1

            # Apply weights to BQM
            bqm.add_interaction(coord0.r, coord1.b, weight)
            bqm.add_interaction(coord0.r, coord1.g, weight)
            bqm.add_interaction(coord0.b, coord1.r, weight)
            bqm.add_interaction(coord0.b, coord1.g, weight)
            bqm.add_interaction(coord0.g, coord1.r, weight)
            bqm.add_interaction(coord0.g, coord1.b, weight)

    # Submit problem to D-Wave sampler
    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample(bqm,
                               chain_strength=4,
                               num_reads=1000,
                               label='Example - Clustering')
    best_sample = sampleset.first.sample

    # Visualize graph problem
    if problem_inspector:
        dwave.inspector.show(bqm, sampleset)

    # Visualize solution
    groupings = get_groupings(best_sample)
    visualize_groupings(groupings, filename)

    # Print solution onto terminal
    # Note: This is simply a more compact version of 'best_sample'
    print(groupings)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--no-problem-inspector', action='store_false', dest='problem_inspector', help='do not show problem inspector')
    args = parser.parse_args()

    # Simple, hardcoded data set
    scattered_points = [(0, 0), (1, 1), (2, 4), (3, 2)]

    # Save the original, un-clustered plot
    orig_filename = "four_points.png"
    visualize_scatterplot(scattered_points, orig_filename)

    # Find clusters
    # Note: the key part of this demo is in the construction of this function
    clustered_filename = "four_points_clustered.png"
    cluster_points(scattered_points, clustered_filename, args.problem_inspector)

    print("Your plots are saved to '{}' and '{}'.".format(orig_filename,
                                                     clustered_filename))