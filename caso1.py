
from optimizers import investimentos, items_to_table, greedy_investments, knapsack_milp
budget = 1000000

opcoes = [1,2,3,4,5,6,7,8]

descricoes = ['Ampliação da capacidade do armazém ZDP em 5%','Ampliação da capacidade do armazém MGL em 7%','Compra de empilhadeira',
              'Projeto de P&D I','Projeto de P&D II','Aquisição de novos equipamentos','Capacitação de funcionários',
              'Ampliação da estrutura de carga rodoviária']

custos = [470000,400000,170000,270000,340000,230000,50000,440000]

retornos = [410000,330000,140000,250000,320000,320000,90000,190000]

opcoes_investimento = [investimentos(i,descricoes, v, w) for i, (v, w) in enumerate(zip(custos, retornos))]

items_to_table(opcoes_investimento)

chosen_items = greedy_investments(budget,opcoes_investimento)
guloso = items_to_table(chosen_items)

chosen_items = knapsack_milp(budget,opcoes_investimento, verbose=True)
milp = items_to_table(chosen_items)
print(guloso)
print(milp)