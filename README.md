# Path-ranking-algorithm
Implement the Path ranking algorithm by python

NELL995_data 是NELL995的works_for关系数据集。


DFS.py 深度优先遍历获取基础路经，path_dfs_all.txt 是结果；path_dfs.txt 是部分结果；path_threshold.txt是加了限制后的结果


model.py 获取实体路经三元组的特征值，train_data.txt是全量的训练数据，第一位表示正例还是反例，其余维度是不同路经对应的特征值。
