import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo

class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")

        # Text widget terminal
        self.text = tk.Text(root, bg="black", fg="white", insertbackground="white",
                            font=("Consolas", 12), wrap="none")
        self.text.pack(fill="both", expand=True)

        # Tag warna
        self.text.tag_config("success", background="green", foreground="white")

        # Welcome message
        self.print_line("-"*60 + " WELCOME TO SWIFT NET " + "-"*60)
        self.print_line("$  global_server /start\n")

        # Login awal
        self.ask_input("   Login                : ", max_length=15, mask=True, var="login")

    def print_line(self, msg, tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def ask_input(self, prompt, max_length=20, mask=False, var=None):
        self.text.insert("end", prompt)
        self.text.see("end")

        entry = tk.Entry(self.text, font=("Consolas", 12), bg="black", fg="white",
                         insertbackground="white", relief="flat", width=max_length)
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

            # Alur input
            if var == "login":
                self.ask_input("   Password             : ", max_length=10, mask=True, var="password")

            elif var == "password":
                self.text.insert("end", "   ")
                self.text.insert("end", "CONNECTED!!!!!", "success")
                self.text.insert("end", "\n")
                now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                self.print_line("$  global_server/trace")
                self.ask_input("   TRN/UTR              : ", max_length=30, var="trn")

            elif var == "trn":
                # tampilkan hasil trace seperti di gambar
                self.text.insert("end", "\n")
                self.print_line("2026-03-25  O  PAYMENT SENT WITH MT 103 CASH TRANSFER")
                self.print_line("23:00:38    |  SWIFTCODE")
                self.print_line("            |  DEUTSCHE BANK AG")
                self.print_line("            |")
                self.print_line("            |")
                self.print_line("2026-03-25  O  RECEIVED AT COMMON ACCOUNT")
                self.print_line("23:00:38    |  SWIFTCODE")
                self.print_line("            |  KRUNG THAI BANK PUBLIC COMPANY LIMITED")
                self.print_line("            |")
                self.print_line("            |")
                self.print_line("            O  PROCESSING")

        def on_enter(event=None):
            process_input(entry.get()[:max_length])

        def on_type(event=None):
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)


if __name__ == "__main__":
    root = tk.Tk()
    root.bind_all("<KeyPress-Tab>", lambda e: "break")
    root.bind_all("<KeyRelease-Tab>", lambda e: "break")
    root.bind_class("Entry", "<Tab>", lambda e: "break")
    root.bind_class("Text", "<Tab>", lambda e: "break")
    root.attributes("-fullscreen", True)
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())
    app = TerminalGUI(root)
    root.mainloop()
