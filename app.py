from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def regula_falsi(f, a, b, tol=1e-6, max_iter=50):
    """Regula Falsi method"""
    steps = []
    
    try:
        fa = f(a)
        fb = f(b)
        
        if fa * fb >= 0:
            return None, 0, [{"error": "f(a) and f(b) must have opposite signs"}]
        
        for i in range(max_iter):
            c = (a * fb - b * fa) / (fb - fa)
            fc = f(c)
            
            steps.append({
                "iteration": i + 1,
                "a": round(a, 6),
                "b": round(b, 6),
                "c": round(c, 6),
                "f_c": round(fc, 6)
            })
            
            if abs(fc) < tol or abs(b - a) < tol:
                return c, i + 1, steps
            
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        
        return c, max_iter, steps
    except Exception as e:
        return None, 0, [{"error": str(e)}]

# Function definitions
def f1(x):
    return x**3 - x - 2

def f2(x):
    return x**2 - 4

def f3(x):
    return math.cos(x) - x

def f4(x):
    return math.exp(-x) - x

def f5(x):
    return x**3 - 2*x - 5

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Regula Falsi Method</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            h2 { color: #555; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
            input, select, button {
                padding: 10px;
                margin: 5px 0;
                width: 100%;
                max-width: 300px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover { background: #0056b3; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            th { background: #007bff; color: white; }
            .result { background: #d4edda; padding: 15px; border-radius: 5px; margin-top: 15px; }
            .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-top: 15px; }
            .example { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .math { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
            @media (max-width: 600px) {
                body { padding: 10px; }
                table { font-size: 12px; }
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📐 Regula Falsi (False Position) Method</h1>
            <p>A root-finding algorithm that combines the bisection and secant methods.</p>
        </div>

        <div class="card">
            <h2>📖 Mathematical Formula</h2>
            <div class="math">
                <p>The Regula Falsi method uses linear interpolation:</p>
                \[
                c = \\frac{a \\cdot f(b) - b \\cdot f(a)}{f(b) - f(a)}
                \]
                <p>Where \(a\) and \(b\) are points where \(f(a)\) and \(f(b)\) have opposite signs.</p>
            </div>
        </div>

        <div class="card">
            <h2>📝 Example 1: Find root of \(x^3 - x - 2 = 0\)</h2>
            <div class="example">
                <p><strong>Step 1:</strong> Find interval where sign changes.</p>
                <p>\(f(1) = 1^3 - 1 - 2 = -2\) (negative)</p>
                <p>\(f(2) = 8 - 2 - 2 = 4\) (positive)</p>
                <p>Root lies in \([1, 2]\) since signs are opposite.</p>
                
                <p><strong>Step 2:</strong> Apply formula:</p>
                <p>\(c = \\frac{1 \\times 4 - 2 \\times (-2)}{4 - (-2)} = \\frac{4 + 4}{6} = 1.3333\)</p>
                
                <p><strong>Step 3:</strong> Evaluate \(f(1.3333) = -0.963\)</p>
                
                <p><strong>Step 4:</strong> Since \(f(1.3333)\) is negative and \(f(2)\) is positive, new interval is \([1.3333, 2]\)</p>
                
                <p><strong>Final Root after iterations:</strong> \(x \\approx 1.52138\)</p>
            </div>
        </div>

        <div class="card">
            <h2>📝 Example 2: Find root of \(x^2 - 4 = 0\)</h2>
            <div class="example">
                <p><strong>Step 1:</strong> Interval [1, 3]</p>
                <p>\(f(1) = -3\), \(f(3) = 5\) ✓ opposite signs</p>
                
                <p><strong>Step 2:</strong> First iteration:</p>
                <p>\(c = \\frac{1 \\times 5 - 3 \\times (-3)}{5 - (-3)} = 1.75\)</p>
                <p>\(f(1.75) = -0.9375\)</p>
                
                <p><strong>Step 3:</strong> Second iteration using [1.75, 3]:</p>
                <p>\(c = 1.9474\), \(f(1.9474) = -0.208\)</p>
                
                <p><strong>Final Root:</strong> \(x = 2.0000\)</p>
            </div>
        </div>

        <div class="card">
            <h2>🧮 Interactive Calculator</h2>
            <form method="POST">
                <div>
                    <label>Select Function:</label>
                    <select name="function" required>
                        <option value="x³ - x - 2">x³ - x - 2</option>
                        <option value="x² - 4">x² - 4</option>
                        <option value="cos(x) - x">cos(x) - x</option>
                        <option value="e^(-x) - x">e^(-x) - x</option>
                        <option value="x³ - 2x - 5">x³ - 2x - 5</option>
                    </select>
                </div>
                
                <div>
                    <label>Lower bound (a):</label>
                    <input type="number" name="a" step="any" required placeholder="e.g., 1">
                </div>
                
                <div>
                    <label>Upper bound (b):</label>
                    <input type="number" name="b" step="any" required placeholder="e.g., 2">
                </div>
                
                <div>
                    <label>Tolerance (e.g., 0.000001):</label>
                    <input type="number" name="tolerance" step="any" value="0.000001">
                </div>
                
                <button type="submit">Find Root</button>
            </form>
            
            <!-- Results will be shown here from the POST request -->
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def index_post():
    try:
        func_name = request.form.get('function')
        a = float(request.form.get('a'))
        b = float(request.form.get('b'))
        tolerance = float(request.form.get('tolerance', 1e-6))
        
        func_map = {
            "x³ - x - 2": f1,
            "x² - 4": f2,
            "cos(x) - x": f3,
            "e^(-x) - x": f4,
            "x³ - 2x - 5": f5
        }
        
        if func_name not in func_map:
            return index() + f'<div class="card error"><h3>Error</h3><p>Invalid function</p></div>'
        
        f = func_map[func_name]
        root, iterations, steps = regula_falsi(f, a, b, tolerance)
        
        if root is None:
            return index() + f'<div class="card error"><h3>Error</h3><p>f(a) and f(b) must have opposite signs! f({a}) = {f(a)}, f({b}) = {f(b)}</p></div>'
        
        # Build results HTML
        result_html = f'''
        <div class="card">
            <h2>✅ Results</h2>
            <div class="result">
                <p><strong>Root found:</strong> x = {root:.8f}</p>
                <p><strong>Iterations needed:</strong> {iterations}</p>
            </div>
            <h3>📊 Iteration Details:</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Iteration</th>
                            <th>a</th>
                            <th>b</th>
                            <th>c</th>
                            <th>f(c)</th>
                        </tr>
                    </thead>
                    <tbody>
        '''
        
        for step in steps:
            if 'error' in step:
                result_html += f'<tr><td colspan="5">Error: {step["error"]}</td></tr>'
            else:
                result_html += f'''
                        <tr>
                            <td>{step["iteration"]}</td>
                            <td>{step["a"]}</td>
                            <td>{step["b"]}</td>
                            <td>{step["c"]}</td>
                            <td>{step["f_c"]}</td>
                        </tr>
                '''
        
        result_html += '''
                    </tbody>
                </table>
            </div>
        </div>
        '''
        
        return index() + result_html
        
    except Exception as e:
        return index() + f'<div class="card error"><h3>Error</h3><p>{str(e)}</p></div>'

if __name__ == '__main__':
    app.run(debug=True)
