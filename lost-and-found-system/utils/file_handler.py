# utils/file_handler.py
import json
import os
import shutil
from datetime import datetime
from config.settings import DATA_FILE, DATA_DIR, IMAGES_DIR

def ensure_data_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_data():
    ensure_data_exists()
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Urutkan data dari yang paling baru
            return data[::-1] 
    except (json.JSONDecodeError, OSError):
        return []

def save_data(item, image_path=None):
    # Buat ID dan Waktu saat data dibuat
    item['id'] = int(datetime.now().timestamp()) 
    item['waktu'] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Salin gambar ke folder images jika ada
    if image_path and os.path.isfile(image_path):
        ext = os.path.splitext(image_path)[1]
        dest_filename = f"{item['id']}{ext}"
        dest_path = os.path.join(IMAGES_DIR, dest_filename)
        shutil.copy2(image_path, dest_path)
        item['gambar'] = dest_filename
    else:
        item['gambar'] = None
    
    # Baca data lama
    current_data = load_data()
    # Karena load_data me-reverse, kita balikin dulu biar urutannya benar saat append
    current_data = current_data[::-1] 
    
    current_data.append(item)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(current_data, f, indent=4)

def mark_as_done(item_id):
    """Mengubah status barang menjadi SELESAI (Hijau)"""
    ensure_data_exists()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == item_id:
            item['status'] = "Selesai" # Ubah status jadi Selesai
            found = True
            break
            
    if found:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

def delete_item(item_id):
    """Menghapus barang dari database permanen"""
    ensure_data_exists()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    new_data = [x for x in data if x.get('id') != item_id]
    
    with open(DATA_FILE, 'w') as f:
        json.dump(new_data, f, indent=4)

def get_image_path(filename):
    """Kembalikan path lengkap gambar, atau None jika tidak ada"""
    if not filename:
        return None
    path = os.path.join(IMAGES_DIR, filename)
    return path if os.path.isfile(path) else None