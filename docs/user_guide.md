# Power Python Compiler User Guide

## Introduction

The Power Python Compiler is a tool that allows you to write markdown documents with embedded Python code that gets executed and rendered into rich HTML pages. This guide will help you get started with using the compiler and IDE.

## Installation

1. Clone the repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Basic Usage

### Command Line Compiler

To compile a markdown file to HTML, use the following command:

```bash
python compiler/main.py input.md -o output.html
```

If you don't specify an output file, the compiler will create a file with the same name as the input file but with an `.html` extension.

### Web IDE

To start the web-based IDE, run:

```bash
python ide/app.py
```

Then open your browser to `http://localhost:5000`

## Markdown Syntax

The Power Python Compiler supports standard markdown syntax with some extensions.

### Standard Markdown

- Headers: `# Heading 1`, `## Heading 2`, etc.
- Emphasis: `*italic*`, `**bold**`
- Lists: `- item 1`, `1. numbered item`
- Links: `[link text](url)`
- Images: `![alt text](image-url)`
- Code blocks: ```code```

### Python Code Execution

You can embed Python code that will be executed and its output included in the HTML:

```markdown
```python-power
print("Hello, World!")
for i in range(3):
    print(f"Number: {i}")
```
```

### Custom CSS

You can add custom CSS styles that will be included in the output:

```markdown
```css-power
.python-power-output {
    background-color: #f0f0f0;
    padding: 10px;
}
```
```

### HTML Attributes

You can add custom IDs and classes to HTML elements using the `{#id .class}` syntax:

```markdown
## This is a heading {#main-title .blue-text}

Paragraph with custom class {.highlight}
```

## Frontmatter

You can include metadata at the beginning of your markdown file using YAML frontmatter:

```markdown
---
title: My Document
css:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
js:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
---

# Document Content
```

## Examples

Check the `examples/` directory for sample files that demonstrate the various features of the Power Python Compiler.

## Troubleshooting

### Common Issues

1. **Python code not executing**: Make sure you're using the `python-power` language identifier in your code blocks.
2. **CSS not applied**: Ensure your CSS code blocks use the `css-power` language identifier.
3. **HTML attributes not working**: Check that you're using the correct syntax `{#id .class}`.

### Getting Help

If you encounter any issues, please check the GitHub issues or contact the development team.
