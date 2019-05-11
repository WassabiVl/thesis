import json

result = {}
with open('DataSets/mknap1-2.txt') as f:
    lines = f.readlines()
i = 0
result['varCon'] = {}
y = 1
for line in lines:
    if i == 0:
        data = line.split(" ")
        result['variableNum'] = data[0]
        result['constrainNum'] = data[1]
        result['bestSolution'] = data[2].rstrip()
    if i == 1:
        datas = line.split(" ")
        x = 1
        result['variables'] = {}
        for data in datas:
            profit = {'vid': x, 'value': data.rstrip()}
            result['variables'][x] = profit
            x += 1
    if i == 2:
        datas = line.split(" ")
        x = 1
        result['constraints'] = {}
        for data in datas:
            profit = {'cid': x, 'weightLimit': data.rstrip()}
            result['constraints'][x] = profit
            x += 1
    else:
        datas = line.split(" ")
        result['varCon'][y] = {}
        x = 1
        for data in datas:
            profit = {'vid': x, "cid": y, 'weight': data.rstrip()}
            result['varCon'][y][x] = profit
            x += 1
        y += 1
    i += 1
print(result)
app_json = json.dumps(result)
with open('DataSets/mknap1-2.json', 'w') as json_file:
    json.dump(result, json_file)
