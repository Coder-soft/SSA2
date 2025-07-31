"""
Main application for the Power Python Desktop IDE.
A GUI-based IDE built with Tkinter and Pygments.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import webbrowser
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Try to import SyntaxHighlighter, but handle missing dependencies gracefully
try:
    from ide.syntax.highlighter import SyntaxHighlighter
    HIGHLIGHTING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Syntax highlighting not available: {e}")
    SyntaxHighlighter = None
    HIGHLIGHTING_AVAILABLE = False


class PowerPythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Power Python IDE")
        self.root.geometry("1200x800")
        
        # Track open files
        self.open_files = {}
        self.current_file = None
        
        # Navigation history for file explorer
        self.nav_history = []
        self.nav_history_index = -1
        
        # Working directory for saving files
        self.working_directory = self.get_or_set_working_directory()
        
        # Create the UI
        self.create_menu()
        self.create_toolbar()
        self.create_main_panels()
        self.create_status_bar()
        
        # Create a new empty document by default
        self.new_file()
        
        # Start periodic file explorer refresh
        self.start_periodic_refresh()
    
    def get_or_set_working_directory(self):
        """Get the working directory from config or prompt user to select one."""
        config_file = os.path.join(os.path.expanduser("~"), ".power_python_ide_config.json")
        
        # Try to load existing configuration
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    if "working_directory" in config and os.path.exists(config["working_directory"]):
                        return config["working_directory"]
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # If no valid config, prompt user to select directory
        messagebox.showinfo("Welcome", "Please select a directory to store your Power Python files.")
        directory = filedialog.askdirectory(title="Select Working Directory for Power Python Files")
        
        if directory and os.path.exists(directory):
            # Save the configuration
            try:
                config = {"working_directory": directory}
                with open(config_file, "w") as f:
                    json.dump(config, f)
                return directory
            except Exception as e:
                print(f"Error saving config: {e}")
                messagebox.showerror("Error", f"Could not save configuration: {e}")
        
        # Fallback to current directory
        return os.getcwd()
    
    def get_language_from_extension(self, filepath):
        """Determine the language from file extension."""
        extension = os.path.splitext(filepath)[1].lower()
        language_map = {
            '.py': 'python',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.js': 'javascript',
            '.md': 'markdown',
            '.markdown': 'markdown',
            '.pyp': 'powerpython',
            '.powerpy': 'powerpython',
        }
        return language_map.get(extension, 'python')
    
    def bind_text_events(self, text_widget, file_id):
        """Bind text change events for live syntax highlighting."""
        def on_text_change(event=None):
            # Schedule syntax highlighting to avoid performance issues
            if hasattr(self, '_after_id'):
                text_widget.after_cancel(self._after_id)
            self._after_id = text_widget.after(300, self.apply_syntax_highlighting, file_id)
        
        # Bind key events
        text_widget.bind('<KeyRelease>', on_text_change)
        text_widget.bind('<Button-1>', on_text_change)
        
        # Bind paste event
        text_widget.bind('<<Paste>>', on_text_change)
        
    def apply_syntax_highlighting(self, file_id):
        """Apply syntax highlighting to the current file."""
        if file_id in self.open_files:
            file_info = self.open_files[file_id]
            # Only apply highlighting if highlighter is available
            if file_info["highlighter"]:
                content = file_info["text_widget"].get("1.0", tk.END)
                file_info["highlighter"].highlight(content, file_info["language"])
    
    def update_line_numbers(self, text_widget, line_numbers):
        """Update line numbers for a text widget."""
        # Get the number of lines
        line_count = int(text_widget.index('end-1c').split('.')[0])
        
        # Generate line numbers
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        
        # Update line numbers widget
        line_numbers.config(state='normal')
        line_numbers.delete('1.0', tk.END)
        line_numbers.insert('1.0', line_numbers_text)
        line_numbers.config(state='disabled')
    
    def bind_auto_indent(self, text_widget):
        """Bind auto-indentation functionality to a text widget."""
        def on_key_press(event):
            # Handle Enter key for auto-indentation
            if event.keysym == 'Return':
                # Get current line
                cursor_pos = text_widget.index(tk.INSERT)
                line_num = cursor_pos.split('.')[0]
                line_content = text_widget.get(f"{line_num}.0", f"{line_num}.end")
                
                # Calculate indentation
                indent = ""
                for char in line_content:
                    if char in [' ', '\t']:
                        indent += char
                    else:
                        break
                
                # Add extra indentation for blocks
                if line_content.rstrip().endswith(':'):
                    # Python-style indentation after colons
                    indent += "    "  # Add 4 spaces
                
                # Insert newline and indentation
                text_widget.insert(tk.INSERT, "\n" + indent)
                return "break"  # Prevent default behavior
            
            # Handle Tab key for indentation
            elif event.keysym == 'Tab':
                # Insert 4 spaces instead of tab character
                text_widget.insert(tk.INSERT, "    ")
                return "break"  # Prevent default behavior
        
        # Bind key events
        text_widget.bind('<KeyPress>', on_key_press)
    
    def create_menu(self):
        """Create the main menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Find and Replace", command=self.find_replace, accelerator="Ctrl+H")
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-f>', lambda e: self.find_text())
        self.root.bind('<Control-h>', lambda e: self.find_replace())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle File Explorer", command=self.toggle_file_explorer)
        view_menu.add_command(label="Refresh File Explorer", command=self.refresh_file_explorer)
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Compile", command=self.compile_file, accelerator="F5")
        
        # Additional useful shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<F5>', lambda e: self.compile_file())
        
        # Save As shortcut
        self.root.bind('<Control-Shift-S>', lambda e: self.save_file_as())
        
        # Close tab shortcut
        self.root.bind('<Control-w>', lambda e: self.close_current_tab())
        
        # Refresh file explorer shortcut
        self.root.bind('<F6>', lambda e: self.refresh_file_explorer())
        
        # Select all shortcut
        self.root.bind('<Control-a>', lambda e: self.select_all())
    
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Toolbar buttons
        new_btn = ttk.Button(toolbar, text="New", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=2)
        
        open_btn = ttk.Button(toolbar, text="Open", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = ttk.Button(toolbar, text="Save", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        compile_btn = ttk.Button(toolbar, text="Compile", command=self.compile_file)
        compile_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        undo_btn = ttk.Button(toolbar, text="Undo", command=self.undo)
        undo_btn.pack(side=tk.LEFT, padx=2)
        
        redo_btn = ttk.Button(toolbar, text="Redo", command=self.redo)
        redo_btn.pack(side=tk.LEFT, padx=2)
    
    def create_main_panels(self):
        """Create the main panels: file explorer, editor, and preview."""
        # Main container
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - File explorer
        self.file_explorer_frame = ttk.Frame(main_paned, width=200)
        main_paned.add(self.file_explorer_frame, weight=1)
        
        # Center panel - Editor area
        editor_frame = ttk.Frame(main_paned)
        main_paned.add(editor_frame, weight=3)
        
        # Right panel - Preview
        self.preview_frame = ttk.Frame(main_paned, width=300)
        main_paned.add(self.preview_frame, weight=2)
        
        # Create file explorer
        self.create_file_explorer()
        
        # Create editor area
        self.create_editor(editor_frame)
        
        # Create preview area
        self.create_preview()
    
    def create_file_explorer(self):
        """Create the file explorer panel."""
        # File explorer header
        header = ttk.Label(self.file_explorer_frame, text="File Explorer", font=("Arial", 10, "bold"))
        header.pack(fill=tk.X, pady=(0, 5))
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.file_explorer_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 5))
        
        back_btn = ttk.Button(nav_frame, text="← Back", command=self.go_back, state=tk.DISABLED)
        back_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        forward_btn = ttk.Button(nav_frame, text="Forward →", command=self.go_forward, state=tk.DISABLED)
        forward_btn.pack(side=tk.LEFT)
        
        # Store references to navigation buttons
        self.back_btn = back_btn
        self.forward_btn = forward_btn
        
        # Current directory label
        self.current_dir_label = ttk.Label(self.file_explorer_frame, text="Current Directory:")
        self.current_dir_label.pack(fill=tk.X)
        
        # Directory tree
        self.tree_frame = ttk.Frame(self.file_explorer_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # Bind tree events
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Open working directory
        self.open_directory(self.working_directory)
    
    def create_editor(self, parent):
        """Create the editor area."""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Bind notebook events
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_preview(self):
        """Create the preview panel."""
        # Preview header
        header = ttk.Label(self.preview_frame, text="Preview", font=("Arial", 10, "bold"))
        header.pack(fill=tk.X, pady=(0, 5))
        
        # Preview text area
        self.preview_text = tk.Text(self.preview_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for preview
        preview_scroll = ttk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.preview_text.yview)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def new_file(self):
        """Create a new file."""
        # Create a new tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Untitled")
        
        # Create frame for text widget and line numbers
        text_frame = ttk.Frame(tab)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create line numbers text widget
        line_numbers = tk.Text(text_frame, width=4, padx=3, takefocus=0, border=0,
                              state='disabled', wrap='none', font=('Consolas', 10))
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create main text widget
        text_widget = tk.Text(text_frame, wrap=tk.WORD, undo=True)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scroll = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=text_widget.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scroll.set)
        
        # Sync line numbers with text widget
        text_widget.bind('<KeyRelease>', lambda e: self.update_line_numbers(text_widget, line_numbers))
        text_widget.bind('<Button-1>', lambda e: self.update_line_numbers(text_widget, line_numbers))
        text_widget.bind('<MouseWheel>', lambda e: self.update_line_numbers(text_widget, line_numbers))
        
        # Create syntax highlighter if available
        highlighter = SyntaxHighlighter(text_widget) if HIGHLIGHTING_AVAILABLE else None
        
        # Store reference
        file_id = f"untitled_{len(self.open_files)}"
        self.open_files[file_id] = {
            "tab": tab,
            "text_widget": text_widget,
            "line_numbers": line_numbers,
            "highlighter": highlighter,
            "filepath": None,
            "filename": "Untitled",
            "language": "python"
        }
        
        # Bind text change events for live syntax highlighting
        self.bind_text_events(text_widget, file_id)
        
        # Bind key events for auto-indentation
        self.bind_auto_indent(text_widget)
        
        # Initialize line numbers
        self.update_line_numbers(text_widget, line_numbers)
        
        # Select the new tab
        self.notebook.select(tab)
        self.current_file = file_id
        
        # Update status
        self.status_bar.config(text="New file created")
    
    def open_file(self):
        """Open an existing file."""
        filepath = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("Markdown Files", "*.md"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("All Files", "*.*")
            ]
        )
        
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Create a new tab
                tab = ttk.Frame(self.notebook)
                self.notebook.add(tab, text=os.path.basename(filepath))
                
                # Create frame for text widget and line numbers
                text_frame = ttk.Frame(tab)
                text_frame.pack(fill=tk.BOTH, expand=True)
                
                # Create line numbers text widget
                line_numbers = tk.Text(text_frame, width=4, padx=3, takefocus=0, border=0,
                                      state='disabled', wrap='none', font=('Consolas', 10))
                line_numbers.pack(side=tk.LEFT, fill=tk.Y)
                
                # Create main text widget
                text_widget = tk.Text(text_frame, wrap=tk.WORD, undo=True)
                text_widget.insert("1.0", content)
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                # Add scrollbar
                scroll = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=text_widget.yview)
                scroll.pack(side=tk.RIGHT, fill=tk.Y)
                text_widget.configure(yscrollcommand=scroll.set)
                
                # Sync line numbers with text widget
                text_widget.bind('<KeyRelease>', lambda e: self.update_line_numbers(text_widget, line_numbers))
                text_widget.bind('<Button-1>', lambda e: self.update_line_numbers(text_widget, line_numbers))
                text_widget.bind('<MouseWheel>', lambda e: self.update_line_numbers(text_widget, line_numbers))
                
                # Determine language from file extension
                language = self.get_language_from_extension(filepath)
                
                # Create syntax highlighter if available
                highlighter = SyntaxHighlighter(text_widget) if HIGHLIGHTING_AVAILABLE else None
                
                # Store reference
                file_id = filepath
                self.open_files[file_id] = {
                    "tab": tab,
                    "text_widget": text_widget,
                    "line_numbers": line_numbers,
                    "highlighter": highlighter,
                    "filepath": filepath,
                    "filename": os.path.basename(filepath),
                    "language": language
                }
                
                # Apply initial syntax highlighting if available
                if highlighter:
                    highlighter.highlight(content, language)
                
                # Initialize line numbers
                self.update_line_numbers(text_widget, line_numbers)
                
                # Bind text change events for live syntax highlighting
                self.bind_text_events(text_widget, file_id)
                
                # Bind key events for auto-indentation
                self.bind_auto_indent(text_widget)
                
                # Select the new tab
                self.notebook.select(tab)
                self.current_file = file_id
                
                # Update status
                self.status_bar.config(text=f"Opened {filepath}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def save_file(self):
        """Save the current file."""
        if not self.current_file:
            return
        
        file_info = self.open_files[self.current_file]
        
        if file_info["filepath"]:
            # Save to existing file
            try:
                content = file_info["text_widget"].get("1.0", tk.END)
                with open(file_info["filepath"], "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Update tab title if needed
                self.notebook.tab(file_info["tab"], text=file_info["filename"])
                
                # Update status
                self.status_bar.config(text=f"Saved {file_info['filepath']}")
                
                # Re-apply syntax highlighting
                content = file_info["text_widget"].get("1.0", tk.END)
                file_info["highlighter"].highlight(content, file_info["language"])
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
        else:
            # Save as new file
            self.save_file_as()
    
    def save_file_as(self):
        """Save the current file with a new name."""
        if not self.current_file:
            return
        
        file_info = self.open_files[self.current_file]
        filepath = filedialog.asksaveasfilename(
            title="Save File As",
            initialdir=self.working_directory,
            defaultextension=".md",
            filetypes=[
                ("Markdown Files", "*.md"),
                ("Python Files", "*.py"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js"),
                ("All Files", "*.*")
            ]
        )
        
        if filepath:
            try:
                content = file_info["text_widget"].get("1.0", tk.END)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # Update file info
                file_info["filepath"] = filepath
                file_info["filename"] = os.path.basename(filepath)
                
                # Update tab title
                self.notebook.tab(file_info["tab"], text=file_info["filename"])
                
                # Update status
                self.status_bar.config(text=f"Saved as {filepath}")
                
                # Update language if needed
                file_info["language"] = self.get_language_from_extension(filepath)
                
                # Re-apply syntax highlighting
                content = file_info["text_widget"].get("1.0", tk.END)
                file_info["highlighter"].highlight(content, file_info["language"])
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def open_directory(self, directory):
        """Open a directory in the file explorer."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Update current directory label
        self.current_dir_label.config(text=f"Current Directory: {os.path.abspath(directory)}")
        
        # Add to navigation history if it's a new directory
        if not self.nav_history or self.nav_history[self.nav_history_index] != directory:
            # Remove forward history if we're not at the end
            if self.nav_history_index < len(self.nav_history) - 1:
                self.nav_history = self.nav_history[:self.nav_history_index + 1]
            
            self.nav_history.append(directory)
            self.nav_history_index = len(self.nav_history) - 1
        
        # Add directory contents
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    self.tree.insert("", "end", text=f"📁 {item}", values=[item_path, "dir"])
                else:
                    self.tree.insert("", "end", text=f"📄 {item}", values=[item_path, "file"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not read directory: {str(e)}")
        
        # Update navigation buttons
        self.update_nav_buttons()
    
    def refresh_file_explorer(self):
        """Refresh the file explorer to show current directory contents."""
        if hasattr(self, 'working_directory'):
            self.open_directory(self.working_directory)
    
    def start_periodic_refresh(self):
        """Start periodic refresh of the file explorer."""
        def periodic_refresh():
            # Refresh file explorer every 5 seconds
            self.refresh_file_explorer()
            # Schedule next refresh
            self.root.after(5000, periodic_refresh)
        
        # Start the first refresh
        self.root.after(5000, periodic_refresh)
    
    def on_tree_select(self, event):
        """Handle tree selection events."""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            item_path, item_type = self.tree.item(item, "values")
            
            if item_type == "file":
                # Open file
                self.open_file_path(item_path)
            elif item_type == "dir":
                # Navigate to directory
                self.open_directory(item_path)
    
    def go_back(self):
        """Navigate to the previous directory in history."""
        if self.nav_history_index > 0:
            self.nav_history_index -= 1
            directory = self.nav_history[self.nav_history_index]
            self.open_directory_no_history(directory)
            self.update_nav_buttons()
    
    def go_forward(self):
        """Navigate to the next directory in history."""
        if self.nav_history_index < len(self.nav_history) - 1:
            self.nav_history_index += 1
            directory = self.nav_history[self.nav_history_index]
            self.open_directory_no_history(directory)
            self.update_nav_buttons()
    
    def open_directory_no_history(self, directory):
        """Open a directory without adding to history."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Update current directory label
        self.current_dir_label.config(text=f"Current Directory: {os.path.abspath(directory)}")
        
        # Add directory contents
        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    self.tree.insert("", "end", text=f"📁 {item}", values=[item_path, "dir"])
                else:
                    self.tree.insert("", "end", text=f"📄 {item}", values=[item_path, "file"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not read directory: {str(e)}")
    
    def update_nav_buttons(self):
        """Update the state of navigation buttons."""
        # Update back button state
        if self.nav_history_index > 0:
            self.back_btn.config(state=tk.NORMAL)
        else:
            self.back_btn.config(state=tk.DISABLED)
        
        # Update forward button state
        if self.nav_history_index < len(self.nav_history) - 1:
            self.forward_btn.config(state=tk.NORMAL)
        else:
            self.forward_btn.config(state=tk.DISABLED)
    
    def open_file_path(self, filepath):
        """Open a file by its path."""
        # Check if file is already open
        if filepath in self.open_files:
            file_info = self.open_files[filepath]
            self.notebook.select(file_info["tab"])
            self.current_file = filepath
            return
        
        # Open file
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Create a new tab
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=os.path.basename(filepath))
            
            # Create frame for text widget and line numbers
            text_frame = ttk.Frame(tab)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            # Create line numbers text widget
            line_numbers = tk.Text(text_frame, width=4, padx=3, takefocus=0, border=0,
                                  state='disabled', wrap='none', font=('Consolas', 10))
            line_numbers.pack(side=tk.LEFT, fill=tk.Y)
            
            # Create main text widget
            text_widget = tk.Text(text_frame, wrap=tk.WORD, undo=True)
            text_widget.insert("1.0", content)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Add scrollbar
            scroll = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=text_widget.yview)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)
            text_widget.configure(yscrollcommand=scroll.set)
            
            # Sync line numbers with text widget
            text_widget.bind('<KeyRelease>', lambda e: self.update_line_numbers(text_widget, line_numbers))
            text_widget.bind('<Button-1>', lambda e: self.update_line_numbers(text_widget, line_numbers))
            text_widget.bind('<MouseWheel>', lambda e: self.update_line_numbers(text_widget, line_numbers))
            
            # Determine language from file extension
            language = self.get_language_from_extension(filepath)
            
            # Create syntax highlighter if available
            highlighter = SyntaxHighlighter(text_widget) if HIGHLIGHTING_AVAILABLE else None
            
            # Store reference
            self.open_files[filepath] = {
                "tab": tab,
                "text_widget": text_widget,
                "line_numbers": line_numbers,
                "highlighter": highlighter,
                "filepath": filepath,
                "filename": os.path.basename(filepath),
                "language": language
            }
            
            # Apply initial syntax highlighting if available
            if highlighter:
                highlighter.highlight(content, language)
            
            # Initialize line numbers
            self.update_line_numbers(text_widget, line_numbers)
            
            # Bind text change events for live syntax highlighting
            self.bind_text_events(text_widget, filepath)
            
            # Bind key events for auto-indentation
            self.bind_auto_indent(text_widget)
            
            # Select the new tab
            self.notebook.select(tab)
            self.current_file = filepath
            
            # Update status
            self.status_bar.config(text=f"Opened {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
    
    def on_tab_changed(self, event):
        """Handle tab change events."""
        selected_tab = event.widget.select()
        
        # Find the file associated with this tab
        for file_id, file_info in self.open_files.items():
            if file_info["tab"] == selected_tab:
                self.current_file = file_id
                self.status_bar.config(text=f"Selected: {file_info['filename']}")
                break
    
    def compile_file(self):
        """Compile the current file and open the result in the browser."""
        if not self.current_file:
            messagebox.showwarning("Warning", "No file to compile")
            return
        
        file_info = self.open_files[self.current_file]
        # Get content without the extra newline that tkinter adds
        content = file_info["text_widget"].get("1.0", "end-1c")
        
        # Initialize compiled_html to ensure it's not carrying over content from previous compilations
        compiled_html = ""
        
        # Try to import the Power Python compiler
        try:
            # Add the project root to sys.path to import compiler modules
            project_root = os.path.join(os.path.dirname(__file__), '..')
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            from compiler.main import compile_markdown
            
            # Save content to a temporary file
            import tempfile
            import io
            temp_file = None
            html_file = None
            try:
                # Create a temporary file with .md extension
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                    f.write(content)
                    temp_file = f.name
                
                # Ensure we're not importing or calling the compiler multiple times
                # Compile the temporary file exactly once
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                
                try:
                    # Call compile_markdown exactly once
                    compile_markdown(temp_file)
                    output = sys.stdout.getvalue()
                finally:
                    sys.stdout = old_stdout
                
                # Read the compiled HTML exactly once
                html_file = temp_file.rsplit('.', 1)[0] + '.html'
                # Force a fresh read of the file to avoid any caching issues
                with open(html_file, 'r', encoding='utf-8') as f:
                    compiled_html = f.read()
                
                # Clean up temporary files immediately after reading
                try:
                    if temp_file and os.path.exists(temp_file):
                        os.unlink(temp_file)
                    if html_file and os.path.exists(html_file):
                        os.unlink(html_file)
                except:
                    pass
                
                # Additional check to ensure no duplication in the content
                # This is a workaround for the duplication issue
                if compiled_html.count('<!DOCTYPE html>') > 1:
                    # If we find multiple DOCTYPE declarations, take only the first complete HTML document
                    first_doctype = compiled_html.find('<!DOCTYPE html>')
                    second_doctype = compiled_html.find('<!DOCTYPE html>', first_doctype + 1)
                    if second_doctype != -1:
                        # Take only the content up to the second DOCTYPE
                        compiled_html = compiled_html[:second_doctype]
                
            except Exception as e:
                # Clean up temporary file if it exists
                try:
                    if temp_file and os.path.exists(temp_file):
                        os.unlink(temp_file)
                    if html_file and os.path.exists(html_file):
                        os.unlink(html_file)
                except:
                    pass
                raise e
            
        except ImportError as e:
            # Fallback: use the content as-is if compiler is not available
            print(f"Warning: Could not import compiler: {e}")
            compiled_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Compiled Output</title>
</head>
<body>
    <h1>Compiled Output</h1>
    <pre>{content}</pre>
</body>
</html>"""
        except Exception as e:
            # Handle compilation errors
            messagebox.showerror("Compilation Error", f"Error compiling file: {str(e)}")
            return
        
        # Generate a unique filename in the working directory
        base_name = "render"
        extension = ".html"
        counter = 0
        filename = os.path.join(self.working_directory, f"{base_name}{extension}")
        
        # Check if file exists and increment counter if needed
        while os.path.exists(filename):
            counter += 1
            filename = os.path.join(self.working_directory, f"{base_name}{counter}{extension}")
        
        # Save the compiled HTML
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(compiled_html)
            
            # Show in preview as rendered text (stripped of HTML tags)
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            
            # Extract just the body content for preview
            import re
            body_match = re.search(r'<body[^>]*>(.*?)</body>', compiled_html, re.DOTALL | re.IGNORECASE)
            if body_match:
                body_content = body_match.group(1)
                # Remove script tags for preview
                body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                # Remove style tags for preview
                body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
                # Remove HTML tags and decode HTML entities
                preview_content = re.sub(r'<[^>]+>', '', body_content)
                # Decode common HTML entities
                preview_content = preview_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
                # Clean up extra whitespace
                preview_content = re.sub(r'\s+', ' ', preview_content).strip()
            else:
                # Fallback to showing first 500 characters if no body tag found
                preview_content = compiled_html[:500] + "..."
                # Still strip HTML tags for fallback
                preview_content = re.sub(r'<[^>]+>', '', preview_content)
                preview_content = preview_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
                preview_content = re.sub(r'\s+', ' ', preview_content).strip()
            
            self.preview_text.insert("1.0", f"Compiled HTML saved as: {filename}\n\nPreview:\n{preview_content}")
            self.preview_text.config(state=tk.DISABLED)
            
            # Open in browser
            file_path = os.path.abspath(filename)
            webbrowser.open(f"file://{file_path}")
            
            self.status_bar.config(text=f"File compiled and saved as {filename}")
            
            # Refresh file explorer to show new file
            self.open_directory(self.working_directory)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save compiled file: {str(e)}")
    
    def toggle_file_explorer(self):
        """Toggle the file explorer panel."""
        # Check if file explorer is currently visible
        if self.file_explorer_frame.winfo_viewable():
            # Hide the file explorer
            self.file_explorer_frame.pack_forget()
            self.status_bar.config(text="File explorer hidden")
        else:
            # Show the file explorer
            self.file_explorer_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
            self.refresh_file_explorer()
            self.status_bar.config(text="File explorer shown")
    
    def undo(self):
        """Undo the last action."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            try:
                file_info["text_widget"].edit_undo()
            except tk.TclError:
                pass  # Nothing to undo
    
    def redo(self):
        """Redo the last undone action."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            try:
                file_info["text_widget"].edit_redo()
            except tk.TclError:
                pass  # Nothing to redo
    
    def cut(self):
        """Cut selected text."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            try:
                file_info["text_widget"].event_generate("<<Cut>>")
            except tk.TclError:
                pass
    
    def copy(self):
        """Copy selected text."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            try:
                file_info["text_widget"].event_generate("<<Copy>>")
            except tk.TclError:
                pass
    
    def paste(self):
        """Paste text from clipboard."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            try:
                file_info["text_widget"].event_generate("<<Paste>>")
            except tk.TclError:
                pass
    
    def select_all(self):
        """Select all text in the current file."""
        if self.current_file:
            file_info = self.open_files[self.current_file]
            file_info["text_widget"].tag_add(tk.SEL, "1.0", tk.END)
            file_info["text_widget"].mark_set(tk.INSERT, "1.0")
            file_info["text_widget"].see(tk.INSERT)
            return "break"  # Prevent default behavior
    
    def close_current_tab(self):
        """Close the current tab."""
        if self.current_file and self.current_file in self.open_files:
            file_info = self.open_files[self.current_file]
            tab = file_info["tab"]
            
            # Remove from notebook
            self.notebook.forget(tab)
            
            # Remove from open files
            del self.open_files[self.current_file]
            
            # Update current file
            if self.open_files:
                # Select first available file
                first_file = list(self.open_files.keys())[0]
                self.current_file = first_file
                self.notebook.select(self.open_files[first_file]["tab"])
            else:
                self.current_file = None
                # Create a new empty file
                self.new_file()
            
            self.status_bar.config(text="Tab closed")
    
    def find_text(self):
        """Open a find dialog."""
        if not self.current_file:
            return
        
        # Create find dialog
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")
        find_dialog.transient(self.root)
        find_dialog.grab_set()
        
        # Search term
        tk.Label(find_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        search_entry = tk.Entry(find_dialog, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        search_entry.focus()
        
        # Search button
        def do_search():
            search_term = search_entry.get()
            if search_term:
                self.perform_search(search_term)
                find_dialog.destroy()
        
        search_btn = tk.Button(find_dialog, text="Find", command=do_search)
        search_btn.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        
        # Bind Enter key
        search_entry.bind('<Return>', lambda e: do_search())
        
        # Center dialog
        find_dialog.update_idletasks()
        x = (find_dialog.winfo_screenwidth() // 2) - (find_dialog.winfo_width() // 2)
        y = (find_dialog.winfo_screenheight() // 2) - (find_dialog.winfo_height() // 2)
        find_dialog.geometry(f"+{x}+{y}")
    
    def perform_search(self, search_term):
        """Perform the actual search in the current document."""
        if not self.current_file:
            return
        
        file_info = self.open_files[self.current_file]
        text_widget = file_info["text_widget"]
        
        # Get current position
        current_pos = text_widget.index(tk.INSERT)
        
        # Search from current position to end
        pos = text_widget.search(search_term, current_pos, tk.END)
        
        # If not found, search from beginning
        if not pos:
            pos = text_widget.search(search_term, "1.0", current_pos)
        
        # If found, highlight and move cursor
        if pos:
            end_pos = f"{pos}+{len(search_term)}c"
            text_widget.tag_remove(tk.SEL, "1.0", tk.END)
            text_widget.tag_add(tk.SEL, pos, end_pos)
            text_widget.mark_set(tk.INSERT, pos)
            text_widget.see(pos)
            
            # Update status
            line, col = pos.split('.')
            self.status_bar.config(text=f"Found '{search_term}' at line {line}, column {col}")
        else:
            self.status_bar.config(text=f"'{search_term}' not found")
            messagebox.showinfo("Find", f"'{search_term}' not found")
    
    def find_replace(self):
        """Open a find and replace dialog."""
        if not self.current_file:
            return
        
        # Create find/replace dialog
        replace_dialog = tk.Toplevel(self.root)
        replace_dialog.title("Find and Replace")
        replace_dialog.geometry("350x150")
        replace_dialog.transient(self.root)
        replace_dialog.grab_set()
        
        # Search term
        tk.Label(replace_dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        search_entry = tk.Entry(replace_dialog, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        search_entry.focus()
        
        # Replace term
        tk.Label(replace_dialog, text="Replace with:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        replace_entry = tk.Entry(replace_dialog, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        def do_find():
            search_term = search_entry.get()
            if search_term:
                self.perform_search(search_term)
        
        def do_replace():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            if search_term and replace_term:
                self.perform_replace(search_term, replace_term)
                
        def do_replace_all():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            if search_term and replace_term:
                self.perform_replace_all(search_term, replace_term)
                replace_dialog.destroy()
        
        # Button frame
        button_frame = ttk.Frame(replace_dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        find_btn = tk.Button(button_frame, text="Find", command=do_find)
        find_btn.pack(side=tk.LEFT, padx=5)
        
        replace_btn = tk.Button(button_frame, text="Replace", command=do_replace)
        replace_btn.pack(side=tk.LEFT, padx=5)
        
        replace_all_btn = tk.Button(button_frame, text="Replace All", command=do_replace_all)
        replace_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to find
        search_entry.bind('<Return>', lambda e: do_find())
        
        # Center dialog
        replace_dialog.update_idletasks()
        x = (replace_dialog.winfo_screenwidth() // 2) - (replace_dialog.winfo_width() // 2)
        y = (replace_dialog.winfo_screenheight() // 2) - (replace_dialog.winfo_height() // 2)
        replace_dialog.geometry(f"+{x}+{y}")
    
    def perform_replace(self, search_term, replace_term):
        """Replace the current occurrence of search_term with replace_term."""
        if not self.current_file:
            return
        
        file_info = self.open_files[self.current_file]
        text_widget = file_info["text_widget"]
        
        # Get current selection
        try:
            current_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if current_text == search_term:
                # Replace selected text
                text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
                text_widget.insert(tk.INSERT, replace_term)
                self.status_bar.config(text=f"Replaced '{search_term}' with '{replace_term}'")
                # Move to next occurrence
                self.perform_search(search_term)
            else:
                # Find the term first
                self.perform_search(search_term)
        except tk.TclError:
            # No selection, find the term first
            self.perform_search(search_term)
    
    def perform_replace_all(self, search_term, replace_term):
        """Replace all occurrences of search_term with replace_term."""
        if not self.current_file:
            return
        
        file_info = self.open_files[self.current_file]
        text_widget = file_info["text_widget"]
        
        # Get all content
        content = text_widget.get("1.0", tk.END)
        
        # Count occurrences
        count = content.count(search_term)
        
        if count > 0:
            # Replace all occurrences
            new_content = content.replace(search_term, replace_term)
            
            # Update text widget
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", new_content)
            
            # Re-apply syntax highlighting if available
            if file_info["highlighter"]:
                file_info["highlighter"].highlight(new_content, file_info["language"])
            
            self.status_bar.config(text=f"Replaced {count} occurrences of '{search_term}' with '{replace_term}'")
        else:
            self.status_bar.config(text=f"'{search_term}' not found")
            messagebox.showinfo("Replace All", f"'{search_term}' not found")


def main():
    root = tk.Tk()
    app = PowerPythonIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
