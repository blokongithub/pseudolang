import os
from pseudolexer import Pseudolexer
#from pseudoparser import Pseudoparser
#from pseudointerpreter import PseudoInterpreter

class Cli():
    def __init__(self) -> None:
        self.command = ""
        self.commands = ["run", "exit", "help", "clear", "new", "del"]
        self.running = True
        self.lexer = Pseudolexer()
        
    def runcli(self):
        while self.running:
            self.askinput()
            self.getcommand()
            
    def exit(self):
        self.running = False
        
    def askinput(self):
        self.command = input("pseudolang > ")
    
    def getfirstword(self, string):
        if string == "": return string
        return string.split()[0]
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def makenewfile(self, filename):
        with open(filename, "w") as file:
            file.write("")
            
    def deletefile(self, filename):
        os.remove(filename)
        
    def getcommand(self):
        if self.getfirstword(self.command) in self.commands:
            if self.getfirstword(self.command) == "run":
                with open (self.command.split()[1], "r") as file:
                    data = file.read()
                    for tok in self.lexer.tokenize(data):
                        print(tok)
                
            elif self.getfirstword(self.command) == "exit":
                self.exit()
                
            elif self.getfirstword(self.command) == "help":
                print("""Commands:\n
run - Runs a file, usage run [filename]\n
exit - Exit the CLI\n
help - Show this message\n
clear - Clear the screen\n
new - Create a new file, usage new [filename]\n
del - Delete a file, usage del [filename]""")
                
            elif self.getfirstword(self.command) == "clear":
                self.clear()
            
            elif self.getfirstword(self.command) == "new":
                print("creating new file...")
                self.makenewfile(self.command.split()[1])
                print("file created")
                
            elif self.getfirstword(self.command) == "del":
                print("deleting file...")
                self.deletefile(self.command.split()[1])
                print("file deleted")
                
        else:
            print("Invalid command, please use 'help' if you are unsure of ther commands")