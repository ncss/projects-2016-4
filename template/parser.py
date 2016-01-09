class Parser:
    def __init__(self, expr):
        self._expr = expr
        self._len = len(expr)
        self._pos = 0

    def end(self):
        return self._pos == self._len

    def peek(self):
        return None if self.end() else self._expr[self._pos]

    def next(self):
        if not self.end():
            self._pos += 1

    def _parse_e1(self):
        ret0 = self._parse_e2()
        ret1 = None
        if not ret0:
            return None
        if self.peek() == '+':
            self.next()
            ret1 = self._parse_e1()
            if not ret1:
                return None
            return AddNode(ret0, ret1)
        return ret0

    def _parse_e2(self):
        ret0 = self._parse_e3()
        ret1 = None
        if not ret0:
            return False
        if self.peek() == '*':
            self.next()
            ret1 = self._parse_e2()
            if not ret1:
                return None
            return MulNode(ret0, ret1)
        return ret0

    def _parse_e3(self):
        if self.peek() == "(":
            self.next()
            ret = self._parse_e1()
            if not ret:
                return None
            if self.peek() != ")":
                return None
            self.next()
            return ret
        else:
            positive = True
            builder = ''
            if self.peek() == '-':
                positive = False
                self.next()
            while self.peek() is not None and self.peek() in '0123456789':
                builder += self.peek()
                self.next()
            if len(builder) == 0:
                return None
            if not positive:
                builder = '-'+builder
            return LiteralNode(int(builder), None)

        return self._parse_e1()

    def parse(self):
        try:
            return self._parse_e1()
        except Exception:
            print('Oh noes!')
