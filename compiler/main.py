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

        # Fallback to the default renderer for all other languages
        return _default_fence_renderer(tokens, idx, options, env, self)

    md.add_render_rule("fence", custom_fence_renderer)


def process_html_attributes(html_content):
    """Process custom attribute syntax in HTML content."""
    # First, handle paragraphs with embedded attribute blocks
    # Find all <p> tags that contain attribute blocks in their text
    for p_match in re.finditer(r'<p([^>]*)>(.*?)</p>', html_content, re.DOTALL):
        p_attrs = p_match.group(1)  # Attributes of the paragraph tag
        p_content = p_match.group(2)  # Content of the paragraph
        
        # Check if the paragraph content contains an attribute block
        attr_match = re.search(r'\{([#.])(.+?)\}', p_content)
        if attr_match:
            prefix = attr_match.group(1)  # '#' or '.'
            attr_block = attr_match.group(2)
            
            # Prepend the prefix if it's missing
            if ' ' not in attr_block and not attr_block.startswith('.') and not attr_block.startswith('#'):
                attr_block = prefix + attr_block
            
            # Extract IDs and classes from the block
            attrs = {"id": "", "class": []}
            for part in attr_block.split():
                if part.startswith('#'):
                    attrs["id"] = part[1:]
                elif part.startswith('.'):
                    attrs["class"].append(part[1:])
            
            # Construct new attributes for the paragraph tag
            new_attrs = p_attrs  # Start with existing attributes
            if attrs["id"]:
                new_attrs += f' id="{attrs["id"]}"'
            if attrs["class"]:
                class_str = " ".join(attrs["class"])
                # Check if a class attribute already exists
                if 'class="' in new_attrs:
                    # Append new classes
                    new_attrs = re.sub(r'class="([^"]*)"', rf'class="\1 {class_str}"', new_attrs)
                else:
                    new_attrs += f' class="{class_str}"'
            
            # Remove the attribute block from the paragraph content
            clean_content = re.sub(r'\{([#.])(.+?)\}', '', p_content)
            
            # Create the new paragraph tag
            new_p_tag = f"<p{new_attrs}>{clean_content}</p>"
            
            # Replace the old paragraph with the new one
            start, end = p_match.span()
            html_content = html_content[:start] + new_p_tag + html_content[end:]
    
    # Then, handle standalone attribute blocks (for headings, etc.)
    # Find all attribute blocks, e.g., `{#my-id .my-class}` or `{.my-class}`
    for match in re.finditer(r'\{([#.])(.+?)\}', html_content):
        prefix = match.group(1)  # '#' or '.'
        attr_block = match.group(2)
        
        # Prepend the prefix if it's missing
        if ' ' not in attr_block and not attr_block.startswith('.') and not attr_block.startswith('#'):
            attr_block = prefix + attr_block
        
        # Extract IDs and classes from the block
        attrs = {"id": "", "class": []}
        for part in attr_block.split():
            if part.startswith('#'):
                attrs["id"] = part[1:]
            elif part.startswith('.'):
                attrs["class"].append(part[1:])
        
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
            new_attrs = ""
            if attrs["id"]:
                new_attrs += f' id="{attrs["id"]}"'
            if attrs["class"]:
                class_str = " ".join(attrs["class"])
                # Check if a class attribute already exists
                if 'class="' in existing_attrs:
                    # Append new classes
                    existing_attrs = re.sub(r'class="([^"]*)"', rf'class="\1 {class_str}"', existing_attrs)
                else:
                    new_attrs += f' class="{class_str}"'

            # Replace the old tag with the new one
            start, end = last_tag_match.span()
            new_tag = f"<{tag_name}{existing_attrs}{new_attrs}>"
            # Fix: Use the content after the matched HTML tag, not the attribute block
            html_content = preceding_html[:start] + new_tag + html_content[end:]
    
    # Remove any remaining attribute blocks from the HTML
    html_content = re.sub(r'\{([#.])(.+?)\}', '', html_content)
    
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

    env = {}
    html_content = md.render(post.content, env)
    
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
