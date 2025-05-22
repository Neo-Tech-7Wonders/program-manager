import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os

class ProgramManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Program Manager")
        self.window.configure(bg='#c0c0c0')
        
        # Set window size and position
        self.window.geometry("600x400")
        
        # Create menubar
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)
        
        # Options menu
        self.options_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_checkbutton(label="Auto Arrange", command=self.dummy_command)
        self.options_menu.add_checkbutton(label="Minimize on Use", command=self.dummy_command)
        self.options_menu.add_checkbutton(label="Save Settings on Exit", command=self.dummy_command)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Preferences...", command=self.dummy_command)
        
        # Window menu
        self.window_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=self.window_menu)
        self.window_menu.add_command(label="Cascade", command=self.dummy_command)
        self.window_menu.add_command(label="Tile Horizontally", command=self.dummy_command)
        self.window_menu.add_command(label="Tile Vertically", command=self.dummy_command)
        self.window_menu.add_separator()
        self.window_menu.add_command(label="Arrange Icons", command=self.dummy_command)
        self.window_menu.add_separator()
        self.window_menu.add_command(label="Close All", command=self.dummy_command)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Contents", command=self.dummy_command)
        self.help_menu.add_command(label="Search for Help...", command=self.dummy_command)
        self.help_menu.add_command(label="How to Use Help", command=self.dummy_command)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About Program Manager", command=self.show_about)
        
        # Create main container with border
        self.container = tk.Frame(self.window, bg='#c0c0c0', relief='sunken', bd=1)
        self.container.pack(padx=4, pady=4, fill='both', expand=True)
        
        # Create program groups frame
        self.groups_frame = tk.Frame(self.container, bg='#c0c0c0')
        self.groups_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create program group icons in main window
        self.create_group_icon("Main", self.show_main_menu, 0, 0)
        self.create_group_icon("Accessories", self.show_accessories_menu, 0, 1)
        
        # Initialize windows
        self.main_window = None
        self.accessories_window = None
        
        # Initialize program lists with Windows 3.1 style programs
        self.main_programs = [
            ("File Manager", "explorer.exe"),
            ("Control Panel", "control.exe"),
            ("Print Manager", "printui.exe"),
            ("Task Manager", "taskmgr.exe"),
            ("MS-DOS Prompt", "cmd.exe")
        ]
        
        self.accessories_programs = [
            ("Notepad", "notepad.exe"),
            ("Paint", "mspaint.exe"),
            ("Calculator", "calc.exe"),
            ("WordPad", "write.exe"),
            ("Character Map", "charmap.exe"),
            ("Edge", "msedge.exe"),
        ]

    def create_menu_button(self, text, command):
        button = tk.Button(self.menu_frame, text=text, 
                          relief='raised',
                          bg='#c0c0c0',
                          bd=1,
                          font=('System', 8),
                          padx=6,
                          pady=1,
                          command=command)
        button.pack(side='left', padx=1, pady=1)
        return button

    def create_group_icon(self, name, command, row, col):
        frame = tk.Frame(self.groups_frame, bg='#c0c0c0', width=80, height=70)
        frame.grid_propagate(False)
        frame.grid(row=row, column=col, padx=5, pady=5)
        
        icon_frame = tk.Frame(frame, width=32, height=32, bg='white', relief='sunken', bd=1)
        icon_frame.place(relx=0.5, y=5, anchor='n')
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(icon_frame, text="📁", font=('Segoe UI Emoji', 14), bg='white')
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        label = tk.Label(frame, text=name, bg='#c0c0c0', 
                        font=('System', 8),
                        wraplength=75)
        label.place(relx=0.5, rely=0.8, anchor='n')
        
        frame.bind('<Button-1>', lambda e: command())
        icon_frame.bind('<Button-1>', lambda e: command())
        label.bind('<Button-1>', lambda e: command())
        icon_label.bind('<Button-1>', lambda e: command())

    def dummy_command(self):
        messagebox.showinfo("Info", "This feature is not implemented")

    def create_group_window(self, title):
        window = tk.Toplevel(self.window)
        window.title(title)
        window.configure(bg='#c0c0c0')
        window.geometry("320x240")
        
        # Create title bar with Windows 3.1 style
        title_frame = tk.Frame(window, bg='#000080', relief='raised', bd=1)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame, text=title, fg='white', bg='#000080', 
                              font=('System', 8, 'bold'))
        title_label.pack(side='left', padx=4, pady=2)
        
        # Create content area with Windows 3.1 border
        content_area = tk.Frame(window, bg='#c0c0c0', relief='sunken', bd=1)
        content_area.pack(fill='both', expand=True, padx=4, pady=4)
        
        # Create scrollable content frame
        canvas = tk.Canvas(content_area, bg='#c0c0c0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_area, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg='#c0c0c0')
        
        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Create window inside canvas for content
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor='nw')
        
        # Configure canvas scrolling
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(canvas_window, width=event.width)
        
        content_frame.bind('<Configure>', configure_scroll)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        return window, content_frame

    def show_main_menu(self):
        if self.main_window is None or not self.main_window.winfo_exists():
            self.main_window, content_frame = self.create_group_window("Main Programs")
            for name, command in self.main_programs:
                self.create_program_button(name, command, content_frame)

    def show_accessories_menu(self):
        if self.accessories_window is None or not self.accessories_window.winfo_exists():
            self.accessories_window, content_frame = self.create_group_window("Accessories")
            for name, command in self.accessories_programs:
                self.create_program_button(name, command, content_frame)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def create_program_button(self, name, command, parent_frame):
        # Create frame for each program button
        btn_frame = tk.Frame(parent_frame, bg='#c0c0c0', width=60, height=50)  # Smaller frame
        btn_frame.grid_propagate(False)
        
        # Calculate grid position (5 items per row for better space usage)
        row = len(parent_frame.winfo_children()) // 5
        col = len(parent_frame.winfo_children()) % 5
        btn_frame.grid(row=row, column=col, padx=2, pady=2)  # Reduced padding
        
        # Create button with icon
        icon_frame = tk.Frame(btn_frame, width=24, height=24, bg='white', relief='raised', bd=1)  # Smaller icon
        icon_frame.place(relx=0.5, y=2, anchor='n')  # Adjusted position
        icon_frame.pack_propagate(False)
        
        # Add a simple icon representation
        icon_label = tk.Label(icon_frame, text="📄", font=('Segoe UI Emoji', 10), bg='white')  # Smaller icon
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Create label below icon with word wrap
        label = tk.Label(btn_frame, text=name, bg='#c0c0c0', 
                        font=('System', 7),  # Smaller font
                        wraplength=55,  # Adjusted wrap length
                        justify='center')
        label.place(relx=0.5, rely=0.65, anchor='n')  # Adjusted position
        
        # Make the whole frame clickable
        icon_frame.bind('<Button-1>', lambda e: self.run_program(command))
        label.bind('<Button-1>', lambda e: self.run_program(command))
        btn_frame.bind('<Button-1>', lambda e: self.run_program(command))

    def run_program(self, program):
        try:
            subprocess.Popen(program)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {program}: {str(e)}")
    
    def show_about(self):
        about_window = tk.Toplevel(self.window)
        about_window.title("About Program Manager")
        about_window.geometry("300x200")
        about_window.configure(bg='#c0c0c0')
        about_window.resizable(False, False)
        
        # Create content with Windows 3.1 style
        frame = tk.Frame(about_window, bg='#c0c0c0', relief='raised', bd=1)
        frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Program Manager icon/logo
        icon_frame = tk.Frame(frame, width=32, height=32, bg='white', relief='sunken', bd=1)
        icon_frame.pack(pady=(20,10))
        icon_frame.pack_propagate(False)
        icon_label = tk.Label(icon_frame, text="🖥️", font=('Segoe UI Emoji', 16), bg='white')
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # About text
        tk.Label(frame, text="Program Manager", font=('System', 12, 'bold'), bg='#c0c0c0').pack()
        tk.Label(frame, text="Windows 3.1 Style", font=('System', 8), bg='#c0c0c0').pack()
        tk.Label(frame, text="Version 1.0", font=('System', 8), bg='#c0c0c0').pack()
        tk.Label(frame, text="© 2025 logan", font=('System', 8), bg='#c0c0c0').pack()
        
        # OK button
        ok_button = tk.Button(frame, text="OK", width=8, command=about_window.destroy)
        ok_button.pack(pady=20)
        
        # Make dialog modal
        about_window.transient(self.window)
        about_window.grab_set()
        self.window.wait_window(about_window)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ProgramManager()  # Create an instance
    app.run()  # Call run() on the instance
