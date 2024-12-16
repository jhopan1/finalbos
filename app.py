from flask import Flask, render_template, request, url_for, session, redirect, flash, Response
from werkzeug.security import check_password_hash, generate_password_hash
from mysql import connector
import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configuration
conn = connector.connect(
    user="finalyy",
    password="Finalyy1",
    host="finalyy.mysql.database.azure.com",
    port=3306,
    database="komputasi"
)
cursor = conn.cursor()

app.secret_key = 'jhoofanganteng'
if conn.is_connected():
    print('Connection to database established.')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('lobby.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user is None:
            # Registrasi berhasil
            cursor.execute('INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)', (name, email, phone, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')  # Pesan sukses
            return redirect(url_for('login'))
        else:
            # Email sudah terdaftar
            flash('Email already registered!', 'error')  # Pesan error

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[4], password):  # user[4] is the hashed password
            session['loggedin'] = True
            session['id'] = user[0]
            session['email'] = user[1]
            return redirect(url_for('user_home'))

    return render_template('loginuser.html')



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/home')
def user_home():
    if 'loggedin' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/ringan')
def ringan():
    if 'loggedin' in session:
        return render_template('ringan.html')


@app.route('/sedang')
def sedang():
    if 'loggedin' in session:
        return render_template('sedang.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/berat')
def berat():
    if 'loggedin' in session:
        return render_template('berat.html')    
    

@app.route('/metpem')
def metpem():
    if 'loggedin' in session:
        return render_template('metpem.html')
    
@app.route('/adminuser')
def adminuser():
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return render_template('/admin/user.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/export_to_excel')
def export_to_excel():
    if 'loggedin' in session:
        # Mengambil data pengguna dari database
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        # Mencetak data pertama untuk memeriksa jumlah kolom
        print(users[0])  # Ini akan mencetak data pengguna pertama di console
        
        # Misalkan jumlah kolomnya 5, maka kita sesuaikan dengan nama kolom yang sesuai.
        # Sesuaikan nama kolom berdasarkan struktur database Anda
        df = pd.DataFrame(users, columns=["id_user", "name", "email", "phone", "Column4"])  # Ganti "Column5" dengan nama kolom yang sesuai
        
        # Menyimpan DataFrame ke file Excel
        excel_file = pd.ExcelWriter("/C:/Users/ACER/Downloads/users_data.xlsx", engine='openpyxl')
        df.to_excel(excel_file, index=False)
        excel_file.save()
        
        # Mengirim file sebagai response untuk diunduh
        return Response(
            open("/mnt/data/users_data.xlsx", "rb").read(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment;filename=users_data.xlsx"}
        )
    else:
        return redirect(url_for('login'))

@app.route('/loginadmin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query untuk mencari admin berdasarkan email
        cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            # Cek apakah password valid
            if user[2] == password:  # user[2] adalah kolom password (plaintext)
                session['loggedin'] = True
                session['admin_id'] = user[0]  # user[0] adalah kolom id admin
                session['admin_email'] = user[1]  # user[1] adalah kolom email admin
                return redirect(url_for('admindashboard'))
            else:
                return render_template('/admin/ladmin.html', error="Password salah.")
        else:
            return render_template('/admin/ladmin.html', error="Email tidak ditemukan.")

    return render_template('/admin/ladmin.html')

# Logout admin
@app.route('/logoutadmin')
def logout_admin():
    session.clear()
    return redirect(url_for('login_admin'))

@app.route('/adminpekerja')
def adminpekerja():
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM pekerja')
        pekerja = cursor.fetchall()
        return render_template('/admin/pekerja.html', pekerja=pekerja)
    else:
        return redirect(url_for('login'))


@app.route('/add_worker', methods=['POST'])
def add_worker():
    if 'loggedin' in session:
        nama = request.form['nama']
        kontak = request.form['kontak']
        cursor.execute('INSERT INTO pekerja (nama_pekerja, kontak) VALUES (%s, %s)', (nama, kontak))
        conn.commit()  # Pastikan Anda memanggil commit untuk menyimpan perubahan ke database
        return redirect(url_for('adminpekerja'))
    else:
        return redirect(url_for('login'))

# Route untuk Edit Pekerja (Update)
@app.route('/edit_worker', methods=['POST'])
def edit_worker():
    if 'loggedin' in session:
        worker_id = request.form['id']
        nama = request.form['nama']
        kontak = request.form['kontak']
        cursor.execute('UPDATE pekerja SET nama_pekerja = %s, kontak = %s WHERE id_pekerja = %s', (nama, kontak, worker_id))
        conn.commit()  # Pastikan Anda memanggil commit untuk menyimpan perubahan ke database
        return redirect(url_for('adminpekerja'))
    else:
        return redirect(url_for('login'))


# Route untuk Hapus Pekerja (Delete)
@app.route('/delete_worker/<int:id>', methods=['GET'])
def delete_worker(id):
    if 'loggedin' in session:
        cursor.execute('DELETE FROM pekerja WHERE id_pekerja = %s', (id,))
        conn.commit()  # Pastikan Anda memanggil commit untuk menyimpan perubahan ke database
        return redirect(url_for('adminpekerja'))
    else:
        return redirect(url_for('login'))

    


@app.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    if 'loggedin' in session:
        cursor.execute('UPDATE pemesanan SET status = %s WHERE id = %s', ('Accepted', order_id))
        conn.commit()
        flash('Order has been accepted.')
        return redirect(url_for('admindashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    if 'loggedin' in session:
        cursor.execute('UPDATE pemesanan SET status = %s WHERE id = %s', ('Rejected', order_id))
        conn.commit()
        flash('Order has been rejected.')
        return redirect(url_for('admindashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/admindashboard')
def admindashboard():
    if 'loggedin' in session:
        cursor.execute('SELECT COUNT(*) FROM pemesanan')
        total_orders = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM users')
        users = cursor.fetchone()[0]    
            
        cursor.execute('SELECT COUNT(*) FROM pekerja')
        pekerja = cursor.fetchone()[0]        

        cursor.execute('SELECT * FROM pemesanan')
        orders = cursor.fetchall()
        
        return render_template('/admin/dashboard.html', orders=orders, total_orders=total_orders, users=users, pekerja=pekerja)
    else:
        return redirect(url_for('login'))
    

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    if 'loggedin' in session:
        try:
            id = session['id']
            name = request.form['name']
            payment_method = request.form['payment_method']
            status = "pending"
            cursor.execute('INSERT INTO pemesanan (id_user, nama_pemesan, metode_pembayaran, status) VALUES (%s, %s, %s, %s)', 
                           (id, name, payment_method, status))
            conn.commit()
            cursor.execute('UNLOCK TABLES')

            flash('Payment submitted successfully!')
            return redirect(url_for('user_home'))
        except Exception as e:
            print(e)
            conn.rollback()
            flash(f'An error occurred: {e}')
            return redirect(url_for('metpem'))
    else:
        return redirect(url_for('login'))
    
@app.route('/index')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
