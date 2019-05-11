import json
import pprint
import random
from copy import deepcopy
import numpy as np

# constants
variables = 'variables'
constraints = 'constraints'
varCon = 'varCon'
weight = 'weight'
weightLimit = 'weightLimit'
value = 'value'
weightedProfit = 'weightedProfit'
var_id = 'vid'
con_id = 'cid'

order_batch_matrix = dict()
batch_matrix = dict()
order_matrix = dict()
comp_population = []

pop_num = 50


def get_order_batches() -> dict:
    global order_matrix
    global batch_matrix
    global order_batch_matrix
    with open('DataSets/mknap1-2.json') as file_object:
        # store file data in object
        datas = json.load(file_object)

    orders = order_matrix = datas[variables]
    batches = batch_matrix = datas[constraints]
    batch_order = datas[varCon]
    order_batches = {}
    for order in orders:
        order_batches[order] = {}
        for batch in batches:
            if int(batch_order[batch][order].get(weight)) < int(batches[batch].get(weightLimit)) and int(
                    batch_order[batch][order].get(weight)) != 0:
                profit_weight = float(orders[order].get(value)) / float(batch_order[batch][order].get(weight))
                order_batches[order][batch] = batch_order[batch][order]
                order_batches[order][batch][weightedProfit] = profit_weight

    for order_batch in order_batches:
        temp_dat = sorted(order_batches[order_batch].values(), key=
        lambda kv: (kv[weightedProfit], kv[weightedProfit]), reverse=True)
        order_batches[order_batch] = temp_dat

    order_batch_matrix = order_batches
    return order_batches


def get_max_weight_value() -> list:
    order_batch = get_order_batches()
    for ob in order_batch:
        tmp = order_batch[ob][0]
        order_batch[ob] = tmp

    order_batch = sorted(order_batch.values(), key=
    lambda kv: (kv[weightedProfit], kv[weightedProfit]), reverse=True)

    return order_batch


def shuffle_order(item: dict) -> dict:
    tmp1 = {}
    keys = list(item.keys())
    print(keys)
    random.shuffle(keys)
    print(keys)
    for key1 in keys:
        tmp1[key1] = item[key1]
    return tmp1


def initiate_population() -> dict:
    global order_batch_matrix
    order_batch_matrix1 = deepcopy(order_batch_matrix)
    for obm in order_batch_matrix1:
        tmp2 = random.choice(order_batch_matrix1[obm])
        order_batch_matrix1[obm] = tmp2
    return shuffle_order(order_batch_matrix1)


def hash_item(item: dict) -> int:
    rred = json.dumps(item)
    return hash(rred)


def initiate_populations() -> list:
    global pop_num
    global comp_population
    populations = []
    for i in range(pop_num):
        pop_pop = initiate_population()
        pop_hash = hash_item(pop_pop)
        if pop_hash not in comp_population:
            comp_population.append(pop_hash)
            populations.append(initiate_population())
    return populations


get_order_batches()
tmp = initiate_population()
print(hash_item(tmp))
tmp = initiate_population()
print(hash_item(tmp))
