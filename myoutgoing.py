import tkinter as tk
import random
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================================
#  TIMING
# =========================================================
CONNECT_DELAY        = 5000       # jeda setelah password -> SYSTEM CONNECTED
AFTER_CONNECT_DELAY  = 3000       # jeda setelah CONNECTED -> dashboard
AUTO_MIN, AUTO_MAX   = 2000, 4000 # kedap-kedip tiap step dashboard (random 2-4 dtk)
DETAILS_DELAY        = 3000       # jeda setelah input Transaction ID -> Transaction Details

# Processing Status (konsep download, sama seperti myswift):
#   300000ms = 5 menit per 1% -> 0..100% lama sekali.
#   Ganti mis. 30000 (30 dtk/1%) atau 3000 (3 dtk/1%) kalau mau cepat.
PROC_INTERVAL        = 300000

USERID_LEN           = 7          # length User ID
PASS_LEN             = 12         # length Password
USERPASS_LEN         = 100        # length input Transaction ID
LABEL_WIDTH          = 28         # supaya semua titik dua ( : ) sejajar

TZ = ZoneInfo("Asia/Kuala_Lumpur")


class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MySwift")

        # ---- Layar terminal ----
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

        # ---- Header ----
        self.print_line("SWIFT ALLIANCE ACCESS")
        self.print_line("MX PAYMENT MONITOR ISO 20022")
        self.print_line("")
        self.print_line("Secure System Access")

        # ---- mulai: Secure System Access ----
        self.ask_input(self.prompt("User ID"), max_length=USERID_LEN, mask=True, var="userid")

    # =====================================================
    #  Helpers
    # =====================================================
    def prompt(self, label):
        """Format label supaya titik dua sejajar semua."""
        return "   " + label.ljust(LABEL_WIDTH) + ": "

    def print_line(self, msg, tag=None):
        self.text.insert("end", msg + "\n", tag)
        self.text.see("end")

    def field(self, label, value="", tag=None):
        """Baris 'label : value' dengan titik dua sejajar (putih by default)."""
        self.text.insert("end", self.prompt(label) + value + "\n", tag)
        self.text.see("end")

    def stamp_line(self, tag="green"):
        """Baris tanggal + waktu realtime (Kuala Lumpur). Default hijau, 'red' utk error."""
        ts = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        self.text.insert("end", "   " + ts + "\n", tag)
        self.text.see("end")

    # =====================================================
    #  Input inline
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

    def blink_cursor(self, on_done):
        """Buat 1 cursor 'I' kedap-kedip (auto) di posisi 'end', random 2-4 dtk,
        lalu panggil on_done()."""
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
            on_done()

        self.root.after(random.randint(AUTO_MIN, AUTO_MAX), finish)

    def activate_create_input(self):
        """Setelah semua kedap-kedip, user input di Transaction ID (tampil biasa)."""
        entry = tk.Entry(self.text, font=("Consolas", 12), bg="black", fg="white",
                         insertbackground="white", relief="flat", width=USERPASS_LEN)
        self.text.window_create("tid_mark", window=entry)
        entry.focus()

        def submit(value):
            value = value[:USERPASS_LEN]
            entry.destroy()
            self.text.insert("tid_mark", value)
            self.text.see("end")
            self.message_id = value
            self.root.after(DETAILS_DELAY, self.show_transaction_details)  # jeda 3 dtk

        def on_enter(event=None):
            submit(entry.get())

        def on_type(event=None):
            if len(entry.get()) >= USERPASS_LEN:
                submit(entry.get())

        entry.bind("<Return>", on_enter)
        entry.bind("<KeyRelease>", on_type)

    # =====================================================
    #  Alur utama
    # =====================================================
    def dispatch(self, var, value):
        if var == "userid":
            self.ask_input(self.prompt("Password"), max_length=PASS_LEN, mask=True, var="password")

        elif var == "password":
            self.root.after(CONNECT_DELAY, self.show_connected)

    # ---- SYSTEM CONNECTED (hijau) + jeda lalu dashboard ----
    def show_connected(self):
        self.print_line("   SYSTEM CONNECTED", "green")
        self.stamp_line("green")
        self.root.after(AFTER_CONNECT_DELAY, self.show_dashboard)

    # ---- Payment Operations Dashboard ----
    def show_dashboard(self):
        self.text.insert("end", "\n")
        self.print_line("Payment Operations Dashboard")

        # Kedap-kedip dulu (auto) utk SEMUA step: Profile -> Transaction History
        # -> Transaction ID -> Transaction Tracking.
        # Baru setelah itu user input di Transaction ID.
        steps = ["Profile", "Transaction History", "Transaction ID", "Transaction Tracking"]

        def do_step(i):
            if i < len(steps):
                self.text.insert("end", self.prompt(steps[i]))
                if steps[i] == "Transaction ID":
                    # tandai posisi utk input user (dipakai setelah semua kedap-kedip)
                    self.text.mark_set("tid_mark", "end-1c")
                    self.text.mark_gravity("tid_mark", "left")
                self.text.see("end")
                self.blink_cursor(lambda: do_step(i + 1))
            else:
                # semua sudah kedap-kedip -> user input di Transaction ID
                self.activate_create_input()

        do_step(0)

    # ---- Transaction Details ----
    def show_transaction_details(self):
        self.text.insert("end", "\n")              # jarak 1 line dgn Transaction Tracking
        self.print_line("Transaction Details")     # pepet ke kiri screen

        now_kl = datetime.now(TZ)

        # Message ID s/d Value Date
        self.field("Message ID",   self.message_id)
        self.field("Message Type", "MX pacs.008")
        self.field("Direction",    "Outgoing")
        # Status pakai Label supaya bisa berubah saat Completed
        self.text.insert("end", self.prompt("Status"))
        self.status_label = tk.Label(
            self.text, text="In Progress",
            font=("Consolas", 12), fg="white", bg="black",
            bd=0, highlightthickness=0, anchor="w"
        )
        self.text.window_create("end", window=self.status_label)
        self.text.insert("end", "\n")
        self.field("Time",         now_kl.strftime("%H:%M:%S"))   # realtime KL, jam:menit:detik, putih
        self.field("Value Date",   now_kl.strftime("%d %b %Y"))   # tanggal realtime KL

        # Sender side
        self.field("Sender's Correspondent", "Deutsche Bank AG")
        self.field("Sender's Bank Address", "Taunusanlage 12 60262, Frankfurt Am Main, Germany")
        self.field("Account Name",           "Carlo Damanti")
        self.field("BIC/SWIFT Code",                  "DEUTDEFFXXX")
        self.field("Currency",               "USD")
        self.field("Amount",                 "3,000,000,000")
        # Receiver side (nempel ke Currency, tanpa garis pemisah)
        self.field("Receiver's Correspondent", "Krung Thai Bank Public Company Limited")
        self.field("Receiver's Bank Address", "435 Phahonyothin Rd., Anusawari Sub-District, "
                                             "Bangkhen District, Bangkok, Thailand 10220 Zipcode")
        self.field("Account Name",            "Mr.Mangkon Mangkonkaeo")
        self.field("Account Number",          "899000002518")
        self.field("BIC/SWIFT Code",                   "KRTHTHBK")

        # flow berhenti di sini
        self.status_label.config(text="Received at Common Account")


if __name__ == "__main__":
    root = tk.Tk()
    # matikan Tab
    root.bind_all("<KeyPress-Tab>", lambda e: "break")
    root.bind_all("<KeyRelease-Tab>", lambda e: "break")
    root.bind_class("Entry", "<Tab>", lambda e: "break")
    root.bind_class("Text", "<Tab>", lambda e: "break")
    root.attributes("-fullscreen", True)
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())
    app = TerminalGUI(root)
    root.mainloop()