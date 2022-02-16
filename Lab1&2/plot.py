import numpy as np
import matplotlib.pyplot as plt


def main():
    array = np.loadtxt(
        'data_0.csv',
        unpack=True,
        dtype=int,
        delimiter=',',
        skiprows=1,
        usecols=[0, 1, 5],
    )
    rule, width, cyclen = array
    rule = np.average(rule.reshape(-1, 10), axis=1)
    cyclen = np.average(cyclen.reshape(-1, 10), axis=1)

    rule_classes = dict(
        np.loadtxt('rule_class_wolfram.csv', dtype=int, delimiter=',')
    )

    class1 = [x for x in rule_classes if rule_classes.get(x) == 1]
    class1cycle = []
    for elem in class1:
        class1cycle.append(cyclen[elem])
    class2 = [x for x in rule_classes if rule_classes.get(x) == 2]
    class2cycle = []
    for elem in class2:
        class2cycle.append(cyclen[elem])
    class3 = [x for x in rule_classes if rule_classes.get(x) == 3]
    class3cycle = []
    for elem in class3:
        class3cycle.append(cyclen[elem])
    class4 = [x for x in rule_classes if rule_classes.get(x) == 4]
    class4cycle = []
    for elem in class4:
        class4cycle.append(cyclen[elem])

    plt.bar(class1, class1cycle)
    plt.bar(class2, class2cycle)
    plt.bar(class3, class3cycle)
    plt.bar(class4, class4cycle)
    plt.legend(['Class 1', 'Class 2', 'Class 3', 'Class 4'])
    plt.xlim([0, 255])
    plt.xlabel('Wolfram rules')
    plt.ylabel('Cycle length')
    plt.title(
        'Average cycle lengths plotted per wolfram rule, divided per class,\n with initial values 0 with 1 in the middle'
    )
    plt.show()

    print(np.average(cyclen))


if __name__ == '__main__':
    main()
