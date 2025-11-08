import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os
from datetime import datetime

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure styles
        self.setup_styles()
        
        # Database setup
        self.setup_database()
        
        # Current user
        self.current_user = None
        
        # Show login screen
        self.show_login_screen()
    
    def setup_styles(self):
        """Configure application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#34495e')
        style.configure('TButton', padding=6, relief="flat", background="#3498db", foreground="white")
        style.map('TButton', background=[('active', '#2980b9')])
        style.configure('Accent.TButton', padding=6, relief="flat", background="#27ae60", foreground="white")
        style.map('Accent.TButton', background=[('active', '#229954')])
        style.configure('Danger.TButton', padding=6, relief="flat", background="#e74c3c", foreground="white")
        style.map('Danger.TButton', background=[('active', '#c0392b')])
    
    def setup_database(self):
        """Initialize the SQLite database with users and messages tables"""
        self.conn = sqlite3.connect('chat_app.db')
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def hash_password(self, password):
        """Hash a password for storing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_screen(self):
        """Display the login screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left decorative panel
        left_panel = tk.Frame(main_container, bg="#3498db", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        # Decorative elements
        decor_label = tk.Label(left_panel, text="💬", font=("Arial", 100), bg="#3498db", fg="white")
        decor_label.pack(pady=50)
        
        app_title = tk.Label(left_panel, text="Secure Chat", font=("Arial", 24, "bold"), bg="#3498db", fg="white")
        app_title.pack()
        
        app_subtitle = tk.Label(left_panel, text="Connect with friends securely", font=("Arial", 12), bg="#3498db", fg="white")
        app_subtitle.pack(pady=10)
        
        # Right content panel
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Centered login form
        login_frame = ttk.Frame(right_panel)
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = ttk.Label(login_frame, text="Welcome Back!", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Username
        ttk.Label(login_frame, text="Username:", font=("Arial", 12)).pack(anchor=tk.W)
        self.username_entry = ttk.Entry(login_frame, width=30, font=("Arial", 12))
        self.username_entry.pack(pady=(5, 15))
        
        # Password
        ttk.Label(login_frame, text="Password:", font=("Arial", 12)).pack(anchor=tk.W)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30, font=("Arial", 12))
        self.password_entry.pack(pady=(5, 20))
        
        # Buttons
        buttons_frame = ttk.Frame(login_frame)
        buttons_frame.pack(fill=tk.X)
        
        login_btn = ttk.Button(buttons_frame, text="Login", style='Accent.TButton', command=self.login)
        login_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        register_btn = ttk.Button(buttons_frame, text="Register", command=self.show_register_screen)
        register_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def show_register_screen(self):
        """Display the registration screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left decorative panel
        left_panel = tk.Frame(main_container, bg="#27ae60", width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        # Decorative elements
        decor_label = tk.Label(left_panel, text="👤", font=("Arial", 100), bg="#27ae60", fg="white")
        decor_label.pack(pady=50)
        
        app_title = tk.Label(left_panel, text="Join Us", font=("Arial", 24, "bold"), bg="#27ae60", fg="white")
        app_title.pack()
        
        app_subtitle = tk.Label(left_panel, text="Create your secure account", font=("Arial", 12), bg="#27ae60", fg="white")
        app_subtitle.pack(pady=10)
        
        # Right content panel
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Centered register form
        register_frame = ttk.Frame(right_panel)
        register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = ttk.Label(register_frame, text="Create Account", style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Username
        ttk.Label(register_frame, text="Username:", font=("Arial", 12)).pack(anchor=tk.W)
        self.reg_username_entry = ttk.Entry(register_frame, width=30, font=("Arial", 12))
        self.reg_username_entry.pack(pady=(5, 15))
        
        # Password
        ttk.Label(register_frame, text="Password:", font=("Arial", 12)).pack(anchor=tk.W)
        self.reg_password_entry = ttk.Entry(register_frame, show="*", width=30, font=("Arial", 12))
        self.reg_password_entry.pack(pady=(5, 15))
        
        # Confirm Password
        ttk.Label(register_frame, text="Confirm Password:", font=("Arial", 12)).pack(anchor=tk.W)
        self.reg_confirm_password_entry = ttk.Entry(register_frame, show="*", width=30, font=("Arial", 12))
        self.reg_confirm_password_entry.pack(pady=(5, 20))
        
        # Buttons
        buttons_frame = ttk.Frame(register_frame)
        buttons_frame.pack(fill=tk.X)
        
        register_btn = ttk.Button(buttons_frame, text="Register", style='Accent.TButton', command=self.register)
        register_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        back_btn = ttk.Button(buttons_frame, text="Back to Login", command=self.show_login_screen)
        back_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Bind Enter key to registration
        self.reg_username_entry.bind('<Return>', lambda e: self.reg_password_entry.focus())
        self.reg_password_entry.bind('<Return>', lambda e: self.reg_confirm_password_entry.focus())
        self.reg_confirm_password_entry.bind('<Return>', lambda e: self.register())
        
        # Focus on username entry
        self.reg_username_entry.focus()
    
    def login(self):
        """Handle user login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password_hash=?", 
                      (username, self.hash_password(password)))
        user = cursor.fetchone()
        
        if user:
            self.current_user = username
            self.show_chat_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        """Handle user registration"""
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm_password = self.reg_confirm_password_entry.get().strip()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                          (username, self.hash_password(password)))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_chat_screen(self):
        """Display the main chat screen with user list"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create main window with menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        welcome_label = ttk.Label(header_frame, text=f"Welcome, {self.current_user}!", style='Title.TLabel')
        welcome_label.pack(side=tk.LEFT)
        
        # User list panel
        user_list_frame = ttk.LabelFrame(main_container, text="Registered Users", padding=10)
        user_list_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create treeview for users
        columns = ('username', 'created_at')
        self.user_tree = ttk.Treeview(user_list_frame, columns=columns, show='headings', height=5)
        
        # Define headings
        self.user_tree.heading('username', text='Username')
        self.user_tree.heading('created_at', text='Member Since')
        
        # Define column widths
        self.user_tree.column('username', width=200)
        self.user_tree.column('created_at', width=200)
        
        # Add scrollbars
        user_scroll_y = ttk.Scrollbar(user_list_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        user_scroll_x = ttk.Scrollbar(user_list_frame, orient=tk.HORIZONTAL, command=self.user_tree.xview)
        self.user_tree.configure(yscrollcommand=user_scroll_y.set, xscrollcommand=user_scroll_x.set)
        
        # Pack treeview and scrollbars
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        user_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        user_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load users
        self.load_registered_users()
        
        # Chat partner selection
        partner_frame = ttk.LabelFrame(main_container, text="Start Chat", padding=10)
        partner_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(partner_frame, text="Partner Username:").pack(side=tk.LEFT)
        self.partner_entry = ttk.Entry(partner_frame, width=25, font=("Arial", 11))
        self.partner_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(partner_frame, text="Start Chat", style='Accent.TButton', command=self.start_chat).pack(side=tk.LEFT)
        
        # Chat display area
        self.chat_frame = ttk.LabelFrame(main_container, text="Chat", padding=10)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initially hide chat area
        self.chat_frame.pack_forget()
        
        # Message entry area (initially hidden)
        self.message_frame = ttk.Frame(main_container)
        self.message_frame.pack(fill=tk.X, pady=(10, 0))
        self.message_frame.pack_forget()
    
    def load_registered_users(self):
        """Load and display registered users"""
        # Clear existing items
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        # Load users from database
        cursor = self.conn.cursor()
        cursor.execute("SELECT username, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        # Insert users into treeview
        for user in users:
            username, created_at = user
            # Format the date for display
            formatted_date = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y")
            self.user_tree.insert('', tk.END, values=(username, formatted_date))
    
    def start_chat(self):
        """Start chatting with a selected partner"""
        partner = self.partner_entry.get().strip()
        
        if not partner:
            messagebox.showerror("Error", "Please enter a partner username")
            return
        
        if partner == self.current_user:
            messagebox.showerror("Error", "You cannot chat with yourself")
            return
        
        # Check if partner exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (partner,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "User not found")
            return
        
        self.chat_partner = partner
        self.show_chat_area()
    
    def show_chat_area(self):
        """Show the chat display and message entry areas"""
        # Show chat frame
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear previous chat content
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Create chat display area
        self.chat_display = tk.Text(self.chat_frame, height=15, state=tk.DISABLED, wrap=tk.WORD, 
                                   font=("Arial", 11), bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Show message frame
        self.message_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Clear previous message frame content
        for widget in self.message_frame.winfo_children():
            widget.destroy()
        
        # Create message entry
        ttk.Label(self.message_frame, text="Message:").pack(side=tk.LEFT)
        self.message_entry = ttk.Entry(self.message_frame, font=("Arial", 11))
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        
        ttk.Button(self.message_frame, text="Send", style='Accent.TButton', command=self.send_message).pack(side=tk.RIGHT)
        
        # Load chat history
        self.load_chat_history()
    
    def load_chat_history(self):
        """Load and display chat history with the current partner"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sender, message, timestamp FROM messages 
            WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
            ORDER BY timestamp ASC
        """, (self.current_user, self.chat_partner, self.chat_partner, self.current_user))
        
        messages = cursor.fetchall()
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        
        for sender, message, timestamp in messages:
            time_str = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            tag = "me" if sender == self.current_user else "them"
            
            # Configure tags for styling
            if not self.chat_display.tag_names():
                self.chat_display.tag_configure("me", foreground="#2980b9", font=("Arial", 11, "bold"))
                self.chat_display.tag_configure("them", foreground="#27ae60", font=("Arial", 11, "bold"))
            
            self.chat_display.insert(tk.END, f"[{time_str}] {sender}: ", tag)
            self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        """Send a message to the chat partner"""
        message = self.message_entry.get().strip()
        
        if not message:
            return
        
        # Save message to database
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)
        """, (self.current_user, self.chat_partner, message))
        self.conn.commit()
        
        # Clear message entry
        self.message_entry.delete(0, tk.END)
        
        # Reload chat history to show new message
        self.load_chat_history()
    
    def logout(self):
        """Handle user logout"""
        self.current_user = None
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()