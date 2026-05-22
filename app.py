from flask import Flask, request, render_template_string
import math

app = Flask(__name__)

def regula_falsi(f, a, b, tol=1e-6, max_iter=100):
    """Regula Falsi Method Implementation"""
    steps = []
    
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        return None, 0, [{"error": f"f({a}) and f({b}) must have opposite signs"}]
    
    for i in range(max_iter):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        
        steps.append({
            "iteration": i + 1,
            "a": round(a, 6),
            "b": round(b, 6),
            "c": round(c, 6),
            "f_a": round(fa, 6),
            "f_b": round(fb, 6),
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

# Define functions
def f1(x): return x**3 - x - 2
def f2(x): return x**2 - 4
def f3(x): return math.cos(x) - x
def f4(x): return math.exp(-x) - x
def f5(x): return x**3 - 2*x - 5

FUNCTIONS = {
    "x³ - x - 2": f1,
    "x² - 4": f2,
    "cos(x) - x": f3,
    "e^(-x) - x": f4,
    "x³ - 2x - 5": f5
}

# HTML Template as a string (so no template files needed)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Regula Falsi Method - Root Finder</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { color: #667eea; margin-bottom: 10px; }
        h2 { color: #764ba2; border-left: 4px solid #764ba2; padding-left: 15px; margin-top: 0; }
        h3 { color: #555; margin-top: 20px; }
        .math {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-size: 18px;
        }
        .example {
            background: #e8f4f8;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            max-width: 300px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: scale(1.05); }
        .result {
            background: #d4edda;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            overflow-x: auto;
            display: block;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:nth-child(even) { background: #f9f9f9; }
        @media (max-width: 768px) {
            body { padding: 10px; }
            .card { padding: 15px; }
            th, td { padding: 5px; font-size: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📐 Regula Falsi (False Position) Method</h1>
            <p>A root-finding algorithm that combines the bisection and secant methods for solving equations of the form f(x) = 0.</p>
        </div>

        <div class="card">
            <h2>📖 Mathematical Discussion</h2>
            <div class="math">
                <p><strong>Formula:</strong></p>
                \[
                c = \frac{a \cdot f(b) - b \cdot f(a)}{f(b) - f(a)}
                \]
                <p><strong>Algorithm:</strong></p>
                <ol>
                    <li>Find a and b such that f(a) and f(b) have opposite signs</li>
                    <li>Calculate c using the formula above</li>
                    <li>If |f(c)| &lt; tolerance, c is the root</li>
                    <li>If f(a) · f(c) &lt; 0, set b = c, else set a = c</li>
                    <li>Repeat steps 2-4 until convergence</li>
                </ol>
                <p><strong>Convergence:</strong> Linear, but faster than bisection for many functions.</p>
            </div>
        </div>

        <div class="card">
            <h2>📝 Worked Example 1: x³ - x - 2 = 0</h2>
            <div class="example">
                <p><strong>Step 1:</strong> Find interval [a,b] with sign change.</p>
                <p>f(1) = 1³ - 1 - 2 = <strong>-2</strong> (negative)</p>
                <p>f(2) = 8 - 2 - 2 = <strong>4</strong> (positive)</p>
                <p>✓ Root lies in [1, 2]</p>
                
                <p><strong>Step 2:</strong> Apply Regula Falsi formula:</p>
                <p>c = (1 × 4 - 2 × (-2)) / (4 - (-2)) = (4 + 4) / 6 = 8/6 = <strong>1.3333</strong></p>
                
                <p><strong>Step 3:</strong> f(1.3333) = (1.3333)³ - 1.3333 - 2 = 2.370 - 1.3333 - 2 = <strong>-0.9633</strong></p>
                
                <p><strong>Step 4:</strong> New interval: [1.3333, 2] (signs: - and +)</p>
                
                <p><strong>Step 5:</strong> Continue iterations...</p>
                <p><strong>Final Result:</strong> After 10 iterations, root ≈ <strong>1.52138</strong></p>
                <p>✓ f(1.52138) ≈ 0</p>
            </div>
        </div>

        <div class="card">
            <h2>📝 Worked Example 2: x² - 4 = 0</h2>
            <div class="example">
                <p><strong>Step 1:</strong> Try interval [1, 3]</p>
                <p>f(1) = 1 - 4 = <strong>-3</strong> (negative)</p>
                <p>f(3) = 9 - 4 = <strong>5</strong> (positive)</p>
                <p>✓ Root lies in [1, 3]</p>
                
                <p><strong>Step 2:</strong> First iteration:</p>
                <p>c = (1 × 5 - 3 × (-3)) / (5 - (-3)) = (5 + 9) / 8 = 14/8 = <strong>1.75</strong></p>
                <p>f(1.75) = 3.0625 - 4 = <strong>-0.9375</strong></p>
                
                <p><strong>Step 3:</strong> Second iteration using [1.75, 3]:</p>
                <p>c = (1.75 × 5 - 3 × (-0.9375)) / (5 - (-0.9375)) = (8.75 + 2.8125) / 5.9375 = 11.5625/5.9375 = <strong>1.9474</strong></p>
                <p>f(1.9474) = 3.792 - 4 = <strong>-0.208</strong></p>
                
                <p><strong>Step 4:</strong> After 6 iterations:</p>
                <p><strong>Final Root:</strong> x = <strong>2.0000</strong></p>
                <p>✓ f(2) = 0 exactly</p>
            </div>
        </div>

        <div class="card">
            <h2>🧮 Interactive Calculator</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Select Function:</label>
                    <select name="function" required>
                        {% for func in functions %}
                        <option value="{{ func }}">{{ func }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Lower bound (a):</label>
                    <input type="number" name="a" step="any" required placeholder="e.g., 1">
                    <small>f(a) should be negative or positive</small>
                </div>
                
                <div class="form-group">
                    <label>Upper bound (b):</label>
                    <input type="number" name="b" step="any" required placeholder="e.g., 2">
                    <small>f(b) should have opposite sign from f(a)</small>
                </div>
                
                <div class="form-group">
                    <label>Tolerance:</label>
                    <input type="number" name="tolerance" step="any" value="0.000001" placeholder="1e-6">
                    <small>Smaller = more accurate but more iterations</small>
                </div>
                
                <button type="submit">🔍 Find Root</button>
            </form>
            
            {% if error %}
            <div class="error">
                <h3>⚠️ Error</h3>
                <p>{{ error }}</p>
                <small>Tip: Choose a and b where f(a) and f(b) have opposite signs!</small>
            </div>
            {% endif %}
            
            {% if result %}
            <div class="result">
                <h3>✅ Root Found!</h3>
                <p><strong>Root:</strong> x = {{ result }}</p>
                <p><strong>Iterations:</strong> {{ iterations }}</p>
            </div>
            {% endif %}
            
            {% if steps %}
            <h3>📊 Detailed Iterations:</h3>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Iter</th>
                            <th>a</th>
                            <th>b</th>
                            <th>c</th>
                            <th>f(a)</th>
                            <th>f(b)</th>
                            <th>f(c)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for step in steps %}
                        <tr>
                            <td>{{ step.iteration }}</td>
                            <td>{{ step.a }}</td>
                            <td>{{ step.b }}</td>
                            <td>{{ step.c }}</td>
                            <td>{{ step.f_a }}</td>
                            <td>{{ step.f_b }}</td>
                            <td>{{ step.f_c }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

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
                    error = steps_data[0].get('error', 'Invalid interval')
            else:
                error = "Please select a valid function"
                
        except ValueError:
            error = "Please enter valid numbers for a, b, and tolerance"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    
    return render_template_string(
        HTML_TEMPLATE,
        result=result,
        iterations=iterations,
        steps=steps,
        error=error,
        functions=FUNCTIONS.keys()
    )

# This is required for Vercel
app.debug = False
