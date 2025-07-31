# Power Python Compiler Developer Guide

## Project Structure

```
SSA2/
├── compiler/       # Core compilation engine
│   ├── __init__.py
│   ├── main.py     # Main compiler module
│   └── template.html # HTML template
├── ide/           # Web-based IDE
│   ├── __init__.py
│   ├── app.py      # Flask application
│   ├── static/     # Static files (CSS, JS)
│   └── templates/  # HTML templates
├── examples/      # Sample files
├── docs/          # Documentation
├── tests/         # Unit tests
├── requirements.txt # Python dependencies
├── README.md      # Project overview
└── gemini.md      # Project plan
```

## Architecture

### Compiler

The compiler consists of several components:

1. **Markdown Parser**: Uses `markdown-it-py` to parse markdown syntax
2. **Custom Plugins**: Extensions for handling Python code blocks and CSS
3. **HTML Renderer**: Uses templates to generate the final HTML output
4. **Frontmatter Processor**: Handles YAML frontmatter metadata

### IDE

The IDE is built with Flask and provides:

1. **Web Interface**: CodeMirror editor for markdown editing
2. **Real-time Preview**: Live rendering of compiled output
3. **File Management**: Save and load documents

## Code Organization

### Compiler Module

- `main.py`: Entry point with argument parsing and main compilation logic
- `template.html`: HTML template for output

Key functions:
- `compile_markdown()`: Main compilation function
- `execute_python_code()`: Safely executes Python code
- `process_html_attributes()`: Handles custom HTML attributes

### IDE Module

- `app.py`: Flask application with routes
- `templates/`: HTML templates for the web interface
- `static/`: CSS and JavaScript files

Key routes:
- `/`: Main IDE interface
- `/compile`: Compiles markdown content
- `/save`: Saves documents

## Testing

Tests are written using Python's `unittest` framework and are located in the `tests/` directory.

To run tests:

```bash
python -m unittest tests/test_compiler.py -v
```

## Contributing

### Code Style

- Follow PEP 8 guidelines for Python code
- Use descriptive variable and function names
- Include docstrings for all functions and classes
- Write unit tests for new functionality

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Implement your feature
4. Write tests
5. Update documentation
6. Submit a pull request

### Extending Markdown Syntax

To add new markdown extensions:

1. Create a new plugin function similar to `custom_fence_plugin`
2. Register it with the markdown parser
3. Add corresponding template support if needed

## Dependencies

- **Flask**: Web framework for the IDE
- **markdown-it-py**: Markdown parser
- **mdit-py-plugins**: Extensions for markdown-it-py
- **pygments**: Syntax highlighting
- **python-frontmatter**: Frontmatter parsing
- **watchdog**: File system monitoring

## Release Process

1. Update version number in `setup.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Publish to PyPI

## Future Enhancements

- Plugin system for custom extensions
- Collaboration features
- Version control integration
- Mobile-responsive design
- Dark mode support
