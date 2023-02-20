import networkx as nx
import matplotlib.pyplot as plt


def tree_from_prufer(code):
    """
    Builds tree from Prufer code

    :param code: Prufer code
    :type code: list

    :return: tree generated from Prufer code
    :rtype: nx.Graph()
    """
    code_len = len(code)
    if any(i > code_len + 2 for i in code):
        return None

    vertices = [i for i in range(1, len(code) + 3)]
    tree = nx.Graph()
    for _ in range(code_len):
        # looking for min vertex to pair
        temp = vertices.copy()
        while True:
            minimal = min(temp)
            temp.remove(minimal)
            if minimal not in code:
                break
        tree.add_edge(code[0], minimal)
        vertices.remove(minimal)
        code.pop(0)

    # last edge of 2 remaining vertices in prufer sequence
    tree.add_edge(vertices[0], vertices[1])
    return tree


def create_tree(vertices, edges):
    """
    Builds tree from given lists of vertices and edges

    :param vertices: List of vertices
    :type vertices: list

    :param edges: list of edges
    :type edges: list

    :return: tree generated from given lists of vertices and edges
    :rtype: nx.Graph()
    """
    if vertices is None and edges is None:
        return None

    tree = nx.Graph()
    if vertices is not None:
        tree.add_nodes_from(vertices)

    if edges is not None:
        for edge in edges:
            tree.add_edge(edge[0], edge[1])

    return tree
