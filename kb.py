from logic import Not, And, Or, If, Iff, Atomic


class KB:
    def __init__(self):
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def remove(self, sentence):
        self.sentences.remove(sentence)

    def __str__(self):
        return str(self.sentences)

    def check(self, sentence): # check if sentence is in KB
        return sentence in self.sentences

    def toCnf(self):
        result = []
        for sentence in self.sentences:
            result.append(sentence.toCnf())
        return result

    def backward_chaining(self, q):

        if q in self.sentences:
            return True

        if isinstance(q, Not):
            return not self.backward_chaining(q.child)

        if isinstance(q, And):
            return self.backward_chaining(q.left) and self.backward_chaining(q.right)

        if isinstance(q, Or):
            return self.backward_chaining(q.left) or self.backward_chaining(q.right)

        for sentence in self.sentences:
            if isinstance(sentence, If):
                if sentence.left == q:
                    return self.backward_chaining(sentence.right)
                elif sentence.right == q: # nếu trong câu implies mà q nằm ở vế phải (được suy ra)
                    return self.backward_chaining(sentence.left)

            elif isinstance(sentence, Iff):
                if sentence.left == q:
                    return self.backward_chaining(sentence.right)

        return False

    def resolution(self, alpha):
        def disjunction_clauses(or_clause):
            if isinstance(or_clause, Atomic) or isinstance(or_clause, Not):
                return [or_clause]

            if not isinstance(or_clause, Or):
                return None

            res = []
            if isinstance(or_clause.left, Or):
                res += disjunction_clauses(or_clause.left)
            else:
                res.append(or_clause.left)

            if isinstance(or_clause.right, Or):
                res += disjunction_clauses(or_clause.right)
            else:
                res.append(or_clause.right)

            return res

        clauses = self.toCnf()
        clauses.append(Not(alpha).toCNF()) # add not alpha to clauses

        new = set()
        while True:
            n = len(clauses)
            pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)] # traverse through pairs of clauses

            for (clauseA, clauseB) in pairs:
                clauses_fromA = disjunction_clauses(clauseA)
                clauses_fromB = disjunction_clauses(clauseB)

                if clauses_fromA is None or clauses_fromB is None:
                    continue

                for cA in clauses_fromA:
                    for cB in clauses_fromB:
                        if cA == Not(cB) or Not(cA) == cB: # if cA and cB are opposite
                            clauses.remove(clauseA)
                            clauses.remove(clauseB)
                            resolvents = [c for c in clauses_fromA + clauses_fromB if c != cA and c != cB]
                            new_clause = None
                            for r in resolvents:
                                if new_clause is None:
                                    new_clause = r
                                else:
                                    new_clause = Or(new_clause, r)

                            clauses.append(new_clause)

            if len(clauses) == 0 or clauses[0] is None:
                return True # satisfiable
            return False
