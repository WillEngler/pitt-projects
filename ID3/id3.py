# Make division return floats!
from __future__ import division
import sys
from ArgsParser import *
import decision_tree_builder


def main():
    args = sys.argv
    if not args_are_valid(args):
        sys.exit()

    div_funct_name = args[1]
    parser = InputParser(args[2], args[3], args[4])

    trained_tree = decision_tree_builder.learn_tree(parser.features,
                                                    parser.possible_classification_values,
                                                    div_funct_name,
                                                    parser.train_data)
    train_num_correct = classify_all(trained_tree, parser.train_data)
    test_num_correct = classify_all(trained_tree, parser.test_data)

    report_outcome(trained_tree, div_funct_name, train_num_correct, test_num_correct,
                   len(parser.train_data), len(parser.test_data))


def classify_all(tree, training_examples):
    count = 0
    for ex in training_examples:
        if tree.classify(ex) == ex.classification:
            count += 1
    return count


def pretty_print(node, depth):
    out = ""
    for value in node.feature.possible_values:
        out += "\t" * depth
        out += "{}={}".format(node.feature.name, value)
        child = node.children[value]
        try:
            out += " {} : {}/{}\n".format(child.label, child.num_with_label, child.num_examples)
        except AttributeError:
            out += "\n" + pretty_print(child, depth + 1)
    return out


def report_outcome(tree, div_funct_name, train_num_passed, test_num_passed, num_train, num_test):
    print "Using {} in Gain function:".format(div_funct_name)
    print "The accuracy on the training data is: {0}/{1} = {2:.1%}".format(train_num_passed, num_train,
                                                                           (train_num_passed / num_train))
    print "The accuracy on the test data is: {0}/{1} = {2:.1%}".format(test_num_passed, num_test,
                                                                       (test_num_passed / num_test))
    print "The final decision tree:"
    print pretty_print(tree, 0)


'''Structures to store input data'''


class Feature:
    def __init__(self, _name, _values):
        # A string
        self.name = _name
        # A list of strings
        self.possible_values = _values


class Example:
    def __init__(self, _classification, _feature_names, _feature_values):
        self.classification = _classification
        self.features = self.make_features_dict(_feature_names, _feature_values)

    def make_features_dict(self, feature_names, feature_values):
        features_dict = {}
        for i in range(len(feature_names)):
            features_dict[feature_names[i]] = feature_values[i]
        return features_dict


'''Decision tree structure'''


class Leaf():
    def __init__(self, _label, _num_with_label, _num_examples):
        self.label = _label
        self.num_with_label = _num_with_label
        self.num_examples = _num_examples


class Node():
    def __init__(self, _feature):
        self.feature = _feature
        self.children = {}

    def link(self, value, child):
        assert value in self.feature.possible_values
        self.children[value] = child

    def classify(self, example):

        # Fetch the child with the right feature value
        child = self.children[example.features[self.feature.name]]

        try:
            return child.label
        except AttributeError:
            return child.classify(example)


if __name__ == '__main__':
    main()