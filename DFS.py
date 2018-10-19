# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
sys.setrecursionlimit(20000000)

class graph:

	def __init__(self):

		self.nodes =  {} # 节点名字到(r,子节点)组构成的词典
		self.paths = [] # 记录所有搜索到的路径
		self.begin = ""
		self.path = defaultdict(list) # 记录单条路径
		# self.times = 0  # 已经搜索到多少路径了？
		self.max_length = 5
		self.end = ""
		self.steps = 0

	def add(self, node, relation, next_node):
		if node in self.nodes:
			if next_node not in self.nodes:  # 需要先建立Node结构
				self.nodes[next_node] = Node(next_node)
			self.nodes[node].conjunctions.append((relation, self.nodes[next_node]))
		else:
			self.nodes[node] = Node(node) # 创建头节点，然后依然调用此函数
			self.add(node, relation,next_node)


	def set_init(self, begin, end, max_length): # 路径搜索时，初始化一些参数

		self.begin = begin
		self.end = end
		self.max_length = max_length
		self.path = [("root",self.begin)]
		# self.max_times = max_search_times


	def dfs(self, relation, begin): # 深度优先搜索

		if begin == self.end:

			tem = []
			for n in self.path:
				tem.append(n)

			self.paths.append(tem)
			# print("paths",self.paths)
			return

		if self.nodes[begin].conjunctions is None:
			return

		if len(self.path) == self.max_length+1: # 设置一下最大路径长度
			return

		for (_relation, subnode) in self.nodes[begin].conjunctions:

			if (_relation, subnode.NodeName) not in self.path:
				# print((_relation, subnode.NodeName))
				self.path.append((_relation, subnode.NodeName))
				self.dfs(_relation, subnode.NodeName)
				self.path.remove((_relation, subnode.NodeName))
				# print(self.path)
		return

"""
对于知识图谱来说，这里的每个节点不仅包含节点的名称，而且包含从它出去的每个关系以及关系的另一端的另一个节点
"""
class Node:

	def __init__(self,NodeName):
		self.NodeName = NodeName
		self.conjunctions = []


if __name__ == "__main__":

	kg = graph()
	with open("../concept_worksfor/graph.txt","r") as f:
		datas = f.readlines()
		for data in datas:
			[node, relation, next_node] = data.strip().split("\t")
			# print(node)
			kg.add(node, relation, next_node)
	begin = "concept_architect_opinion"
	end = "concept_stateorprovince_times"
	max_length = 4
	kg.set_init(begin, end, max_length)
	print("开始BFS：\n")
	kg.dfs("root",begin)
	for path in kg.paths:
		print(path)
	# m = len(kg.paths)
	# n = len(list(set(kg.paths)))
	# print(m,n)

