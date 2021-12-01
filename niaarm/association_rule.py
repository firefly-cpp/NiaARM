import math


class AssociationRule:
    r"""Class for main operations and quality measures.

    Attributes:
        features (Iterable[Feature]): List of features.
        permutation (Iterable[])
    """

    def __init__(self, features):
        self.features = features
        self.permutation = []

    def build_rule(self, vector):
        rule = []

        permutation = self.map_permutation(vector)
        self.permutation = self.get_permutation(permutation)

        for i in range(len(self.features)):
            current_feature = self.permutation[i]

            threshold_position = self.get_current_position_of_feature(
                current_feature) + self.calculate_threshold_move(current_feature)

            vector_position = self.get_current_position_of_feature(
                current_feature)

            if vector[vector_position] > vector[threshold_position]:
                vector_position = vector_position + 2
                if self.features[current_feature].dtype == 'float':
                    border1 = (vector[vector_position] * (self.features[current_feature].max_val -
                               self.features[current_feature].min_val)) + self.features[current_feature].min_val
                    vector_position = vector_position + 1
                    border2 = (vector[vector_position] * (self.features[current_feature].max_val -
                               self.features[current_feature].min_val)) + self.features[current_feature].min_val

                    if border1 > border2:
                        inter = border1
                        border1 = border2
                        border2 = inter
                    borders = [border1, border2]
                    rule.append(borders)

                elif self.features[current_feature].dtype == 'int':
                    border1 = int(
                        math.ceil(
                            (vector[vector_position] *
                             (
                                self.features[current_feature].max_val -
                                self.features[current_feature].min_val))) +
                        self.features[current_feature].min_val)
                    vector_position = vector_position + 1
                    border2 = int(
                        math.ceil(
                            (vector[vector_position] *
                             (
                                self.features[current_feature].max_val -
                                self.features[current_feature].min_val))) +
                        self.features[current_feature].min_val)

                    if border1 > border2:
                        inter = border1
                        border1 = border2
                        border2 = inter
                    borders = [border1, border2]
                    rule.append(borders)

                else:
                    categories = self.features[current_feature].categories
                    selected = int(vector[vector_position]
                                   * (len(categories) - 1))
                    rule.append(
                        [self.features[current_feature].categories[selected]])
            else:
                rule.append('NO')
        return rule

    def map_permutation(self, vector):
        return vector[-len(self.features):]

    def is_rule_feasible(self, ant, con):
        ant_count = ant.count("NO")
        con_count = con.count("NO")
        if (ant_count == len(ant)) or (con_count == len(con)):
            return False
        else:
            return True

    def calculate_threshold_move(self, current_feature):
        if self.features[current_feature].dtype == "float" or self.features[current_feature].dtype == "int":
            move = 2
        else:
            move = 1
        return move

    def get_current_position_of_feature(self, feature):
        return feature * 3

    def return_permutation(self):
        return self.permutation

    def get_cut_point(self, sol, num_attr):
        cut = int(sol * num_attr)
        if cut == 0:
            cut = 1
        if cut > num_attr - 1:
            cut = num_attr - 2
        return cut

    def get_ant_con(self, rule, cut):
        ant = rule[:cut]
        con = rule[cut:]

        return ant, con

    def get_permutation(self, s):
        return sorted(range(len(s)), key=lambda k: s[k])

    def calculate_support_confidence(
            self,
            antecedent,
            consequence,
            transactions):

        supp = 0
        conf = 0
        conf_counter = 0

        # firstly antecedent
        for i in range(0, len(transactions)):
            match1 = 0
            match2 = 0
            for l in range(len(antecedent)):
                if self.features[self.permutation[l]
                                 ].dtype == 'float' or self.features[self.permutation[l]].dtype == 'int':
                    if antecedent[l] == 'NO':
                        pass
                    else:
                        border = antecedent[l]
                        if (float(transactions[i][self.permutation[l]]) >= border[0]) and (
                                float(transactions[i][self.permutation[l]]) <= border[1]):
                            match1 = match1 + 1
                elif self.features[self.permutation[l]].dtype == 'cat':
                    if antecedent[l] == 'NO':
                        pass
                    else:
                        ant = antecedent[l]
                        if transactions[i][self.permutation[l]
                                           ] == ant[0]:
                            match1 = match1 + 1

            # secondly consequence
            con_counter = 0
            for ll in range(
                    len(antecedent),
                    len(antecedent) +
                    len(consequence)):
                if self.features[self.permutation[ll]
                                 ].dtype == 'float' or self.features[self.permutation[ll]].dtype == 'int':
                    if consequence[con_counter] == 'NO':
                        pass
                    else:
                        border = consequence[con_counter]
                        if (float(transactions[i][self.permutation[ll]]) >= border[0]) and (
                                float(transactions[i][self.permutation[ll]]) <= border[1]):
                            match2 = match2 + 1
                elif self.features[self.permutation[ll]].dtype == 'cat':
                    if consequence[con_counter] == 'NO':
                        pass
                    else:
                        con = consequence[con_counter]

                        if transactions[i][self.permutation[ll]] == con[0]:
                            match2 = match2 + 1

                con_counter = con_counter + 1

            missing_ant = antecedent.count('NO')
            missing_con = consequence.count('NO')

            if (missing_ant + match1) == len(antecedent):
                conf_counter += 1
                if (missing_con + match2) == len(consequence):
                    conf = conf + 1

            skupno = match1 + match2 + missing_ant + missing_con

            if skupno == len(self.features):
                supp = supp + 1

            if (missing_ant + missing_con) == len(self.features):
                supp = 0.0

        skupni_supp = supp / transactions
        if conf_counter == 0:
            skupni_conf = 0.0
        else:
            skupni_conf = conf / conf_counter

        return skupni_supp, skupni_conf

    def check_no(self, antecedent, consequence):
        check = True
        missing_ant = antecedent.count("NO")
        missing_con = consequence.count("NO")

        if missing_ant == len(antecedent):
            check = False

        if missing_con == len(consequence):
            check = False

        return check

    def calculate_coverage(self, antecedent, consequence):
        missing_ant = antecedent.count("NO")
        missing_con = consequence.count("NO")

        missing_total = missing_ant + missing_con

        return (1 - float(float(missing_total) / float(len(self.features))))

    def calculate_fitness(self, alpha, beta, gamma, delta, support, confidence, shrinkage, coverage):
        fitness = ((alpha * support) +  (beta * confidence) + (gamma * shrinkage) + (delta * coverage)) / (alpha + beta + gamma + delta)
