from logic import Not, And, Or, If, Iff, Atomic, Formula, Operator


class KB:
    def __init__(self):
        self.sentences = []

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
            if isinstance(sentence, Atomic):
                count[str(sentence)] = 0
                inferred[str(sentence)] = False

        for sentence in self.sentences:
            if isinstance(sentence, If):
                if count.get(str(sentence.right)) is None:
                    count[str(sentence.right)] = 0
                    inferred[str(sentence.right)] = False
                count[str(sentence.right)] += 1
            elif isinstance(sentence, Iff):
                if count.get(str(sentence.right)) is None:
                    count[str(sentence.right)] = 0
                    inferred[str(sentence.right)] = False
                count[str(sentence.right)] += 1
                if count.get(str(sentence.left)) is None:
                    count[str(sentence.left)] = 0
                    inferred[str(sentence.left)] = False
                count[str(sentence.left)] += 1

        agenda = []  # list of symbols known to be true
        for sentence in self.sentences:
            if isinstance(sentence, Atomic):
                if sentence == q:
                    agenda.append(sentence)

        while len(agenda) > 0:
            p = agenda.pop()  # pop a symbol p
            if p == q:  # if p is the query symbol
                return True  # return true
            if not inferred[p]:  # if p is not inferred yet
                inferred[str(p)] = True  # mark p as inferred
                for sentence in self.sentences:  # for each sentence in KB
                    if isinstance(sentence, If):  # if sentence is an implication
                        if sentence.left == p:  # if p is the premise of the implication
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
                        if sentence.left == p:
                            count[str(sentence.right)] -= 1
                            if count[str(sentence.right)] == 0:
                                agenda.append(sentence.right)
                        elif sentence.right == p:
                            count[str(sentence.left)] -= 1
                            if count[str(sentence.left)] == 0:
                                agenda.append(sentence.left)
        return False

    def resolution(self, query):
        if self.check(query):
            return True

        if self.check(Not(query)):
            return False

        def resolve(clause1, clause2):
            resolvents = set()
            resolved = False

            for literal in clause1.get_literals():
                negated_literal = Not(literal)

                if str(negated_literal) in [str(l) for l in clause2.get_literals()]:
                    resolved = True

                    new_clause = [
                        l for l in clause1.get_literals() if str(l) != str(literal)
                    ] + [
                        l
                        for l in clause2.get_literals()
                        if str(l) != str(negated_literal)
                    ]

                    if not new_clause or len(new_clause) == 0:
                        resolvents.update(frozenset())
                        break

                    resolvents.update(frozenset(new_clause))

            return resolvents, resolved

        clauses = self.toCnf()
        query = query.toCNF()
        clauses.append(Not(query).toCNF())

        new = []
        resolved_clauses = set()  # Keep track of resolved clauses

        while True:
            n = len(clauses)

            for i in range(n):
                for j in range(i + 1, n):
                    if (i, j) in resolved_clauses:  # Skip already resolved clauses
                        continue

                    resolvents, resolved = resolve(clauses[i], clauses[j])
                    if resolved:
                        if len(resolvents) == 0:
                            return True
                        new.extend(resolvents)

                    resolved_clauses.add((i, j))  # Mark clauses as resolved

            if set(new).issubset(set(clauses)):
                return False

            clauses.extend(new)
