__author__ = 'William'
import sys
import csv

# Training examples from lecture notes
# First element is number of times a song was played
# Second element is whether song was liked (1) or disliked (0)
music_examples = [
    (1, 0)
    (6, 1)
    (2, 0)
    (5, 1)
]


def main():

    args = sys.argv
    if len(args) < 3:
        print "Expected usage: perceptron.py [learning rate], [number of iterations]"
        sys.exit(1)

    eta = float(args[1])
    num_iterations = int(args[2])

    perceptron_log = learn('perceptron', eta, num_iterations )
    gradient_log = learn('gradient', eta, num_iterations)

    append_csv('perceptron.txt', perceptron_log)
    append_csv('gradient.txt', gradient_log)


def append_csv(fname,log):
    with open(fname, 'a') as output:
        writer = csv.writer(output)
        writer.writerows(log)


def learn(alg_name, eta, num_iterations):

    # Initialize w0 and w1 to 0
    w = [0, 0]
    # Let x0 be 1. Define x1 later.
    x = [1, None]

    # Close hypothesis function over w and x
    if alg_name == 'perceptron':
        def h(example):
            if (x[0]*w[0] + x[1]*w[1]) >= 0:
                return 1
            else:
                return 0
    elif alg_name == "gradient":
        def h(example):
            return x[0]*w[0] + x[1]*w[1]

    # Concept function
    def c(example):
        return example[1]

    def update(example):
        scalar = eta*(c(example) - h(example))
        w[0] += scalar*x[0]
        w[1] += scalar*x[1]

    log = [['Iteration', 'c(x)', 'h(x)', 'x1', 'w0', 'w1']]

    for i in range(1, num_iterations+1):
        for ex in music_examples:
            # Update feature value to value of this example
            x[1] = ex[0]
            update(ex)
            log.append([i, c(ex), h(ex), x[1], w[0], w[1]])

    return log

if __name__ == "__main__":
    main()