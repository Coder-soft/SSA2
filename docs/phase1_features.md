# PowerPython Phase 1 Features

This document describes the new features implemented in Phase 1 of the PowerPython enhancements.

## 1. Enhanced HTML Tag Support

PowerPython now supports a new syntax for embedding raw HTML directly in your markdown documents.

### Syntax

```
!html[<your-html-content-here>]
```

### Examples

```
!html[<div class="alert alert-info">This is a Bootstrap alert!</div>]

!html[<button class="btn btn-primary" onclick="alert('Hello!')">Click Me</button>]
```

### Notes

- The HTML content inside the brackets is rendered directly as HTML
- You can include JavaScript event handlers and complex HTML structures
- This syntax is processed before Markdown conversion, so it works anywhere in your document

## 2. JavaScript Execution Blocks

PowerPython now supports client-side JavaScript execution in addition to Python code execution.

### Syntax

```markdown
```js-power
// Your JavaScript code here
console.log("Hello from PowerPython!");
```
```

### Examples

```js-power
console.log("This will appear in the browser console");
document.getElementById("output").innerHTML = "<p>Content dynamically added!</p>";
```

### Notes

- JavaScript code is embedded directly in the output HTML within `<script>` tags
- This allows for client-side interactivity in your documents
- JavaScript executes in the browser when the page loads

## 3. Improved Attribute Syntax

The attribute syntax has been enhanced to support more flexible attribute definitions.

### Standard Syntax (still supported)

```
# Heading {#my-id .my-class}

Paragraph text {.my-class}
```

### Enhanced Syntax

The new syntax supports:

1. **Key-Value Pairs**
   ```
   Element {data-toggle="tooltip" data-title="Tooltip text"}
   ```

2. **Quoted Values**
   ```
   Element {style="color: red; font-weight: bold;"}
   ```

3. **Bare Classes** (without dot prefix)
   ```
   Element {highlight important}
   ```

### Examples

```
This div has data attributes {#data-div .card data-toggle="tooltip" data-title="This is a tooltip"}

This paragraph has custom styles {.p-3 style="border: 2px solid #007acc;"}

This element has multiple classes {primary-element highlight bg-light}
```

### Notes

- All existing attribute syntax continues to work
- New syntax provides more flexibility for complex attribute definitions
- Quoted values properly handle spaces and special characters
- Bare classes (without dots) are automatically treated as classes

## Testing the Features

A demo file `examples/phase1_demo.md` has been created to showcase all these features working together.

To test:

1. Compile the demo: `python compiler/main.py examples/phase1_demo.md -o examples/phase1_demo.html`
2. Open the HTML file in a browser to see the features in action

## Implementation Details

- Enhanced HTML tag processing happens before Markdown conversion
- JavaScript blocks are rendered as `<script>` tags in the output
- Attribute parsing now supports a more flexible grammar for attribute definitions
- All features maintain backward compatibility with existing documents
