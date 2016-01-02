from __future__ import division

from random import shuffle
import copy
import math

import decision_tree_builder
import diversity_experiment
import id3


K = 5
DIV_FUNCT = 'entropy'


def main():
    train_data = diversity_experiment.get_nursery_data()
    shuffle(train_data.examples)
    outcomes = {'unpruned': [],
                'conservative': [],
                'liberal': []}

    for i in range(0, K):
        # Split into training, test, and validation sets
        training_set, the_rest = diversity_experiment.split(train_data.examples, i, K)
        test_set, validation_set = validation_split(the_rest)

        # Learn the original tree
        unpruned = decision_tree_builder.learn_tree(train_data.features,
                                                    train_data.class_vals,
                                                    DIV_FUNCT,
                                                    training_set)

        # Make pruned versions too
        print "Pruning conservatively"
        conservative_tree = TreePruner(copy.deepcopy(unpruned), 'conservative', validation_set).root

        print "Pruning liberally."
        liberal_tree = TreePruner(copy.deepcopy(unpruned), 'liberal', validation_set).root

        trees = {
            'unpruned': unpruned,
            'liberal':  liberal_tree,
            'conservative':  conservative_tree
        }

        # Test ALL the trees!
        for tree in trees:
            outcomes[tree].append(evaluate(trees[tree], test_set))

    pairwise = [
        ('unpruned', 'liberal'),
        ('unpruned', 'conservative'),
        ('liberal', 'conservative')
    ]

    # Get t-statistics
    diversity_experiment.analyze(outcomes, pairwise, [], 'prune.csv', K)


def validation_split(examples):
    border = int(math.floor(len(examples)/2))
    return examples[border:], examples[: border]


class TreePruner:

    def __init__(self, _root, method_name, validation_set):
        self.root = _root
        if method_name == 'conservative':
            self.should_prune = self.conservative_should_prune
        elif method_name == 'liberal':
            self.should_prune = self.liberal_should_prune
        else:
            raise NameError("TreePruner must be initialized as 'liberal' or 'conservative'.")
        self.val_set = validation_set
        for val in self.root.feature.possible_values:
            self.prune(self.root, self.root.children[val], val)

    def prune(self, parent, child, child_value):
        if is_leaf(child):
            # Child is already as pruned as can be
            return

        # Depth-first traversal
        for val in child.feature.possible_values:
            self.prune(child, child.children[val], val)

        if parent.feature.name == 'has_nurs':
            i = 'break_here!!!'

        unpruned_perf = evaluate(self.root, self.val_set)
        unpruned_child = copy.deepcopy(child)

        # Try replacing the child with a leaf with its most common label
        parent.link(child_value, id3.Leaf(child.pruned_label, 0, 0))

        pruned_perf = evaluate(self.root, self.val_set)

        if self.should_prune(unpruned_perf, pruned_perf):
            # We've already linked the parent to the pruned child
            return
        else:
            # Relink the parent to the unpruned child
            parent.link(child_value, unpruned_child)
            return

    def conservative_should_prune(self, unpruned_perf, pruned_perf):
        Z_95_one_sided = 1.65
        # return true if pruned performance is significantly better than unpruned
        z_stat = self.z_statistic(1 - pruned_perf, 1 - unpruned_perf, len(self.val_set))
        return z_stat > Z_95_one_sided

    def liberal_should_prune(self, unpruned_perf, pruned_perf):
        Z_05_one_sided = -1.65
        # return true if pruned performance is at least as good as unpruned
        # That is, return false if pruned performance is significantly worse than unpruned
        z_stat = self.z_statistic(1 - pruned_perf, 1 - unpruned_perf, len(self.val_set))
        return z_stat > Z_05_one_sided

    @staticmethod
    def z_statistic(err1, err2, n):
        sigma = math.sqrt((err1*(1 - err1)) + (err2*(1 - err2)))
        z = (err1 - err2)*(math.sqrt(n)/sigma)
        # We want the statistic to be positive if err2 is greater than err1
        # to indicate that method 1 performed better than method 2
        return -z


def is_leaf(tree):
    try:
        if tree.label:
            return True
    except AttributeError:
        return False


def evaluate(tree, test_set):
    return id3.classify_all(tree, test_set)/len(test_set)

if __name__ == '__main__':
    main()