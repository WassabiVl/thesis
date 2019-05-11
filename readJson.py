import json

with open('DataSets/mknap1-2.json') as file_object:
    # store file data in object
    datas = json.load(file_object)

orders = datas['variables']
batches = datas['constraints']
batch_order = datas['varCon']
order_batch = {}
print(batch_order)
for order in orders:
    print(order)
    order_batch[order] = {}
    for batch in batches:
        if order in batch_order[batch][order]:
            order_batch[order][batch] = batch_order[batch][order]


print(order_batch)
