

class Zookeeper(object):
    def __init__(self):
        """Rule based Zookeeper system constructor
        Args:

        Attributes:

        """
        # TODO: set the rules as a graph structure
        self.rules = [Z1, Z2, Z3, Z4, Z5, Z6, Z7,
                      Z8, Z9, Z10, Z11, Z12, Z13, Z14, Z15]
        # TODO: Iterate over each rules and set the ancestor and consequent rules that can be reachable
        for i, rule in enumerate(self.rules):
            rule.set_consequents_rules(
                [Z for idx, Z in enumerate(self.rules) if idx != i])
            rule.set_antecedents_rules(
                [Z for idx, Z in enumerate(self.rules) if idx != i])

    def backward_chaining(self, hypotheses):
        """Tests set of hypotheses to identify the animal
        TODO: Implement backward_chaining
        """
        return None

    def __repr__(self):
        return "Zookeeper()"

    def __str__(self):
        """String representation of the zookeeper state
        Returns:
            type(str), formatted string
        """
        state_str = ""
        return state_str

    def __eq__(self, other):
        """Comparison function for states
        Args:
            other: type(State), state to be compared
        Returns:
            type(bool) true if they are equal, false otherwise
        """

    def __hash__(self):
        """Calculates an hash number from the properties indicated.
        Hash can be used in comparison of two instances.
        Returns:
            type(int) hash number
        """
        return hash(
            (
                self.rules,
            )
        )


class Rule(object):
    def __init__(self, antecedents, consequents):
        """Antecedent-consequent rules
        Uses tree structure to find possible descendants
        Args:
          antecedents, type(list)
          consequents, type(list)
          antecedents_rules, type(list(Rule))
          consequents_rules, type(list(Rule))
        """
        self.antecedents = set(antecedents)
        self.consequents = set(consequents)
        self.antecedents_rules = []
        self.consequents_rules = []

    def get_antecedents(self, consequents):
        """ Returns the set of antecedents if all consequents satisfied
        Args:
            consequents: type(list(str))
        Returns:
            antecedents: type(set(str))
        """
        if set(consequents) != self.consequents:
            return None
        return self.antecedents

    def get_consequents(self, antecedents):
        """ Returns the set of consequents if all antecedents satisfied
        Args:
            antecedents: type(list(str))
        Returns:
            consequents: type(set(str))
        """
        if set(antecedents) != self.antecedents:
            return None
        return self.consequents

    def set_consequents_rules(self, rules):
        """ Sets possible rules can reached from the given rule
        Args:
            rules: type(list(Rule))
        """
        for rule in rules:
            for consequent in self.consequents:
                if consequent in rule.antecedents:
                    self.consequents_rules.append(rule)

    def set_antecedents_rules(self, rules):
        """ Sets possible rules can reached to the current rule
        Args:
            rules: type(list(Rule))
        """
        for rule in rules:
            for antecedent in self.antecedents:
                if antecedent in rule.consequents:
                    self.antecedents_rules.append(rule)

    def __repr__(self):
        return "Rule()"

    def __str__(self):
        """String representation of the rule
        Returns:
            type(str), formatted string
        """
        state_str = ""
        state_str += "antecedents(" + str(self.antecedents) + ") -> "
        state_str += "consequents( " + str(self.consequents) + ") \n"
        return state_str


# define set of rules from Winston ch. 7
Z1 = Rule(["?x has hair"], ["?x is a mammal"])
Z2 = Rule(["?x gives milk"], ["?x is a mammal"])
Z3 = Rule(["?x has feathers"], ["?x is a bird"])
Z4 = Rule(["?x flies", "?x lays eggs"], ["?x is a bird"])
Z5 = Rule(["?x is a mammal", "?x eats meat"], ["?x is a carnivore"])
Z6 = Rule(["?x is a mammal", "?x has pointed teeth", "?x has claws",
           "?x has forward-pointing eyes"], ["?x is a carnivore"])
Z7 = Rule(["?x is a mammal", "?x has hoofs"], ["?x is an ungulate"])
Z8 = Rule(["?x is a mammal", "?x chews cud"], ["?x is an ungulate"])
Z9 = Rule(["?x is a carnivore", "?x has tawny color",
           "?x has dark spots"], ["?x is a cheetah"])
Z10 = Rule(["?x is a carnivore", "?x has tawny color",
            "?x has black stripes"], ["?x is a tiger"])
Z11 = Rule(["?x is an ungulate", "?x has long legs",
            "?x has long neck", "?x has tawny color", "?x has dark spots"],
           ["?x is a giraffe"])
Z12 = Rule(["?x is an ungulate", "?x has white color", "?x has black stripes"],
           ["?x is a zebra"])
Z13 = Rule(["?x is a bird", "?x does not fly",
            "?x has long legs", "?x has long neck", "?x is black and white"],
           ["?x is an ostrich"])

Z14 = Rule(["?x is a bird", "?x does not fly",
            "?x swims", "?x is black and white"], ["?x is a penguin"])
Z15 = Rule(["?x is a bird", "?x is a good flyer"], ["?x is an albatross"])
