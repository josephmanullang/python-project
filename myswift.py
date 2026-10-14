import tkinter as tk
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================================
#  TIMING (mengikuti file python kamu)
# =========================================================
CONNECT_DELAY        = 5000      # jeda setelah input password -> SYSTEM CONNECTED (py: 5000)
AFTER_CONNECT_DELAY  = 3000      # jeda setelah CONNECTED -> lanjut section (py: 3000)
AUTO_MIN, AUTO_MAX   = 2000, 4000  # auto-enter Profile..Create Transaction (random 2-4 dtk)
TRN_DELAY            = 3000      # jeda setelah input TRN -> TRANSACTION FOUND (py: data found 3000)
FOUND_DELAY          = 3000      # jeda setelah TRANSACTION FOUND -> Proceed
AUTH_DELAY           = 2000      # jeda setelah input auth -> INVALID (py: handle_code 2000)

# Processing Status mengikuti KONSEP DOWNLOAD di file py:
#   py -> self.root.after(300000, start_download(percent+1))  (= 5 menit per 1%)
# NOTE: 300000ms = 5 menit per 1% -> 0..100% makan waktu sangat lama.
#       Ganti angka ini kalau mau lebih cepat (mis. 30000 = 30 dtk/1%).
PROC_INTERVAL        = 300000

USERPASS_LEN         = 15        # length User ID & Password disamakan
LABEL_WIDTH          = 25        # supaya semua titik dua ( : ) sejajar

TZ = ZoneInfo("Asia/Kuala_Lumpur")


class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")

        # ---- Layar terminal (identik dgn file py kamu) ----
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

        # matikan cursor / seleksi mouse
        for seq in ("<Button-1>", "<B1-Motion>", "<ButtonRelease-1>",
                    "<Double-Button-1>", "<Triple-Button-1>"):
            self.text.bind(seq, lambda e: "break")

        # ---- warna teks ----
        self.text.tag_config("green", foreground="#3EE06E", background="black")
        self.text.tag_config("red",   foreground="#FF5252", background="black")
        self.text.tag_config("gold",  foreground="#FFD580", background="black")

        # ---- Header (dari foto) ----
        self.print_line("SWIFT ALLIANCE ACCESS")
        self.print_line("MX PAYMENT MONITOR ISO 20022")
        self.print_line("")
        self.print_line("Secure System Access")

        # ---- mulai: Secure System Access ----
        self.ask_input(self.prompt("User ID"), max_length=USERPASS_LEN, mask=True, var="userid")

    # =====================================================
    #  Helpers
    # =====================================================
    def prompt(self, label):
        """Format label supaya titik dua sejajar semua."""
        return "   " + label.ljust(LABEL_WIDTH) + ": "

    def print_line(self, msg, tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def stamp_line(self, tag="green"):
        """Baris tanggal + waktu realtime. Default hijau, kirim 'red' utk kasus error."""
        ts = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        self.text.insert("end", "   " + ts + "\n", tag)
        self.text.see("end")

    # =====================================================
    #  Input inline (mekanik dari file py + auto uppercase)
    # =====================================================
    def ask_input(self, prompt, max_length=20, mask=False, uppercase=False, var=None):
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
            self.dispatch(var, value)

        def on_enter(event=None):
            process_input(entry.get()[:max_length])

        def on_type(event=None):
            if uppercase:
                cur = entry.get()
                up = cur.upper()
                if up != cur:
                    entry.delete(0, "end")
                    entry.insert(0, up)
            if len(entry.get()) >= max_length:
                process_input(entry.get()[:max_length])

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)

    # =====================================================
    #  Alur utama
    # =====================================================
    def dispatch(self, var, value):
        if var == "userid":
            self.ask_input(self.prompt("Password"), max_length=USERPASS_LEN, mask=True, var="password")

        elif var == "password":
            self.root.after(CONNECT_DELAY, self.show_connected)

        elif var == "trn":
            self.root.after(TRN_DELAY, self.show_transaction_found)

        elif var == "proceed":
            self.handle_proceed(value)

        elif var == "auth":
            self.handle_auth(value)

    # ---- 3) SYSTEM CONNECTED (hijau) + jeda lalu lanjut ----
    def show_connected(self):
        self.print_line("   SYSTEM CONNECTED", "green")
        self.stamp_line("green")
        self.root.after(AFTER_CONNECT_DELAY, self.show_dashboard)

    # ---- 4) Payments Operations Dashboard Monitor ----
    def show_dashboard(self):
        self.text.insert("end", "\n")
        self.print_line("Payments Operations Dashboard Monitor")

        # Profile .. Create Transaction -> input otomatis,
        # tapi tetap tampil cursor "I" kedap-kedip seperti input teks.
        steps = ["Profile", "Transaction History", "Create Transaction"]

        def do_step(i):
            if i < len(steps):
                # tampilkan prompt lalu munculkan cursor kedip (auto, tanpa ketikan)
                self.text.insert("end", self.prompt(steps[i]))
                self.text.see("end")

                entry = tk.Entry(
                    self.text, font=("Consolas", 12),
                    bg="black", fg="white",
                    insertbackground="white",      # warna cursor "I"
                    relief="flat", width=2,
                    insertontime=600, insertofftime=400  # efek kedap-kedip
                )
                self.text.window_create("end", window=entry)
                entry.focus()
                entry.bind("<Key>", lambda e: "break")  # blok ketikan manual (tetap otomatis)

                def finish():
                    entry.destroy()
                    self.text.insert("end", "\n")
                    self.text.see("end")
                    do_step(i + 1)

                self.root.after(random.randint(AUTO_MIN, AUTO_MAX), finish)
            else:
                # Transaction Tracking = input manual (length ikut INPUT TRN = 100)
                self.ask_input(self.prompt("Transaction Tracking"), max_length=100, var="trn")

        do_step(0)

    # ---- 5) TRANSACTION FOUND (hijau) s/d Amount + REALTIME ----
    def show_transaction_found(self):
        self.text.insert("end", "\n")
        self.print_line("   TRANSACTION FOUND", "green")   # hijau
        # Message Type s/d Amount -> PUTIH (tanpa tag)
        for lbl in ["Message Type", "Bank Name", "Swift Code", "Country", "Currency", "Amount"]:
            self.text.insert("end", self.prompt(lbl) + "\n")   # putih
            self.text.see("end")
        self.stamp_line()   # waktu di bawah Amount -> hijau

        # jeda (ikut data found) lalu Proceed
        self.root.after(FOUND_DELAY, self.show_proceed)

    def show_proceed(self):
        self.text.insert("end", "\n")
        self.ask_input(self.prompt("Proceed (Y/N)"), max_length=3, uppercase=True, var="proceed")

    # ---- 6) Proceed -> Processing Status (konsep download) ----
    def handle_proceed(self, value):
        if value.strip().upper().startswith("Y"):
            self.stamp_line()
            self.start_processing(0)
        else:
            self.text.insert("end", "\n")
            self.print_line("   PROCESS CANCELLED!!!!!", "red")
            self.stamp_line("red")

    def start_processing(self, percent=0):
        if percent == 0:
            self.text.insert("end", "\n   ")
            self.proc_label = tk.Label(
                self.text,
                text="Processing Status  ( 0% )",
                font=("Consolas", 12),
                fg="#FFD580",          # emas saat berjalan
                bg="black", bd=0, highlightthickness=0, anchor="w"
            )
            self.text.window_create("end", window=self.proc_label)
            self.text.insert("end", "\n")
            self.text.see("end")
        else:
            self.proc_label.config(text=f"Processing Status  ( {percent}% )")
            if percent == 100:
                self.proc_label.config(fg="#3EE06E")   # hijau saat selesai
            self.text.see("end")

        if percent < 100:
            self.root.after(PROC_INTERVAL, lambda: self.start_processing(percent + 1))
        else:
            self.print_line("   Completed", "green")   # pepet ke atas, tanpa space
            self.stamp_line("green")
            self.root.after(1500, self.show_security)

    # ---- 7) Payment Security Verification (selalu INVALID / merah) ----
    def show_security(self):
        self.auth_attempts = 0
        self.max_auth = 3   # konsep release code (3x percobaan)
        self.text.insert("end", "\n")
        self.print_line("Payment Security Verification")
        self.ask_input(self.prompt("Authentication Required"), max_length=50, var="auth")

    def handle_auth(self, value):
        self.auth_attempts += 1

        def show_result():
            self.print_line("   INVALID", "red")
            if self.auth_attempts >= self.max_auth:
                # INVALID -> langsung TRANSACTION BLOCKED -> timestamp (semua merah, tanpa jarak)
                self.print_line("   TRANSACTION BLOCKED!!!!!", "red")
                self.stamp_line("red")
            else:
                self.stamp_line("red")   # waktu di bawah INVALID -> merah
                self.text.insert("end", "\n")
                self.ask_input(self.prompt("Authentication Required"), max_length=50, var="auth")

        self.root.after(AUTH_DELAY, show_result)


if __name__ == "__main__":
    root = tk.Tk()
    # matikan Tab (persis file py kamu)
    root.bind_all("<KeyPress-Tab>", lambda e: "break")
    root.bind_all("<KeyRelease-Tab>", lambda e: "break")
    root.bind_class("Entry", "<Tab>", lambda e: "break")
    root.bind_class("Text", "<Tab>", lambda e: "break")
    root.attributes("-fullscreen", True)
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())
    app = TerminalGUI(root)
    root.mainloop()