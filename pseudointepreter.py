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
            case "assign":      self.assign_variable(node)
            case "constant":    self.assign_constant(node)
            case "output":      self.output(node)
            
    def assign_variable(self, node):
        value = self.evaluate_expression(node["value"])
        self.variables[node["target"]] = value
        
    def assign_constant(self, node):
        value = self.evaluate_expression(node["value"])
        self.constants[node["name"]] = value
        
    def output(self, node):
        values = [self.evaluate_expression(value) for value in node["value"]]
        print(*values)
        
    def evaluate_expression(self, node):
        node_type = node['type']

        if node_type == 'literal':
            return node['value']
        
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
            