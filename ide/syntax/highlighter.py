"""
Syntax highlighter for the Power Python IDE.
Provides syntax highlighting for various languages using Pygments.
"""

import tkinter as tk
from pygments import lex
from pygments.lexers import get_lexer_by_name, PythonLexer, HtmlLexer, CssLexer, JavascriptLexer, MarkdownLexer
from pygments.token import Token
from ide.syntax.power_python import PowerPythonLexer


class SyntaxHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.setup_tags()
        
    def setup_tags(self):
        """Configure text tags for syntax highlighting."""
        # Define color scheme
        colors = {
            Token.Keyword: '#0000FF',
            Token.Keyword.Namespace: '#0000FF',
            Token.Keyword.Constant: '#0000FF',
            Token.Keyword.Declaration: '#0000FF',
            Token.Keyword.Type: '#0000FF',
            Token.Name.Class: '#008080',
            Token.Name.Function: '#008080',
            Token.Name.Builtin: '#008080',
            Token.Name.Builtin.Pseudo: '#008080',
            Token.Name.Exception: '#008080',
            Token.Name.Variable: '#000000',
            Token.Name.Variable.Instance: '#000000',
            Token.Name.Variable.Class: '#000000',
            Token.Name.Constant: '#800080',
            Token.Literal.String: '#008000',
            Token.Literal.String.Doc: '#008000',
            Token.Literal.String.Double: '#008000',
            Token.Literal.String.Single: '#008000',
            Token.Literal.String.Escape: '#008000',
            Token.Literal.Number: '#000000',
            Token.Literal.Number.Integer: '#000000',
            Token.Literal.Number.Float: '#000000',
            Token.Operator: '#000000',
            Token.Operator.Word: '#0000FF',
            Token.Punctuation: '#000000',
            Token.Comment: '#808080',
            Token.Comment.Single: '#808080',
            Token.Comment.Multiline: '#808080',
            Token.Generic.Heading: '#FF0000',
            Token.Generic.Subheading: '#FF0000',
            Token.Generic.Emph: '#000000',
            Token.Generic.Strong: '#000000',
        }
        
        # Create tags for each token type
        for token_type, color in colors.items():
            self.text_widget.tag_configure(str(token_type), foreground=color)
    
    def get_lexer_for_language(self, language):
        """Get the appropriate lexer for a language."""
        lexers = {
            'python': PythonLexer(),
            'html': HtmlLexer(),
            'css': CssLexer(),
            'javascript': JavascriptLexer(),
            'js': JavascriptLexer(),
            'markdown': MarkdownLexer(),
            'md': MarkdownLexer(),
            'powerpython': PowerPythonLexer(),
        }
        return lexers.get(language, PythonLexer())
    
    def highlight(self, content, language='python'):
        """Apply syntax highlighting to the content."""
        # Remove existing tags
        for tag in self.text_widget.tag_names():
            if tag != 'sel':  # Don't remove selection tag
                self.text_widget.tag_remove(tag, '1.0', tk.END)
        
        # Get the appropriate lexer
        lexer = self.get_lexer_for_language(language)
        
        # Tokenize the content
        tokens = lex(content, lexer)
        
        # Apply tags for each token
        start_line = 1
        start_char = 0
        
        for token_type, token_value in tokens:
            # Calculate end position
            lines = token_value.split('\n')
            end_line = start_line + len(lines) - 1
            
            if len(lines) == 1:
                end_char = start_char + len(token_value)
            else:
                end_char = len(lines[-1])
            
            # Create position strings
            start_pos = f'{start_line}.{start_char}'
            end_pos = f'{end_line}.{end_char}'
            
            # Apply tag
            if str(token_type) in self.text_widget.tag_names():
                self.text_widget.tag_add(str(token_type), start_pos, end_pos)
            
            # Update position for next token
            if '\n' in token_value:
                start_line = end_line
                start_char = end_char
            else:
                start_char += len(token_value)
                if start_char >= len(lines[-1]) and len(lines) > 1:
                    start_line += 1
                    start_char = 0
    
    def highlight_range(self, start_pos, end_pos, language='python'):
        """Apply syntax highlighting to a range of text."""
        # Get the content in the range
        content = self.text_widget.get(start_pos, end_pos)
        
        # Remove existing tags in the range
        for tag in self.text_widget.tag_names():
            if tag != 'sel':  # Don't remove selection tag
                self.text_widget.tag_remove(tag, start_pos, end_pos)
        
        # Get the appropriate lexer
        lexer = self.get_lexer_for_language(language)
        
        # Tokenize the content
        tokens = lex(content, lexer)
        
        # Apply tags for each token
        current_pos = start_pos
        for token_type, token_value in tokens:
            # Calculate end position
            lines = token_value.split('\n')
            if len(lines) == 1:
                end_line, end_char = map(int, current_pos.split('.'))
                end_char += len(token_value)
                end_pos = f'{end_line}.{end_char}'
            else:
                end_line = int(current_pos.split('.')[0]) + len(lines) - 1
                end_char = len(lines[-1])
                end_pos = f'{end_line}.{end_char}'
            
            # Apply tag
            if str(token_type) in self.text_widget.tag_names():
                self.text_widget.tag_add(str(token_type), current_pos, end_pos)
            
            # Update position for next token
            current_pos = end_pos
