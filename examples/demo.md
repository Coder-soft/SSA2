---
title: Power Python Demo Document
css:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
js:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
---

# Power Python Compiler Demo {#main-title .text-center .mt-5}

Welcome to the Power Python Compiler demo! This document showcases the capabilities of our markdown compiler.

## Features

1. **Standard Markdown**: _Italic_, **Bold**, `code`, [links](https://example.com)
2. **Python Code Execution**: Run Python code directly in your document
3. **Custom CSS**: Style your document with embedded CSS
4. **HTML Attributes**: Add IDs and classes to elements

## Python Code Execution

Here's a simple Python code block that will be executed:

```python-power
print("Hello from Python!")
print(f"Current working directory: {os.getcwd()}")

# Let's do some calculations
result = 2 + 2
print(f"2 + 2 = {result}")

# And a loop
for i in range(3):
    print(f"Iteration {i}")
```

## Custom CSS

We can also add custom CSS styles:

```css-power
#main-title {
    color: #007acc;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.python-power-output {
    background-color: #f8f9fa;
    border-left: 4px solid #007acc;
    padding: 15px;
    margin: 15px 0;
    border-radius: 0 4px 4px 0;
}

.feature-list {
    background-color: #e9ecef;
    padding: 20px;
    border-radius: 5px;
}
```

## HTML Attributes

We can add custom attributes to elements:

### This heading has an ID and classes {#feature-heading .feature-list .mb-3}

Paragraph with custom styling {.feature-list}

## Table Example

| Feature | Description |
|---------|-------------|
| Markdown | Standard markdown syntax |
| Python | Execute Python code |
| CSS | Custom styling |
| HTML | Full HTML support |

## Conclusion {#conclusion .text-center .mt-5}

The Power Python Compiler provides a powerful way to create interactive documents with embedded Python code execution.

Try creating your own documents with Python code blocks!
