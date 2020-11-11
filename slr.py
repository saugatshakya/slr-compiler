import copy
class SLR:
    def __init__(self):
        self.grammar = []
        self.new_grammar = []
        self.terminals = []
        self.non_terminals = []
        self.Items = {}
        self.shift_list = []
        self.reduction_list = []
        self.action_list = []
        self.rule_dict = {}
        self.follow_dict = {}
        self.SR = []
        self.RR = []

    def _read_grammar(self):
        file_name = input('Enter the name of Grammar File: ')
        try:
            with open(file_name) as grammar_file:
                for each_grammar in grammar_file:
                    self.grammar.append(each_grammar.strip())
                    if each_grammar[0] not in self.non_terminals:
                        self.non_terminals.append(each_grammar[0])
                for each_grammar in self.grammar:
                    for token in each_grammar.strip().replace(" ","").replace("->", ""):
                        if token not in self.non_terminals and token not in self.terminals:
                            self.terminals.append(token)
                for l in range(1,len(self.grammar)+1):
                    self.rule_dict[l] = self.grammar[l-1]


        except:
            print("File not found")
            exit(0)

    def _agument_grammar(self):
        self._read_grammar()
        if "'" not in self.grammar[0]:
            self.grammar.insert(0, self.grammar[0][0]+"'"+"->"+ self.grammar[0][0])
        for each_grammar in self.grammar:
            idx = each_grammar.index(">")
            each_grammar = each_grammar[:idx+1]+"."+each_grammar[idx+1:]
            self.new_grammar.append(each_grammar)
    
    def _compute_I0(self):
        self._agument_grammar()
        added_grammar = []
        added_grammar.append(self.new_grammar[0])
        for each in added_grammar:
            current_pos = each.index(".")
            current_variable = each[current_pos+1]
            if current_variable not in self.new_grammar:
                for each_grammar in self.new_grammar:
                    if each_grammar[0] == current_variable and each_grammar not in added_grammar:
                        added_grammar.append(each_grammar)
            self.Items[0] = added_grammar
        
    def GOTO(self):
        self._compute_I0()
        variables = self.non_terminals + self.terminals
        i = 0
        current_state = 0
        done = False
        while(not done):
            for each_variable in variables:
                added_grammar = []
                try:
                    for each_rule in self.Items[current_state]:
                        if each_rule[-1] == ".":
                            continue
                        dot_idx = each_rule.index(".")
                        if each_rule[dot_idx+1] == each_variable:
                            rule = copy.deepcopy(each_rule)
                            rule = rule.replace(".", "")
                            rule = rule[:dot_idx+1]+"."+rule[dot_idx+1:]
                            added_grammar.append(rule)
                            
                            for rule in added_grammar:
                                dot_idx = rule.index(".")
                                if rule[-1] == ".":
                                    pass
                                else:
                                    current_variable = rule[dot_idx+1]
                                    if current_variable in self.non_terminals:
                                        for each_grammar in self.new_grammar:
                                            if each_grammar[0] == current_variable and each_grammar[1] != "'" and each_grammar not in added_grammar:
                                                added_grammar.append(each_grammar)
                
                except:
                    done = True
                    break
                if added_grammar:
                    if added_grammar not in self.Items.values():
                        i +=1
                        self.Items[i] = added_grammar
                    
                    for j,k in self.Items.items():
                        if added_grammar == k:
                            idx = j
                    self.shift_list.append([current_state, each_variable, idx])

            current_state +=1

    def follow(self,var):
        value = []
        if var == self.rule_dict[1][0]:
            value.append("$")
        
        for rule in self.rule_dict.values():
            lhs, rhs = rule.split("->")

            if var == rule[-1]:
                for each in self.follow(rule[0]):
                    if each not in value:
                        value.append(each)
            
            if var in rhs:
                idx = rhs.index(var)

                try:
                    if rhs[idx+1] in self.non_terminals and rhs[idx+1] != var:
                        for each in self.follow(rhs[idx+1]):
                            value.append(each)
                    else:
                        value.append(rhs[idx+1])
                except:
                    pass
        return value

    def reduction(self):
        self.reduction_list.append([1, "$", "Accept"])
        for item in self.Items.items():
            try:
                for each_production in item[1]:
                    lhs, rhs = each_production.split(".")
                    for rule in self.rule_dict.items():
                        if lhs == rule[1]:
                            f = self.follow(lhs[0])
                            for each_var in f:
                                self.reduction_list.append([item[0], each_var, "R"+str(rule[0])])
            except:
                pass

    def check_conflict(self):
        conflict = False
        for S in self.shift_list:
            for R in self.reduction_list:
                if S[:2] == R[:2]:
                    self.SR.append([S, R])
                    conflict = True
        for R1 in self.reduction_list:
            for R2 in self.reduction_list:
                if R1 == R2:
                    continue

                if R1[:2] == R2[:2]:
                    self.RR.append(R1)
                    conflict = True
        return conflict
    
    def test_simulation(self,string):
        done = False
        stack = []
        stack.append(0)
        print ("\n\nSTACK".ljust(32),"STRING".ljust(30),"ACTION".ljust(32))
        
        while not done:
            Reduce = False 
            Shift = False 
            for r in self.reduction_list:
                if r[0] == int(stack[-1]) and r[1] == string[0]:
                    Reduce = True
                    print (''.join(str(p) for p in stack).ljust(30), string.ljust(30), "Reduce", r[2])

                    if r[2] == 'Accept':
                        return 1
                    
                    var = self.rule_dict[int(r[2][1])]
                    lhs, rhs = var.split("->")

                    for x in range(len(rhs)):
                        stack.pop()
                        stack.pop()
                    
                    var = lhs
                    stack.append(var)

                    for a in self.action_list:
                        if a[0] == int(stack[-2]) and a[1] == stack[-1]:
                            stack.append(str(a[2]))
                            break
            
            for s in self.shift_list:
                if s[0] == int(stack[-1]) and s[1] == string[0]:
                    Shift = True
                    print(''.join(str(p) for p in stack).ljust(30), string.ljust(30), "Shift", "S"+str(s[2]))
                    stack.append(string[0])
                    stack.append(str(s[2]))
                    string = string[1:]

            if not Reduce and not Shift:
                print (''.join(str(p) for p in stack), "\t\t\t\t", string)
                return 0 

