"""

"""

import logging
import csv
from .graph import Relation
import operator
import math

def matrix_read_train(file_name):
    matrix = []
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            matrix.append(row)

    people_list = matrix[0]
    word_list = matrix[1]
    frequency = []
    for i in range(2, len(matrix)):
        frequency.append(list(map(int, matrix[i])))

    options = {}
    options.update({'acquaintance': Relation.CATEGORIES['acquaintance']})
    options.update({'friend': Relation.CATEGORIES['friend']})

    friend = [0]*len(frequency[0])
    acquaint = [0]*len(frequency[0])
    print(options['friend'])
    for row in frequency:
        if row[0] == options['friend']:
            friend = list(map(operator.add, friend, row))
        if row[0] == options['acquaintance']:
            acquaint = list(map(operator.add, acquaint, row))

    return word_list, friend, acquaint, len(frequency)


def naive_bayes(words, friends, acquaintances, num_people):
    ttl_num_words = len(words)

    num_friend_words = sum([1 if i else 0 for i in friends])
    ttl_num_friend_words = sum(friends)

    num_acquaint_words = sum([1 if i else 0 for i in friends])
    ttl_num_acquaint_words = sum(acquaintances)

    friend_prior = math.log(num_friend_words / num_people)
    acquaint_prior = math.log(num_acquaint_words / num_people)

    friend_phi = []
    acquaint_phi = []
    for i in range(len(words)):
        friend_phi.append(math.log((friends[i]+1)/(ttl_num_friend_words + ttl_num_words)))
        acquaint_phi.append(math.log((acquaintances[i]+1)/(ttl_num_acquaint_words + ttl_num_words)))

    return friend_phi, friend_prior, acquaint_phi, acquaint_prior


if __name__ == '__main__':
    import sys

    train_name = sys.argv[1]
    words, friend_words, acquaint_words, num_people = matrix_read_train(train_name)
    friend_phi, friend_prior, acquaint_phi, acquaint_prior = naive_bayes(words, friend_words,
                                                                         acquaint_words, num_people)


