def NOT(formula):
    return Not(formula)


def AND(main, other):
    return And(main, other)


def OR(main, other):
    return Or(main, other)


def IFF(main, other):
    return Iff(main, other)


def IF(main, other):
    return If(main, other)


class Formula:
    def eval(self, q):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        return str(self) == str(other)

    def count_symbols(self):
        pass

    def contain(self, item):
        pass

    def get_symbols(self):
        pass

    def isSymbol(self):
        if isinstance(self, Atomic):
            return True
        if isinstance(self, Not):
            return self.child.isSymbol()
        return False

    def toCNF(self):
        def imply_remove(s):
            if not isinstance(s, Atomic) and not isinstance(s, Not):
                s.left = imply_remove(s.left)
                s.right = imply_remove(s.right)
            if isinstance(s, If):
                a = s.left
                b = s.right
                return OR(NOT(a), b)
            elif isinstance(s, Iff):
                a = s.left
                b = s.right
                return AND(OR(NOT(a), b), OR(NOT(b), a))
            return s

        def not_inside(s):
            if isinstance(s, Not):
                a = s.child
                if isinstance(a, Not):  # double negation
                    return not_inside(a.child)
                if isinstance(a, And) or isinstance(
                    a, Or
                ):  # De Morgan's Law (not (a and b)) = (not a) or (not b))
                    if isinstance(a, And):
                        x = OR(NOT(a.left), NOT(a.right))
                    else:
                        x = AND(NOT(a.left), NOT(a.right))
                    x.left = not_inside(x.left)
                    x.right = not_inside(x.right)
                    return x
                return s
            else:
                return s  # if not negation, return itself

        def distribute_and_or(s):
            if not isinstance(s, Atomic) and not isinstance(
                s, Not
            ):  # if not atomic and not negation
                s.left = distribute_and_or(s.left)
                s.right = distribute_and_or(s.right)

            if isinstance(s, Or):  # ví dù laf a or (b and c) => (a or b) and (a or c)
                if isinstance(
                    s.right, And
                ):  # ví dụ là a or (b and c) => (a or b) and (a or c)
                    s = AND(OR(s.left, s.right.left), OR(s.left, s.right.right))
                if isinstance(
                    s.left, And
                ):  # ví dụ là (b and c) or a => (b or a) and (c or a)
                    s = AND(OR(s.right, s.left.left), OR(s.right, s.left.right))

            return s

        q = self
        q = imply_remove(q)
        q = not_inside(q)
        q = distribute_and_or(q)

        return q


class Operator(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.op = ""

    def __str__(self):
        return "( " + str(self.left) + self.op + str(self.right) + " )"

    def contain(self, item):
        if str(self) == str(item):
            return True
        return self.left.contain(item) or self.right.contain(item)

    def get_symbols(self):  # get all symbols in the formula
        result = set()

        l = self.left.get_symbols()
        r = self.right.get_symbols()

        for i in l:
            result.add(str(i))
        for i in r:
            if not str(i) in result:
                result.add(str(i))

        return result

    def count_symbols(self):
        return self.left.count_symbols() + self.right.count_symbols()


class And(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.op = " ∧ "

    def eval(self, q):
        return self.left.eval(q) and self.right.eval(q)


class Or(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.op = " ∨ "

    def eval(self, q):
        return self.left.eval(q) or self.right.eval(q)


class If(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.op = " → "

    def eval(self, q):
        return not self.left.eval(q) or self.right.eval(q)


class Iff(Operator):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.op = " ↔ "

    def eval(self, q):
        return (not self.left.eval(q) or self.right.eval(q)) and (
            not self.right.eval(q) or self.left.eval(q)
        )


class Not(Formula):
    def __init__(self, other):
        self.child = other

    def eval(self, q):
        return not self.child.eval(q)

    def __str__(self):
        return "¬" + str(self.child)

    def contain(self, item):
        if str(self) == str(item):
            return True
        return self.child.contain(item)

    def get_symbols(self):
        res = set()
        if self.isSymbol():
            res.add(self)
            return res
        return self.child.get_symbols()

    def count_symbols(self):
        return self.child.count_symbols()


class Atomic(Formula):
    def __init__(self, name):
        self.name = name

    def eval(self, q):
        return str(self) in q

    def __str__(self):
        return self.name

    def contain(self, item):
        if str(self) == str(item):
            return True
        return False

    def get_symbols(self):
        res = set()
        res.add(self)

    def count_symbols(self):
        return 1
