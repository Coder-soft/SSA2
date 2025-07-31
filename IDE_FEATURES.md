# Power Python IDE - Feature Summary

## Overview
The Power Python IDE is a feature-rich desktop application built with Python's Tkinter and Pygments libraries. It provides a comprehensive development environment for Python and other languages with advanced editing capabilities.

## Core Features

### 1. Multi-Document Interface
- Tabbed interface for editing multiple files simultaneously
- Intuitive file management with new, open, save, and save-as operations
- File explorer panel for browsing directories

### 2. Syntax Highlighting
- Real-time syntax highlighting for multiple languages:
  - Python
  - JavaScript
  - HTML
  - CSS
  - Markdown
  - Power Python (custom syntax)
- Language detection based on file extensions
- Custom color schemes for different token types

### 3. Advanced Editing Features
- **Line Numbers**: Visual line numbering for better code navigation
- **Auto-Indentation**: Automatic indentation that follows Python conventions
- **Smart Tabs**: Tab key inserts 4 spaces for consistent formatting
- **Undo/Redo**: Full editing history management
- **Cut/Copy/Paste**: Standard text manipulation operations

### 4. Search and Replace
- Find dialog with keyboard shortcut (Ctrl+F)
- Find and replace functionality
- Replace all occurrences option
- Visual highlighting of search results

### 5. Custom Power Python Support
- Special lexer for Power Python syntax
- Support for custom code blocks and attributes
- Recognition of `.pyp` and `.powerpy` file extensions

### 6. User Interface
- Main menu bar with File, Edit, and View options
- Toolbar with common actions
- Status bar for contextual information
- Scrollable text areas with vertical scrollbars
- Responsive design that adapts to window resizing

## Keyboard Shortcuts
- `Ctrl+N`: New file
- `Ctrl+O`: Open file
- `Ctrl+S`: Save file
- `Ctrl+F`: Find text
- `F5`: Compile (placeholder)

## File Management
- New file creation
- Opening existing files
- Saving files
- Save-as functionality
- Directory browsing in file explorer

## Technical Implementation
- Built with Python 3.x
- Uses Tkinter for GUI components
- Uses Pygments for syntax highlighting
- Modular architecture with separate syntax highlighting module
- Event-driven design for responsive user experience

## Future Enhancements
- Integration with Power Python compiler
- Live preview panel
- Code folding
- Bracket matching
- Preferences/settings dialog
- Plugin system for extensibility
