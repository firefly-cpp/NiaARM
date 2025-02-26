import unittest
from niaarm.visualize import sankey_diagram
from niaarm import Rule

class TestSankeyDiagram(unittest.TestCase):
	
	@classmethod
	def setUpClass(cls):
		cls.rule1 = Rule(antecedent=["A", "B"], consequent=["C"])
		cls.rule1.fitness = 1.0
		cls.rule1.num_transactions = 10  
		cls.rule2 = Rule(antecedent=["D"], consequent=["E", "F"])
		cls.rule2.fitness = 0.8
		cls.rule2.num_transactions = 15  
		cls.rule3 = Rule(antecedent=["G", "H"], consequent=["I"])
		cls.rule3.fitness = 0.9
		cls.rule3.num_transactions = 12  
		
		cls.rules = [cls.rule1, cls.rule2, cls.rule3]

	def test_sankey_output_type(self):
		fig = sankey_diagram(self.rules, "support", M=3)
		self.assertEqual(fig.__class__.__name__, "Figure")

	def test_sankey_structure(self):
		fig = sankey_diagram(self.rules, "support", M=3)
		self.assertTrue("source" in fig.data[0].link)
    
	def test_sankey_values(self):
		fig = sankey_diagram(self.rules, "support", M=3)
		link_data = fig.data[0].link
		flow_values = link_data['value']  
		expected_links = sum(len(rule.antecedent) * len(rule.consequent) for rule in self.rules)
		self.assertEqual(len(flow_values), expected_links)
    
	def test_sankey_with_custom_fitness(self):
		fig = sankey_diagram(self.rules, "support", M=2)
		link_data = fig.data[0].link
		flow_values = link_data['value']  
		self.assertGreater(len(flow_values), 0)  
    
	def test_sankey_no_empty_rules(self):
		fig = sankey_diagram([], "support", M=3)
		self.assertEqual(len(fig.data[0].link['source']), 0)
		self.assertEqual(len(fig.data[0].link['target']), 0)
		self.assertEqual(len(fig.data[0].link['value']), 0)
		