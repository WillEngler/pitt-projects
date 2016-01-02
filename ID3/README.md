# ID3
William Engler's submission for Pitt CS1675 Homework 3

## Info to run
* Requires Python 2.7.x interpreter.
* Expected command line input for HW2: `python id3.py diversity_function, config_path, training_data_path, test_data_path`
* Expected command line input for HW3 diversity experiment: `python diversity_experiment.py <5 or 10>` (specify 5 or 10 for k).
* Expected command line input for HW3 pruning experiment: `python pruning_experiment.py`

## Notes to modify
* The restriction on 5 or 10 for k in diversity_experiment is arbitrary. Could've let user input arbitrary k, but YAGNI.
* To test a different Z value in pruning_experiment, I changed the hardcoded Z values in the should_prune_conservative and should_prune_liberal functions. Could've parameterized it, but again: YAGNI.

##Testing for HW2
* Three of the included files are a unit test suite. My discipline broke down near the end of the assignment, so some units are not well covered. However, most of the tree building and input processing code is covered. Also find included three folders of test data. Some unit tests rely on them. One folder (`big_input`), contains over 10,000 training examples. However, the feature set is very small. Also, the examples are the 16 examples Dr. Hwa provided, but copied a whole bunch. Noting those limitations, running the program on that input shows that my implementation scales pretty well.

## Testing for HW3
* I was less formal for this homework because the programming was less complex.
* I stepped through my pruner with a debugger as an informal check.


## Resources
* t table: https://s3.amazonaws.com/udacity-hosted-downloads/t-table.jpg
* z table: http://www.stat.ufl.edu/~athienit/Tables/Ztable.pdf
* Discussed the assignment with the usual suspects: Joel Roggeman, Nick Peluso, Pete Mash
