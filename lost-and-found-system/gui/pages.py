# gui/pages.py
import customtkinter as ctk
from tkinter import messagebox
from utils.file_handler import save_data, load_data, mark_as_done, delete_item

# --- KARTU BARANG  ---
class ItemCard(ctk.CTkFrame):
    def __init__(self, parent, item_data, refresh_callback):
        super().__init__(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#DDDDDD")
        self.item = item_data
        self.refresh_callback = refresh_callback 
        
        # Ambil data
        status = item_data.get('status', 'Open') # Open atau Selesai
        jenis = item_data.get('jenis', 'Hilang')

        # --- LOGIKA WARNA ---
        # Jika Status SELESAI -> Warna HIJAU (Apapun jenisnya)
        if status == "Selesai":
            main_color = "#2ecc71" # Hijau
            status_text = "SUDAH DIAMBIL / KEMBALI"
        # Jika Masih OPEN dan HILANG -> Warna MERAH
        elif jenis == "Hilang":
            main_color = "#e74c3c" # Merah
            status_text = "SEDANG DICARI (HILANG)"
        # Jika Masih OPEN dan DITEMUKAN -> Warna BIRU
        else:
            main_color = "#3498db" # Biru
            status_text = "DIAMANKAN (DITEMUKAN)"

        # Strip Warna Kiri
        self.strip = ctk.CTkFrame(self, width=15, fg_color=main_color, corner_radius=0)
        self.strip.pack(side="left", fill="y")

        # Container Info Tengah
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)

        # Judul Barang
        ctk.CTkLabel(self.info_frame, text=item_data.get('nama', 'Tanpa Nama'), font=("Arial", 16, "bold"), text_color="#333").pack(anchor="w")
        
        # Detail Status Text (Biar user paham ini statusnya apa)
        ctk.CTkLabel(self.info_frame, text=status_text, font=("Arial", 12, "bold"), text_color=main_color).pack(anchor="w", pady=(0, 5))

        # Detail Lokasi
        kategori = item_data.get('kategori', '-')
        lokasi = item_data.get('lokasi', '-')
        detail_text = f"Lokasi: {lokasi}  |  Kategori: {kategori}"
        ctk.CTkLabel(self.info_frame, text=detail_text, font=("Arial", 12), text_color="#666").pack(anchor="w")
        
        # Waktu
        waktu = item_data.get('waktu', '-')
        ctk.CTkLabel(self.info_frame, text=f"Diposting: {waktu}", font=("Arial", 10), text_color="#999").pack(anchor="w")

        # --- TOMBOL AKSI (KANAN) ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(side="right", padx=15)

        if status == "Open":
            # Kalau masih Open, tombolnya "Tandai Selesai"
            if jenis == "Hilang":
                btn_text = "Saya Sudah Menemukannya"
            else:
                btn_text = "Sudah Diambil Pemilik"
                
            self.btn_action = ctk.CTkButton(
                self.action_frame, 
                text=btn_text, 
                fg_color=main_color, 
                hover_color="#333",
                width=180,
                command=self.tandai_selesai
            )
            self.btn_action.pack(pady=10)
        else:
            # Kalau sudah Selesai (Hijau), tombolnya "Hapus Data"
            ctk.CTkLabel(self.action_frame, text="✅ Masalah Beres", text_color="green", font=("Arial", 12, "bold")).pack()
            
            self.btn_delete = ctk.CTkButton(
                self.action_frame, 
                text="Hapus Data (Arsip)", 
                fg_color="#7f8c8d", # Abu-abu
                hover_color="#c0392b", # Merah pas dihover
                width=150,
                command=self.hapus_permanen
            )
            self.btn_delete.pack(pady=5)

    def tandai_selesai(self):
        # Ubah status jadi Hijau
        mark_as_done(self.item['id'])
        self.refresh_callback() # Refresh halaman otomatis

    def hapus_permanen(self):
        if messagebox.askyesno("Hapus", "Hapus data ini selamanya?"):
            delete_item(self.item['id'])
            self.refresh_callback()


#  HALAMAN DASHBOARD 
class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Hero Section
        self.hero = ctk.CTkFrame(self, fg_color="#1F6AA5", corner_radius=15)
        self.hero.pack(fill="x", pady=20, padx=20)
        
        ctk.CTkLabel(self.hero, text="Dashboard Lost & Found", font=("Arial", 24, "bold"), text_color="white").pack(pady=(20,5))
        ctk.CTkLabel(self.hero, text="Pantau status barang disini", font=("Arial", 14), text_color="#E0E0E0").pack(pady=(0,20))

        # Statistik
        self.stats_container = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_container.pack(pady=10, padx=20, fill="x")
        self.stats_container.grid_columnconfigure((0,1,2), weight=1)

        # Kotak 1: Hilang (Merah)
        self.card_lost = ctk.CTkFrame(self.stats_container, fg_color="#e74c3c", corner_radius=10)
        self.card_lost.grid(row=0, column=0, padx=5, sticky="ew")
        self.lbl_lost = ctk.CTkLabel(self.card_lost, text="0", font=("Arial", 30, "bold"), text_color="white")
        self.lbl_lost.pack(pady=10)
        ctk.CTkLabel(self.card_lost, text="Sedang Dicari", text_color="white").pack(pady=(0,10))

        # Kotak 2: Ditemukan (Biru)
        self.card_found = ctk.CTkFrame(self.stats_container, fg_color="#3498db", corner_radius=10)
        self.card_found.grid(row=0, column=1, padx=5, sticky="ew")
        self.lbl_found = ctk.CTkLabel(self.card_found, text="0", font=("Arial", 30, "bold"), text_color="white")
        self.lbl_found.pack(pady=10)
        ctk.CTkLabel(self.card_found, text="Diamankan", text_color="white").pack(pady=(0,10))

        # Kotak 3: Selesai (Hijau)
        self.card_done = ctk.CTkFrame(self.stats_container, fg_color="#2ecc71", corner_radius=10)
        self.card_done.grid(row=0, column=2, padx=5, sticky="ew")
        self.lbl_done = ctk.CTkLabel(self.card_done, text="0", font=("Arial", 30, "bold"), text_color="white")
        self.lbl_done.pack(pady=10)
        ctk.CTkLabel(self.card_done, text="Kasus Selesai", text_color="white").pack(pady=(0,10))
        
        self.update_stats()

    def update_stats(self):
        data = load_data()
        # Hitung statistik
        lost = len([x for x in data if x.get('jenis') == 'Hilang' and x.get('status') != 'Selesai'])
        found = len([x for x in data if x.get('jenis') == 'Ditemukan' and x.get('status') != 'Selesai'])
        done = len([x for x in data if x.get('status') == 'Selesai'])
        
        self.lbl_lost.configure(text=str(lost))
        self.lbl_found.configure(text=str(found))
        self.lbl_done.configure(text=str(done))


#  HALAMAN LAPOR 
class LaporPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.form_frame.pack(pady=20, padx=40, fill="both", expand=True)

        ctk.CTkLabel(self.form_frame, text="Buat Laporan Baru", font=("Arial", 20, "bold"), text_color="#333").pack(pady=20)

        # Input Nama
        ctk.CTkLabel(self.form_frame, text="Nama Barang", text_color="#333", anchor="w").pack(padx=40, fill="x")
        self.entry_nama = ctk.CTkEntry(self.form_frame, placeholder_text="Contoh: Dompet Coklat")
        self.entry_nama.pack(pady=(5, 15), padx=40, fill="x")

        # Input Kategori
        ctk.CTkLabel(self.form_frame, text="Kategori", text_color="#333", anchor="w").pack(padx=40, fill="x")
        self.kategori_opt = ctk.CTkOptionMenu(self.form_frame, values=["Elektronik", "Dokumen", "Pakaian", "Kunci", "Lainnya"])
        self.kategori_opt.pack(pady=(5, 15), padx=40, fill="x")

        # Input Lokasi
        ctk.CTkLabel(self.form_frame, text="Lokasi", text_color="#333", anchor="w").pack(padx=40, fill="x")
        self.entry_lokasi = ctk.CTkEntry(self.form_frame, placeholder_text="Contoh: Kantin Bengkok")
        self.entry_lokasi.pack(pady=(5, 15), padx=40, fill="x")

        # Kontak
        ctk.CTkLabel(self.form_frame, text="Kontak Anda (WA/Line)", text_color="#333", anchor="w").pack(padx=40, fill="x")
        self.entry_kontak = ctk.CTkEntry(self.form_frame)
        self.entry_kontak.pack(pady=(5, 20), padx=40, fill="x")

        # Radio Button (Pilihan Jenis)
        ctk.CTkLabel(self.form_frame, text="Apa Situasinya?", text_color="#333", anchor="w", font=("Arial", 12, "bold")).pack(padx=40, fill="x")
        
        self.jenis_var = ctk.StringVar(value="Hilang")
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        # Pilihan 1: Saya Kehilangan
        r1 = ctk.CTkRadioButton(btn_frame, text="Saya KEHILANGAN Barang", variable=self.jenis_var, value="Hilang", fg_color="#e74c3c", text_color="#333")
        r1.pack(side="left", padx=20)
        
        # Pilihan 2: Saya Menemukan
        r2 = ctk.CTkRadioButton(btn_frame, text="Saya MENEMUKAN Barang", variable=self.jenis_var, value="Ditemukan", fg_color="#3498db", text_color="#333")
        r2.pack(side="left", padx=20)

        # Submit
        self.btn_submit = ctk.CTkButton(self.form_frame, text="Kirim Laporan", command=self.submit_data, height=45, font=("Arial", 14, "bold"))
        self.btn_submit.pack(pady=30, padx=40, fill="x")

    def submit_data(self):
        nama = self.entry_nama.get()
        lokasi = self.entry_lokasi.get()
        
        if not nama or not lokasi:
            messagebox.showwarning("Gagal", "Nama barang dan lokasi wajib diisi!")
            return

        data_baru = {
            "nama": nama,
            "kategori": self.kategori_opt.get(),
            "lokasi": lokasi,
            "kontak": self.entry_kontak.get(),
            "jenis": self.jenis_var.get(),
            "status": "Open" # Default status selalu Open
        }

        save_data(data_baru)
        messagebox.showinfo("Berhasil", "Laporan tercatat! Cek menu 'Cari Barang'.")
        
        # Reset Form
        self.entry_nama.delete(0, 'end')
        self.entry_lokasi.delete(0, 'end')
        self.entry_kontak.delete(0, 'end')


# --- HALAMAN CARI ---
class CariPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # Filter dan Search
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.pack(pady=10, padx=20, fill="x")

        self.entry_search = ctk.CTkEntry(ctrl_frame, placeholder_text="🔍 Cari nama barang...", width=300)
        self.entry_search.pack(side="left", padx=(0, 10))
        
        # Filter Status (Mau lihat yang Aktif aja atau yang udah Selesai juga)
        self.filter_status = ctk.CTkOptionMenu(ctrl_frame, values=["Semua Status", "Masih Dicari/Ada", "Sudah Selesai"], width=150)
        self.filter_status.set("Semua Status")
        self.filter_status.pack(side="left", padx=10)

        ctk.CTkButton(ctrl_frame, text="Cari / Refresh", width=100, command=self.refresh_list).pack(side="left")

        # Area List Barang
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.refresh_list()

    def refresh_list(self):
        keyword = self.entry_search.get().lower()
        status_filter = self.filter_status.get()
        data = load_data()

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        count = 0
        for item in data:
            nama = item.get('nama', '').lower()
            lokasi = item.get('lokasi', '').lower()
            status = item.get('status', 'Open')
            
            # Logika Filter
            match_keyword = keyword in nama or keyword in lokasi
            
            match_status = True
            if status_filter == "Masih Dicari/Ada" and status == "Selesai":
                match_status = False
            elif status_filter == "Sudah Selesai" and status == "Open":
                match_status = False

            if match_keyword and match_status:
                card = ItemCard(self.scroll_frame, item, self.refresh_list)
                card.pack(pady=5, fill="x")
                count += 1
        
        if count == 0:
            ctk.CTkLabel(self.scroll_frame, text="Belum ada data...", text_color="gray").pack(pady=50)