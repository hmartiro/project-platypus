import logging
import csv
import operator
import math
from selfgraph.core.graph import Relation


def import_train_CSV(file_name):
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


def import_read_CSV(file_name):
    matrix = []
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            matrix.append(row)

    people = matrix[0]
    word = matrix[1]
    frequency = []
    for i in range(2, len(matrix)):
        frequency.append(list(map(int, matrix[i])))

    return word, people, frequency


def train(words, friends, acquaintances, num_people):
    ttl_num_words = len(words)

    num_friend_words = sum([1 if i else 0 for i in friends])
    ttl_num_friend_words = sum(friends)

    num_acquaint_words = sum([1 if i else 0 for i in acquaintances])
    ttl_num_acquaint_words = sum(acquaintances)

    friend_prior = math.log(num_friend_words / num_people)
    acquaint_prior = math.log(num_acquaint_words / num_people)

    friend_phi = []
    acquaint_phi = []
    for i in range(len(words)):
        friend_phi.append(math.log((friends[i]+1)/(ttl_num_friend_words + ttl_num_words)))
        acquaint_phi.append(math.log((acquaintances[i]+1)/(ttl_num_acquaint_words + ttl_num_words)))

    # print top friend words
    logging.debug("Friend words")
    old_i = 0
    for i in sorted(friend_phi)[:5]:
        if i == old_i:
            continue
        old_i = i
        index = [k for k, v in enumerate(friend_phi) if v == i]
        for j in index:
            logging.debug("{} {}".format(words[j], i))

    # print top acquaint words
    logging.debug("Acquaintance Words")
    old_i = 0
    for i in sorted(acquaint_phi)[:5]:
        if i == old_i:
            continue
        old_i = i
        index = [k for k, v in enumerate(acquaint_phi) if v == i]
        for j in index:
            logging.debug("{} {}".format(words[j], i))

    return friend_phi, friend_prior, acquaint_phi, acquaint_prior

def test(frequency, friend_phi, friend_prior, acquaint_phi, acquaint_prior):
    friend_prob = []
    acquaint_prob = []
    for i in range(len(frequency)):
        friend_prob.append(sum(list(map(operator.mul, frequency[i], friend_phi))) + friend_prior)
        acquaint_prob.append(sum(list(map(operator.mul, frequency[i], acquaint_phi))) + acquaint_prior)

    return friend_prob, acquaint_prob


def output_results(friend_prob, acquaint_prob, people):
    for x in zip(friend_prob, acquaint_prob, people):
        if(x[0] > x[1]):
            print("{} is a friend with {} to {}".format(x[2], x[0], x[1]))
        elif(x[0] < x[1]):
            print("{} is a acquaintance with {} to {}".format(x[2], x[0], x[1]))
        else:
            print("Can not decide relationship for {}".format(x[2], x[0], x[1]))
