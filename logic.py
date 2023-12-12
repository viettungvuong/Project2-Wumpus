from sympy.logic.boolalg import And, Implies, Not, Or

# A -> B
# A 
# => B
def modus_ponens(rule, antecedent):
    if rule.func==Implies and antecedent == rule.args[0]:
        return rule.args[1]
    return None

# A -> B 
# -B 
# => -A
def modus_tollens(rule, negated_consequent):
    if rule.func==Implies and Not(rule.args[1]) == negated_consequent:
        return Not(rule.args[0])
    return None

def resolution_refutation(clause1, clause2):
    resolved = Or()

    for literal in clause1.args:
        if Not(literal) in clause2.args: # if the negation of the literal is in the second clause
            resolved = Or(resolved, Or([other for other in clause1.args if other != literal] + [other for other in clause2.args if other != Not(literal)]))

    return resolved