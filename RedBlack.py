from graphviz import Digraph
import uuid
import matplotlib.pyplot as plt
import networkx as nx
import uuid

class Node:
    def __init__(self, data):
        self.data = data
        self.color = 'RED'  # New nodes are red by default
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL_LEAF = Node(None)  # Sentinel NIL leaf node
        self.NIL_LEAF.color = 'BLACK'
        self.root = self.NIL_LEAF

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL_LEAF:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def _fix_insert(self, k):
        while k.parent and k.parent.color == 'RED':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'RED':
                    k.parent.color = 'BLACK'
                    u.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self._right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'RED':
                    k.parent.color = 'BLACK'
                    u.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self._left_rotate(k.parent.parent)
        self.root.color = 'BLACK'

    def insert(self, data):
        node = Node(data)
        node.left = self.NIL_LEAF
        node.right = self.NIL_LEAF
        if self.root == self.NIL_LEAF:
            self.root = node
            node.color = 'BLACK'
        else:
            current = self.root
            while current != self.NIL_LEAF:
                parent = current
                if node.data < current.data:
                    current = current.left
                else:
                    current = current.right
            node.parent = parent
            if node.data < parent.data:
                parent.left = node
            else:
                parent.right = node
            self._fix_insert(node)

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        while node.left != self.NIL_LEAF:
            node = node.left
        return node

    def _fix_delete(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.right.color == 'BLACK':
                        s.left.color = 'BLACK'
                        s.color = 'RED'
                        self._right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.right.color = 'BLACK'
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self._right_rotate(x.parent)
                    s = x.parent.left
                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.left.color == 'BLACK':
                        s.right.color = 'BLACK'
                        s.color = 'RED'
                        self._left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.left.color = 'BLACK'
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def delete(self, data):
        node = self.root
        z = self.NIL_LEAF
        while node != self.NIL_LEAF:
            if node.data == data:
                z = node
            if node.data <= data:
                node = node.right
            else:
                node = node.left
        if z == self.NIL_LEAF:
            print("Couldn't find key in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL_LEAF:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'BLACK':
            self._fix_delete(x)

    def search(self, data):
        current = self.root
        while current != self.NIL_LEAF and current.data != data:
            if data < current.data:
                current = current.left
            else:
                current = current.right
        return current if current != self.NIL_LEAF else None

class VisualRedBlackTree(RedBlackTree):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()

    def visualize_tree(self):
        self.graph = nx.DiGraph()  # Reset graph
        self._add_nodes_edges(self.root)
        
        pos = nx.drawing.nx_agraph.graphviz_layout(self.graph, prog="dot")
        colors = [self.graph.nodes[node]['color'] for node in self.graph.nodes]
        labels = nx.get_node_attributes(self.graph, 'label')

        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, with_labels=True, labels=labels, node_color=colors, 
                edge_color='black', node_size=1000, font_size=10, font_weight='bold')
        file_name = f"rb_tree_{uuid.uuid4()}.png"
        plt.savefig(file_name)
        plt.show()
        print(f"Tree visualization saved as {file_name}")

    def _add_nodes_edges(self, node):
        if node == self.NIL_LEAF:
            return

        color = "black" if node.color == "BLACK" else "red"
        label = str(node.data) if node.data is not None else "NIL"

        # Add the current node
        self.graph.add_node(str(id(node)), label=label, color=color)

        # Add edges to children
        if node.left != self.NIL_LEAF:
            self.graph.add_edge(str(id(node)), str(id(node.left)))
            self._add_nodes_edges(node.left)

        if node.right != self.NIL_LEAF:
            self.graph.add_edge(str(id(node)), str(id(node.right)))
            self._add_nodes_edges(node.right)

    def insert(self, data):
        print(f"Inserting {data}")
        super().insert(data)
        self.visualize_tree()

    def delete(self, data):
        print(f"Deleting {data}")
        super().delete(data)
        self.visualize_tree()


# class VisualRedBlackTree(RedBlackTree):
#     def __init__(self):
#         super().__init__()
#         self.dot = Digraph(comment="Red-Black Tree")

#     def visualize_tree(self):
#         self.dot = Digraph(comment="Red-Black Tree")  # Reset graph
#         self._add_nodes_edges(self.root)
#         file_name = f"rb_tree_{uuid.uuid4()}.gv"
#         self.dot.render(file_name, format="png", cleanup=True)
#         print(f"Tree visualization saved as {file_name}.png")

#     def _add_nodes_edges(self, node):
#         if node == self.NIL_LEAF:
#             return
        
#         color = "black" if node.color == "BLACK" else "red"
#         self.dot.node(str(id(node)), label=str(node.data), color=color, fontcolor=color)

#         if node.left != self.NIL_LEAF:
#             self.dot.edge(str(id(node)), str(id(node.left)), label="L")
#             self._add_nodes_edges(node.left)
        
#         if node.right != self.NIL_LEAF:
#             self.dot.edge(str(id(node)), str(id(node.right)), label="R")
#             self._add_nodes_edges(node.right)

#     def insert(self, data):
#         print(f"Inserting {data}")
#         super().insert(data)
#         self.visualize_tree()

#     def delete(self, data):
#         print(f"Deleting {data}")
#         super().delete(data)
#         self.visualize_tree()


# Example Usage
if __name__ == "__main__":
    rbt = VisualRedBlackTree()
    rbt.insert(8453)
    rbt.insert(4553)
    rbt.insert(453)
    rbt.insert(843)
    rbt.insert(84)
    rbt.insert(20)
    rbt.insert(30)
    rbt.insert(15)
    rbt.insert(25)
    rbt.insert(5)
    rbt.insert(15)  # Automatically visualizes the updated tree
    rbt.delete(10)  # Automatically visualizes the updated tree
    rbt.delete(20)

    # # Search for a node
    # node = rbt.search(15)
    # if node:
    #     print("Node found:", node.data)
    # else:
    #     print("Node not found")

    # Delete a node
