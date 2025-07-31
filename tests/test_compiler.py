"""
Test suite for the Power Python Compiler.
"""

import unittest
import os
import tempfile
from compiler.main import compile_markdown


class TestCompiler(unittest.TestCase):
    """Test cases for the compiler functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_md_content = """---
title: Test Document
---

# Test Heading

This is a test paragraph.
"""
        
    def test_compile_markdown(self):
        """Test that markdown compilation works."""
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as md_file:
            md_file.write(self.test_md_content)
            md_filename = md_file.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as html_file:
            html_filename = html_file.name
        
        try:
            # Compile the markdown file
            compile_markdown(md_filename, html_filename)
            
            # Check that output file was created
            self.assertTrue(os.path.exists(html_filename))
            
            # Check that output file has content
            with open(html_filename, 'r') as f:
                content = f.read()
                self.assertIn('<h1>Test Heading</h1>', content)
                
        finally:
            # Clean up temporary files
            if os.path.exists(md_filename):
                os.unlink(md_filename)
            if os.path.exists(html_filename):
                os.unlink(html_filename)
                
    def test_python_code_execution(self):
        """Test that Python code execution works."""
        python_md_content = """---
title: Python Test
---

```python-power
print("Hello, World!")
```
"""
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as md_file:
            md_file.write(python_md_content)
            md_filename = md_file.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as html_file:
            html_filename = html_file.name
        
        try:
            # Compile the markdown file
            compile_markdown(md_filename, html_filename)
            
            # Check that output file was created
            self.assertTrue(os.path.exists(html_filename))
            
            # Check that Python output is in the HTML
            with open(html_filename, 'r') as f:
                content = f.read()
                self.assertIn('Hello, World!', content)
                
        finally:
            # Clean up temporary files
            if os.path.exists(md_filename):
                os.unlink(md_filename)
            if os.path.exists(html_filename):
                os.unlink(html_filename)


if __name__ == '__main__':
    unittest.main()
