# Padel Rental — Deskripsi

Padel Rental adalah aplikasi sederhana untuk manajemen penyewaan lapangan padel. Pengguna dapat melihat daftar lapangan, membuat reservasi, melihat detail, mengedit, dan membatalkan reservasi. Aplikasi dibuat dengan Flask (WSGI) dan MySQL, dan dikemas untuk dijalankan menggunakan Docker.

**Fitur utama**

- Daftar lapangan dengan tipe dan harga per jam
- CRUD reservasi (tambah, lihat, edit, batalkan)
- Halaman detail reservasi dengan perhitungan total harga
- Status reservasi: `Aktif`, `Selesai`, `Dibatalkan`
- Dijalankan menggunakan Flask + Apache (mod_wsgi) dan MySQL di Docker

# Cara Menjalankan Aplikasi

Berikut instruksi singkat menjalankan aplikasi menggunakan Docker.

Docker Engine (Linux / macOS):

- Pastikan Docker Engine dan Compose tersedia.
- Dari direktori proyek jalankan:

  sudo docker compose up --build -d

- Akses aplikasi di: `http://localhost:8080`

Docker Desktop (Windows):

- Buka PowerShell atau WSL2 terminal di folder proyek.
- Jalankan (tanpa `sudo`):

  docker compose up --build -d

- Akses aplikasi di: `http://localhost:8080`

Catatan singkat:
- Untuk melihat output real-time tanpa detached, hilangkan `-d`.
- Jika mengubah dependensi di `web/requirements.txt` atau konfigurasi image, jalankan `docker compose build web` lalu restart.

Itu saja — cukup perintah di atas untuk menjalankan aplikasi di kedua lingkungan.
