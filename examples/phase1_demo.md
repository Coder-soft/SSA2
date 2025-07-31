---
title: PowerPython Phase 1 Enhancements Demo
css:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
js:
  - https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js
---

# PowerPython Phase 1 Enhancements Demo {#main-title .text-center .mt-5}

This document demonstrates the new features implemented in Phase 1 of the PowerPython enhancements.

## 1. Enhanced HTML Tag Support

Using the new `!html[]` syntax to embed raw HTML:

!html[<div class="alert alert-info">This is a Bootstrap alert created with the new HTML tag syntax!</div>]

!html[<button class="btn btn-primary" onclick="alert('Hello from embedded HTML!')">Click Me</button>]

## 2. JavaScript Execution Blocks

PowerPython now supports client-side JavaScript execution:

```js-power
console.log("Hello from PowerPython JavaScript!");
document.getElementById("js-output").innerHTML = "<p class='text-success'>JavaScript executed successfully!</p>";
```

<div id="js-output"></div>

## 3. Improved Attribute Syntax

The enhanced attribute syntax now supports key-value pairs:

### Standard ID and Class Attributes

This paragraph has custom attributes {#custom-paragraph .highlight .bg-light}

### Advanced Attribute Syntax

This div has data attributes and custom styles {#data-div .card .p-3 data-toggle="tooltip" data-title="This is a tooltip" style="border: 2px solid #007acc;"}

## Testing All Features Together

!html[<div class="card" id="combined-demo">]

This card demonstrates all Phase 1 features working together {#card-content .card-body}

```js-power
// JavaScript to enhance the card
document.addEventListener('DOMContentLoaded', function() {
  const card = document.getElementById('combined-demo');
  if (card) {
    card.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
    console.log('Card enhanced with JavaScript!');
  }
});
```

!html[</div>]

## Conclusion

The Phase 1 enhancements have successfully expanded PowerPython's capabilities with:

1. Enhanced HTML tag support via `!html[]` syntax
2. Client-side JavaScript execution via `js-power` code blocks
3. Improved attribute syntax supporting key-value pairs and quoted values

These features make PowerPython even more powerful for creating interactive documents.
