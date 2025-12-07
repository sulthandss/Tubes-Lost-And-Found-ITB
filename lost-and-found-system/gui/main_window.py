import customtkinter as ctk
from config.settings import APP_TITLE, WINDOW_SIZE
from gui.pages import DashboardPage, LaporPage, CariPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Utama
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        
        # Layout Grid: 2 Kolom (Sidebar kiri, Konten kanan)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (KIRI) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ITB L&F", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tombol Navigasi
        self.btn_dash = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.btn_dash.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_lapor = ctk.CTkButton(self.sidebar_frame, text="Lapor Barang", command=self.show_lapor)
        self.btn_lapor.grid(row=2, column=0, padx=20, pady=10)

        self.btn_cari = ctk.CTkButton(self.sidebar_frame, text="Cari Barang", command=self.show_cari)
        self.btn_cari.grid(row=3, column=0, padx=20, pady=10)

        # --- AREA KONTEN (KANAN) ---
        self.dashboard_frame = DashboardPage(self)
        self.lapor_frame = LaporPage(self)
        self.cari_frame = CariPage(self)
        self.show_dashboard()

    def hide_all_frames(self):
        """Menyembunyikan semua halaman sebelum menampilkan yang baru"""
        self.dashboard_frame.grid_forget()
        self.lapor_frame.grid_forget()
        self.cari_frame.grid_forget()

    def show_dashboard(self):
        self.hide_all_frames()
        self.dashboard_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        # Update statistik saat dashboard dibuka
        self.dashboard_frame.update_stats()

    def show_lapor(self):
        self.hide_all_frames()
        self.lapor_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_cari(self):
        self.hide_all_frames()
        self.cari_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)