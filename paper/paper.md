---
title: 'NiaARM: A minimalistic framework for numerical association rule mining'
tags:
  - Python
  - association rule mining
  - data mining
  - evolutionary algorithms
  - numerical association rule mining
  - visualization
authors:
  - name: Žiga Stupan^[Corresponding author]
    orcid:  0000-0001-9847-7306
    affiliation: "1"
  - name: Iztok Fister Jr.
    orcid: 0000-0002-6418-1272
    affiliation: "1"
affiliations:
- name: University of Maribor, Faculty of Electrical Engineering and Computer Science
  index: 1
date: 7 March 2022
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

Association Rule Mining (ARM) is a data mining method intended for discovering relations between attributes in
transaction databases in the form of implications [@agrawal_fast_1994, @fister_jr_brief_2020]. Traditional
approaches, such as the Apriori algorithm [@agrawal_fast_1994] or ECLAT [@zaki_scalable_2000],
require the attributes in the database to be discretized. This can result in the incorporation of noise into data,
and potentially obtained associations may not fully reveal the story [@varol2020performance]. On the contrary,
Numerical association rule mining (NARM) is an extension of ARM that allows handling numerical attributes without
discretization [fister_jr_improved_2021]. Interestingly, most of the NARM algorithms are based on
population-based nature-inspired metaheuristics.

The NiaARM framework is an implementation of the ARM-DE algorithm [fister_differential_2018; @fister_jr_improved_2021], where
numeric association rule mining is modeled as a single objective, continuous optimization problem, where the fitness is a
weighted sum of the support and confidence of the built rule. The approach is extended by allowing the use of any optimization
algorithm from the related NiaPy framework [@vrbancic_niapy_2018], as well as having the option to select various interest 
measures and their corresponding weights for the fitness function.
Additionally, the framework also includes methods for loading and preprocessing data, powerful
visualization methods, such as the hill slopes method [@fister_visualization_2020] and a simple command line interface for
mining association rules. 

# Statement of need

Numeric association rule mining is an important topic amidst the data revolution 
era [@fister_jr_improved_2021; @telikani_survey_2020]. The NiaARM framework
is a collects methods to easily process data, mine association rules and interpret
the results, implementing many interest measures and powerful visualization techniques. Combined with the NiaPy
library it also gives the opportunity to test the ARM-DE approach using arbitrary nature-inspired algorithms.

# References
