from flask import Flask, render_template, request, render_template_string
import logging
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Create a custom logger for the application messages
logger = logging.getLogger('CustomLogger')
logger.setLevel(logging.DEBUG)

# Create file handler for the custom logs
custom_handler = logging.FileHandler('custom_logs.log')
custom_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
custom_handler.setFormatter(formatter)

# Add the handler to the custom logger
logger.addHandler(custom_handler)

# Prevent the custom logger from propagating to the root logger
logger.propagate = False

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Log Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
        }
        .form-container {
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        select, input[type="text"] {
            margin: 10px 0;
            padding: 5px;
            width: 100%;  /* Keep original full width */
            box-sizing: border-box;  /* Ensures padding is included in width */
            display: block;  /* Forces consistent full-width behavior */
        }
        button {
            margin: 10px 0;
            padding: 5px;
            width: 100%;  /* Matches the inputs */
        }
        .success {
            color: green;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Log Generator</h2>
        <form method="POST">
            <select name="log_level">
                <option value="DEBUG">Debug</option>
                <option value="INFO">Info</option>
                <option value="WARNING">Warning</option>
                <option value="ERROR">Error</option>
                <option value="CRITICAL">Critical</option>
            </select>
            <input type="text" name="message" placeholder="Enter your log message" maxlength="100" required>
            <button type="submit">Generate Log</button>
        </form>
        {% if success %}
            <p class="success">Log entry created successfully!</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def log_generator():
    success = False
    if request.method == 'POST':
        # Get form data
        log_level = request.form['log_level']
        message = request.form['message']
        
        # Log the message based on selected level
        if log_level == 'DEBUG':
            logger.debug(message)
        elif log_level == 'INFO':
            logger.info(message)
        elif log_level == 'WARNING':
            logger.warning(message)
        elif log_level == 'ERROR':
            logger.error(message)
        elif log_level == 'CRITICAL':
            logger.critical(message)
            
        success = True
    
    return render_template_string(HTML_TEMPLATE, success=success)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)