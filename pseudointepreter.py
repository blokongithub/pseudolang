class PseudoCodeInterpreter():
    def __init__(self, programme):
        self.variables = {}
        self.subroutines = {}
        self.constants = {}
        #self.records = {} uncomment when records are implemented
        self.programme = programme
        self.load_subroutines()

    def load_subroutines(self):
        for node in self.programme:
            if node["type"] == "subroutine":
                self.subroutines[node["name"]] = node
    
    def run(self):
        for node in self.programme:
            self.execute(node)
    
    def execute(self, node):
        ntype = node["type"]
        
        match ntype:
            case "assign":              self.assign_variable(node)
            case "constant":            self.assign_constant(node)
            case "output":              self.output(node)
            case "if":                  self.if_statement(node)
            case "if_else":             self.if_else_statement(node)
            case "for":                 self.for_loop(node)
            case "while":               self.while_loop(node)
            case "repeat_until":        self.repeat_until(node)
            case "userinput":           self.userinp(node)
            case "record":              self.definerecord(node)
            case "subroutine":          pass
            case "call":                self.call_subroutine(node)
            case "if_elseif":           self.if_elseif_statement(node)
            case "list_assign":         self.list_assign(node)
            case "list_call":           self.list_call(node)
            case "listvalue_assign":    self.listvalue_assign(node)
            
    def assign_variable(self, node):
        if node["value"]["type"] != "call":
            value = self.evaluate_expression(node["value"])
        else:
            value = self.call_subroutine(node["value"])
        self.variables[node["target"]] = value
        
    def list_assign(self, node):
        var = []
        for i in node["value"]:
            var.append(self.evaluate_expression(i))
        self.variables[node["target"]] = var
        
    def listvalue_assign(self, node):
        self.variables[node["target"]][self.evaluate_expression(node["index"])] = self.evaluate_expression(node["value"])
    
    def list_call(self, node):
        return self.variables[node["name"]][self.evaluate_expression(node["args"][0])]
        
    def assign_constant(self, node):
        value = self.evaluate_expression(node["value"])
        self.constants[node["name"]] = value
        
    def output(self, node):
        values = [self.evaluate_expression(value) for value in node["value"]]
        print(*values)
        
    def if_statement(self, node):
        condition = self.evaluate_expression(node["condition"])
        if condition:
            for statement in node["then"]:
                self.execute(statement)
                
    def if_elseif_statement(self, node):
        executed = False

        if self.evaluate_expression(node["condition"]):
            for statement in node["then"]:
                self.execute(statement)
            executed = True
        else:
            for elseif in node.get("else_if", []):
                if self.evaluate_expression(elseif["condition"]):
                    if not executed:
                        for statement in elseif["then"]:
                            self.execute(statement)
                        executed = True
                    break

        if not executed and "else" in node:
            for statement in node["else"]:
                self.execute(statement)

    def for_loop(self, node):
        start = self.evaluate_expression(node["start"])
        end = self.evaluate_expression(node["end"])
        step = self.evaluate_expression(node.get("step", {"type": "literal", "value": 1}))
        variable_name = node["variable"]

        for value in range(start, end + 1, step):
            self.variables[variable_name] = value
            for statement in node["body"]:
                if statement["type"] == "break":
                    break
                self.execute(statement)
        del self.variables[variable_name]

    def while_loop(self, node):
        while self.evaluate_expression(node["condition"]):
            for statement in node["body"]:
                if statement["type"] == "break":
                    break
                self.execute(statement)
                
    def repeat_until(self, node):
        while True:
            for statement in node["body"]:
                self.execute(statement)
                if statement["type"] == "break":
                    break
            if self.evaluate_expression(node["condition"]):
                break
    def userinp(self, node):
        if "target" in node:
            value = input(f"input for variable \"{node['target']}\": ")
            self.variables[node["target"]] = value
        else:
            value = input("input: ")
        if value is None:
            raise ValueError("input cannot be none.")

        return str(value)  
            
    def call_subroutine(self, node):
        subroutine = self.subroutines.get(node["name"])
        
        if not subroutine:
            raise ValueError(f"subroutine \"{node['name']}\" not found")
        
        local_variables = {}
        
        for param, arg in zip(subroutine["params"], node["args"]):
            local_variables[param] = self.evaluate_expression(arg)
            
        saved_variables = self.variables.copy()
        self.variables = local_variables
        
        for statement in subroutine["body"]:
            if statement["type"] == "return":
                if statement["value"]:
                    return_value = self.evaluate_expression(statement["value"])
                    self.variables = saved_variables
                    return return_value
            self.execute(statement)
            
        self.variables = saved_variables
                     
    def evaluate_expression(self, node):
        node_type = node["type"]

        if node_type == "literal":
            return node["value"]
        
        if node_type == "int":
            return int(node["value"])
        
        elif node_type == "var":
            return self.variables.get(node["name"], self.constants.get(node["name"]))
        
        elif node_type == "binop":
            left = self.evaluate_expression(node["left"])
            right = self.evaluate_expression(node["right"])
            return self.apply_operator(node["operator"], left, right)
        
        elif node_type == "call":
            return self.call_subroutine(node)
        
        elif node_type == "userinput":
            return self.userinp(node)
        
        else:
            return self.other_funcs(node)
    
    def apply_operator(self, op, l, r):
        match op:
            case "+":   return l + r
            case "-":   return l - r
            case "*":   return l * r
            case "/":   return l / r
            case "MOD": return l % r
            case "DIV": return l // r
            case "<":   return l < r
            case ">":   return l > r
            case "≤":   return l <= r
            case "≥":   return l >= r
            case "≠":   return l != r
            case "=":   return l == r
            case _:     raise ValueError(f"unknown operator: {op}")
            
    def other_funcs(self, node):
        if node["type"] == "len":
            return len(self.evaluate_expression(node["value"])) - 2
        elif node["type"] == "position":
            string = self.evaluate_expression(node["string"])
            substring = self.evaluate_expression(node["substring"])
            return string.find(substring)
        elif node["type"] == "random_int":
            import random
            return random.randint(self.evaluate_expression(node["min"]), self.evaluate_expression(node["max"]))
        elif node["type"] == "substring":
            string = self.evaluate_expression(node["string"])
            start = self.evaluate_expression(node["start"])
            length = self.evaluate_expression(node["length"])
            return string[start:start + length]
        elif node["type"] == "string_to_int":
            return int(self.evaluate_expression(node["value"]))
        elif node["type"] == "string_to_real":
            return float(self.evaluate_expression(node["value"]))
        elif node["type"] == "int_to_string":
            return str(self.evaluate_expression(node["value"]))
        elif node["type"] == "real_to_string":
            return str(self.evaluate_expression(node["value"]))
        elif node["type"] == "char_to_code":
            return ord(self.evaluate_expression(node["value"]))
        elif node["type"] == "code_to_char":
            return chr(self.evaluate_expression(node["value"]))
        elif node["type"] == "list_call":
            return self.list_call(node)
        else:
            raise ValueError("unknown expression type:", node["type"])
