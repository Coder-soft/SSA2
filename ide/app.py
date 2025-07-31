"""
Main Flask application for the Power Python IDE.
Provides a web-based interface for editing and compiling markdown files.
"""

import os
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'md', 'markdown'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main IDE interface."""
    return render_template('index.html')


@app.route('/compile', methods=['POST'])
def compile_file():
    """Compile a markdown file and return the HTML output."""
    try:
        # Get the markdown content from the request
        markdown_content = request.json.get('content', '')
        
        # Save to a temporary file
        temp_md_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.md')
        with open(temp_md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Compile the markdown file
        # Note: In a full implementation, you would import and use the compiler functions directly
        # For now, we'll simulate the output
        html_output = f"<h1>Compiled Output</h1><p>{markdown_content[:100]}...</p>"
        
        return jsonify({'success': True, 'html': html_output})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/save', methods=['POST'])
def save_file():
    """Save markdown content to a file."""
    try:
        filename = request.json.get('filename', 'document.md')
        content = request.json.get('content', '')
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return jsonify({'success': True, 'message': f'File saved as {filename}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/examples/<path:filename>')
def serve_example(filename):
    """Serve example files."""
    return send_from_directory('../examples', filename)


if __name__ == '__main__':
    # Disable reloader on Windows to avoid threading issues
    import os
    if os.name == 'nt':  # Windows
        app.run(debug=True, use_reloader=False)
    else:
        app.run(debug=True)
