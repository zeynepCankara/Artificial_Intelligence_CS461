"""
@Date: 14/04/2021 ~ Version: 1.1
@Group: RIDDLER
@Author: Ahmet Feyzi Halaç
@Author: Aybars Altınışık
@Author: Ege Şahin
@Author: Göktuğ Gürbüztürk
@Author: Zeynep Cankara


@Description: A rule based Zookeeper System from Winston chapter 7
              - Contains classes Zookeeper, Rule
              - Zookeeper class implements bacward-chaining

"""


class Rule(object):
    def __init__(self, antecedents, consequents, rule_no=""):
        """Antecedent-consequent rules
        Uses tree structure to find possible connections between rules
        Args:
          antecedents, type(list)
          consequents, type(list)
          antecedents_rules, type(list(Rule))
          consequents_rules, type(list(Rule))
        """
        self.antecedents = set(antecedents)
        self.consequents = set(consequents)
        # the list of rules leading to current rule
        self.antecedents_rules = []
        # the list of rules the current rule leads to
        self.consequents_rules = []
        self.rule_no = rule_no

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
        return self.rule_no

    def __str__(self):
        """String representation of the rule
        Returns:
            type(str), formatted string
        """
        state_str = (self.rule_no + "\n")
        state_str += "antecedents(" + str(self.antecedents) + ") -> "
        state_str += "consequents( " + str(self.consequents) + ") \n"
        return state_str


# define set of rules from Winston ch. 7 for the  Zookeeper
Z1 = Rule(["?x has hair"], ["?x is a mammal"], "Z1")
Z2 = Rule(["?x gives milk"], ["?x is a mammal"], "Z2")
Z3 = Rule(["?x has feathers"], ["?x is a bird"], "Z3")
Z4 = Rule(["?x flies", "?x lays eggs"], ["?x is a bird"], "Z4")
Z5 = Rule(["?x is a mammal", "?x eats meat"], ["?x is a carnivore"], "Z5")
Z6 = Rule(["?x is a mammal", "?x has pointed teeth", "?x has claws",
           "?x has forward-pointing eyes"], ["?x is a carnivore"], "Z6")
Z7 = Rule(["?x is a mammal", "?x has hoofs"], ["?x is an ungulate"], "Z7")
Z8 = Rule(["?x is a mammal", "?x chews cud"], ["?x is an ungulate"],  "Z8")
Z9 = Rule(["?x is a carnivore", "?x has a tawny color",
           "?x has dark spots"], ["?x is a cheetah"], "Z9")
Z10 = Rule(["?x is a carnivore", "?x has a tawny color",
            "?x has black stripes"], ["?x is a tiger"], "Z10")
Z11 = Rule(["?x is an ungulate", "?x has long legs",
            "?x has a long neck", "?x has a tawny color", "?x has dark spots"],
           ["?x is a giraffe"], "Z11")
Z12 = Rule(["?x is an ungulate", "?x has white color", "?x has black stripes"],
           ["?x is a zebra"], "Z12")
Z13 = Rule(["?x is a bird", "?x does not fly",
            "?x has long legs", "?x has a long neck", "?x is black and white"],
           ["?x is an ostrich"],  "Z13")
Z14 = Rule(["?x is a bird", "?x does not fly",
            "?x swims", "?x is black and white"], ["?x is a penguin"], "Z14")
Z15 = Rule(["?x is a bird", "?x is a good flyer"],
           ["?x is an albatross"], "Z15")


class Zookeeper(object):
    def __init__(self, wm, traceMode):
        """Rule based Zookeeper system constructor
        Args:
          wm: type(list), working memory
          traceMode: type(bool), flag for enabling single stepping mode
        Attributes:
          wm: type(list), working memory
          traceMode: type(bool), flag for enabling single stepping mode
          rules: type(list(Rule)), list of rules for BC
        """
        self.wm = wm
        self.traceMode = traceMode

        self.rules = [Z1, Z2, Z3, Z4, Z5, Z6, Z7,
                      Z8, Z9, Z10, Z11, Z12, Z13, Z14, Z15]

        for i, rule in enumerate(self.rules):
            rule.set_consequents_rules(
                [Z for idx, Z in enumerate(self.rules) if idx != i])
            rule.set_antecedents_rules(
                [Z for idx, Z in enumerate(self.rules) if idx != i])

    def backward_chaining(self, animalName, hypothesis):
        """Tests the animal against hypothesis
        """
        for i in range(8, 15):
            if ("?x " + hypothesis) in self.rules[i].consequents:
                found = self.recursiveBackward(self.rules[i], animalName)
                break
        if not found:
            i = -1
            print("Animal is not found!")
        else:
            for final_conseq in self.rules[i].consequents:
                print(animalName, final_conseq[3:])
                print()

    def recursiveBackward(self, rule, animalName):
        if self.traceMode:
            print('Checking for rule', rule.rule_no)
        # Initially, assume all rules are satisfied. If there are any counter-examples, make this variable false, return true otherwise
        rulesSatisfied = True
        for antecedent in rule.antecedents:
            if self.traceMode:
                input()
                print('Checking if', antecedent.replace('?x', animalName))
            # Initially, assume specified antecedent is basic, meaning there are no rules whose consequent is this antecedent
            # If there is any rule which disproves this assumption, make it false
            basicAntecedent = True

            # There can be multiple rules with same consequence equal to specified antecedent
            # So, initially, assume there are no triggered rules whose consequence equals to specified antecedent
            # If any rule returns true, make this variable true
            validRuleExists = False

            # Look for a rule whose consequence is specified antecedent
            for antecedent_rule in rule.antecedents_rules:
                if antecedent in antecedent_rule.consequents:
                    # Rule is found, so antecedent is not a basic one
                    basicAntecedent = False

                    # Call recursiveBackward with this rule
                    if self.recursiveBackward(antecedent_rule, animalName):
                        # Rule is triggered
                        validRuleExists = True
                        break

            if basicAntecedent:
                # Antecedent is a basic one, so, just search working memory for antecedent
                if antecedent not in self.wm:
                    # Antecedent is not in working memory, so rule should not be satisfied
                    rulesSatisfied = False
                    if self.traceMode:
                        print('\'' + antecedent.replace('?x',
                                                        animalName) + '\' is wrong')
                    break
            else:
                # Antecedent is not a basic antecedent
                if not validRuleExists:
                    # There are no satisfied rules whose consequence is specified antecedent
                    rulesSatisfied = False
                    if self.traceMode:
                        print('\'' + antecedent.replace('?x',
                                                        animalName) + '\' is wrong')
                    break
            if self.traceMode:
                if rulesSatisfied:
                    print(antecedent.replace('?x', animalName))

        return rulesSatisfied

    def __repr__(self):
        return "Zookeeper()"

    def __str__(self):
        """String representation of the zookeeper state
        Returns:
            type(str), formatted string
        """
        state_str = "*** Zookeeper *** \n"
        state_str += "working memory: \n" + str(self.wm) + "\n"
        state_str += "rules: \n" + str(self.rules) + "\n"
        return state_str

    def __eq__(self, other):
        """Comparison function for Zookeepers
        Args:
            other: type(State), state to be compared
        Returns:
            type(bool) true if they are equal, false otherwise
        """
        return (
            self.wm == other.wm and self.rule == other.rules
        )

    def __hash__(self):
        """Calculates an hash number from the properties indicated.
        Hash can be used in comparison of two instances.
        Returns:
            type(int) hash number
        """
        return hash(
            (
                self.wm,
                self.rules,
            )
        )
