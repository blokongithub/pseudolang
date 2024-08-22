from pseudointepreter import PseudoCodeInterpreter
import json

with open("debug/debugparser.json") as f:
    data = json.load(f)
    data = data["body"]
    interpreter = PseudoCodeInterpreter(data)
    interpreter.run()