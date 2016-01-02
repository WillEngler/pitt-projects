from ArgsParser import *
from id3 import *
import sys
import os
import unittest


class ArgsCheckTests(unittest.TestCase):
    def test_valid_args(self):
        args = ['id3.py',
                'gini',
                'sample_input/sample.config',
                'sample_input/sampletrain.dat',
                'sample_input/sampletest.dat']
        self.assertTrue(right_length(args))
        self.assertTrue(valid_diversity(args))
        self.assertTrue(valid_paths(args))
        self.assertTrue(args_are_valid(args))

    def test_invalid_diversity_function(self):
        args = ['id3.py',
                'this_name_is_donk',
                'sample_input/sample.config',
                'sample_input/sampletrain.dat',
                'sample_input/sampletest.dat']
        self.assertFalse(valid_diversity(args))
        self.assertFalse(args_are_valid(args))

    def test_invalid_path(self):
        args = ['id3.py',
                'entropy',
                'sample_input/wrong.config',
                'sample_input/sampletrain.dat',
                'sample_input/sampletest.dat']
        self.assertFalse(valid_paths(args))
        self.assertFalse(args_are_valid(args))

    def test_invalid_args_count(self):
        args = ['id3.py',
                'entropy',
                'sample_input/wrong.config',
                'sample_input/sampletrain.dat',
                'sample_input/sampletest.dat',
                'Chunky Bacon']
        self.assertFalse(right_length(args))
        self.assertFalse(args_are_valid(args))


class InputParserTests(unittest.TestCase):
    def setUp(self):
        args = ['id3.py',
                'gini',
                'sample_input/sample.config',
                'sample_input/sampletrain.dat',
                'sample_input/sampletest.dat']
        self.parser = InputParser(args[2], args[3], args[4])
        self.humidity = Feature('Humidity', ('normal', 'high'))

    def test_possible_classification_values(self):
        self.assertTrue('yes' in self.parser.possible_classification_values)

    def test_feature_values(self):
        '''The features list should preserve the order features were presented in the file.'''
        self.assertEqual(self.parser.features[2].name, self.humidity.name)

    def test_features_start_at_second_line(self):
        self.assertNotIn('yes', [feat.name for feat in self.parser.features])

    def test_train_data(self):
        '''9,yes,sunny,cold,normal,weak'''
        self.assertEquals(self.parser.train_data[8].features[self.humidity.name], 'normal')

    def test_test_data(self):
        '''102,no,rain,hot,high,weak'''
        self.assertEquals(self.parser.test_data[1].features[self.humidity.name], 'high')