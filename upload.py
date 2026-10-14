import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo

class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")

        self.text = tk.Text(
            root,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Consolas", 12),
            wrap="none",
            borderwidth=0,
            highlightthickness=0,
            padx=0,               
            pady=0 
        )
        self.text.pack(fill="both", expand=True)
        for seq in ("<Button-1>", "<B1-Motion>", "<ButtonRelease-1>", "<Double-Button-1>", "<Triple-Button-1>"):
            self.text.bind(seq, lambda e: "break")

        # Style warna
        self.text.tag_config("success", background="green", foreground="white")
        self.text.tag_config("error", background="red", foreground="white")
        self.text.tag_config("upload", foreground="white")

        # Welcome message
        self.print_line("-"*60 + " WELCOME TO SWIFT NET " + "-"*60)
        self.print_line("")
        self.print_line("$  global_server /start\n")

        self.ask_input("   Login                               : ", max_length=15, mask=True, var="login")

    def print_line(self, msg, tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def print_field(self, label, value, width=142):
        prefix = label + "            : "
        indent = " " * len(prefix)

        words = value.split()
        lines = []
        current_line = ""

        for word in words:
            if len(prefix + current_line + word) <= width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())

        # baris pertama
        self.print_line(prefix + lines[0])

        # baris berikutnya (indent)
        for line in lines[1:]:
            self.print_line(indent + line)

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

            # Flow
            if var == "login":
                self.ask_input("   Password                            : ", max_length=10, mask=True, var="password")

            elif var == "password":
                def show_connected():
                    self.text.insert("end", "   ")
                    self.text.insert("end", "CONNECTED..... ", "success")
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    def swift_input():
                        self.print_line("$  global_server /start")
                        self.print_line("")
                        self.print_line("   SWIFT INPUT                         : GPI MT103 CASH TRANSFER")
                        self.print_line("   ***BANK SENDER                      : DEUTSCHE BANK AG")
                        self.print_line("   ***BANK ADDRESS SENDER              : TAUNUSANLAGE 12 60262, FRANKFURT AM MAIN, GERMANY")
                        self.print_line("   ***ACCOUNT NAME                     : CARLO DAMANTI")
                        self.print_line("   ***SWIFT CODE                       : DEUTDEFFXXX")
                        self.print_line("   ***AMOUNT                           : 3,000,000,000")
                        self.print_line("   ***CURRENCY                         : USD")
                        self.print_line(" ")
                        self.print_line(142*"-")
                        self.print_line(" ")
                        self.print_line("   ***BANK RECEIVER                    : KRUNG THAI BANK PUBLIC COMPANY LIMITED")
                        self.print_field("   ***BANK ADDRESS RECEIVER",
                                         "435 PHAHONYOTHIN RD., ANUSAWARI SUB-DISTRICT, BANGKHEN DISTRICT, BANGKOK, THAILAND 10220 ZIPCODE")
                        self.print_line("   ***ACCOUNT NAME                     : MR.MANGKON MANGKONKAEO")
                        self.print_line("   ***ACCOUNT NUMBER                   : 899000002518")
                        self.print_line("   ***SWIFT CODE                       : KRTHTHBK")
                        self.print_line("   ***DESCRIPTION                      : INVESTMENT")
                        self.ask_input("\n   UPLOAD CONFIRMATION (Y/N) : ", max_length=5, var="opt")
                    self.root.after(5000, swift_input)
                self.root.after(5000, show_connected)
            elif var == "opt":
                if value.strip().lower().startswith("y"):
                    self.text.insert("end", "\n")
                    self.text.insert("end", "="*65 + " ")
                    self.uploading_label = tk.Label(
                        self.text,
                        text="UPLOADING",
                        font=("Consolas", 12),
                        fg="#E4B071",
                        bg="black",
                        bd=0,
                        highlightthickness=0
                    )
                    self.text.window_create("end", window=self.uploading_label)
                    self.text.insert("end", " " + "="*66 + "\n")
                    self.start_upload()
                else:
                    self.print_line("UPLOAD CANCELLED!!!!!", "error")

        def on_enter(event=None):
            process_input(entry.get()[:max_length])

        def on_type(event=None):
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)

    def start_upload(self, percent=0):
        if percent == 0:
            left = f"{'='*65} "
            right = f" {'='*66}\n"

            # kiri
            self.text.insert("end", left, "upload")

            # label persen dengan width tetap
            self.percent_label = tk.Label(
                self.text,
                text=f"{percent}%".center(7),   # teks dipaksa rata tengah
                font=("Consolas", 12),
                fg="#E4B071",
                bg="black",
                bd=0,
                highlightthickness=0,
                width=9,            # fix width supaya stabil
                anchor="center"
            )
            self.text.window_create("end", window=self.percent_label)

            # kanan
            self.text.insert("end", right, "upload")
            self.text.see("end")
            now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
            self.text.insert("end", "   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        else:
            if hasattr(self, "percent_label") and self.percent_label:
                if percent == 100:
                    self.percent_label.config(text=f"{percent}%".center(7), fg="#A8DB9D", bg="black")
                    self.uploading_label.config(fg="#A8DB9D", bg="black")
                else:
                    self.percent_label.config(text=f"{percent}%".center(7), fg="#E4B071", bg="black")
                    self.uploading_label.config(fg="#E4B071", bg="black")

                self.text.see("end")
            else:
                self.start_upload(0)

        if percent < 100:
            self.root.after(600000, lambda: self.start_upload(percent + 1))
        else:
            self.text.insert("end", "\n   ")
            completed_label = tk.Label(
                self.text,
                text="UPLOAD COMPLETED!!!!!",
                font=("Consolas", 12),
                fg="#A8DB9D",
                bg="black",
                bd=0,
                highlightthickness=0
            )
            self.text.window_create("end", window=completed_label)
            self.text.insert("end", "\n")
            now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
            self.text.insert("end", "   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")

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
