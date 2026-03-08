from flask import Flask, render_template_string
import webbrowser
import threading
import time
import os

app = Flask(__name__)

# Stunning Glassmorphic Scientific Calculator HTML/CSS/JS
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scientific Calculator</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent-purple: #9d50bb;
            --accent-blue: #6e48aa;
            --text-main: #ffffff;
            --text-dim: rgba(255, 255, 255, 0.6);
            --key-num: #2a2a40;
            --key-op: #3a3a55;
            --key-equal: linear-gradient(90deg, #9d50bb, #6e48aa);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: var(--bg-gradient);
            background-attachment: fixed;
            overflow: hidden;
        }

        .background-blobs {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            filter: blur(80px);
        }

        .blob {
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            opacity: 0.4;
            animation: move 20s infinite alternate;
        }

        .blob-1 { background: #9d50bb; top: 10%; left: 10%; }
        .blob-2 { background: #6e48aa; bottom: 10%; right: 10%; animation-delay: -5s; }

        @keyframes move {
            from { transform: translate(0, 0); }
            to { transform: translate(100px, 100px); }
        }

        .calculator-container {
            width: 100%;
            max-width: 420px;
            padding: 25px;
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--glass-border);
            border-radius: 30px;
            box-shadow: 0 25px 45px rgba(0,0,0,0.5);
            position: relative;
            z-index: 10;
        }

        .header {
            margin-bottom: 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 1.2rem;
            color: var(--text-dim);
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 300;
        }

        .display-area {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 25px;
            min-height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: flex-end;
            border: 1px solid rgba(255,255,255,0.05);
        }

        #history {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--text-dim);
            word-break: break-all;
            text-align: right;
            height: 20px;
        }

        #current-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.5rem;
            color: var(--text-main);
            width: 100%;
            text-align: right;
            overflow-x: auto;
            white-space: nowrap;
        }

        .keypad {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        button {
            height: 60px;
            border-radius: 18px;
            border: none;
            outline: none;
            background: var(--key-num);
            color: var(--text-main);
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }

        button:active {
            transform: scale(0.95);
        }

        button:hover {
            background: rgba(255, 255, 255, 0.15);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        button.op {
            background: var(--key-op);
            color: #bfa0ff;
            font-weight: 600;
        }

        button.sci {
            font-size: 0.85rem;
            background: rgba(255, 255, 255, 0.03);
            color: #8ab4f8;
        }

        button.clear {
            color: #ff6b6b;
        }

        button.equal {
            background: var(--key-equal);
            grid-column: span 2;
            width: 100%;
            font-weight: 700;
        }

        .history-panel {
            margin-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 15px;
            max-height: 100px;
            overflow-y: auto;
        }

        .history-item {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 5px;
            text-align: right;
            cursor: pointer;
        }

        .history-item:hover {
            color: var(--text-main);
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--glass-border);
            border-radius: 10px;
        }

        .mode-toggle {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
            gap: 10px;
        }

        .badge {
            font-size: 0.6rem;
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--accent-blue);
            color: white;
            vertical-align: middle;
            margin-left: 5px;
        }
        
    </style>
</head>
<body>
    <div class="background-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
    </div>

    <div class="calculator-container">
        <div class="header">
            <h1>CALCULATOR</h1>
        </div>

        <div class="display-area">
            <div id="history"></div>
            <div id="current-value">0</div>
        </div>

        <div class="keypad">
            <!-- Row 1: Sci Functions -->
            <button class="sci" onclick="appendFunc('sin(')">sin</button>
            <button class="sci" onclick="appendFunc('cos(')">cos</button>
            <button class="sci" onclick="appendFunc('tan(')">tan</button>
            <button class="sci" onclick="appendFunc('log(')">log</button>

            <!-- Row 2 -->
            <button class="clear" onclick="clearDisplay()">AC</button>
            <button class="op" onclick="deleteLast()">DEL</button>
            <button class="op" onclick="appendValue('%')">%</button>
            <button class="op" onclick="appendValue('/')">÷</button>

            <!-- Row 3 -->
            <button onclick="appendValue('7')">7</button>
            <button onclick="appendValue('8')">8</button>
            <button onclick="appendValue('9')">9</button>
            <button class="op" onclick="appendValue('*')">×</button>

            <!-- Row 4 -->
            <button onclick="appendValue('4')">4</button>
            <button onclick="appendValue('5') =">5</button>
            <button onclick="appendValue('6')">6</button>
            <button class="op" onclick="appendValue('-')">−</button>

            <!-- Row 5 -->
            <button onclick="appendValue('1')">1</button>
            <button onclick="appendValue('2')">2</button>
            <button onclick="appendValue('3')">3</button>
            <button class="op" onclick="appendValue('+')">+</button>

            <!-- Row 6 -->
            <button onclick="appendValue('e')">e</button>
            <button onclick="appendValue('0')">0</button>
            <button onclick="appendValue('.')">.</button>
            <button class="sci" onclick="appendValue('**')">xʸ</button>

            <!-- Row 7 -->
            <button class="sci" onclick="appendValue('Math.PI')">π</button>
            <button class="sci" onclick="appendFunc('Math.sqrt(')">√</button>
            <button class="equal" onclick="calculate()">=</button>
        </div>

        <div class="history-panel" id="history-log">
            <!-- History items go here -->
        </div>
    </div>

    <script>
        let currentExpression = "";
        let history = [];
        const display = document.getElementById('current-value');
        const historyDisplay = document.getElementById('history');
        const logPanel = document.getElementById('history-log');

        function appendValue(val) {
            if (currentExpression === "0" && val !== ".") {
                currentExpression = val;
            } else {
                currentExpression += val;
            }
            updateDisplay();
        }

        function appendFunc(func) {
            currentExpression += func;
            updateDisplay();
        }

        function clearDisplay() {
            currentExpression = "";
            historyDisplay.innerText = "";
            updateDisplay();
        }

        function deleteLast() {
            currentExpression = currentExpression.toString().slice(0, -1);
            updateDisplay();
        }

        function updateDisplay() {
            display.innerText = currentExpression || "0";
            // Auto scroll to right
            display.scrollLeft = display.scrollWidth;
        }

        function calculate() {
            try {
                let expr = currentExpression;
                
                // Replace constants and functions for JS eval
                // (Though some are already Math.something)
                const safeExpr = expr
                    .replace(/sin\(/g, 'Math.sin(Math.PI/180*')
                    .replace(/cos\(/g, 'Math.cos(Math.PI/180*')
                    .replace(/tan\(/g, 'Math.tan(Math.PI/180*')
                    .replace(/log\(/g, 'Math.log10(')
                    .replace(/e/g, 'Math.E');

                const result = eval(safeExpr);
                
                if (result !== undefined) {
                    const formattedResult = Number.isInteger(result) ? result : result.toFixed(6);
                    historyDisplay.innerText = currentExpression + " =";
                    
                    // Add to log
                    addToHistory(currentExpression + " = " + formattedResult);
                    
                    currentExpression = formattedResult.toString();
                    updateDisplay();
                }
            } catch (e) {
                display.innerText = "Error";
                setTimeout(() => {
                    updateDisplay();
                }, 1000);
            }
        }

        function addToHistory(item) {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerText = item;
            div.onclick = () => {
                currentExpression = item.split("=")[1].trim();
                updateDisplay();
            };
            logPanel.prepend(div);
            if (logPanel.children.length > 5) {
                logPanel.removeChild(logPanel.lastChild);
            }
        }

        // Support Keyboard Input
        document.addEventListener('keydown', (e) => {
            if (e.key >= '0' && e.key <= '9') appendValue(e.key);
            if (e.key === '+') appendValue('+');
            if (e.key === '-') appendValue('-');
            if (e.key === '*') appendValue('*');
            if (e.key === '/') appendValue('/');
            if (e.key === '.') appendValue('.');
            if (e.key === 'Enter' || e.key === '=') calculate();
            if (e.key === 'Backspace') deleteLast();
            if (e.key === 'Escape') clearDisplay();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

def run_server():
    # Use port 5000 by default, or find another if busy
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("Launching Scientific Calculator...")
    
    # Start Flask in a separate thread so we can open the browser
    threading.Thread(target=run_server, daemon=True).start()
    
    # Wait a bit for server to start
    time.sleep(1.5)
    
    url = "http://127.0.0.1:5000"
    print(f"Calculator is running at: {url}")
    print("Opening your browser now...")
    
    webbrowser.open(url)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCalculator server stopped.")
