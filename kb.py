from logic import Not, And, Or, If, Iff, Atomic, Formula, Operator


class KB:
    def __init__(self):
        self.sentences = []

    def print(self):
        for s in self.sentences:
            print(s)

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def remove(self, sentence):
        for s in self.sentences:
            if str(s) == str(sentence):
                self.sentences.remove(s)

    def check(self, sentence):  # check if sentence is in KB
        return str(sentence) in [str(s) for s in self.sentences]

    def toCnf(self):
        result = []
        for sentence in self.sentences:
            if (
                isinstance(sentence, Formula) == False
                and isinstance(sentence, Operator) == False
            ):
                continue
            result.append(sentence.toCNF())
            # print(result[-1])
        return result

    def forward_chaining(self, q):
        if self.check(q):
            return True

        if self.check(Not(q)):
            return False

        count = {}  # number of premises of each implication
        inferred = {}

        for sentence in self.sentences:
            if isinstance(sentence, Atomic) or (
                isinstance(sentence, Not) and isinstance(sentence.child, Atomic)
            ):
                count[str(sentence)] = 0
                inferred[str(sentence)] = False
            elif isinstance(sentence, If):
                if isinstance(sentence.left, And):
                    count[str(sentence.right)] = len(sentence.left.get_literals())
                elif isinstance(sentence.left, Or):
                    count[str(sentence.right)] = 1
                inferred[str(sentence.right)] = False
            elif isinstance(sentence, Iff):
                if isinstance(sentence.left, And):
                    count[str(sentence.right)] = len(sentence.left.get_literals())
                elif isinstance(sentence.left, Or):
                    count[str(sentence.right)] = 1
                inferred[str(sentence.right)] = False

                if isinstance(sentence.right, And):
                    count[str(sentence.left)] = len(sentence.right.get_literals())
                elif isinstance(sentence.right, Or):
                    count[str(sentence.left)] = 1
                inferred[str(sentence.left)] = False

        agenda = []  # list of symbols known to be true

        for sentence in self.sentences:
            if isinstance(sentence, Atomic) or (
                isinstance(sentence, Not) and isinstance(sentence.child, Atomic)
            ):
                agenda.append(sentence)

        while len(agenda) > 0:
            p = agenda.pop(0)  # pop a symbol p
            if str(p) == str(q):  # if p is the query symbol
                return True  # return true
            if (
                inferred.get(str(p)) is None or inferred[str(p)] == False
            ):  # if p is not inferred yet
                inferred[str(p)] = True  # mark p as inferred
                for sentence in self.sentences:  # for each sentence in KB
                    if isinstance(sentence, If):  # if sentence is an implication
                        if str(sentence.left) == str(
                            p
                        ):  # if p is the premise of the implication
                            count[
                                str(sentence.right)
                            ] -= 1  # decrease the number of premises of the implication
                            if (
                                count[str(sentence.right)] == 0
                            ):  # if all premises of the implication are true
                                agenda.append(
                                    sentence.right
                                )  # add the conclusion to the agenda (true)
                    elif isinstance(sentence, Iff):
                        if str(sentence.left) == str(p):
                            count[str(sentence.right)] -= 1
                            if count[str(sentence.right)] == 0:
                                agenda.append(sentence.right)
                        elif str(sentence.right) == str(p):
                            count[str(sentence.left)] -= 1
                            if count[str(sentence.left)] == 0:
                                agenda.append(sentence.left)

        return False

    def resolution(self, query):
        if self.check(query):
            return True

        if self.check(Not(query)):
            return False

        def resolve(clause1, clause2):  # resolve clause 1 và clause 2
            resolvents = set()
            resolved = False

            for literal in clause1.get_literals():
                negated_literal = Not(literal)

                if str(negated_literal) in [str(l) for l in clause2.get_literals()]:
                    # nếu gặp 2 literal đối nhau
                    resolved = True

                    new_clause = [
                        l for l in clause1.get_literals() if str(l) != str(literal)
                    ] + [
                        l
                        for l in clause2.get_literals()
                        if str(l) != str(negated_literal)
                    ]

                    if len(new_clause) == 0:
                        break

                    resolvents.update(frozenset(new_clause))

            return resolvents, resolved

        clauses = self.toCnf()
        query = query.toCNF()
        clauses.append(Not(query).toCNF())

        # print([str(c) for c in clauses])

        new = []

        while True:
            n = len(clauses)

            for i in range(n):
                for j in range(i + 1, n):
                    resolvents, resolved = resolve(clauses[i], clauses[j])
                    if resolved:
                        if len(resolvents) == 0:  # KB and negation q unsatisfiable
                            # print(str(clauses[i]) + " " + str(clauses[j]))
                            return True
                        new.extend(resolvents)

            if set(new).issubset(set(clauses)):
                return False

            clauses.extend(new)

    def dpll_satisfiable(self, query):
        if self.check(query):
            return True

        if self.check(Not(query)):
            return False

        def unit_propagate(clauses, model):
            while True:
                unit_clauses = [c for c in clauses if len(c.get_literals()) == 1]
                if len(unit_clauses) == 0:
                    break
                for clause in unit_clauses:
                    literal = list(clause.get_literals())[0]
                    clauses = [
                        c
                        for c in clauses
                        if str(literal) not in [str(l) for l in c.get_literals()]
                    ]
                    model[str(literal)] = True
                    clauses = [
                        c
                        for c in clauses
                        if str(Not(literal)) not in [str(l) for l in c.get_literals()]
                    ]
                    model[str(Not(literal))] = False
            return clauses, model

        def pure_symbol(clauses):
            symbols = set()
            for clause in clauses:
                for literal in clause.get_literals():
                    symbols.add(str(literal))
            pure_symbols = set()
            for s in symbols:
                if str(Not(Atomic(s))) not in symbols:
                    pure_symbols.add(s)
            return pure_symbols

        def find_pure_symbol(clauses):
            pure_symbols = pure_symbol(clauses)
            for clause in clauses:
                for literal in clause.get_literals():
                    if str(literal) in pure_symbols:
                        return literal
            return None

        def dpll(clauses, symbols, model):
            clauses, model = unit_propagate(clauses, model)
            if len(clauses) == 0:
                return True, model
            if set().issubset(symbols):
                return False, None
            P = find_pure_symbol(clauses)
            if P is not None:
                symbols.remove(str(P))
                clauses = [
                    c
                    for c in clauses
                    if str(P) not in [str(l) for l in c.get_literals()]
                ]
                model[str(P)] = True
                return dpll(clauses, symbols, model)
            P = symbols.pop()
            symbols.add(P)
            clauses = [
                c
                for c in clauses
                if str(Not(Atomic(P))) not in [str(l) for l in c.get_literals()]
            ]
            model[str(Not(Atomic(P)))] = False
            return dpll(clauses, symbols, model)

        clauses = self.toCnf()
        query = query.toCNF()
        clauses.append(Not(query).toCNF())
        symbols = set()
        for clause in clauses:
            for literal in clause.get_literals():
                symbols.add(str(literal))
        model = {}
        satisfiable, model = dpll(clauses, symbols, model)
        print(f"{query} is {satisfiable} satisfiable")
        return satisfiable
