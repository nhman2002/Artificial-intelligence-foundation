from Defi import Definition
from copy import deepcopy
from StaticMethod import Stt_Med

class Util:
    # INIT FUNCTION, SO THAT I CAN USE METHODS FROM StaticMethod.py
    def __init__(self):
        self.med = Stt_Med
    # RETURN A STANDARDIZED CNF SENTENCE:
    # 1. STANDARDIZE ALL OF CLAUSES.
    # 2. GET RID OF ALL VALID CLAUSE.
    # 3. GET RID OF ALL DUPLICATED CLAUSES.
    def standard_cnf_sentence(self, cnf_sentence: list):
        std_sentence = []
        for clause in cnf_sentence:
            std_clause = self.med.standard_clause(clause)
            if not self.is_valid_clause(std_clause) and std_clause not in std_sentence:
                std_sentence.append(std_clause)
        return std_sentence

    # SECONDARY FUNCTION FOR (generate_combinations), GENERATE COMBINATION RECURSIVELY
    def generate_combinations_recursive(self, list: list, combination_list: list, combination: list, depth: int):
        if depth == len(list):
            combination_list.append(deepcopy(combination))
            return
        for ele in list[depth]:
            combination.append(deepcopy(ele))
            self.generate_combinations_recursive(list, combination_list, combination, depth + 1)
            combination.pop()

    # GENERATE A COMBINATION LIST:
    # EX: I HAVE 2 SETS OF ENTITY AS BELOW:
    # set_1 (x,y)
    # set_2 (a,b)
    # COMBINATION SET: (x, a), (x, b), (y, a), (y, b)
    def generate_combinations(self, list: list):
        combination_list, combination, depth = [], [], 0
        self.generate_combinations_recursive(list, combination_list, combination, depth)
        return combination_list

    # RETURN A NEGATION OF A CNF SENTENCE
    def negation_of_cnf_sentence(self, cnf_sentence: list):
        neg_sen = [[self.med.negation_of_literal(literal) for literal in clause] for clause in cnf_sentence]
        neg_cnf_sentence = self.generate_combinations(neg_sen)
        return neg_cnf_sentence

    # RESOLVE 2 CLAUSES THEN RETURN A LIST OF RESULT 
    def resolve(self, clause_1: list, clause_2: list):
        result = []
        for index in range(len(clause_1)):
            for j in range(len(clause_2)):
                if self.med.is_complentary_literal(clause_1[index], clause_2[j]):
                    rev = clause_1[:index] + clause_1[index + 1:] + clause_2[:j] + clause_2[j + 1:]       
                    result.append(self.med.standard_clause(rev))
        return result

    # RETURN A FORMATED-STRING CLAUSE.
    def formated_clause(self, clause):
        if self.med.is_empty_clause(clause):
            return Definition.EMPTY_CLAUSE.value
        rev = ''
        for i in range(len(clause) - 1):
            rev += str(clause[i]) + Definition.OR_OPERATOR.value
        rev += str(clause[-1])
        return rev

    # CHECK IF A CLAUSE IS VALID (ALWAYS TRUE)
    def is_valid_clause(self, clause):
        for index in range(len(clause) - 1):
            if self.med.is_complentary_literal(clause[index], clause[index + 1]):
                return True
        return False