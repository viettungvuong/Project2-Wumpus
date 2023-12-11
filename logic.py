from sympy import Not, Or

# A -> B 
# A 
# => B
def modus_ponens(rule, antecedent):
    if antecedent in rule.args:
        return rule.rhs

# A -> B 
# -B 
# => -A
def modus_tollens(rule, negated_consequent):
    if Not(rule.rhs) == negated_consequent:
        return Not(rule.lhs)



def resolution_refutation(clause1, clause2):
    resolved = Or()

    for literal in clause1.args:
        if Not(literal) in clause2.args: # if the negation of the literal is in the second clause
            resolved = Or(resolved, Or([other for other in clause1.args if other != literal] + [other for other in clause2.args if other != Not(literal)]))

    return resolved