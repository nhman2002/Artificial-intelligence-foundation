from enum import Enum
from copy import deepcopy
import os

class Definition(Enum):
    EMPTY_CLAUSE_SYMBOL = '{}'
    NOT_OPERATOR_SYMBOL = '-'
    OR_OPERATOR_DELIMETER = ' OR '


class MyAlgo:
    #CONSTRUCTOR: 
    def __init__(self):
        self.alpha =[]
        self.KB = []
        self.new_clauses_list = []
        self.solution = False

                                    ### PRIMARY FUNCTION ###
    #READ INPUT DATA
    def read_file(self, input_file: str):
        with open(input_file, 'r') as file:
            lines = file.readlines()
        # alpha_index = 0 -> alpha nằm ở dòng thứ 1
        # alpha_index = 1 -> alpha nằm ở dòng thứ 2
        alpha_index = 1 if lines[0].strip().isdigit() else 0
        # Tách alpha và KB
        self.alpha = lines[alpha_index].strip().split(Definition.OR_OPERATOR_DELIMETER.value)
        # Cắt từ dòng thứ 3 trở đi để lấy KB (sau câu alpha)
        self.KB = [line.strip().split(Definition.OR_OPERATOR_DELIMETER.value) for line in lines[alpha_index + 2:]] 
        # Chuẩn hóa alpha và KB
        self.alpha = self.standard_cnf_sentence([self.alpha])
        self.KB = self.standard_cnf_sentence(self.KB)
        file.close()
    
    #WRITE OUTPUT DATA
    def write_file(self, output_file: str):
        file = open(output_file, 'w')
        for new_clause in self.new_clauses_list:
            file.write(str(len(new_clause)) + '\n')
            for clause in new_clause:
                file.write(self.formated_clause(clause) + '\n')
        file.write('YES \n') if self.solution else file.write('NO \n')
        file.close()
        
    def pl_resolution(self):
        cnf_clause_list = deepcopy(self.KB)
        neg_alpha = self.standard_cnf_sentence(self.negation_of_cnf_sentence(self.alpha))
        for clause in neg_alpha:
            if clause not in cnf_clause_list:
                cnf_clause_list.append(clause)

        while True:
            self.new_clauses_list.append([])

            for i in range(len(cnf_clause_list)):
                for j in range(i + 1, len(cnf_clause_list)):
                    resolvents = self.resolve(cnf_clause_list[i], cnf_clause_list[j])
                    if [] in resolvents:    
                        self.solution = True
                        self.new_clauses_list[-1].append([])
                        return self.solution

                    for resolvent in resolvents:
                        if self.is_valid_clause(resolvent):
                            break
                        if resolvent not in cnf_clause_list and resolvent not in self.new_clauses_list[-1]:
                            self.new_clauses_list[-1].append(resolvent)

            if len(self.new_clauses_list[-1]) == 0:
                self.solution = False
                return self.solution
            cnf_clause_list += self.new_clauses_list[-1]
                                        ### SECONDARY FUNCTION ###

    # RETURN A STANDARDIZED CNF SENTENCE:
    # 1. STANDARDIZE ALL OF CLAUSES.
    # 2. GET RID OF ALL VALID CLAUSE.
    # 3. GET RID OF ALL DUPLICATED CLAUSES.
    def standard_cnf_sentence(self, cnf_sentence: list):
        std_sentence = []
        for clause in cnf_sentence:
            std_clause = self.standard_clause(clause)
            if not self.is_valid_clause(std_clause) and std_clause not in std_sentence:
                std_sentence.append(std_clause)
        return std_sentence


    

    # HELPER FUNCTION FOR (generate_combiantions)
    def generate_combinations_recursive(self, list: list, combination_list: list, combination: list, depth: int):
        if depth == len(list):
            combination_list.append(deepcopy(combination))
            return
        for ele in list[depth]:
            combination.append(deepcopy(ele))
            self.generate_combinations_recursive(list, combination_list, combination, depth + 1)
            combination.pop()

    # GENERATE A COMBINATION LIST:
    # set_1 (x,y)
    # set_2 (a,b)
    # COMBINATION SET: (x, a), (x, b), (y, a), (y, b)
    def generate_combinations(self, list: list):
        combination_list, combination, depth = [], [], 0
        self.generate_combinations_recursive(list, combination_list, combination, depth)
        return combination_list

    # RETURN A NEGATION OF A CNF SENTENCE
    def negation_of_cnf_sentence(self, cnf_sentence: list):
        neg_sen = [[self.negation_of_literal(literal) for literal in clause] for clause in cnf_sentence]
        neg_cnf_sentence = self.generate_combinations(neg_sen)
        return neg_cnf_sentence

    # RESOLVE 2 CLAUSES THEN RETURN A LIST OF RESULT 
    def resolve(self, clause_1: list, clause_2: list):
        result = []
        for index in range(len(clause_1)):
            for j in range(len(clause_2)):
                if self.is_complentary_literal(clause_1[index], clause_2[j]):
                    rev = clause_1[:index] + clause_1[index + 1:] + clause_2[:j] + clause_2[j + 1:]       
                    result.append(self.standard_clause(rev))
        return result

    # RETURN A FORMATED-STRING CLAUSE.
    def formated_clause(self, clause):
        if self.is_empty_clause(clause):
            return Definition.EMPTY_CLAUSE_SYMBOL.value
        rev = ''
        for i in range(len(clause) - 1):
            rev += str(clause[i]) + Definition.OR_OPERATOR_DELIMETER.value
        rev += str(clause[-1])
        return rev

    # CHECK IF A CLAUSE IS VALID (ALWAYS TRUE)
    def is_valid_clause(self, clause):
        for index in range(len(clause) - 1):
            if self.is_complentary_literal(clause[index], clause[index + 1]):
                return True
        return False

    # CHECK IF A CLAUSE IS EMPTY
    @staticmethod
    def is_empty_clause(clause: list):
        return len(clause) == 0

    # RETURN A STD CLAUSE:
    # 1. GET RID OF ALL DUPLICATES
    # 2. LITERALS WITHIN A CLAUSE ARE SORTED BASE ON ALPHABET PRIORITIZED ORDER
    @staticmethod
    def standard_clause(clause: list):
        return sorted(list(set(deepcopy(clause))), key=lambda x: x[-1])


    # CHECK IF 2 LITERALS ARE COMPLETE
    @staticmethod
    def is_complentary_literal(literal_1: str, literal_2: str):
        return len(literal_1) != len(literal_2) and literal_1[-1] == literal_2[-1]

    # RETURN A NEGATION OF A LITERAL
    @staticmethod
    def negation_of_literal(literal: str):
        if literal[0] == Definition.NOT_OPERATOR_SYMBOL.value:
            return literal[1]
        return Definition.NOT_OPERATOR_SYMBOL.value + literal
    
