
from collections import defaultdict


class Graph(object):
    """ Adjacency list representation of the hierarchy graph
    Args:
        items: type(set), Unique nodes in the graph
    Attributes:
        items: type(set), Unique nodes (items) in the graph
        graph: type(dict(list)), Adjacency list graph
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
    """Builds the class precedence list using fish-hook algorithm
    Args:
        hierarchy_graph: type(Graph), Unique nodes in the graph
        cpl_node: type(str), The item to build CPL for
        trace_mode: type(int), flag for the single stepping mode
    Attributes:
        hierarchy_graph: type(Graph), Unique nodes in the graph
        cpl_node: type(str), The item to build CPL for
        trace_mode: type(int), flag for the single stepping mode
        cpl: type(list), The resulting CPL
        fish_hook_pairs: type(dict(list)), Fish hook pairs of the graph
        visited_fish_hook_pairs: type(set), fish-hook pairs that are crossed out
        exposed_table: type(dict(list)), Table finding next exposed items from visited fish-hook pairs
        exposed_items: type(set), Available exposed items for next iteration
    """

    def __init__(self, hierarchy_graph, cpl_node, trace_mode):
        self.cpl_node = cpl_node
        self.cpl = []
        self.hierarchy_graph = hierarchy_graph
        self.fish_hook_pairs = dict()
        self.visited_fish_hook_pairs = set()
        self.exposed_table = dict()
        self.exposed_items = set()
        self.trace_mode = trace_mode

        self._init_fish_hook_pairs()
        self._build_exposed_table()
        self._build_cpl()

    def _init_fish_hook_pairs(self):
        """Computes the fish-hook pairs for the hierarchy graph
        """
        for item in self.hierarchy_graph.items:
            self.fish_hook_pairs[item] = []
            pair_item1 = item
            for pair_item in self.hierarchy_graph.graph[item]:
                pair_item2 = pair_item
                self.fish_hook_pairs[item].append((pair_item1, pair_item2))
                pair_item1 = pair_item2

    def _build_exposed_table(self):
        """Exposed table keeps track of the exposed items at each iteration
        by looking at the number of times each item appeared in the left and
        right side of the fish hook.
        """
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
                if (pair_item1 == exposed
                    or pair_item2 == exposed and (pair_item1, pair_item2)
                        not in self.visited_fish_hook_pairs):
                    # strike out the pair
                    self.visited_fish_hook_pairs.add((pair_item1, pair_item2))
                    self.exposed_table[pair_item2][1] -= 1
                    self.exposed_table[pair_item1][0] -= 1

    def _is_superclass(self, item, cpl_item):
        for adj_nodes in self.hierarchy_graph.graph[item]:
            if adj_nodes == cpl_item:
                return True
        return False

    def _update_exposed_items(self):
        for item in self.hierarchy_graph.items:
            if self.exposed_table[item][1] == 0 and item not in set(self.cpl):
                self.exposed_items.add(item)

    def print_fish_hook_pairs(self):
        state_str = "{0:25s} {1:6s} {2:6s}".format(
            "Node", "  " * 6, "Fish-hook pairs"
        )
        state_str += "\n"
        state_str += "{0:25s} {1:6s} {2:6s}".format(
            "----", "  " * 6, "--------------"
        )
        state_str += "\n"
        for node, fish_hook_pair in self.fish_hook_pairs.items():
            not_visited_fish_hook_pair = []
            for pair_item1, pair_item2 in fish_hook_pair:
                if (pair_item1, pair_item2) not in self.visited_fish_hook_pairs:
                    not_visited_fish_hook_pair.append((pair_item1, pair_item2))
            state_str += "{0:25s} {1:6s} {2:6s}".format(
                str(node), "  " * 6, str(not_visited_fish_hook_pair)
            )
            state_str += "\n"
        print(state_str)

    def _get_next_exposed(self):
        """Finds the next exposed item from the updated fish-hook table
        Tie braker: Selects the class that is a direct super-class of the
        lowest precedence class on the emerging class-precedence list
        """
        if self.trace_mode:
            self.print_fish_hook_pairs()
            print("--- CPL ---")
            print(self.cpl, "\n")
            input("> Press the key 'Enter' to continue: ")

        exposed = None
        if len(self.exposed_items) == 1:
            exposed = list(self.exposed_items)[-1]
            self._update_exposed_table(exposed)
            self._update_exposed_items()
            self.exposed_items.remove(exposed)
            return exposed
        elif len(self.exposed_items) > 1:
            # use the precedence relationship from Winston ch9 as tie breaker
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
            print("ERROR: No exposed item available!")
            return None

    def _build_cpl(self):
        """Builds the CPL ordering by processing the fish hooks
        """
        while len(self.cpl) != len(self.hierarchy_graph.items):
            exposed = self._get_next_exposed()
            if exposed not in self.cpl:
                self.cpl.append(exposed)
