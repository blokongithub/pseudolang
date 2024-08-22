class PseudoCodeInterpreter():
    def __init__(self, programme):
        self.variables = {}
        self.subroutines = {}
        self.constants = {}
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
            case "assign":          self.assign_variable(node)
            case "constant":        self.assign_constant(node)
            case "output":          self.output(node)
            case "if":              self.if_statement(node)
            case "if_else":         self.if_else_statement(node)
            case "for":             self.for_loop(node)
            case "while":           self.while_loop(node)
            case "repeat_until":    self.repeat_until(node)
            case "userinput":       self.userinp(node)
            case "record":          self.definerecord(node)
            case "subroutine":      pass
            case "call":            self.call_subroutine(node)
            
    def assign_variable(self, node):
        value = self.evaluate_expression(node["value"])
        self.variables[node["target"]] = value
        
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
    
    def if_else_statement(self, node):
        condition = self.evaluate_expression(node["condition"])
        if condition:
            for statement in node["then"]:
                self.execute(statement)
        else:
            for statement in node["else"]:
                self.execute(statement)
    
    def for_loop(self, node):
        start = self.evaluate_expression(node['start'])
        end = self.evaluate_expression(node['end'])
        step = self.evaluate_expression(node.get('step', {"type": "literal", "value": 1}))
        variable_name = node['variable']

        for value in range(start, end + 1, step):
            self.variables[variable_name] = value
            for statement in node['body']:
                self.execute(statement)
        del self.variables[variable_name]

    def while_loop(self, node):
        while self.evaluate_expression(node['condition']):
            for statement in node['body']:
                self.execute(statement)
                
    def repeat_until(self, node):
        while True:
            for statement in node['body']:
                self.execute(statement)
            if self.evaluate_expression(node['condition']):
                break
            
    def userinp(self, node):
        value = input(f"Input for variable '{node['target']}': ")
        self.variables[node['target']] = value
        
    def call_subroutine(self, node):
        subroutine = self.subroutines.get(node["name"])
        
        if not subroutine:
            raise ValueError(f"Subroutine '{node['name']}' not found")
        
        local_variables = {}
        
        for param, arg in zip(subroutine['params'], node['args']):
            local_variables[param] = self.evaluate_expression(arg)
            
        saved_variables = self.variables.copy()
        self.variables = local_variables
        
        for statement in subroutine['body']:
            self.execute(statement)
            
        self.variables = saved_variables
                     
    def evaluate_expression(self, node):
        node_type = node['type']

        if node_type == 'literal':
            return node['value']
        
        if node_type == 'int':
            return int(node['value'])
        
        elif node_type == 'var':
            return self.variables.get(node['name'], self.constants.get(node['name']))
        
        elif node_type == 'binop':
            left = self.evaluate_expression(node['left'])
            right = self.evaluate_expression(node['right'])
            return self.apply_operator(node['operator'], left, right)
    
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
            case _:     raise ValueError(f"unknown operator: {operator}")
            