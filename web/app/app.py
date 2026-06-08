from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import date

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='db',
        user='padel_user',
        password='padel_password',
        database='padel_db',
        cursorclass=pymysql.cursors.DictCursor
    )

def update_status_otomatis(cursor, conn):
    cursor.execute("""
        UPDATE reservasi 
        SET status = 'Selesai' 
        WHERE status = 'Aktif' 
        AND TIMESTAMP(tanggal, jam_mulai) + INTERVAL durasi_jam HOUR <= NOW()
    """)
    conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
   
    update_status_otomatis(cursor, conn)
    
    cursor.execute("SELECT * FROM lapangan")
    lapangan = cursor.fetchall()
    
    cursor.execute("""
        SELECT r.*, l.nama_lapangan, 
               (l.harga_per_jam * r.durasi_jam) as total_harga 
        FROM reservasi r 
        JOIN lapangan l ON r.lapangan_id = l.id 
        ORDER BY r.tanggal DESC, r.jam_mulai DESC
    """)
    reservasi = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', lapangan=lapangan, reservasi=reservasi)

@app.route('/sewa', methods=('GET', 'POST'))
def tambah_sewa():
    conn = get_db_connection()
    cursor = conn.cursor()
    hari_ini = date.today().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        lapangan_id = request.form['lapangan_id']
        nama = request.form['nama_penyewa']
        tanggal = request.form['tanggal']
        jam = request.form['jam_mulai']
        durasi = request.form['durasi_jam']
        
        
        if tanggal < hari_ini:
            return "Error: Tidak dapat memesan untuk tanggal yang sudah lewat!", 400

        cursor.execute("""
            INSERT INTO reservasi (lapangan_id, nama_penyewa, tanggal, jam_mulai, durasi_jam, status)
            VALUES (%s, %s, %s, %s, %s, 'Aktif')
        """, (lapangan_id, nama, tanggal, jam, durasi))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    cursor.execute("SELECT * FROM lapangan")
    lapangan = cursor.fetchall()
    conn.close()
    return render_template('sewa.html', lapangan=lapangan, data=None, hari_ini=hari_ini)

@app.route('/detail/<int:id>')
def detail_sewa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_status_otomatis(cursor, conn)
    
    cursor.execute("""
        SELECT r.*, l.nama_lapangan, l.tipe, l.harga_per_jam,
               (l.harga_per_jam * r.durasi_jam) as total_harga 
        FROM reservasi r 
        JOIN lapangan l ON r.lapangan_id = l.id 
        WHERE r.id = %s
    """, (id,))
    detail = cursor.fetchone()
    conn.close()
    return render_template('detail.html', detail=detail)

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update_sewa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    hari_ini = date.today().strftime('%Y-%m-%d')
    
    
    cursor.execute("SELECT status FROM reservasi WHERE id = %s", (id,))
    cek_status = cursor.fetchone()
    
    if not cek_status or cek_status['status'] != 'Aktif':
        conn.close()
        return "Akses Ditolak: Pesanan yang sudah dibatalkan atau selesai tidak dapat diedit.", 403
    
    if request.method == 'POST':
        lapangan_id = request.form['lapangan_id']
        nama = request.form['nama_penyewa']
        tanggal = request.form['tanggal']
        jam = request.form['jam_mulai']
        durasi = request.form['durasi_jam']
        
        cursor.execute("""
            UPDATE reservasi 
            SET lapangan_id=%s, nama_penyewa=%s, tanggal=%s, jam_mulai=%s, durasi_jam=%s
            WHERE id=%s
        """, (lapangan_id, nama, tanggal, jam, durasi, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    cursor.execute("SELECT * FROM reservasi WHERE id = %s", (id,))
    data = cursor.fetchone()
    cursor.execute("SELECT * FROM lapangan")
    lapangan = cursor.fetchall()
    conn.close()
    return render_template('sewa.html', lapangan=lapangan, data=data, hari_ini=hari_ini)

@app.route('/batal/<int:id>')
def batalkan_sewa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE reservasi SET status='Dibatalkan' WHERE id=%s AND status='Aktif'", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/hapus/<int:id>')
def hapus_sewa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM reservasi WHERE id=%s AND status IN ('Dibatalkan', 'Selesai')", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()