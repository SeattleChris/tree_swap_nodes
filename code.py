#!/bin/python3

import os
from collections import deque

#
# Complete the 'swapNodes' function below.
#
# The function is expected to return a 2D_INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY indexes
#  2. INTEGER_ARRAY queries
#

class Node:
    def __init__(self, idx):
        self.index = idx
        self.left = None
        self.right = None


def tree_by_depth(root):
    q = deque([[root]])
    depth, tree_gens = 0, {}
    while q:
        depth += 1
        generation = q.popleft()
        tree_gens[depth] = generation
        nxt = [
            child
            for ea in generation
            for child in (ea.left, ea.right)
            if child is not None
        ]
        if nxt:
            q.append(nxt)
    return tree_gens

def tree_from_indexes(indexes):
    root = Node(1)
    q = deque([root])
    for (left, right) in indexes:
        curr = q.popleft()
        curr.left = Node(left) if left != -1 else None
        curr.right = Node(right) if right != -1 else None
        q.extend([ea for ea in (curr.left, curr.right) if ea is not None])
    if len(q):
        # print(f"Remaining {list(q)}")
        raise ValueError("Invalid indexes to represent Nodes.")
    return root

def inorder(curr):
    visit, data = deque(), []
    while curr is not None:
        while curr.left is not None:
            visit.append(curr)
            curr = curr.left
        data.append(curr.index)
        while curr.right is None and visit:
            curr = visit.pop()
            data.append(curr.index)
        curr = curr.right
    return data

def swapNodes(indexes, queries):
    root = tree_from_indexes(indexes)
    gen_tree = tree_by_depth(root)
    result = []
    for pos in queries:
        for depth, generation in gen_tree.items():
            if depth % pos:
                continue
            for node in generation:
                node.left, node.right = node.right, node.left
        result.append(inorder(root))
    return result


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input().strip())
    indexes = []
    for _ in range(n):
        indexes.append(list(map(int, input().rstrip().split())))
    queries_count = int(input().strip())
    queries = []
    for _ in range(queries_count):
        queries_item = int(input().strip())
        queries.append(queries_item)
    result = swapNodes(indexes, queries)
    fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
    fptr.write('\n')
    fptr.close()
