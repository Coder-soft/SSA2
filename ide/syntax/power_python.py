"""
Custom lexer for Power Python syntax.
Extends the standard Python lexer to support Power Python specific features.
"""

from pygments.lexer import inherit
from pygments.lexers import PythonLexer
from pygments.token import Name, Keyword, String, Comment, Generic


class PowerPythonLexer(PythonLexer):
    """
    A lexer for Power Python syntax that extends the standard Python lexer.
    """
    name = 'PowerPython'
    aliases = ['powerpython', 'power-python']
    filenames = ['*.pyp', '*.powerpy']
    
    tokens = {
        'root': [
            # Power Python code blocks
            (r'```python-power\n', String.Backtick, 'powerpython-code'),
            (r'```css-power\n', String.Backtick, 'powercss-code'),
            # Inherit all other tokens from PythonLexer
            inherit,
        ],
        'powerpython-code': [
            (r'```', String.Backtick, '#pop'),
            # Inherit all Python tokens for the code block
            inherit,
        ],
        'powercss-code': [
            (r'```', String.Backtick, '#pop'),
            # Inherit all CSS tokens for the code block
            (r'.*', Generic),
        ],
    }
