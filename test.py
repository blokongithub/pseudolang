from pseudointepreter import PseudoCodeInterpreter
import json

with open("debug/debugparser.json") as f:
    data = json.load(f)
    data = data["body"]
    interpreter = PseudoCodeInterpreter(data)
    print("\n" + "-"*6 + "\nOUTPUT\n" + "-"*6 +"\n")
    interpreter.run()
    print("\n")
    print("vars", interpreter.variables)
    print("constants", interpreter.constants)