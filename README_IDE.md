# Power Python IDE

A feature-rich desktop IDE built with Python's Tkinter and Pygments libraries.

## Features

- Multi-document interface with tabbed editing
- Syntax highlighting for Python, JavaScript, HTML, CSS, and Markdown
- Custom Power Python syntax support
- Line numbers
- Auto-indentation
- Search and replace functionality
- File explorer
- Keyboard shortcuts

## Installation

1. Make sure you have Python 3.6 or higher installed
2. Install the required dependencies:

```bash
python install_deps.py
```

Or manually install dependencies:

```bash
pip install -r requirements.txt
```

## Running the IDE

```bash
python ide/desktop_ide.py
```

## Usage

- **File Menu**: New, Open, Save, Save As
- **Edit Menu**: Undo, Redo, Cut, Copy, Paste, Find, Find and Replace
- **Keyboard Shortcuts**:
  - `Ctrl+N`: New file
  - `Ctrl+O`: Open file
  - `Ctrl+S`: Save file
  - `Ctrl+F`: Find text
  - `F5`: Compile (placeholder)

## Supported File Types

- `.py` - Python
- `.js` - JavaScript
- `.html`/`.htm` - HTML
- `.css` - CSS
- `.md`/`.markdown` - Markdown
- `.pyp`/`.powerpy` - Power Python

## Troubleshooting

If you encounter import errors, make sure all dependencies are installed:

```bash
pip install pygments
```
