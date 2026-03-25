import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
from downloader import InstagramDownloader

class InstagramDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Photo Downloader")
        self.root.geometry("600x650")
        self.root.configure(bg="#fafafa") # Light Instagram-like background

        # Style Configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#fafafa")
        style.configure("TLabel", background="#fafafa", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#262626")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.configure("Download.TButton", background="#0095f6", foreground="white")
        style.map("Download.TButton", background=[('active', '#0074cc')])

        # Main Container
        self.main_container = tk.Frame(root, bg="#fafafa", padx=40, pady=20)
        self.main_container.pack(expand=True, fill="both")

        # Header / Logo Placeholder
        self.header_label = ttk.Label(self.main_container, text="Instagram Downloader", style="Header.TLabel")
        self.header_label.pack(pady=(0, 20))

        # --- Login Section (Card-like) ---
        self.login_card = tk.LabelFrame(self.main_container, text=" Login (Improves Reliability) ", 
                                         bg="white", font=("Segoe UI", 9, "bold"), 
                                         fg="#8e8e8e", padx=15, pady=15, bd=1, relief="solid")
        self.login_card.pack(fill="x", pady=10)

        login_inner = tk.Frame(self.login_card, bg="white")
        login_inner.pack(fill="x")

        ttk.Label(login_inner, text="Username:", background="white").grid(row=0, column=0, sticky="w", pady=5)
        self.login_user = ttk.Entry(login_inner)
        self.login_user.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=5)

        ttk.Label(login_inner, text="Password:", background="white").grid(row=1, column=0, sticky="w", pady=5)
        self.login_pass = ttk.Entry(login_inner, show="*")
        self.login_pass.grid(row=1, column=1, sticky="ew", padx=(5, 10), pady=5)
        
        login_inner.columnconfigure(1, weight=1)

        self.login_btn = ttk.Button(self.login_card, text="Login to Instagram", command=self.do_login)
        self.login_btn.pack(pady=(10, 0), fill="x")

        # --- Target Section ---
        self.target_card = tk.LabelFrame(self.main_container, text=" Target Profile ", 
                                          bg="white", font=("Segoe UI", 9, "bold"), 
                                          fg="#8e8e8e", padx=15, pady=15, bd=1, relief="solid")
        self.target_card.pack(fill="x", pady=20)

        ttk.Label(self.target_card, text="Username to Download From:", background="white").pack(anchor="w")
        self.username_entry = ttk.Entry(self.target_card, font=("Segoe UI", 12))
        self.username_entry.pack(fill="x", pady=10)

        button_frame = tk.Frame(self.target_card, bg="white")
        button_frame.pack(fill="x", pady=5)

        self.download_pic_button = ttk.Button(button_frame, text="DOWNLOAD PROFILE PIC", 
                                          style="Download.TButton", command=self.start_download_pic)
        self.download_pic_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.download_button = ttk.Button(button_frame, text="DOWNLOAD POSTS", 
                                          style="Download.TButton", command=self.start_download)
        self.download_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # --- Status Area ---
        self.status_frame = tk.Frame(self.main_container, bg="#fafafa")
        self.status_frame.pack(fill="both", expand=True)

        self.status_label = ttk.Label(self.status_frame, text="Ready", foreground="#8e8e8e")
        self.status_label.pack(anchor="w", pady=(10, 5))

        self.status_text = tk.Text(self.status_frame, height=8, font=("Consolas", 9), 
                                   bg="#ffffff", fg="#262626", bd=1, relief="solid", padx=10, pady=10)
        self.status_text.pack(fill="both", expand=True)
        
        # Downloader Instance
        self.downloader = InstagramDownloader()
        
        # Check initial login status
        if self.downloader.current_user:
            self.update_status(f"System: Found existing session for '{self.downloader.current_user}'")
            self.status_label.config(text=f"Logged in: {self.downloader.current_user}", foreground="#262626")

    def update_status(self, message):
        self.root.after(0, self._update_status, message)

    def _update_status(self, message):
        self.status_text.insert(tk.END, f"[{message}]\n")
        self.status_text.see(tk.END)
        if ":" in message:
            self.status_label.config(text=message.split(':')[0])

    def do_login(self):
        user = self.login_user.get().strip()
        pw = self.login_pass.get().strip()
        if not user or not pw:
            messagebox.showwarning("Input Required", "Please enter both credentials.")
            return
        
        self.update_status("System: Logging in...")
        def run_login():
            if self.downloader.login(user, pw):
                self.root.after(0, lambda: messagebox.showinfo("Success", "Login successful!"))
                self.root.after(0, lambda: self.status_label.config(text=f"Logged in: {user}", foreground="#262626"))
                self.update_status(f"System: Synchronized session for '{user}'")
            else:
                self.root.after(0, lambda: messagebox.showerror("Failed", "Authentication failed."))
        
        threading.Thread(target=run_login, daemon=True).start()

    def start_download(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Input Error", "Enter a username.")
            return

        self.status_text.delete(1.0, tk.END)
        self.download_button.state(['disabled'])
        threading.Thread(target=self.run_download, args=(username,), daemon=True).start()

    def run_download(self, username):
        try:
            # Sanitization: Extract username from URL if provided
            username = username.strip()
            if "instagram.com/" in username:
                # Handle URLs like https://www.instagram.com/username/ or instagram.com/username
                parts = username.rstrip('/').split('/')
                username = parts[-1]
            
            # Defensive check for repetitions (useruser -> user)
            halflen = len(username) // 2
            if len(username) > 4 and username[:halflen] == username[halflen:]:
                username = username[:halflen]

            success = self.downloader.download_profile_photos(username, callback=self.update_status)
            if success:
                self.root.after(0, lambda: messagebox.showinfo("Finished", f"Successfully saved to downloads/{username}"))
            # downloader.py already sends specific error messages via callback, so we don't need a generic warning
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Fatal Error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.download_button.state(['!disabled']))
            self.root.after(0, lambda: self.download_pic_button.state(['!disabled']))

    def start_download_pic(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Input Error", "Enter a username.")
            return

        self.status_text.delete(1.0, tk.END)
        self.download_button.state(['disabled'])
        self.download_pic_button.state(['disabled'])
        threading.Thread(target=self.run_download_pic, args=(username,), daemon=True).start()

    def run_download_pic(self, username):
        try:
            # Sanitization: Extract username from URL if provided
            username = username.strip()
            if "instagram.com/" in username:
                parts = username.rstrip('/').split('/')
                username = parts[-1]
            
            # Defensive check for repetitions (useruser -> user)
            halflen = len(username) // 2
            if len(username) > 4 and username[:halflen] == username[halflen:]:
                username = username[:halflen]

            success = self.downloader.download_profile_picture(username, callback=self.update_status)
            if success:
                self.root.after(0, lambda: messagebox.showinfo("Finished", f"Successfully saved profile picture for {username}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Fatal Error: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.download_button.state(['!disabled']))
            self.root.after(0, lambda: self.download_pic_button.state(['!disabled']))

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramDownloaderGUI(root)
    root.mainloop()
