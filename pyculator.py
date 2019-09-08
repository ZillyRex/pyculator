class calculator:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.legal_obj = {'+', '-', '*', '/', '^', '%',
                          '(', ')', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        self.op_prio = {'*': 2,
                        '/': 2,
                        '^': 2,
                        '%': 2,
                        '+': 1,
                        '-': 1,
                        '#': 0,
                        '(': 0,
                        ')': 0}
        self.op_func = {'+': self._add,
                        '-': self._sub,
                        '*': self._mul,
                        '/': self._div,
                        '^': self._pow,
                        '%': self._mod}

    def _add(self, op1, op2):
        return op1+op2

    def _sub(self, op1, op2):
        return op1-op2

    def _mul(self, op1, op2):
        return op1*op2

    def _div(self, op1, op2):
        return op1/op2

    def _pow(self, op1, op2):
        return op1**op2

    def _mod(self, op1, op2):
        return op1 % op2

    def _rpn(self, exp):
        exp += '#'
        res = []
        op_stack = []
        ptr = 0
        while(ptr < len(exp)):
            if(exp[ptr].isdigit()):
                cur_dig_str = ''
                while((exp[ptr].isdigit() or exp[ptr] == '.')and ptr < len(exp)):
                    cur_dig_str += exp[ptr]
                    ptr += 1
                res.append(float(cur_dig_str))
            else:
                if(exp[ptr] == '(' or len(op_stack) == 0 or self.op_prio[exp[ptr]] > self.op_prio[op_stack[-1]]):
                    op_stack.append(exp[ptr])
                elif(exp[ptr] == ')'):
                    while(op_stack[-1] != '('):
                        res.append(op_stack.pop())
                    op_stack.pop()
                else:
                    while(len(op_stack) != 0 and self.op_prio[exp[ptr]] <= self.op_prio[op_stack[-1]]):
                        res.append(op_stack.pop())
                    op_stack.append(exp[ptr])
                ptr += 1
        return res

    def _clear(self, org_exp):
        exp_status = 1
        exp = org_exp.replace(' ', '')
        for i in exp:
            if(i not in self.legal_obj):
                print('illegal obj: \'{}\''.format(i))
                exp_status = 0
                exp = None
                break
        return exp_status, exp

    def calc(self, org_exp):
        exp_status, exp = self._clear(org_exp)
        if(exp_status == 0):
            return None
        exp_rpn = self._rpn(exp)
        stack = []
        for i in range(len(exp_rpn)):
            if(type(exp_rpn[i]) != str):
                stack.append(float(exp_rpn[i]))
            else:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(self.op_func[exp_rpn[i]](op2, op1))
        return stack[0]
