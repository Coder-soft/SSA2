# PowerPython Syntax Guide

PowerPython extends standard Markdown with custom syntax features that enable enhanced document creation with executable code, custom styling, and flexible HTML attributes.

## Table of Contents

1. [Python Code Execution](#python-code-execution)
2. [Custom CSS Styling](#custom-css-styling)
3. [HTML Attributes](#html-attributes)
4. [Frontmatter Metadata](#frontmatter-metadata)
5. [Supported File Extensions](#supported-file-extensions)

## Python Code Execution

PowerPython allows you to embed executable Python code directly in your Markdown documents using special code blocks. When compiled, this code is executed and its output is included in the generated HTML.

### Syntax

To embed Python code, use a fenced code block with the language identifier `python-power`:

````markdown
```python-power
# Your Python code here
print("Hello, World!")
```
````

### How It Works

1. The PowerPython compiler identifies code blocks with the `python-power` language identifier
2. The code inside these blocks is executed in a secure environment
3. The output (stdout) of the code is captured
4. The output is wrapped in a `<div>` with the class `python-power-output`
5. This div is inserted into the HTML at the location of the code block

### Example

````markdown
```python-power
import datetime

current_time = datetime.datetime.now()
print(f"Current time: {current_time}")

# Simple calculations
result = 5 * 7
print(f"5 times 7 equals {result}")
```
````

This will output:

```html
<div class="python-power-output">Current time: 2023-05-15 14:30:22.123456
5 times 7 equals 35
</div>
```

### Use Cases

- Creating dynamic documentation with live code examples
- Generating reports with calculated data
- Building interactive tutorials
- Demonstrating code concepts with executable examples

## Custom CSS Styling

PowerPython supports embedding custom CSS styles directly in your Markdown documents. These styles are applied to the generated HTML output.

### Syntax

To embed CSS, use a fenced code block with the language identifier `css-power`:

````markdown
```css-power
/* Your CSS styles here */
.python-power-output {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
}
```
````

### How It Works

1. The PowerPython compiler identifies code blocks with the `css-power` language identifier
2. The CSS code is collected during compilation
3. All collected CSS is combined into a single `<style>` block
4. This style block is inserted into the `<head>` section of the HTML document

### Example

````markdown
```css-power
.main-title {
    color: #007acc;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.python-power-output {
    background-color: #e9ecef;
    border-left: 4px solid #007acc;
    padding: 15px;
    margin: 15px 0;
}
```
````

### Use Cases

- Customizing the appearance of code output
- Styling specific elements with classes or IDs
- Creating consistent visual themes
- Adding responsive design features

## HTML Attributes

PowerPython provides a convenient syntax for adding IDs and classes to HTML elements directly in Markdown.

### Syntax

Add attributes to any Markdown element by appending them in curly braces `{}`:

```markdown
## Heading with ID and Classes {#main-title .highlight .large}

Paragraph with class {.feature-list}
```

- Use `#` prefix for IDs
- Use `.` prefix for classes
- Separate multiple attributes with spaces
- Place the attribute block immediately after the element it modifies

### How It Works

1. The PowerPython compiler parses the Markdown into HTML
2. It scans the generated HTML for attribute blocks
3. It identifies the preceding HTML element
4. It adds the specified IDs and classes to that element
5. It removes the attribute block from the final output

### Example

```markdown
## My Important Heading {#main-title .text-center .mt-5}

This is a paragraph with custom styling {.feature-list .p-3}
```

This generates:

```html
<h2 id="main-title" class="text-center mt-5">My Important Heading</h2>

<p class="feature-list p-3">This is a paragraph with custom styling</p>
```

### Use Cases

- Creating anchor links to specific sections
- Applying CSS classes for styling
- Integrating with CSS frameworks like Bootstrap
- Making documents more accessible with proper IDs

## Frontmatter Metadata

PowerPython supports YAML frontmatter for document metadata, similar to static site generators.

### Syntax

Place YAML frontmatter at the very beginning of your document, enclosed in `---`:

```markdown
---
title: My Document Title
css:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
js:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
---

# Document Content
```

### Supported Fields

- `title`: Sets the document title in the HTML `<title>` tag
- `css`: List of external CSS files to include
- `js`: List of external JavaScript files to include

### How It Works

1. The compiler parses the YAML frontmatter at the beginning of the document
2. It extracts the metadata fields
3. It uses the title in the HTML `<title>` tag
4. It generates `<link>` tags for CSS files
5. It generates `<script>` tags for JavaScript files
6. The frontmatter is removed from the document content

### Example

```markdown
---
title: PowerPython Demo
css:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
js:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
---

# My Demo Document

Content here...
```

This generates HTML with:

```html
<head>
    <title>PowerPython Demo</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <!-- Other head content -->
</head>
<body>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Body content -->
</body>
```

## Supported File Extensions

The PowerPython IDE recognizes several file extensions for syntax highlighting:

| Extension | Language |
|-----------|----------|
| `.py` | Python |
| `.pyp` | PowerPython |
| `.powerpy` | PowerPython |
| `.md` | Markdown |
| `.markdown` | Markdown |
| `.html` | HTML |
| `.htm` | HTML |
| `.css` | CSS |
| `.js` | JavaScript |

The PowerPython Desktop IDE has special support for `.pyp` and `.powerpy` files, providing enhanced syntax highlighting for PowerPython-specific features.

## IDE Support

The PowerPython ecosystem includes both a web-based IDE and a desktop IDE:

### Web IDE

- Real-time preview of compiled output
- Syntax highlighting for multiple languages
- File management capabilities
- Accessible via web browser

### Desktop IDE

- Multi-document interface with tabbed editing
- Advanced syntax highlighting including PowerPython-specific features
- File explorer panel
- Search and replace functionality
- Custom lexer for PowerPython syntax
- Support for `.pyp` and `.powerpy` file extensions

Both IDEs support all PowerPython syntax features and provide a seamless experience for creating and editing PowerPython documents.
