from collections import defaultdict

class Model():

    def __init__(self):
        self.data_file = "./Nell995_data/Graph.txt"
        self.path_file = "paths_threshold.txt"
        self.train_file = "./Nell995_data/train.pairs"
        self.nodes = {} # 记录节点的关系信息
        self.train_data = defaultdict(list)
        self.set_range()

    def set_range(self): # 设置关系的值域和节点的关系信息
        with open(self.data_file,"r") as f:
            datas = f.readlines()
            for data in datas:
                node_1, relation, node_2 = data.strip().split("\t")
                if node_1 not in self.nodes.keys():
                    tem_node = Node(node_1)
                    self.nodes[node_1] = tem_node
                self.nodes[node_1].add(relation, node_2)

    def prob(self, begin, end, relation_path): # 采取后向截断的动态规划
        prob = 0
        length = len(relation_path)
        if length == 1:
            if end in self.nodes[begin].info[relation_path[0]]:
                prob = 1/len(self.nodes[begin].info[relation_path[0]])
            else:
                prob = 0
            return prob
        else:
            if self.nodes[begin].info[relation_path[0]] == []:
                return 0
            else:
                for entity in self.nodes[begin].info[relation_path[0]]:
                    prob += (1/len(self.nodes[begin].info[relation_path[0]])) * self.prob(entity, end, relation_path[1:])
                return prob

    def get_probs(self): # 完全按照随机游走的公式来计算路径概率

        relation_paths = []
        with open(self.path_file,"r") as f:
            paths = f.readlines()
            for path in paths:
                relation_paths.append(path.strip().split("\t")[1:])

        with open(self.train_file,"r") as f:
            datas = f.readlines()
            for data in datas:
                [node_1, node_2] = data.strip()[0:-3].split(",")
                node_1 = node_1.replace("thing$","")
                if node_1 not in self.nodes.keys():
                    print("发现未注册实体:%s"%node_1)
                    continue
                else:
                    node_2 = node_2.replace("thing$","")
                    flag = data.strip()[-1]
                    if flag == "+":
                        self.train_data[(node_1,node_2)].append(0)
                    else:
                        self.train_data[(node_1,node_2)].append(1)
                    for path in relation_paths:
                        tem = self.prob(node_1,node_2,path)

                        self.train_data[(node_1, node_2)].append(tem)

        with open("train_data.txt","w") as f:
            for key in self.train_data:
                f.write(str(key)+"\t"+str(self.train_data[key])+"\n")
        return


class Node:

    def __init__(self,NodeName):
        self.name = NodeName
        self.info = defaultdict(list) # 记录从实体NodeName出发，经关系relation,能到达的实体
    def add(self,relation, subnode):
        self.info[relation].append(subnode)

if __name__ == "__main__":

    model = Model()
    model.get_probs()
