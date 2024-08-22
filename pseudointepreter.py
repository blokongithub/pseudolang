class PseudoCodeInterpreter():
    def __init__(self, programme):
        self.variables = {}
        self.subroutines = {}
        self.programme = programme
        self.load_subroutines()

    def load_subroutines(self):
        for node in self.programme:
            if node['type'] == "subroutine":
                self.subroutines[node['name']] = node
    