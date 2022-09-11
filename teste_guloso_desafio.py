import unittest

from optimizers import greedy_investments, investimentos, knapsack_milp

class TestGreedyKnapsack(unittest.TestCase):
    def test_Guloso_sem_investimentos(self):
        opcoes_investimento = list()
        budget = 15
        chosen_items = greedy_investments(budget, opcoes_investimento)
        self.assertEqual(chosen_items, list())

    def test_Guloso_unico_investimento_valido(self):
        available_items = [investimentos(0,'ItemX', custo=5, retorno=30)]
        budget = 15
        chosen_items = greedy_investments(budget, available_items)
        self.assertEqual(chosen_items, available_items)
    def test_Guloso_unico_investimento_invalido(self):
        available_items = [investimentos(0,'ItemX', custo=25, retorno=30)]
        budget = 15
        chosen_items = greedy_investments(budget, available_items)
        self.assertEqual(chosen_items, list())
    
    def test_Guloso_primeira_restricao_atendida(self):
        certox1 = investimentos(0,'ItemX', custo=14, retorno=100)
        x2 = investimentos(1,'ItemA', custo=20, retorno=200)
        x3 = investimentos(2,'ItemB', custo=16, retorno=100)
        x4 = investimentos(3,'ItemC', custo=17, retorno=300)
        erradox5 = investimentos(4,'ItemD', custo=1, retorno=1)
        x6 = investimentos(5,'ItemE', custo=19, retorno=1)
        x7 = investimentos(6,'ItemF', custo=22, retorno=1)
        x8 = investimentos(7,'ItemG', custo=23, retorno=1)
        
        available_items = [certox1,x2,x3,x4,erradox5,x6,x7,x8]
        budget = 15
        chosen_items = greedy_investments(budget, available_items)
        self.assertEqual(chosen_items, [certox1])
    def test_Guloso_segunda_restricao_atendida(self):
        x1 = investimentos(0,'ItemX', custo=22, retorno=100)
        certox2 = investimentos(1,'ItemA', custo=14, retorno=200)
        x3 = investimentos(2,'ItemB', custo=16, retorno=100)
        certox4 = investimentos(3,'ItemC', custo=1, retorno=1)
        erradox5 = investimentos(4,'ItemD', custo=1, retorno=2)
        x6 = investimentos(5,'ItemE', custo=19, retorno=1)
        x7 = investimentos(6,'ItemF', custo=22, retorno=1)
        x8 = investimentos(7,'ItemG', custo=23, retorno=1)
        
        available_items = [x1,certox2,x3,certox4,erradox5,x6,x7,x8]
        budget = 15
        chosen_items = greedy_investments(budget, available_items)
        self.assertEqual(chosen_items, [certox2,certox4])
    def test_Guloso_segunda_restricao_atendida_Apenas_x4(self):
        x1 = investimentos(0,'ItemX', custo=22, retorno=100)
        erradox2 = investimentos(1,'ItemA', custo=14, retorno=200)
        x3 = investimentos(2,'ItemB', custo=16, retorno=100)
        certox4 = investimentos(3,'ItemC', custo=2, retorno=1)
        certox5 = investimentos(4,'ItemD', custo=1, retorno=2)
        x6 = investimentos(5,'ItemE', custo=19, retorno=1)
        x7 = investimentos(6,'ItemF', custo=22, retorno=1)
        x8 = investimentos(7,'ItemG', custo=23, retorno=1)
        
        available_items = [x1,erradox2,x3,certox4,certox5,x6,x7,x8]
        budget = 15
        chosen_items = greedy_investments(budget, available_items)
        self.assertEqual(chosen_items, [certox5,certox4])
    

unittest.main(argv=[''], verbosity=2, exit=False)