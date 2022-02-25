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

            # get threshold for each feature
            threshold_position = self.get_vector_position_of_feature(
                current_feature) + self.calculate_threshold_move(current_feature)

            # set current position in vector
            vector_position = self.get_vector_position_of_feature(
                current_feature)

            if vector[vector_position] > vector[threshold_position]:
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
                    border1 = round(
                        (vector[vector_position] *
                         (
                            self.features[current_feature].max_val -
                            self.features[current_feature].min_val)) +
                        self.features[current_feature].min_val)
                    vector_position = vector_position + 1

                    border2 = round(
                        (vector[vector_position] *
                         (
                            self.features[current_feature].max_val -
                            self.features[current_feature].min_val)) +
                        self.features[current_feature].min_val)

                    if border1 > border2:
                        inter = border1
                        border1 = border2
                        border2 = inter
                    borders = [border1, border2]

                    rule.append(borders)

                else:
                    categories = self.features[current_feature].categories

                    selected = round(vector[vector_position] * (len(categories) - 1))

                    rule.append([self.features[current_feature].categories[selected]])
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

    def get_vector_position_of_feature(self, feature):
        position = 0
        for i in range(feature):
            if self.features[i].dtype == "float" or self.features[i].dtype == "int":
                position = position + 3
            else:
                position = position + 2
        return position

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
        for i in range(len(transactions)):
            match1 = 0
            match2 = 0
            for j in range(len(antecedent)):
                if self.features[self.permutation[j]].dtype == 'float' or self.features[self.permutation[j]].dtype == 'int':
                    if antecedent[j] != 'NO':
                        border = antecedent[j]
                        if (float(transactions[i][self.permutation[j]]) >= border[0]) and (
                                float(transactions[i][self.permutation[j]]) <= border[1]):
                            match1 = match1 + 1
                elif self.features[self.permutation[j]].dtype == 'cat':
                    if antecedent[j] != 'NO':
                        ant = antecedent[j]
                        if transactions[i][self.permutation[j]] == ant[0]:
                            match1 = match1 + 1

            # secondly consequence
            con_counter = 0
            for ll in range(
                    len(antecedent),
                    len(antecedent) +
                    len(consequence)):
                if self.features[self.permutation[ll]].dtype == 'float' or self.features[self.permutation[ll]].dtype == 'int':
                    if consequence[con_counter] != 'NO':
                        border = consequence[con_counter]
                        if (float(transactions[i][self.permutation[ll]]) >= border[0]) and (
                                float(transactions[i][self.permutation[ll]]) <= border[1]):
                            match2 = match2 + 1
                elif self.features[self.permutation[ll]].dtype == 'cat':
                    if consequence[con_counter] != 'NO':
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

            total = match1 + match2 + missing_ant + missing_con

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

    def calculate_coverage(self, antecedent, consequence):
        missing_ant = antecedent.count("NO")
        missing_con = consequence.count("NO")

        missing_total = missing_ant + missing_con

        return 1 - float(float(missing_total) / float(len(self.features)))

    def normalize(self, value, actual_bounds, real_bounds):
        return (real_bounds[0] +
                (value -
                 real_bounds[0]) *
                (real_bounds[1] -
                 real_bounds[0]) /
                (actual_bounds[1] -
                 actual_bounds[0]))

    def calculate_shrinkage(self, antecedent, consequence):
        differences = []

        for i in range(len(antecedent)):
            if self.features[self.permutation[i]].dtype == 'float' or self.features[self.permutation[i]].dtype == 'int':
                if antecedent[i] != 'NO':
                    borders = antecedent[i]
                    diff_borders = borders[1] - borders[0]
                    total_borders = self.features[self.permutation[i]].max_val - self.features[self.permutation[i]].min_val
                    diff = float(diff_borders / total_borders)
                    differences.append(diff)

        con_counter = 0
        for ll in range(len(antecedent), len(antecedent) + len(consequence)):
            if self.features[self.permutation[ll]].dtype == 'float' or self.features[self.permutation[ll]].dtype == 'int':
                if consequence[con_counter] != 'NO':
                    borders = consequence[con_counter]
                    diff_borders = borders[1] - borders[0]
                    total_borders = self.features[self.permutation[ll]].max_val - self.features[self.permutation[ll]].min_val
                    diff = float(diff_borders / total_borders)
                    differences.append(diff)
            con_counter = con_counter + 1

        value = 0.0
        for i in range(len(differences)):
            value = value + differences[i]

        if len(differences) > 0:
            normalized = self.normalize(value, [0, len(differences)], [0, 1])
        else:
            return 0.0

        return 1 - normalized

    def calculate_fitness(
            self,
            alpha,
            beta,
            gamma,
            delta,
            support,
            confidence,
            shrinkage,
            coverage):
        fitness = ((alpha * support) + (beta * confidence) + (gamma *
                   shrinkage) + (delta * coverage)) / (alpha + beta + gamma + delta)
        return fitness

    def format_rules(self, antecedent, consequence):
        antecedent1 = []
        consequence1 = []

        for i in range(len(antecedent)):
            if antecedent[i] != "NO":
                if self.features[self.permutation[i]].dtype == "cat":
                    rule = self.features[self.permutation[i]].name + "(" + str(antecedent[i][0]) + ")"
                else:
                    rule = self.features[self.permutation[i]].name + "(" + str(antecedent[i]) + ")"

                antecedent1.append(rule)

        for i in range(len(consequence)):
            if consequence[i] != "NO":
                if self.features[self.permutation[i + len(antecedent)]].dtype == "cat":
                    rule = self.features[self.permutation[i + len(antecedent)]].name + "(" + str(consequence[i]) + ")"
                else:
                    rule = self.features[self.permutation[i + len(antecedent)]].name + "(" + str(consequence[i]) + ")"

                consequence1.append(rule)
        return antecedent1, consequence1
