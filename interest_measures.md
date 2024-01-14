# Interest Measures

## Support

Support is defined on an itemset as the proportion of transactions that contain the attribute $`X`$.

```math
supp(X) = \frac{n_{X}}{|D|},
```

where $`|D|`$ is the number of records in the transactional database.

For an association rule, support is defined as the support of all the attributes in the rule.

```math
supp(X \implies Y) = \frac{n_{XY}}{|D|}
```

**Range:** $`[0, 1]`$

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## Confidence

Confidence of the rule, defined as the proportion of transactions that contain
the consequent in the set of transactions that contain the antecedent. This proportion is an estimate
of the probability of seeing the consequent, if the antecedent is present in the transaction.

```math
conf(X \implies Y) = \frac{supp(X \implies Y)}{supp(X)}
```

**Range:** $`[0, 1]`$

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## Lift

Lift measures how many times more often the antecedent and the consequent Y
occur together than expected if they were statistically independent.

```math
lift(X \implies Y) = \frac{conf(X \implies Y)}{supp(Y)}
```

**Range:** $`[0, \infty]`$ (1 means independence)

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## Coverage

Coverage, also known as antecedent support, is an estimate of the probability that
the rule applies to a randomly selected transaction. It is the proportion of transactions
that contain the antecedent.

```math
cover(X \implies Y) = supp(X)
```

**Range:** $`[0, 1]`$

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## RHS Support

Support of the consequent.

```math
RHSsupp(X \implies Y) = supp(Y)
```

**Range:** $`[0, 1]`$

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## Conviction

Conviction can be interpreted as the ratio of the expected frequency that the antecedent occurs without
the consequent.

```math
conv(X \implies Y) = \frac{1 - supp(Y)}{1 - conf(X \implies Y)}
```

**Range:** $`[0, \infty]`$ (1 means independence, $`\infty`$ means the rule always holds)

**Reference:** Michael Hahsler, A Probabilistic Comparison of Commonly Used Interest Measures for Association Rules,
2015, URL: https://mhahsler.github.io/arules/docs/measures

## Inclusion

Inclusion is defined as the ratio between the number of attributes of the rule
and all attributes in the database.

```math
inclusion(X \implies Y) = \frac{|X \cup Y|}{m},
```

where $`m`$ is the total number of attributes in the transactional database.


**Range:** $`[0, 1]`$

**Reference:** I. Fister Jr., V. Podgorelec, I. Fister. Improved Nature-Inspired Algorithms for Numeric Association
Rule Mining. In: Vasant P., Zelinka I., Weber GW. (eds) Intelligent Computing and Optimization. ICO 2020. Advances in
Intelligent Systems and Computing, vol 1324. Springer, Cham.

## Amplitude

Amplitude measures the quality of a rule, preferring attributes with smaller intervals.

```math
ampl(X \implies Y) = 1 - \frac{1}{n}\sum_{k = 1}^{n}{\frac{Ub_k - Lb_k}{max(o_k) - min(o_k)}},
```

where $`n`$ is the total number of attributes in the rule, $`Ub_k`$ and $`Lb_k`$ are upper and lower
bounds of the selected attribute, and $`max(o_k)`$ and $`min(o_k)`$ are the maximum and minimum
feasible values of the attribute $`o_k`$ in the transactional database.

**Range:** $`[0, 1]`$

**Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
association rule mining. arXiv preprint arXiv:2010.15524 (2020).

## Interestingness

Interestingness of the rule, defined as:

```math
interest(X \implies Y) = \frac{supp(X \implies Y)}{supp(X)} \cdot \frac{supp(X \implies Y)}{supp(Y)}
\cdot (1 - \frac{supp(X \implies Y)}{|D|})
```

Here, the first part gives us the probability of generating the rule based on the antecedent, the second part
gives us the probability of generating the rule based on the consequent and the third part is the probability
that the rule won't be generated. Thus, rules with very high support will be deemed uninteresting.

**Range:** $`[0, 1]`$

**Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
association rule mining. arXiv preprint arXiv:2010.15524 (2020).

## Comprehensibility

Comprehensibility of the rule. Rules with fewer attributes in the consequent are more
comprehensible.

```math
comp(X \implies Y) = \frac{log(1 + |Y|)}{log(1 + |X \cup Y|)}
```

**Range:** $`[0, 1]`$

**Reference:** I. Fister Jr., I. Fister A brief overview of swarm intelligence-based algorithms for numerical
association rule mining. arXiv preprint arXiv:2010.15524 (2020).

## Netconf

The netconf metric evaluates the interestingness of
association rules depending on the support of the rule and the
support of the antecedent and consequent of the rule.

```math
netconf(X \implies Y) = \frac{supp(X \implies Y) - supp(X)supp(Y)}{supp(X)(1 - supp(X))}
```

**Range:** $`[-1, 1]`$ (Negative values represent negative dependence, positive values represent positive
dependence and 0 represents independence)

**Reference:** E. V. Altay and B. Alatas, "Sensitivity Analysis of MODENAR Method for Mining of Numeric Association
Rules," 2019 1st International Informatics and Software Engineering Conference (UBMYK), 2019, pp. 1-6,
doi: 10.1109/UBMYK48245.2019.8965539.

## Yule's Q

The Yule's Q metric represents the correlation between two possibly related dichotomous events.

```math
yulesq(X \implies Y) =
\frac{supp(X \implies Y)supp(\neg X \implies \neg Y) - supp(X \implies \neg Y)supp(\neg X \implies Y)}
{supp(X \implies Y)supp(\neg X \implies \neg Y) + supp(X \implies \neg Y)supp(\neg X \implies Y)}
```

**Range:** $`[-1, 1]`$ (-1 reflects total negative association, 1 reflects perfect positive association
and 0 reflects independence)

**Reference:** E. V. Altay and B. Alatas, "Sensitivity Analysis of MODENAR Method for Mining of Numeric Association
Rules," 2019 1st International Informatics and Software Engineering Conference (UBMYK), 2019, pp. 1-6,
doi: 10.1109/UBMYK48245.2019.8965539.

# Zhang's Metric

Zheng's metric measures the strength of association (positive or negative) between the antecedent and consequent, 
taking into account both their co-occurrence and non-co-occurrence.

```math
zhang(X \implies Y) =
\frac{conf(X \implies Y) - conf(\neg X \implies Y)}{max\{conf(X \implies Y), conf(\neg X \implies Y)\}}
```

**Range:** $`[-1, 1]`$ (-1 reflects total negative association, 1 reflects perfect positive association
and 0 reflects independence)

**Reference:** T. Zhang, “Association Rules,” in Knowledge Discovery and Data Mining. Current Issues and New 
Applications, 2000, pp. 245–256. doi: 10.1007/3-540-45571-X_31. 
