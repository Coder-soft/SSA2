# Power Python Compiler & IDE

An advanced development environment that combines markdown processing with Python code execution capabilities.

## Overview

The Power Python Compiler & IDE allows users to write markdown documents with embedded Python code that gets executed and rendered into rich HTML pages. This tool provides a unique way to create interactive documentation, tutorials, and web pages with live Python code execution.

## Features

- Markdown with custom rules support
- Embedded Python code execution (`python-power` blocks)
- Custom CSS styling (`css-power` blocks)
- HTML attribute syntax (IDs and classes)
- Frontmatter metadata support
- Full HTML tag support
- Web-based IDE interface
- Desktop IDE with syntax highlighting
- Real-time preview
- Export capabilities

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Compiler

```bash
python compiler/main.py input.md -o output.html
```

### Web IDE

```bash
python ide/app.py
```

Then open your browser to `http://localhost:5000`

### Desktop IDE

```bash
python ide/desktop_ide.py
```

## Project Structure

```
SSA2/
├── compiler/       # Core compilation engine
├── ide/           # Web-based IDE and Desktop IDE
├── examples/      # Sample files
├── docs/          # Documentation
└── tests/         # Unit tests
```

## Documentation

- [User Guide](docs/user_guide.md) - Instructions for using the Power Python Compiler
- [Developer Guide](docs/developer_guide.md) - Technical details for developers
- [Contributing Guide](docs/contributing.md) - Guidelines for contributing to the project
- [Changelog](docs/changelog.md) - Version history and changes
- [IDE Features](IDE_FEATURES.md) - Detailed overview of IDE capabilities
- [IDE README](README_IDE.md) - Quick start guide for the IDE
- [PowerPython Syntax Guide](docs/powerpython_syntax.md) - Detailed documentation of PowerPython custom syntaxes (NEW)

## Contributing

Contributions are welcome! Please read [contributing.md](docs/contributing.md) for guidelines.

## License

MIT License
