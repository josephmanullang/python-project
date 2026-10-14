import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo


class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")
        self.root.attributes("-fullscreen", True)
        self.root.state("zoomed")
        self.root.bind("<Escape>", lambda e: root.destroy())

        # Text widget sebagai layar terminal
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

        # Kunci supaya tidak bisa di-drag select
        for seq in (
            "<Button-1>",
            "<B1-Motion>",
            "<ButtonRelease-1>",
            "<Double-Button-1>",
            "<Triple-Button-1>",
        ):
            self.text.bind(seq, lambda e: "break")

        # Style warna
        self.text.tag_config("success", background="green", foreground="white")
        self.text.tag_config("error", background="red", foreground="white")
        self.text.tag_config("gray", foreground="#BFBFBF")
        self.text.tag_config("white", foreground="white")

        # Data tabel
        self.rows = [
            ("  75Q362597GH1436859", "  EUR", "  1,000,000,000.00", "  2026-05-18 20:20:51"),
            ("  R8X4K9T2M7Q5L3PA", "  EUR", "  100,000,000.00", "  2026-04-17 18:24:39"),
            ("  CH33116861727855", "  EUR", "  1,000,000,000.00", "  2026-04-11 16:29:18"),
            ("  UBSW321556789997H", "  EUR", "  790,911,000.00", "  2026-02-26 10:11:37"),
            ("  HSBC2819Q9288F19928", "  USD", "  21,000,000.00", "  2026-01-09 16:50:23"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-07-13 09:21:54"),
            ("  DBS920192G291Y2819", "  USD", "  1,800,000.00", "  2025-12-28 13:47:41"),
        ]

        self.draw_screen()

    def print_line(self, msg="", tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def draw_screen(self):
        banner = "   " + "-" * 55 + " WELCOME TO SWIFT NET " + "-" * 60
        self.print_line(banner, "white")
        self.print_line("")
        self.print_line("   $  global_server /start", "white")
        self.print_line("")
        self.ask_input("      Login                               : ", max_length=15, mask=True, var="login")

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

            if var == "login":
                self.ask_input("      Password                            : ", max_length=10, mask=True, var="password")

            elif var == "password":
                def show_connected():
                    self.text.insert("end", "      ")
                    self.text.insert("end", "CONNECTED..... ", "success")
                    self.text.insert("end", "\n")

                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("      " + now_sg.strftime("%Y-%m-%d %H:%M:%S"))

                    self.print_line("")
                    self.print_line("")

                    def show_search():
                        
                        self.print_line("   $  global_server /search", "white")
                        self.print_line("      |")
                        self.print_line("      Pending Balance")
                        self.print_line("      |")
                        self.show_table()

                    self.root.after(3000, show_search)

                self.root.after(5000, show_connected)

        def on_enter(event=None):
            process_input(entry.get()[:max_length])
            return "break"

        def on_type(event=None):
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])
                return "break"

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)

    def show_table(self):
        self.print_line(
            "           TRN                         "
            "   CURRENCY     "
            "   AMOUNT              "
            "  TIME"
        )

        for trn, curr, amount, time in self.rows:
            line = (
                f"         "
                f"{trn:<28}"
                f"   {curr:<13}"
                f"   {amount:<22}"
                f"{time}"
            )
            self.print_line(line)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())
    app = TerminalGUI(root)
    root.mainloop()