import pandas as pd 
import numpy as np 
from typing import List 
from dataclasses import dataclass
from science_optimization.builder import (
    BuilderOptimizationProblem,
    Variable,
    Constraint,
    Objective,
    OptimizationProblem
)
from science_optimization.function import (
    FunctionsComposite, 
    LinearFunction,
)
from science_optimization.solvers import Optimizer
from science_optimization.algorithms.linear_programming import Glop
import numpy as np
import unittest

@dataclass
class investimentos: 
  opcao: int 
  descricao: str
  custo: float
  retorno: float 

  @property
  def value_density(self) -> float:
        return self.custo / (self.retorno + 1e-9)



def items_to_table(items: List[investimentos]) -> pd.DataFrame:
    records = [{
            'Opção': i.opcao,
            'Descrição': i.descricao[i.opcao],
            'Custo (R$)': i.custo,
            'Retorno (R$)': i.retorno,
        } for i in items]
    records.append({
        'Opção': 'Total',
        'Descrição': 'Total',
        'Custo (R$)': sum(i.custo for i in items),
        'Retorno (R$)': sum(i.retorno for i in items)
    })
    return pd.DataFrame.from_records(records)


"""#### Heuristica: Guloso """

def greedy_investments(
    budget: float, 
    available_investments: List[investimentos]
) -> List[investimentos]:
    chosen_investments = list()
    adicionados = [0,0,0,0,0,0,0,0]

    sorted_investments = sorted(
        available_investments, 
        key=lambda i: i.value_density,
        reverse=False) 
   
    for investment in sorted_investments:
        if investment.custo <= budget:
          if investment.opcao == 1 and (investment.custo + available_investments[3].custo) <= budget: # not(not (not adicionados[1] or adicionados[3]) X2 -> X4 
            adicionados[investment.opcao] = 1
            adicionados[3] = 1 
            chosen_investments.append(investment)
            chosen_investments.append(available_investments[3])
            budget -= investment.custo + available_investments[3].custo
          elif investment.opcao == 1:
            continue
          elif investment.opcao!=0 and investment.opcao!=4 or (adicionados[4] + adicionados[0])<=1:
            if (investment.opcao==4 or investment.opcao==0):
              adicionados[0] = 1
              adicionados[4] = 1
            chosen_investments.append(investment)
            budget -= investment.custo    
    return chosen_investments

"""
chosen_items = greedy_knapsack(budget,opcoes_investimento)
items_to_table(chosen_items)
"""
"""###Modelos de programação inteira: MILP - Usando a biblioteca science-optimization"""

class Investment_optimizer(BuilderOptimizationProblem):
    def __init__(
        self,
        capacity: float, 
        opcoes_investimento: List[investimentos]):

        self.__capacity = capacity
        self.__items = opcoes_investimento
    
    @property
    def __num_vars(self) -> int:
        return len(self.__items)

    @property
    def __custo(self) -> np.array:
        return np.array([
            item.custo for item in self.__items
        ]).reshape(-1, 1)
    
    @property
    def __retorno(self) -> np.array:
        return np.array([
            item.retorno for item in self.__items
        ]).reshape(-1, 1)
    
    @property
    def __restricao1(self) -> np.array:
        restricao1 = np.zeros(self.__num_vars).reshape(-1,1)
        if self.__num_vars>=4:
            restricao1[0][0] = 1
            restricao1[4][0] = 1
        return restricao1
        #return np.array([1,0,0,0,1,0,0,0]).reshape(-1, 1)

    @property
    def __restricao0(self) -> np.array:
        self.__restricao = np.zeros((self.__num_vars, 1)).reshape(-1, 1)
        return self.__restricao

    #@__restricao1.setter
    #def adiciona(self,posicao) -> np.array:
     #   self.__restricao1[posicao][0] = 1 

    @property
    def __restricao2(self) -> np.array:
        restricao2 = np.zeros(self.__num_vars).reshape(-1,1)
        if self.__num_vars>=4:
            restricao2[1][0] = 1
            restricao2[3][0] = -1
        return restricao2
        #return np.array([0,1,0,-1,0,0,0,0]).reshape(-1, 1)


    def build_variables(self):
        x_min = np.zeros((self.__num_vars, 1))
        x_max = np.ones((self.__num_vars, 1))
        x_type=['d']*self.__num_vars # Discrete variable
        variables = Variable(x_min, x_max, x_type)

        return variables

    def build_constraints(self) -> Constraint:
        """Weights cannot exceed capacity"""
        # w * x - c <= 0  Linear Funcion(x) = c'x+d    
       # self.__restricao1.adiciona[2][0] = 1
        #print(self.__restricao1)
        
        constraint = LinearFunction(c=self.__custo, d=-self.__capacity) #Custo menor que o orçamento.  
        #print(f"capacidade -> {self.__capacity} e retorno {self.__retorno};")
        constraint2 = LinearFunction(c=self.__restricao1, d=-1)  
        constraint3 = LinearFunction(c=self.__restricao2) 
        ineq_cons = FunctionsComposite()
        ineq_cons.add(constraint)
        ineq_cons.add(constraint2)
        ineq_cons.add(constraint3)
        constraints = Constraint(ineq_cons=ineq_cons)

        return constraints
    
    def build_objectives(self) -> Objective:
        # minimize -v*x
        obj_fun = LinearFunction(c=-self.__retorno)        
        obj_funs = FunctionsComposite()
        obj_funs.add(obj_fun)
        objective = Objective(objective=obj_funs)

        return objective

def optimization_problem(
    capacity: float,
    available_items: List[investimentos],
    verbose: bool = False
) -> OptimizationProblem:
    investment_optimizer = Investment_optimizer(capacity, available_items)
    problem = OptimizationProblem(builder=investment_optimizer)
    if verbose:
        print(problem.info())
    return problem

def run_optimization(
    problem: OptimizationProblem,
    verbose: bool = False
) -> np.array:
    optimizer = Optimizer(
        opt_problem=problem,
        algorithm=Glop()
    )
    results = optimizer.optimize()
    decision_variables = results.x.ravel()
    if verbose:
        print(f"Decision variable:\n{decision_variables}")
    return decision_variables

def knapsack_milp(
    capacity: float, 
    items: List[investimentos],
    verbose:bool = False) -> List[investimentos]:
    
    problem = optimization_problem(capacity, 
                                   items, 
                                   verbose)
    decision_variables = run_optimization(problem, verbose)
    
    
    # Build list of chosen items
    chosen_items = list()
    for item, item_was_chosen in zip(items, decision_variables):
        if item_was_chosen:
            chosen_items.append(item)
    return chosen_items

'''
chosen_items = knapsack_milp(budget,opcoes_investimento, verbose=True)
items_to_table(chosen_items)

'''