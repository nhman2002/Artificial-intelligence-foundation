from Defi import Definition
from copy import deepcopy

class Stt_Med:
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
        if literal[0] == Definition.NOT_OPERATOR.value:
            return literal[1]
        return Definition.NOT_OPERATOR.value + literal