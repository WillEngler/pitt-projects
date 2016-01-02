import unittest
from id3 import *
from decision_tree_builder import *


class DiversityFunctionTests(unittest.TestCase):
    def setUp(self):
        self.training_examples = []
        feat_names = ['x1', 'x2', 'x3']
        self.training_examples.append(Example('+', feat_names, ['Yes', 'A', 'F']))
        self.training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))
        self.training_examples.append(Example('-', feat_names, ['Yes', 'A', 'T']))
        self.training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))
        self.classification_values = ['+', '-']

    def test_gini(self):
        self.assertAlmostEqual(0.375, gini(self.training_examples, self.classification_values), 3)

    def test_entropy(self):
        # Round to 3 decimal places
        self.assertAlmostEqual(0.811, entropy(self.training_examples, self.classification_values), 3)

    def test_misclassification(self):
        self.assertAlmostEqual(0.25, misclassification(self.training_examples, self.classification_values), 2)


class BuildTests(unittest.TestCase):
    def setUp(self):
        feat_names = ['x1', 'x2', 'x3']
        self.feat_names = feat_names
        self.x1 = Feature('x1', ['Yes', 'No'])
        self.x2 = Feature('x2', ['A', 'B', 'C'])
        self.x3 = Feature('x3', ['T', 'F'])
        self.features = [self.x1, self.x2, self.x3]
        self.classification_values = ['+', '-']

        self.all_training_examples = []
        self.all_training_examples.append(Example('+', feat_names, ['Yes', 'A', 'F']))
        self.all_training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))
        self.all_training_examples.append(Example('+', feat_names, ['No', 'C', 'F']))
        self.all_training_examples.append(Example('-', feat_names, ['No', 'A', 'F']))
        self.all_training_examples.append(Example('+', feat_names, ['No', 'B', 'T']))
        self.all_training_examples.append(Example('-', feat_names, ['Yes', 'A', 'T']))
        self.all_training_examples.append(Example('+', feat_names, ['No', 'A', 'F']))
        self.all_training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))

        self.yes_training_examples = []
        self.yes_training_examples.append(Example('+', feat_names, ['Yes', 'A', 'F']))
        self.yes_training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))
        self.yes_training_examples.append(Example('-', feat_names, ['Yes', 'A', 'T']))
        self.yes_training_examples.append(Example('-', feat_names, ['Yes', 'B', 'F']))

        self.no_training_examples = []
        self.no_training_examples.append(Example('+', feat_names, ['No', 'C', 'F']))
        self.no_training_examples.append(Example('-', feat_names, ['No', 'A', 'F']))
        self.no_training_examples.append(Example('+', feat_names, ['No', 'B', 'T']))
        self.no_training_examples.append(Example('+', feat_names, ['No', 'A', 'F']))

    def test_with_parsing(self):
        parser = InputParser('toy_input/toy.config',
                             'toy_input/toy_train.dat',
                             'toy_input/toy_test.dat')
        tree = learn_tree(parser.features, parser.possible_classification_values,
                          'entropy', parser.train_data)
        self.assertEquals(tree.children['Yes'].children['C'].label, '-')
        self.assertEquals(tree.children['No'].children['B'].label, '+')

    def test_build_small_tree(self):
        tree = learn_tree([self.x2, self.x3], self.classification_values, 'entropy', self.no_training_examples)
        self.assertEquals(tree.feature.name, 'x2')
        self.assertEquals(tree.children['A'].feature.name, 'x3')
        self.assertEquals(tree.children['B'].label, '+')

    def test_build_big_tree(self):
        tree = learn_tree(self.features, self.classification_values, 'entropy', self.all_training_examples)
        self.assertEquals(tree.feature.name, 'x1')
        self.assertEquals(tree.children['Yes'].children['C'].label, '-')
        self.assertEquals(tree.children['No'].children['B'].label, '+')

    def test_classify(self):
        tree = learn_tree(self.features, self.classification_values, 'entropy', self.all_training_examples)
        self.assertEquals('+', tree.classify(Example('+', self.feat_names, ['No', 'B', 'T'])))
        self.assertEquals('-', tree.classify(Example('+', self.feat_names, ['Yes', 'C', 'F'])))

    def test_classify_all(self):
        tree = learn_tree(self.features, self.classification_values, 'entropy', self.all_training_examples)
        # Start with two correct examples
        examples = [Example('+', self.feat_names, ['No', 'B', 'T']), Example('-', self.feat_names, ['Yes', 'C', 'F'])]
        # Add one incorrect example
        examples.append(Example('+', self.feat_names, ['Yes', 'C', 'F']))
        self.assertEquals(id3.classify_all(tree, examples), 2)

    def test_all_examples_have_same_label(self):
        self.assertFalse(all_examples_have_same_label(self.all_training_examples))

    def test_entropy_on_perfectly_diverse_set(self):
        self.assertAlmostEqual(1, entropy(self.all_training_examples, self.classification_values), 3)

    def test_feature_with_highest_gain(self):
        self.assertEquals(self.x1.name,
                          feature_with_highest_gain(self.features, entropy,
                                                    self.all_training_examples, self.classification_values).name)

    def test_most_common_classification_in(self):
        self.all_training_examples.pop()
        self.assertEquals('+',
                          most_common_classification_in(self.all_training_examples))

    def test_get_example_subset(self):
        self.assertTrue(any([ex.features['x1'] is 'Yes' for ex in
                             get_example_subset(self.x1, 'Yes', self.all_training_examples)]))

    def test_weighted_sum_of_diversity(self):
        self.assertAlmostEqual(.811,
                               weighted_sum_of_diversity(entropy, self.all_training_examples,
                                                         self.classification_values,
                                                         [self.yes_training_examples, self.no_training_examples]), 3)

    def test_gain(self):
        self.assertAlmostEqual(.189,
                               gain(entropy, self.all_training_examples, self.x1,
                                    self.classification_values), 3)

        self.assertEquals(0,
                          gain(entropy, self.all_training_examples, self.x3,
                               self.classification_values), )