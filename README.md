# 🏫 Campus Lost & Found System

> Sistem Pelaporan Barang Hilang dan Temuan berbasis Python & GUI Modern.
> **Tugas Besar Pengenalan Komputasi - Institut Teknologi Bandung**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📖 Deskripsi Projek
Aplikasi ini dirancang untuk mempermudah mahasiswa dalam melaporkan barang yang hilang atau menemukan barang tertinggal di area kampus. Menggunakan pendekatan **Computational Thinking** (Dekomposisi, Abstraksi, Algoritma) dan antarmuka modern yang ramah pengguna.

**Masalah:** Informasi barang hilang sering tertumpuk di chat grup.
**Solusi:** Sentralisasi data dengan fitur pencarian dan status klaim yang real-time.

---

## 📸 Tampilan Aplikasi (Screenshot)


### 1. Dashboard Statistik
Menampilkan ringkasan jumlah barang hilang vs ditemukan secara real-time.
![Dashboard View](https://github.com/sulthandss/Tubes-Lost-And-Found-ITB/blob/main/cari.png?raw=true)
![Dashboard View](https://github.com/sulthandss/Tubes-Lost-And-Found-ITB/blob/main/dashboard.png?raw=true)

### 2. Pencarian Pintar (Card View)
Menggunakan sistem kartu (Card UI) dengan indikator warna:
* 🔴 **Merah:** Barang Hilang (Urgent)
* 🔵 **Biru:** Barang Ditemukan (Aman)
* 🟢 **Hijau:** Kasus Selesai

---

## ✨ Fitur Utama
1.  **CRUD System:** Create (Lapor), Read (Cari), Update (Klaim), Delete (Hapus).
2.  **Smart Filtering:** Cari barang berdasarkan Nama, Lokasi, atau Kategori.
3.  **Visual Status:** Warna kartu berubah otomatis sesuai status barang.
4.  **Data Persistence:** Data tersimpan otomatis dalam format JSON (tidak hilang saat aplikasi ditutup).

---

## 🛠️ Cara Menjalankan Program

Pastikan Python sudah terinstall di komputer.

1.  **Clone Repository ini** (atau download ZIP):
    ```bash
    git clone [https://github.com/sulthandss/Tubes-Lost-And-Found-ITB.git](https://github.com/sulthandss/Tubes-Lost-And-Found-ITB.git)
    ```

2.  **Install Library Pendukung:**
    Buka terminal/CMD dan ketik:
    ```bash
    pip install customtkinter Pillow
    ```

3.  **Jalankan Aplikasi:**
    ```bash
    python main.py
    ```

---
*Dibuat dengan ❤️ oleh Mahasiswa STEI-K ITB*
