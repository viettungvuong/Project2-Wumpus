class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignments):
        return assignments[self.name]

class Not:
    def __init__(self, prop):
        self.prop = prop

    def evaluate(self, assignments):
        return not self.prop.evaluate(assignments)

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignments):
        return self.left.evaluate(assignments) and self.right.evaluate(assignments)

class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignments):
        return self.left.evaluate(assignments) or self.right.evaluate(assignments)

class Implies:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignments):
        return not self.left.evaluate(assignments) or self.right.evaluate(assignments)
