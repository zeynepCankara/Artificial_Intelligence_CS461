
from collections import defaultdict

import pprint


class Graph(object):
    """ Adjacency list representation of the hierarchy graph
    """

    def __init__(self, items):
        self.items = items
        self.graph = defaultdict(list)

    def add_edge(self, from_node, to_node):
        self.graph[from_node].append(to_node)

    def add_direct_superclasses(self, from_node, to_direct_superclassses):
        self.graph[from_node].extend(to_direct_superclassses)

    def get_unique_items(self):
        return self.items


class CPL(object):

    """Build the class precedence list using fish-hook algorithm
    """

    def __init__(self, hierarchy_graph, cpl_node):
        self.cpl_node = cpl_node
        self.cpl = []
        self.hierarchy_graph = hierarchy_graph
        self.fish_hook_pairs = dict()
        self.visited_fish_hook_pairs = set()
        self.exposed_table = dict()
        self.exposed_items = set()
        pp = pprint.PrettyPrinter(indent=4)  # pretty printing

        self._init_fish_hook_pairs()
        pp.pprint(self.fish_hook_pairs)
        self._build_exposed_table()
        pp.pprint(self.exposed_table)
        self._build_cpl()

    def _init_fish_hook_pairs(self):
        for item in self.hierarchy_graph.items:
            self.fish_hook_pairs[item] = []
            pair_item1 = item
            for pair_item in self.hierarchy_graph.graph[item]:
                pair_item2 = pair_item
                self.fish_hook_pairs[item].append((pair_item1, pair_item2))
                pair_item1 = pair_item2

    def _build_exposed_table(self):
        for item in self.hierarchy_graph.items:
            self.exposed_table[item] = [0, 0]

        for item in self.hierarchy_graph.items:
            for pair_item1, pair_item2 in self.fish_hook_pairs[item]:
                self.exposed_table[pair_item1][0] += 1
                self.exposed_table[pair_item2][1] += 1

        for item in self.hierarchy_graph.items:
            if self.exposed_table[item][1] == 0 and item == self.cpl_node:
                self.exposed_items.add(item)

    def _update_exposed_table(self,  exposed):
        """Updates the exposed items based on the selected exposed item
        """
        # update the fish hooks and exposed items list
        for node, pair in self.fish_hook_pairs.items():
            for pair_item1, pair_item2 in pair:
                if pair_item1 == exposed or pair_item2 == exposed and (pair_item1, pair_item2) not in self.visited_fish_hook_pairs:
                    # strike out the pair
                    self.visited_fish_hook_pairs.add((pair_item1, pair_item2))
                    self.exposed_table[pair_item2][1] -= 1
                    self.exposed_table[pair_item1][0] -= 1

    def _is_superclass(self, cpl_item, item):
        for adj_nodes in self.hierarchy_graph.graph[item]:
            if adj_nodes == cpl_item:
                return True
        return False

    def _update_exposed_items(self):
        for item in self.hierarchy_graph.items:
            if self.exposed_table[item][1] == 0 and item not in set(self.cpl):
                self.exposed_items.add(item)

    def _get_next_exposed(self):
        exposed = None
        if len(self.exposed_items) == 1:
            exposed = list(self.exposed_items)[-1]
            self._update_exposed_table(exposed)
            self._update_exposed_items()
            self.exposed_items.remove(exposed)
            return exposed
        elif len(self.exposed_items) > 1:
            # use the precedence relationship
            for cpl_item in reversed(self.cpl):
                for item in list(self.exposed_items):
                    if self._is_superclass(cpl_item, item):
                        exposed = item
                        self._update_exposed_table(exposed)
                        self._update_exposed_items()
                        self.exposed_items.remove(exposed)
                        return exposed
                    else:
                        exposed = item
            self._update_exposed_table(exposed)
            self._update_exposed_items()
            self.exposed_items.remove(exposed)
            return exposed
        else:
            print("No exposed item available")
            return None

    def _build_cpl(self):
        # continue untill all the graph processed
        while len(self.cpl) != len(self.hierarchy_graph.items):
            exposed = self._get_next_exposed()
            if exposed not in self.cpl:
                self.cpl.append(exposed)
