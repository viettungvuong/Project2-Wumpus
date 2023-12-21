from logic import Not, And, Or, If, Iff, Atomic


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
            result.append(sentence.toCNF())
        return result

    def forward_chaining(self, q):
        if self.check(q):
            return True

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

    def resolution(kb, query):  # return True if KB entails query
        if kb.check(query):
            return True

        print(query)

        def resolve(clause1, clause2):
            new_clauses = []

            for literal in clause1.get_literals():
                negated_literal = Not(literal)
                if (
                    negated_literal in clause2.get_literals()
                ):  # if two clauses have positive and the other negative
                    combined = []
                    combined.extend(clause1.get_literals())
                    combined.extend(clause2.get_literals())

                    for l in combined:  # remove two literals if resolve
                        if l != literal and l != negated_literal:
                            new_clauses.append(l)
                    break

            return new_clauses

        clauses = kb.toCnf()
        clauses.append(Not(query))  # add negated query to clauses to try to prove
        new = []

        while True:
            n = len(clauses)

            for i in range(n):
                for j in range(i + 1, n):
                    resolvents = resolve(clauses[i], clauses[j])
                    if len(resolvents) == 0:
                        return True
                    new.extend(
                        resolvent for resolvent in resolvents if resolvent not in new
                    )

            if all(item in clauses for item in new):
                return False

            clauses.extend(
                new_clause for new_clause in new if new_clause not in clauses
            )
