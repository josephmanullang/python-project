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
        for seq in ("<Button-1>", "<B1-Motion>", "<ButtonRelease-1>", "<Double-Button-1>", "<Triple-Button-1>"):
            self.text.bind(seq, lambda e: "break")

        # Style warna
        self.text.tag_config("success", foreground="white", background="green")  # balik ke background hijau
        self.text.tag_config("error", foreground="#E4B071", background="black")
        self.text.tag_config("download", foreground="white", background="black")

        # Welcome message
        self.print_line("-"*60 + " WELCOME TO SWIFT NET " + "-"*60)
        self.print_line("$  global_server /start\n")

        # Input login pertama
        self.ask_input("   Login                               : ", max_length=15, mask=True, var="login")

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

            # Flow
            if var == "login":
                self.ask_input("   Password                            : ", max_length=10, mask=True, var="password")

            elif var == "password":
                # Delay 5 detik sebelum CONNECTED
                def show_connected():
                    self.text.insert("end", "   ")
                    self.text.insert("end", "CONNECTED..... ", "success")  # bg hijau
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   2026-04-03 17:16:40" + "\n")

                    # Delay 3 detik sebelum $ global_server /search
                    def show_search():
                        self.print_line("$  global_server /search")
                        self.ask_input("\n   TRN                                 : ", max_length=100, var="trn")

                    self.root.after(3000, show_search)

                self.root.after(5000, show_connected)

            elif var == "trn":
                def show_data_found():
                    self.text.insert("end", "   ")
                    self.text.insert("end", "DATA FOUND!!!!!", "success")  # bg hijau
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   2026-04-03 17:19:46" + "\n")
                    self.ask_input("   Ready for download (Y/N)            : ", max_length=20, var="opt")

                self.root.after(3000, show_data_found)

            elif var == "opt":
                if value.strip().lower().startswith("y"):
                    # label "DOWNLOADING"
                    self.text.insert("end", "="*62 + " ")
                    self.downloading_label = tk.Label(
                        self.text,
                        text="DOWNLOADING",
                        font=("Consolas", 12),
                        fg="#FFD580",  # emas → font color
                        bg="black",
                        bd=0,
                        highlightthickness=0
                    )
                    self.text.window_create("end", window=self.downloading_label)
                    self.text.insert("end", " " + "="*66 + "\n")
                    self.start_download(3)
                else:
                    self.print_line("   DOWNLOAD CANCELLED!!!!!", "error")

            elif var == "release1":
                if value.strip() == "2":
                    # tandai datang dari pilihan 2
                    self.from_two = True

                    # tampilkan waiting message
                    self.text.insert("end", "   ")
                    self.text.insert("end", "WAITING FOR THE SENDER'S RESPONSE!!!!!", "error")
                    self.text.insert("end", "\n")
                    now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                    self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")

                    # minta input KEY lagi
                    self.ask_input("   KEY          : ", max_length=50, var="release1")

                elif value.strip() == "1":
                    # pilih 1 → set max_attempts
                    if not hasattr(self, "from_two") or not self.from_two:
                        self.max_attempts = 3
                    else:
                        self.max_attempts = 2
                    self.code_attempts = 0
                    self.ask_input("\n   RELEASE CODE : ", max_length=100, var="code")

                else:
                    self.print_line("   INVALID OPTION!!!!!", "error")
                    self.ask_input("   KEY          : ", max_length=100, var="release1")

            elif var == "code":
                self.handle_code(value)

        def on_enter(event=None):
            process_input(entry.get()[:max_length])

        def on_type(event=None):
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)

    def start_download(self, percent=0):
        if percent == 3:
            left = f"{'='*62} "
            right = f" {'='*66}\n"

            # kiri
            self.text.insert("end", left, "download")

            # label persen dengan width tetap (supaya flex)
            self.percent_label = tk.Label(
                self.text,
                text=f"{percent}%".center(7),   # teks dirata tengah
                font=("Consolas", 12),
                fg="#E4B071",   # emas → font color
                bg="black",
                bd=0,
                highlightthickness=0,
                width=11,
                anchor="center"
            )
            self.text.window_create("end", window=self.percent_label)

            # kanan
            self.text.insert("end", right, "download")
            self.text.see("end")
            now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
            #awal download
            self.text.insert("end", "   2026-04-03 17:20:15" + "\n")
        else:
            if hasattr(self, "percent_label") and self.percent_label:
                if percent == 100:
                    # selesai → hijau
                    self.percent_label.config(
                        text=f"{percent}%".center(7),
                        fg="#A8DB9D",
                        bg="black"
                    )
                    self.downloading_label.config(fg="#A8DB9D", bg="black")
                else:
                    # progress → emas
                    self.percent_label.config(
                        text=f"{percent}%".center(7),
                        fg="#FFD580",
                        bg="black"
                    )
                    self.downloading_label.config(fg="#FFD580", bg="black")

                self.text.see("end")
            else:
                self.start_download(0)

        if percent < 100:
            # 30 detik per 1%
            self.root.after(300000, lambda: self.start_download(percent + 1))
        else:
            # selesai
            self.text.insert("end", "\n   ")
            completed_label = tk.Label(
                self.text,
                text="DOWNLOAD COMPLETED!!!!!",
                font=("Consolas", 12),
                fg="#A8DB9D",   # font hijau
                bg="black",
                bd=0,
                highlightthickness=0
            )
            self.text.window_create("end", window=completed_label)
            self.text.insert("end", "\n")

            now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
            self.text.insert("end", "   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")

            self.text.after(300, self.show_key_menu)

    def show_key_menu(self):
        self.from_two = False  # default dari awal
        self.print_line("\n   [1] Input Code")
        self.print_line("   [2] Windows Time\n")
        self.ask_input("   KEY          : ", max_length=20, var="release1")

    def handle_code(self, value):
        # cek jumlah percobaan
        if not hasattr(self, "code_attempts"):
            self.code_attempts = 0
        self.code_attempts += 1

        def show_invalid():
            if self.code_attempts >= self.max_attempts:
                # sudah melewati batas → blocked
                self.text.insert("end", "   ")
                self.text.insert("end", "INVALID CODE!!!!!", "error")
                self.text.insert("end", "\n   ")
                self.text.insert("end", "TRANSACTION HAS BEEN BLOCKED!!!!!", "error")
                self.text.insert("end", "\n")
                now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            else:
                # masih ada kesempatan
                self.text.insert("end", "   ")
                self.text.insert("end", "INVALID CODE!!!!!", "error")
                self.text.insert("end", "\n")
                now_sg = datetime.now(ZoneInfo("Asia/Singapore"))
                self.print_line("   " + now_sg.strftime("%Y-%m-%d %H:%M:%S") + "\n")
                self.ask_input("   RELEASE CODE : ", max_length=100, var="code")
            self.root.after(2000, show_invalid)


if __name__ == "__main__":
    root = tk.Tk()
    root.bind_all("<KeyPress-Tab>", lambda e: "break")
    root.bind_all("<KeyRelease-Tab>", lambda e: "break")
    root.bind_class("Entry", "<Tab>", lambda e: "break")
    root.bind_class("Text", "<Tab>", lambda e: "break")
    root.attributes("-fullscreen", True)
    root.state("zoomed")          # maximize window (Windows)
    root.bind("<Escape>", lambda e: root.destroy())  # tekan ESC untuk keluar
    app = TerminalGUI(root)
    root.mainloop()
