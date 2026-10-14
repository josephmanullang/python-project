import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo

class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")

        # Text widget sebagai layar terminal
        self.text = tk.Text(
            root,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Consolas", 12),
            wrap="none",
            borderwidth=0,        # hapus border
            highlightthickness=0, # hapus highlight border
            padx=0,               # hapus padding horizontal
            pady=0                # hapus padding vertikal
        )
        self.text.pack(fill="both", expand=True)

        # Style warna
        self.text.tag_config("success", background="green", foreground="white")
        self.text.tag_config("error", background="red", foreground="white")

        # Welcome message
        self.print_line("-"*60 + " WELCOME TO SWIFT NET " + "-"*60)
        self.print_line("$  global_server /start\n")

        # Input login pertama
        self.ask_input("   Login                : ", max_length=15, mask=True, var="login")

    def print_line(self, msg, tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def ask_input(self, prompt, max_length=20, mask=False, var=None):
        self.text.insert("end", prompt)
        self.text.see("end")

        entry = tk.Entry(
            self.text,
            font=("Consolas", 12),
            bg="black",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=max_length
        )
        if mask:
            entry.config(show="*")

        self.text.window_create("end", window=entry)
        entry.focus()

        def process_input(value):
            entry.destroy()
            if mask:
                self.text.insert("end", "*" * len(value) + "\n")
            else:
                self.text.insert("end", value + "\n")
            self.text.see("end")

            # Flow
            if var == "login":
                self.ask_input("   Password             : ", max_length=10, mask=True, var="password")

            elif var == "password":
                self.text.insert("end", "   ")
                self.text.insert("end", "CONNECTED!!!!!", "success")
                self.text.insert("end", "\n")
                now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                self.print_line("$  global_server/download")
                self.ask_input("\n   TRN                                     : ", max_length=20, var="trn")

            elif var == "trn":
                self.text.insert("end", "   ")
                self.text.insert("end", "DATA FOUND!!!!!", "success")
                self.text.insert("end", "\n")
                now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                self.ask_input("   Ready for download (Y/N)                : ", max_length=20, var="opt")

            elif var == "opt":
                if value.strip().lower().startswith("y"):
                    self.text.insert("end", "   ")
                    self.text.insert("end", "USE THE IPIP SYSTEM TO DOWNLOAD!!!!!", "error")
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                else:
                    self.text.insert("end", "   ")
                    self.text.insert("end", "DOWNLOAD CANCELLED!!!!!", "error")
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        def on_enter(event=None):
            process_input(entry.get()[:max_length])

        def on_type(event=None):
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.state("zoomed")          # maximize window (Windows)
    root.bind("<Escape>", lambda e: root.destroy())  # tekan ESC untuk keluar
    app = TerminalGUI(root)
    root.mainloop()