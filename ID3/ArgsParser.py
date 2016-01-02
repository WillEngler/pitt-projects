import sys
import os
import csv
from id3 import *
import id3


def args_are_valid(args):
    return right_length(args) and valid_diversity(args) and valid_paths(args)


def right_length(args):
    if len(args) != 5:
        print 'Usage: python id3.py diversity_function config_path training_data_path test_data_path'
        print '\n Expected 4 arguments. Received' + str(len(args))
        return False
    else:
        return True


def valid_diversity(args):
    diversity_functions = ('entropy', 'misclassification', 'gini')
    if args[1] not in diversity_functions:
        print 'Expected one of the following diversity functions as first argument:'
        for function in diversity_functions:
            print '\t * ' + function
        return False
    else:
        return True


def valid_paths(args):
    return all([os.path.isfile(path) for path in args[2:]])


class InputParser:
    def __init__(self, config_path, train_path, test_path=None):
        self.possible_classification_values = self.get_classification_values(config_path)
        self.features = self.get_features(config_path)
        self.train_data = self.get_training_examples(train_path)
        self.test_data = self.get_training_examples(test_path)

    def get_classification_values(self, config_path):
        with open(config_path, 'rb') as config_file:
            config_reader = csv.reader(config_file)
            '''We expect the first line of the .config csv file
            to be the values.'''
            return config_reader.next()

    def get_features(self, train_path):
        with open(train_path, 'rb') as config_file:
            config_reader = csv.reader(config_file)
            # We don't care about the first line
            config_reader.next()
            features = []
            for row in config_reader:
                features.append(id3.Feature(row[0], tuple(row[1:])))
            return features

    def get_training_examples(self, examples_path):
        if examples_path is None:
            return
        with open(examples_path, 'rb') as examples_file:
            examples_reader = csv.reader(examples_file)
            # examples_dict maps indices to examples.
            #Examples are mappings from feature names to feature values
            examples = []
            feature_names = [feat.name for feat in self.features]
            for row in examples_reader:
                examples.append(id3.Example(row[1], feature_names, row[2:]))
            return examples