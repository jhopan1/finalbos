-- Membuat database
CREATE DATABASE komputasi;

-- Menggunakan database
USE komputasi;

-- Tabel untuk pengguna
CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password VARCHAR(255) NOT NULL
);

-- Tabel untuk admin
CREATE TABLE admin (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Tabel untuk pekerja
CREATE TABLE pekerja (
    id_pekerja INT AUTO_INCREMENT PRIMARY KEY,
    nama_pekerja VARCHAR(100) NOT NULL,
    kontak VARCHAR(50)
);

-- Tabel untuk pemesanan
CREATE TABLE pemesanan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT NOT NULL,
    nama_pemesan VARCHAR(100) NOT NULL,
    metode_pembayaran VARCHAR(50),
    status VARCHAR(50),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
);
