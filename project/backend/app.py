from flask import Flask, jsonify, request

app = Flask(__name__)


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    operation = data.get("operation")
    a = data.get("a")
    b = data.get("b")

    if operation is None or a is None or b is None:
        return jsonify({"error": "operation, a and b are required"}), 400

    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if operation not in operations:
        return jsonify({"error": f"Unsupported operation: {operation}"}), 400

    try:
        result = operations[operation](a, b)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"result": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
