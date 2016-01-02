from __future__ import division
from ArgsParser import InputParser
from random import shuffle
from id3 import classify_all
from decision_tree_builder import learn_tree
from math import sqrt
import math
import copy
import sys
import csv

DIV_FUNCTS = ('entropy', 'gini', 'misclassification')


class TrainingData:
    def __init__(self, class_vals, features, examples):
        self.class_vals = class_vals
        self.features = features
        self.examples = examples


def main():
    # Grab statistical parameters from user
    args = sys.argv
    if len(args) < 2:
        complain_and_exit()

    k = int(args[1])

    if not valid_input(k):
        complain_and_exit()

    # Make pairwise comparisons
    alg_pairs = [('entropy', 'gini'),
                  ('entropy', 'misclassification'),
                  ('gini', 'misclassification')]

    train_data = get_nursery_data()

    # Run K tests for each diversity function
    print "Beginning k-fold comparison"
    log = [['k', k, 'number of training examples:', len(train_data.examples)]]

    outcomes = test_algorithms_on_k_partitions(train_data, k)
    analyze(outcomes, alg_pairs, log, 'kfold.csv', k)


def analyze(outcomes, alg_pairs, log, fname, k):
    log_outcomes(log, outcomes)

    log.append(['algA', 'algB', 'avg diff', 't statistic'])
    for algA, algB in alg_pairs:
        t_stat, avg_diff = compare(outcomes, algA, algB, k)
        log.append([algA, algB, avg_diff, t_stat])

    append_csv(fname, log)


def log_outcomes(log, outcomes):
        log.append(['function', '[]'])
        for func in outcomes:
            row = [func]
            row.extend(outcomes[func])
            log.append(row)


def complain_and_exit():
    print "Expected argument: <5 or 10>"
    sys.exit


def append_csv(fname, log):
    with open(fname, 'a') as output:
        writer = csv.writer(output)
        writer.writerows(log)


def valid_input(k):
    return k == 5 or k == 10


def get_nursery_data():
    nursery_data = InputParser('nursery/nursery.config', 'nursery/nursery.train')
    class_vals = nursery_data.possible_classification_values
    features = nursery_data.features
    examples = nursery_data.train_data
    return TrainingData(class_vals, features, examples)


def test_algorithms_on_k_partitions(train_data, k):
    outcomes = {}
    examples = copy.deepcopy(train_data.examples)
    # NB: because the examples are randomly shuffled,
    # The outcome will differ slightly for each run
    shuffle(examples)
    for funct in DIV_FUNCTS:

        def test_tree(train_examples, test_examples):
            tree = learn_tree(train_data.features, train_data.class_vals,
                              funct, train_examples)
            return classify_all(tree, test_examples)

        outcomes[funct] = [test_tree(train, test)/len(test) for train, test in
                           [split(examples, i, k) for i in range(0, k)]]

    return outcomes


def split(examples, i, k):
    """Given a list of training examples, a number of possible partitions k,
    and an index i of a partition to select (where i < k), will return a 2-tuple
    of lists of examples (train_list, test_list)"""
    interval = int(math.floor(len(examples)/k))
    test_start = interval*i
    if i == k-1:
        test_end = len(examples)
        train_end = test_start
    else:
        test_end = interval*(i+1)
        train_end = len(examples)

    test_data = examples[test_start:test_end]
    train_data = examples[:test_start] + examples[test_end:train_end]

    return train_data, test_data


def compare(outcomes, funcA, funcB, k):
    outcome_pairs = zip(outcomes[funcA], outcomes[funcB])
    deltas = [pair[0] - pair[1] for pair in outcome_pairs]
    t_stat = abs(t_statistic(deltas, k))
    avg_difference = (avg(outcomes[funcA]) - avg(outcomes[funcB]))
    return t_stat, avg_difference


def std_dev(deltas, k):
    avg_delta = avg(deltas)
    sum_of_squared_deviations = sum((delta - avg_delta)**2 for delta in deltas)
    return sqrt((1/(k-1)) * sum_of_squared_deviations)


def t_statistic(deltas, k):
    sigma = std_dev(deltas, k)
    if sigma == 0:
        return 0
    return avg(deltas) * (sqrt(k)/sigma)


def avg(iterable):
    return sum(iterable)/len(iterable)

if __name__ == '__main__':
    main()