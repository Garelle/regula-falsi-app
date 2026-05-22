from flask import Flask, render_template, request
import math

app = Flask(__name__)

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """
    Regula Falsi method implementation
    Returns: (root, iterations, steps)
    """
    steps = []
    
    if f(a) * f(b) >= 0:
        return None, 0, [{"error": "Function must have opposite signs at a and b"}]
    
    for i in range(max_iter):
        # Calculate c using false position formula
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        fc = f(c)
        
        steps.append({
            "iteration": i + 1,
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "f_a": round(f(a), 6),
            "f_b": round(f(b), 6),
            "f_c": round(fc, 6)
        })
        
        if abs(fc) < tol or abs(b - a) < tol:
            return c, i + 1, steps
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    
    return c, max_iter, steps

# Define functions that users can select
def func1(x):
    """x^3 - x - 2"""
    return x**3 - x - 2

def func2(x):
    """x^2 - 4"""
    return x**2 - 4

def func3(x):
    """cos(x) - x"""
    return math.cos(x) - x

def func4(x):
    """e^(-x) - x"""
    return math.exp(-x) - x

def func5(x):
    """x^3 - 2x - 5"""
    return x**3 - 2*x - 5

FUNCTIONS = {
    "x³ - x - 2": func1,
    "x² - 4": func2,
    "cos(x) - x": func3,
    "e^(-x) - x": func4,
    "x³ - 2x - 5": func5
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    iterations = None
    steps = None
    error = None
    
    if request.method == 'POST':
        try:
            func_name = request.form.get('function')
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))
            tolerance = float(request.form.get('tolerance', 1e-6))
            
            if func_name in FUNCTIONS:
                f = FUNCTIONS[func_name]
                root, iter_count, steps_data = regula_falsi(f, a, b, tolerance)
                
                if root is not None:
                    result = round(root, 8)
                    iterations = iter_count
                    steps = steps_data
                else:
                    error = "Function must have opposite signs at the endpoints!"
            else:
                error = "Please select a valid function"
                
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template('index.html', 
                         result=result, 
                         iterations=iterations, 
                         steps=steps,
                         error=error,
                         functions=FUNCTIONS.keys())

if __name__ == '__main__':
    app.run(debug=True)