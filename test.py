n = 0
relation_path = []
with open("./Nell995_data/train.pairs", "r") as f:
    paths = f.readlines()
    for path in paths:
        if n < 10:
            [node_1, node_2] = path.strip()[0:-3].split(",")
            relation_paths.append([node_1.replace("thing$",""),node_2.replace("thing$","")])
            n += 1