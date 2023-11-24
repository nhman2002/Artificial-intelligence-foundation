from copy import deepcopy
from Defi import Definition
from Util import Util

class MyAlgo:
    #CONSTRUCTOR: 
    def __init__(self):
        self.alpha =[]
        self.KB = []
        self.new_clauses_list = []
        self.solution = False
        self.util = Util()

                                    ### PRIMARY FUNCTION ###
    #READ INPUT DATA
    def read_file(self, input_file: str):
        with open(input_file, 'r') as file:
            lines = file.readlines()
        # ALPHA_INDEX = 0 => ALPHA VARIABLE IS ON THE 1ST LINE
        # ALPHA_INDEX = 1 => ALPHA VARIABLE IS ON THE 2ND LINE
        alpha_index = 1 if lines[0].strip().isdigit() else 0
        # Tách alpha và KB
        # SPLIT 2 VARIABLES ALPHA AND KB(KNOWLEDGE BASED)
        self.alpha = lines[alpha_index].strip().split(Definition.OR_OPERATOR.value)
        # FROM THE 3RD LINE, THIS IS THE KB VARIABLE WE NEED
        self.KB = [line.strip().split(Definition.OR_OPERATOR.value) for line in lines[alpha_index + 2:]] 
        # STANDARDIZED VARIABLE: ALPHA & KB
        self.alpha = self.util.standard_cnf_sentence([self.alpha])
        self.KB = self.util.standard_cnf_sentence(self.KB)
        file.close()
    
    #WRITE OUTPUT DATA
    def write_file(self, output_file: str):
        file = open(output_file, 'w')
        for new_clause in self.new_clauses_list:
            file.write(str(len(new_clause)) + '\n')
            for clause in new_clause:
                file.write(self.util.formated_clause(clause) + '\n')
        file.write('YES') if self.solution else file.write('NO')
        file.close()
        
    def pl_resolution(self):
        cnf_clause_list = deepcopy(self.KB)
        neg_alpha = self.util.standard_cnf_sentence(self.util.negation_of_cnf_sentence(self.alpha))
        for clause in neg_alpha:
            if clause not in cnf_clause_list:
                cnf_clause_list.append(clause)

        while True:
            self.new_clauses_list.append([])

            for i in range(len(cnf_clause_list)):
                for j in range(i + 1, len(cnf_clause_list)):
                    resolvents = self.util.resolve(cnf_clause_list[i], cnf_clause_list[j])
                    if [] in resolvents:    
                        self.solution = True
                        self.new_clauses_list[-1].append([])
                        return self.solution

                    for resolvent in resolvents:
                        if self.util.is_valid_clause(resolvent):
                            break
                        if resolvent not in cnf_clause_list and resolvent not in self.new_clauses_list[-1]:
                            self.new_clauses_list[-1].append(resolvent)

            if len(self.new_clauses_list[-1]) == 0:
                self.solution = False
                return self.solution
            cnf_clause_list += self.new_clauses_list[-1]
