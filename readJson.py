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
            order_batches[order][0] = {'vid': 0, 'cid': int(order), 'weight': 0, 'weightedProfit': 0}
            for batch in batches:
                if int(batch_order[batch][order].get(self.weight)) < int(batches[batch].get(self.weightLimit)) and int(
                        batch_order[batch][order].get(self.weight)) != 0:
                    profit_weight = orders[order].get(self.value) / batch_order[batch][order].get(self.weight)
                    order_batches[order][batch] = batch_order[batch][order]
                    order_batches[order][batch][self.weightedProfit] = profit_weight
                    order_batches[order][batch][self.value] = orders[order].get(self.value)

        for order_batch in order_batches:
            temp_dat = sorted(order_batches[order_batch].values(), key=
            lambda kv: (kv[self.weightedProfit], kv[self.weightedProfit]), reverse=True)
            order_batches[order_batch] = temp_dat

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
                order_batch_matrix1[obm] = {'vid': 0, 'cid': int(obm), 'weight': 0, 'weightedProfit': 0}

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
            if int(order) != 0 and int(pops[order].get(self.con_id)) != 0:
                cid = pops[order].get(self.con_id)
                batch_weight = set_batches[str(cid)].get(self.weightLimit)
                order_weight = pops[order].get(self.weight)
                print(set_batches)
                if batch_weight > order_weight:
                    profit += set_orders[order].get(self.value)
                    batch_weight -= order_weight
                    set_batches[str(cid)][self.weightLimit] = batch_weight
                    print(set_batches)
                elif batch_weight < order_weight:
                    pops[order] = {}
        return {'profit': profit, 'uberPop': pops}

    def start(self):
        uberPop = {}
        populations = self.initiate_populations()
        for population in populations:
            temp_pop = self.access_fitness_and_return_uber_parent(population)
            uberPop[temp_pop['profit']] = temp_pop['uberPop']
        return uberPop


ssclass = UberParentGA()
test = ssclass.start()
pprint.pprint(test)
