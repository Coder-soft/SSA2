"""
Main compiler module for the Power Python Compiler.
Handles parsing markdown files with embedded Python code and rendering HTML output.
"""

import argparse
import sys
import os
import frontmatter
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from string import Template
import re


def execute_python_code(code):
    """Executes Python code and captures its output."""
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    try:
        with redirect_stdout(f):
            exec(code)
        return f.getvalue()
    except Exception as e:
        return f"Error executing Python code:\n<pre>{e}</pre>"


def process_enhanced_html_tags(content):
    """Process enhanced HTML tag syntax: !html[<div class="custom">Content</div>]"""
    # Pattern to match !html[content] where content can contain nested brackets
    pattern = r'!html\[((?:[^\[\]]|\[[^\[\]]*\])*)\]'
    
    def replace_html_tag(match):
        html_content = match.group(1)
        # Unescape any escaped brackets
        html_content = html_content.replace('\\[', '[').replace('\\]', ']')
        return html_content
    
    return re.sub(pattern, replace_html_tag, content)


def custom_fence_plugin(md):
    """A markdown-it-py plugin to handle custom code blocks."""

    # Store the original fence renderer
    _default_fence_renderer = md.renderer.rules.get("fence", lambda tokens, idx, options, env, self: self.renderToken(tokens, idx, options))

    def custom_fence_renderer(self, tokens, idx, options, env):
        token = tokens[idx]
        info = token.info.strip()

        if info == "python-power":
            code = token.content
            output = execute_python_code(code)
            return f'<div class="python-power-output">{output}</div>'
        
        elif info == "css-power":
            if "css_power_styles" not in env:
                env["css_power_styles"] = []
            env["css_power_styles"].append(token.content)
            return "" # Return an empty string to not render the block
        
        elif info == "js-power":
            # For JavaScript, we'll embed it in a script tag for client-side execution
            code = token.content
            return f'<script>{code}</script>'

        # Fallback to the default renderer for all other languages
        return _default_fence_renderer(tokens, idx, options, env, self)

    md.add_render_rule("fence", custom_fence_renderer)


def process_html_attributes(html_content):
    """Process custom attribute syntax in HTML content with enhanced support."""
    # Enhanced regex pattern to match more flexible attribute syntax
    # Supports: {#id .class1 .class2} or {#id} or {.class1 .class2} or {key=value key2="value"}
    attr_pattern = r'\{([^}]+)\}'
    
    def parse_attributes(attr_string):
        """Parse attribute string into id, classes, and other attributes."""
        attrs = {"id": "", "class": [], "other": {}}
        
        # Split by spaces but respect quoted strings
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(attr_string):
            char = attr_string[i]
            
            if char in ['"', "'"] and (i == 0 or attr_string[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                current_part += char
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
            i += 1
        
        if current_part:
            parts.append(current_part)
        
        # Process each part
        for part in parts:
            if part.startswith('#'):
                attrs["id"] = part[1:]
            elif part.startswith('.'):
                attrs["class"].append(part[1:])
            elif '=' in part:
                # Handle key=value pairs
                key, value = part.split('=', 1)
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"') and len(value) > 1:
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'") and len(value) > 1:
                    value = value[1:-1]
                attrs["other"][key] = value
            else:
                # Handle bare classes (without dot prefix)
                attrs["class"].append(part)
        
        return attrs
    
    def build_attributes_string(attrs_dict, existing_attrs=""):
        """Build attribute string from parsed attributes."""
        attr_str = existing_attrs
        
        # Add ID if present
        if attrs_dict["id"]:
            attr_str += f' id="{attrs_dict["id"]}"'
        
        # Add classes
        if attrs_dict["class"]:
            class_str = " ".join(attrs_dict["class"])
            # Check if a class attribute already exists
            if 'class="' in attr_str:
                # Append new classes
                attr_str = re.sub(r'class="([^"]*)"', rf'class="\1 {class_str}"', attr_str)
            else:
                attr_str += f' class="{class_str}"'
        
        # Add other attributes
        for key, value in attrs_dict["other"].items():
            attr_str += f' {key}="{value}"'
        
        return attr_str
    
    # First, handle paragraphs with embedded attribute blocks
    # Find all <p> tags that contain attribute blocks in their text
    for p_match in re.finditer(r'<p([^>]*)>(.*?)</p>', html_content, re.DOTALL):
        p_attrs = p_match.group(1)  # Attributes of the paragraph tag
        p_content = p_match.group(2)  # Content of the paragraph
        
        # Check if the paragraph content contains an attribute block
        attr_match = re.search(attr_pattern, p_content)
        if attr_match:
            attr_string = attr_match.group(1)
            attrs = parse_attributes(attr_string)
            
            # Construct new attributes for the paragraph tag
            new_attrs = build_attributes_string(attrs, p_attrs)
            
            # Remove the attribute block from the paragraph content
            clean_content = re.sub(attr_pattern, '', p_content)
            
            # Create the new paragraph tag
            new_p_tag = f"<p{new_attrs}>{clean_content}</p>"
            
            # Replace the old paragraph with the new one
            start, end = p_match.span()
            html_content = html_content[:start] + new_p_tag + html_content[end:]
    
    # Then, handle standalone attribute blocks (for headings, etc.)
    # Find all attribute blocks
    # Create a list to store all matches to process them in reverse order
    matches = list(re.finditer(attr_pattern, html_content))
    
    # Process matches in reverse order to avoid index shifting issues
    for match in reversed(matches):
        attr_string = match.group(1)
        attrs = parse_attributes(attr_string)
        
        # Find the last HTML tag before the attribute block
        preceding_html = html_content[:match.start()]
        
        # Find the tag immediately before the attribute block
        # Look for the last opening tag in the preceding HTML
        last_tag_match = None
        for tag_match in re.finditer(r'<([a-zA-Z0-9]+)([^>]*?)>', preceding_html):
            last_tag_match = tag_match
        
        if last_tag_match:
            # With our new regex, group(1) is the tag name and group(2) are the existing attributes
            tag_name = last_tag_match.group(1)
            existing_attrs = last_tag_match.group(2)
            
            # Construct the new attributes string
            new_attrs = build_attributes_string(attrs, existing_attrs)
            
            # Replace the old tag with the new one
            start, end = last_tag_match.span()
            new_tag = f"<{tag_name}{new_attrs}>"
            # Fix: Properly reconstruct the HTML with the new tag and content after the attribute block
            html_content = html_content[:start] + new_tag + html_content[end:match.start()] + html_content[match.end():]
    
    # Remove any remaining attribute blocks from the HTML
    html_content = re.sub(attr_pattern, '', html_content)
    
    return html_content


def compile_markdown(input_file, output_file=None):
    """Compile a markdown file to HTML."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        # Use absolute path for template
        template_path = os.path.join(os.path.dirname(__file__), "template.html")
        with open(template_path, "r", encoding="utf-8") as f:
            template_str = f.read()
            html_template = Template(template_str)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)

    md = MarkdownIt(
        options_update={
            "smartquotes": True
        }
    ).use(footnote_plugin).enable("table")
    md.use(custom_fence_plugin)

    # Process enhanced HTML tag syntax before markdown conversion
    processed_content = process_enhanced_html_tags(post.content)
    
    env = {}
    html_content = md.render(processed_content, env)
    
    # Process custom HTML attributes
    html_content = process_html_attributes(html_content)

    custom_styles = "\n".join(env.get("css_power_styles", []))
    
    css_links = "\n".join([f'<link rel="stylesheet" href="{css_file}">'
 for css_file in post.metadata.get("css", [])])
    js_links = "\n".join([f'<script src="{js_file}"></script>'
 for js_file in post.metadata.get("js", [])])

    final_html = html_template.substitute(
        title=post.metadata.get("title", "Rendered Page"),
        css_links=css_links,
        custom_styles=custom_styles,
        html_content=html_content,
        js_links=js_links
    )

    output_file = output_file or input_file.rsplit(".", 1)[0] + ".html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Successfully compiled {input_file} to {output_file}")


def main():
    """Main function to compile the markdown file."""
    parser = argparse.ArgumentParser(description="Compile a special Markdown file to HTML.")
    parser.add_argument("input_file", help="The path to the input Markdown file.")
    parser.add_argument("-o", "--output", dest="output_file", help="The path to the output HTML file.")
    args = parser.parse_args()

    compile_markdown(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
