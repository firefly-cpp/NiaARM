class AssociationRule:
    r"""Class for main operations and quality measures.

    Attributes:
        features (list[Feature]): List of features.
        permutation (list[int]): Permuted feature indices,
    """

    def __init__(self, features):
        self.features = features
        self.permutation = []

    def build_rule(self, vector):
        rule = []

        permutation = self.map_permutation(vector)
        self.permutation = _get_permutation(permutation)

        for i in range(len(self.features)):
            current_feature = self.permutation[i]
            feature = self.features[current_feature]

            # set current position in the vector
            vector_position = self.feature_position(current_feature)

            # get a threshold for each feature
            threshold_position = vector_position + self.threshold_move(current_feature)

            if vector[vector_position] > vector[threshold_position]:
                if feature.dtype == 'float':
                    border1 = vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val
                    vector_position = vector_position + 1
                    border2 = vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val

                    if border1 > border2:
                        border1, border2 = border2, border1
                    borders = [border1, border2]
                    rule.append(borders)

                elif feature.dtype == 'int':
                    border1 = round(vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val)
                    vector_position = vector_position + 1
                    border2 = round(vector[vector_position] * (feature.max_val - feature.min_val) + feature.min_val)

                    if border1 > border2:
                        border1, border2 = border2, border1
                    borders = [border1, border2]
                    rule.append(borders)
                else:
                    categories = feature.categories
                    selected = round(vector[vector_position] * (len(categories) - 1))
                    rule.append([feature.categories[selected]])
            else:
                rule.append('NO')

        return rule

    def map_permutation(self, vector):
        return vector[-len(self.features):]

    def threshold_move(self, current_feature):
        if self.features[current_feature].dtype == "float" or self.features[current_feature].dtype == "int":
            move = 2
        else:
            move = 1
        return move

    def feature_position(self, feature):
        position = 0
        for i in range(feature):
            if self.features[i].dtype == "float" or self.features[i].dtype == "int":
                position = position + 3
            else:
                position = position + 2
        return position

    def __match_antecedent(self, i, antecedent, transactions):
        match = 0
        for j in range(len(antecedent)):
            dtype = self.features[self.permutation[j]].dtype
            if dtype == 'float' or dtype == 'int':
                if antecedent[j] != 'NO':
                    border = antecedent[j]
                    if border[0] <= transactions[i, self.permutation[j]] <= border[1]:
                        match = match + 1
            elif dtype == 'cat':
                if antecedent[j] != 'NO':
                    ant = antecedent[j]
                    if transactions[i, self.permutation[j]] == ant[0]:
                        match = match + 1
        return match

    def __match_consequent(self, i, antecedent, consequent, transactions):
        match = 0
        con_counter = 0
        for ll in range(len(antecedent), len(antecedent) + len(consequent)):
            dtype = self.features[self.permutation[ll]].dtype
            if dtype == 'float' or dtype == 'int':
                if consequent[con_counter] != 'NO':
                    border = consequent[con_counter]
                    if border[0] <= transactions[i, self.permutation[ll]] <= border[1]:
                        match = match + 1
            elif dtype == 'cat':
                if consequent[con_counter] != 'NO':
                    con = consequent[con_counter]

                    if transactions[i, self.permutation[ll]] == con[0]:
                        match = match + 1

            con_counter = con_counter + 1
        return match

    def support_confidence(self, antecedent, consequent, transactions):
        supp = 0
        conf = 0
        conf_counter = 0

        for i in range(len(transactions)):
            match_antecedent = self.__match_antecedent(i, antecedent, transactions)
            match_consequent = self.__match_consequent(i, antecedent, consequent, transactions)

            missing_ant = antecedent.count('NO')
            missing_con = consequent.count('NO')

            if (missing_ant + match_antecedent) == len(antecedent):
                conf_counter += 1
                if (missing_con + match_consequent) == len(consequent):
                    conf = conf + 1

            total = match_antecedent + match_consequent + missing_ant + missing_con

            if total == len(self.features):
                supp = supp + 1

            if (missing_ant + missing_con) == len(self.features):
                supp = 0.0

        total_supp = supp / len(transactions)
        if conf_counter == 0:
            total_conf = 0.0
        else:
            total_conf = conf / conf_counter

        return total_supp, total_conf

    def coverage(self, antecedent, consequent):
        missing_total = antecedent.count("NO") + consequent.count("NO")
        return 1 - missing_total / len(self.features)

    def shrinkage(self, antecedent, consequent):
        differences = []

        for i in range(len(antecedent)):
            feature = self.features[self.permutation[i]]
            if feature.dtype == 'float' or feature.dtype == 'int':
                if antecedent[i] != 'NO':
                    borders = antecedent[i]
                    diff_borders = borders[1] - borders[0]
                    total_borders = feature.max_val - feature.min_val
                    diff = diff_borders / total_borders
                    differences.append(diff)

        con_counter = 0
        for ll in range(len(antecedent), len(antecedent) + len(consequent)):
            feature = self.features[self.permutation[ll]]
            if feature.dtype == 'float' or feature.dtype == 'int':
                if consequent[con_counter] != 'NO':
                    borders = consequent[con_counter]
                    diff_borders = borders[1] - borders[0]
                    total_borders = feature.max_val - feature.min_val
                    diff = diff_borders / total_borders
                    differences.append(diff)
            con_counter = con_counter + 1

        value = sum(differences)

        if len(differences) > 0:
            normalized = _normalize(value, [0, len(differences)], [0, 1])
        else:
            return 0.0
        return 1 - normalized

    def format_rules(self, antecedent, consequent):
        antecedent1 = []
        consequent1 = []

        for i in range(len(antecedent)):
            if antecedent[i] != "NO":
                feature = self.features[self.permutation[i]]
                if feature.dtype == "cat":
                    rule = feature.name + "(" + str(antecedent[i][0]) + ")"
                else:
                    rule = feature.name + "(" + str(antecedent[i]) + ")"
                antecedent1.append(rule)

        for i in range(len(consequent)):
            if consequent[i] != "NO":
                feature = self.features[self.permutation[i + len(antecedent)]]
                if feature.dtype == "cat":
                    rule = feature.name + "(" + str(consequent[i][0]) + ")"
                else:
                    rule = feature.name + "(" + str(consequent[i]) + ")"
                consequent1.append(rule)
        return antecedent1, consequent1


def _normalize(value, actual_bounds, real_bounds):
    return real_bounds[0] + (value - real_bounds[0]) * (real_bounds[1] - real_bounds[0]) / (
                actual_bounds[1] - actual_bounds[0])


def _rule_feasible(ant, con):
    return ant.count("NO") != len(ant) and con.count("NO") != len(con)


def _cut_point(sol, num_attr):
    cut = int(sol * num_attr)
    if cut == 0:
        cut = 1
    if cut > num_attr - 1:
        cut = num_attr - 2
    return cut


def _get_permutation(s):
    return sorted(range(len(s)), key=lambda k: s[k])
