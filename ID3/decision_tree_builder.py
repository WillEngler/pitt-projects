# Make division return floats!
from __future__ import division
import id3
from collections import defaultdict
import copy
import math


def learn_tree(features, classification_values, div_function_name, training_examples):
    
    div_function = name_to_func[div_function_name]
    
    # Ensure that this isn't a degenerate case.
    assert features
    assert not all_examples_have_same_label(training_examples)

    # Make first recursive call to construct tree
    return build(copy.deepcopy(features), training_examples,
                 div_function, classification_values)

'''Implementation of ID3. Recursively construct the tree.'''


def build(features, training_examples, div_function, classification_values):

    if all_examples_have_same_label(training_examples):
        return id3.Leaf(training_examples[0].classification,
                        len(training_examples), len(training_examples))

    if not features:
        label = most_common_classification_in(training_examples)
        return id3.Leaf(label, num_with_label(training_examples, label), len(training_examples))

    winning_feature = feature_with_highest_gain(features, div_function, training_examples, classification_values)
    root = id3.Node(winning_feature)
    # Added for pruning experiment
    root.pruned_label = most_common_classification_in(training_examples)

    for value in winning_feature.possible_values:
        examples_where_value_holds = get_example_subset(winning_feature, value, training_examples)
        
        if not examples_where_value_holds:
            label = most_common_classification_in(training_examples)
            root.link(value, id3.Leaf(label, 0, 0))
        
        else:
            remaining_features = filter(lambda f: f.name != winning_feature.name, features)
            remaining_features = copy.deepcopy(remaining_features)
            root.link(value,
                      build(remaining_features, examples_where_value_holds, div_function, classification_values))
    return root


'''Helper methods for build()'''


def num_with_label(examples, label):
    count = 0
    for e in examples:
        if e.classification == label:
            count += 1
    return count


def all_examples_have_same_label(examples):
    # Adapted from http://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
    #   I didn't *need* help to do this. I just thought there had to be a nice one-liner in Python
    classifications = [ex.classification for ex in examples]
    iterator = iter(classifications)
    first = iterator.next()
    return all([first == rest for rest in iterator])


def feature_with_highest_gain(features, div_function, training_examples, classification_values):
    max_gain = 0
    winning_feature = features[0]
    
    for feat in features:
        candidate_gain = gain(div_function, training_examples,
                              feat, classification_values)
        if candidate_gain > max_gain:
            max_gain = candidate_gain
            winning_feature = feat
    
    return winning_feature


def gain(diversity, training_examples, feature, classification_values):
    subsets = [get_example_subset(feature, value, training_examples)
               for value in feature.possible_values]

    return diversity(training_examples, classification_values) - \
        weighted_sum_of_diversity(diversity, training_examples, classification_values, subsets)


def weighted_sum_of_diversity(diversity, training_examples, classification_values, subsets):
    return sum([(len(subset)/len(training_examples)) *
                diversity(subset, classification_values) for subset in subsets])


def most_common_classification_in(training_examples):
    classifications = [ex.classification for ex in training_examples]
    classification_counter = defaultdict(int)
    
    for c in classifications:
        classification_counter[c] += 1
    max_count = max(classification_counter.values())
    
    for c in classifications:
        if classification_counter[c] == max_count:
            return c


def get_example_subset(winning_feature, value, training_examples):
    example_subset = []

    for ex in training_examples:
        if ex.features[winning_feature.name] == value:
            example_subset.append(ex)
    return example_subset


'''Classification functions'''


def gini(training_examples, classification_values):
    return 1 - sum([proportion_with(label, training_examples)**2
                    for label in classification_values])


def entropy(training_examples, classification_values):
    sum = 0
    for label in classification_values:
        p = proportion_with(label, training_examples)
        if p > 0 and len(classification_values) > 1:
            sum += -p*math.log(p, 2)
    return sum


def misclassification(training_examples, classification_values):
    return 1 - max([proportion_with(label, training_examples)
                    for label in classification_values])


def proportion_with(label, training_examples):
    if len(training_examples) == 0:
        return 0

    count = 0
    for ex in training_examples:
        if ex.classification == label:
            count += 1
    return count/len(training_examples)


name_to_func = {
    'gini': gini,
    'misclassification': misclassification,
    'entropy': entropy
}
