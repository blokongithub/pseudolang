import json
import os
from pseudolexer import PseudoCodeLexer
from pseudoparser import PseudoCodeParser
from pseudointepreter import PseudoCodeInterpreter

class Cli():
    def __init__(self, debuglexer=False, debugparser=False) -> None:
        self.command = ""
        self.commands = ["docs", "run", "exit", "help", "clear", "new", "del", "vars", "compile"]   
        self.running = True
        self.lexer = PseudoCodeLexer()
        self.parser = PseudoCodeParser()
        self.debuglexer = debuglexer
        self.debugparser = debugparser
        
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
            if self.getfirstword(self.command) == "compile":
                try:
                    with open(self.command.split()[1], "r") as file:
                        data = file.read()
                        tree = self.parser.parse(self.lexer.tokenize(data))
                        
                        if self.debuglexer:
                            with open("debug/debuglexer.txt", "w") as debug_file:
                                for token in self.lexer.tokenize(data):
                                    debug_file.write(f"{token.type} {token.value}\n")
                                    
                        if self.debugparser:
                            with open("debug/debugparser.json", "w") as debug_file:
                                json.dump(tree, debug_file, indent=2)
                    print("file compiled")
                except FileNotFoundError:
                    print(f"File {self.command.split()[1]} not found.")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    
            elif self.getfirstword(self.command) == "run":
                try:
                    with open(self.command.split()[1], "r") as file:
                        data = file.read()
                        tree = self.parser.parse(self.lexer.tokenize(data))
                        interpreter = PseudoCodeInterpreter(tree["body"])
                        if self.debuglexer:
                            with open("debug/debuglexer.txt", "w") as debug_file:
                                for token in self.lexer.tokenize(data):
                                    debug_file.write(f"{token.type} {token.value}\n")
                                    
                        if self.debugparser:
                            with open("debug/debugparser.json", "w") as debug_file:
                                json.dump(tree, debug_file, indent=2)
                        interpreter.run()
                except FileNotFoundError:
                    print(f"File {self.command.split()[1]} not found.")
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                
            elif self.getfirstword(self.command) == "exit":
                self.exit()
                
            elif self.getfirstword(self.command) == "help":
                print("""Commands:\n
run - Runs a file, usage run [filename]\n
compile - Compiles a file, usage compile [filename]\n
exit - Exit the CLI\n
help - Show this message\n
clear - Clear the screen\n
new - Create a new file, usage new [filename]\n
del - Delete a file, usage del [filename]\n
vars - Show current variables (if implemented)\n
docs - Show documentation (if implemented)\n""")
                
            elif self.getfirstword(self.command) == "clear":
                self.clear()
            
            elif self.getfirstword(self.command) == "docs":
                print("https://filestore.aqa.org.uk/resources/computing/AQA-8525-NG-PC.PDF")
            
            elif self.getfirstword(self.command) == "new":
                try:
                    self.makenewfile(self.command.split()[1])
                    print("File created.")
                except Exception as e:
                    print(f"An error occurred while creating the file: {str(e)}")
                
            elif self.getfirstword(self.command) == "del":
                try:
                    self.deletefile(self.command.split()[1])
                    print("File deleted.")
                except FileNotFoundError:
                    print("File not found.")
                except Exception as e:
                    print(f"An error occurred while deleting the file: {str(e)}")
                
            elif self.getfirstword(self.command) == "vars":
                # Assuming the parser or environment holds variables (if implemented)
                if hasattr(self.parser, 'variables'):
                    print(self.parser.variables)
                else:
                    print("No variables are currently stored.")
            
        else:
            data = self.command
            try:
                result = self.parser.parse(self.lexer.tokenize(data))
                interpreter = PseudoCodeInterpreter(result["body"])
                interpreter.run()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
