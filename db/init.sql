CREATE TABLE lapangan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_lapangan VARCHAR(100) NOT NULL,
    tipe ENUM('Indoor', 'Outdoor') NOT NULL,
    harga_per_jam DECIMAL(10, 2) NOT NULL
);

CREATE TABLE reservasi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lapangan_id INT,
    nama_penyewa VARCHAR(100) NOT NULL,
    tanggal DATE NOT NULL,
    jam_mulai TIME NOT NULL,
    durasi_jam INT NOT NULL,
    status ENUM('Aktif', 'Selesai', 'Dibatalkan') DEFAULT 'Aktif',
    FOREIGN KEY (lapangan_id) REFERENCES lapangan(id)
);

INSERT INTO lapangan (nama_lapangan, tipe, harga_per_jam) VALUES 
('Padel Pro Indoor 1', 'Indoor', 150000.00),
('Padel Pro Indoor 2', 'Indoor', 150000.00),
('Sky Padel Outdoor 1', 'Outdoor', 120000.00),
('Sky Padel Outdoor 2', 'Outdoor', 120000.00),
('Family Court Padel', 'Indoor', 100000.00);
