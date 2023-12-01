# Copyright 2021 D-Wave Systems Inc.
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

# TODO: Import any required packages here

from dimod import ConstrainedQuadraticModel, Binary, quicksum
from dwave.system import LeapHybridCQMSampler

import csv
import numpy as np
import pandas as pd

# Prepare Stock data from the given csv files
def get_stock_info(verbose=False):
    """Read in stock returns and price information from CSV."""

    # Read the lastday's closing price from csv file,
    # and store them in the list, then convert it as numpy array
    price_read = []
    with open('data/lastday_closing_price.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            price_read.append(row)
    price = np.array(price_read[0],dtype=float)

    # Compute the average monthly returns for each stock
    df_monthreturn = pd.read_csv("data/monthly_returns.csv", index_col='Date')
    ave_monthly_returns = df_monthreturn.mean(axis=0)
    returns = list(ave_monthly_returns)

    # Compute the variance from the monthly returns
    variance = df_monthreturn.cov().values.tolist()

    if verbose:
        print("Data Check")
        print("Monthly return(the first 5 lines):")
        print(df_monthreturn.head(5))
        print("Average monthly return:")
        print(returns)

    return price, returns, variance

# Function to process samples and print the best feasible solution found
def process_sampleset(sampleset, stockcodes):
    """Read in sampleset returned from sample_cqm command and display solution."""

    # Find the first feasible solution
    first_run = True
    feasible = False
    for sample, feas in sampleset.data(fields=['sample','is_feasible']):
        if first_run:
            best_sample = sample
        if feas:
            best_sample = sample
            feasible = True
            break

    # Print the solution as which stocks to buy
    print("Solution:\n")
    if not feasible:
        print("No feasible solution found.\n")
    else:
        print("Best feasible solution found:")
        for stk in stockcodes:
            if best_sample[f's_{stk}'] == 1:
                print(stk)
    print("\n")


def define_variables(stockcodes):
    """Define the variables to be used for the CQM.
    Args:
        stockcodes (list): List of stocks under consideration

    Returns:
        stocks (list):
            List of variables named 's_{stk}' for each stock stk in stockcodes, where stk is replaced by the stock code.
    """

    # TODO: Define your list of variables and call it stocks
    ## Hint: Remember to import the required package at the top of the file for Binary variables
    stocks = [Binary(f's_{i}') for i in stockcodes]

    return stocks


def define_cqm(stocks, num_stocks_to_buy, price, returns, budget, variance):
    """Define a CQM for the exercise.
    Requirements:
        Objectives:
            - Maximize returns
            - Minimize variance
        Constraints:
            - Choose exactly num_stocks_to_buy stocks
            - Spend at most budget on purchase

    Args:
        stocks (list):
            List of variables named 's_{stk}' for each stock in stockcodes
        num_stocks_to_buy (int): Number of stocks to purchase
        price (list):
            List of current price for each stock in stocks
                where price[i] is the price for stocks[i]
        returns (list):
            List of average monthly returns for each stock in stocks
                where returns[i] is the average returns for stocks[i]
        budget (float):
            Budget for purchase
        variance (2D numpy array):
            Entry [i][j] is the variance between stocks i and j

    Returns:
        cqm (ConstrainedQuadraticModel)
    """

    # TODO: Initialize the ConstrainedQuadraticModel called cqm
    ## Hint: Remember to import the required package at the top of the file for ConstrainedQuadraticModels
    cqm = ConstrainedQuadraticModel()

    # TODO: Add a constraint to choose exactly num_stocks_to_buy stocks
    ## Important: Use the label 'choose k stocks', this label is case sensitive
    cqm.add_constraint(
        quicksum(stocks[i] for i in range(len(stocks))) <= num_stocks_to_buy,
        label='choose k stocks')

    # TODO: Add a constraint that the cost of the purchased stocks is less than or equal to the budget
    ## Important: Use the label 'budget_limitation', this label is case sensitive and uses an underscore
    cqm.add_constraint(
        quicksum(price[i] * stocks[i] for i in range(len(stocks))) <= budget,
        label='budget_limitation')

    # TODO: Add an objective function maximize returns AND minimize variance
    ## Hint: Determine each objective separately then add them together
    ## Hint: Variance is computed as a quadratic term: variance[i][j]*stocks[i]*stocks[j]
    # set object는 뒤에만 처리함

    objective = []
    for i in range(len(stocks)):
        objective.append(-1 * returns[i] * stocks[i])
        for j in range(i + 1, len(stocks)):
            objective.append(variance[i][j] * stocks[i] * stocks[j])

    cqm.set_objective(quicksum(objective))

    return cqm


def sample_cqm(cqm):
    # TODO: Define your sampler as LeapHybridCQMSampler
    ## Hint: Remember to import the required package at the top of the file
    sampler = LeapHybridCQMSampler()

    # TODO: Sample the ConstrainedQuadraticModel cqm and store the result in sampleset
    sampleset = sampler.sample_cqm(cqm)

    return sampleset


if __name__ == '__main__':
    # 10 stocks used in this program
    stockcodes = ["T", "SFL", "PFE", "XOM", "MO", "VZ", "IBM", "TSLA", "GILD",
                  "GE"]

    price, returns, variance = get_stock_info()

    # Number of stocks to select
    num_stocks_to_buy = 2

    # Set the budget
    budget = 40

    # Add binary variables for stocks
    stocks = define_variables(stockcodes)

    # Build CQM
    cqm = define_cqm(stocks, num_stocks_to_buy, price, returns, budget,
                     variance)

    # Run CQM on hybrid solver
    sampleset = sample_cqm(cqm)

    # Process and print solution
    print("\nPart 3 solution:\n")
    process_sampleset(sampleset, stockcodes)