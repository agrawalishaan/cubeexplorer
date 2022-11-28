from flask import Flask, request

app = Flask(__name__)

@app.route("/solve", methods=["GET"])
def handle_solve():
    scramble = request.args.get("scramble")
    max_depth = request.args.get("max_depth")
    move_types = request.args.get("move_types")
    if scramble == None or max_depth == None or move_types == None:
        return "Please provide scramble, max_depth, and move_types", 400
    
    # TODO: pass scramble to solver and return the result
    solution = "R U R' U'"

    return solution
