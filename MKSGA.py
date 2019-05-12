import json
import pprint
import random
from copy import deepcopy
import numpy as np


class UberParentGA:

    def __init__(self) -> None:
        # constants
        self.variables = 'variables'
        self.constraints = 'constraints'
        self.varCon = 'varCon'
        self.weight = 'weight'
        self.weightLimit = 'weightLimit'
        self.value = 'value'
        self.weightedProfit = 'weightedProfit'
        self.var_id = 'vid'
        self.con_id = 'cid'
        self.pop_num = 50
        self.solution = 'solution'
        self.uber_parent = 'uberParent'
        self.comp_population = []
        with open('DataSets/mknap1-2.json') as file_object:
            # store file data in object
            datas = json.load(file_object)

        orders = self.order_matrix = datas[self.variables]
        batches = self.batch_matrix = datas[self.constraints]
        batch_order = datas[self.varCon]
        order_batches = {}
        for order in orders:
            order_batches[order] = {}
            for batch in batches:
                if int(batch_order[batch][order].get(self.weight)) < int(batches[batch].get(self.weightLimit)):

                    profit_weight = orders[order].get(self.value) if (
                                batch_order[batch][order].get(self.weight) == 0) else orders[order].get(self.value) / \
                                                                                      batch_order[batch][order].get(
                                                                                          self.weight)
                    order_batches[order][batch] = batch_order[batch][order]
                    order_batches[order][batch][self.weightedProfit] = profit_weight
                    order_batches[order][batch][self.value] = orders[order].get(self.value)
                elif int(batch_order[batch][order].get(self.weight)) > int(batches[batch].get(self.weightLimit)):
                    order_batches[order] = {}
                    order_batches[order][0] = {'vid': 0, 'cid': int(order), 'weight': 0, 'weightedProfit': 0}
                    break
        # for order_batch in order_batches:
        #     temp_dat = sorted(order_batches[order_batch].values(), key=
        #     lambda kv: (kv[self.weightedProfit], kv[self.weightedProfit]), reverse=True)
        #     order_batches[order_batch] = temp_dat

        self.order_batch_matrix = order_batches

    def get_max_weight_value(self) -> list:
        order_batch = deepcopy(self.order_batch_matrix)
        for ob in order_batch:
            tmp = order_batch[ob][0]
            order_batch[ob] = tmp
        order_batch = sorted(order_batch.values(), key=
        lambda kv: (kv[self.weightedProfit], kv[self.weightedProfit]), reverse=True)

        return order_batch

    def shuffle_order(self, item: dict) -> dict:
        tmp1 = {}
        keys = list(item.keys())
        random.shuffle(keys)
        for key1 in keys:
            tmp1[key1] = item[key1]
        return tmp1

    def initiate_population(self) -> dict:
        test_int = np.random.randint(0, 1)
        order_batch_matrix1 = deepcopy(self.order_batch_matrix)
        for obm in order_batch_matrix1:
            if test_int == 1:
                order_batch_matrix1[obm] = {}
                order_batch_matrix1[obm][0] = {'vid': 0, 'cid': int(obm), 'weight': 0, 'weightedProfit': 0}

        return self.shuffle_order(order_batch_matrix1)

    def hash_item(self, item: dict) -> int:
        rred = json.dumps(item)
        return hash(rred)

    def initiate_populations(self) -> list:
        populations = []
        for i in range(self.pop_num):
            pop_pop = self.initiate_population()
            pop_hash = self.hash_item(pop_pop)
            if pop_hash not in self.comp_population:
                self.comp_population.append(pop_hash)
                populations.append(self.initiate_population())
        return populations

    def access_fitness_and_return_uber_parent(self, pops: dict) -> dict:
        set_batches = deepcopy(self.batch_matrix)
        set_orders = deepcopy(self.order_matrix)
        profit = 0
        for order in pops:
            if order != 0 and pops[order].get(self.con_id) != 0 and self.does_order_fit(set_batches, pops[order]):
                profit += set_orders[order].get(self.value)
                set_batches = self.reduce_batches(set_batches, pops[order])
            elif order != 0 and pops[order].get(self.con_id) != 0 and self.does_order_fit(set_batches,
                                                                                          pops[order]) is False:
                pops[order] = {'vid': 0, 'cid': int(order), 'weight': 0, 'weightedProfit': 0}
            pop_hash = self.hash_item(pops[order])
            if pop_hash not in self.comp_population:
                self.comp_population.append(pop_hash)
        return {self.solution: profit, self.uber_parent: pops}

    def does_order_fit(self, set_batches: dict, order: dict) -> bool:
        test_fit = True
        for sb in set_batches:
            for o in order.values():
                if int(o.get(self.con_id)) == int(sb) and set_batches[sb].get(self.weightLimit) < o.get(self.weight):
                    test_fit = False
        return test_fit

    def reduce_batches(self, set_batches: dict, order: dict) -> dict:
        for sb in set_batches:
            for o in order.values():
                if int(o.get(self.con_id)) == int(sb):
                    batch_weight = set_batches[str(sb)].get(self.weightLimit)
                    order_weight = o.get(self.weight)
                    batch_weight -= order_weight
                    set_batches[str(sb)][self.weightLimit] = batch_weight
        return set_batches

    def start(self):
        best_profit = 0
        best_population = None
        uber_pop = {}
        populations = self.initiate_populations()
        for population in populations:
            temp_pop = self.access_fitness_and_return_uber_parent(population)
            uber_pop[temp_pop[self.solution]] = temp_pop[self.uber_parent]
            if temp_pop[self.solution] > best_profit:
                best_profit = temp_pop[self.solution]
                best_population = temp_pop[self.uber_parent]
        return {'best Profit': best_profit, 'best population': best_population}


ssclass = UberParentGA()
test = ssclass.start()
pprint.pprint(test)
