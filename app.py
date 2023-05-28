# Author  FIKRI HADI NUGRAHA
# APLIKASI SEDERHANA DATABASE KAMPUS 


from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

application = Flask(__name__)
application.secret_key = 'something_secret_and_unique'

conn = cursor = None

# Function to open database connection
def openDb():
   global conn, cursor
   conn = mysql.connector.connect(
    host ='localhost',
    user ='root',
    password = '',
    database ='db_kampus'     # DataBase yang dipakai
   )
   cursor = conn.cursor()
   
# Function to close database connection
def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()
   
### login system ##
@application.route('/', methods=['GET', 'POST'])
def login():
    openDb()
    message = ''
    if request.method == 'POST':
        if request.form:
            email = request.form['email']
            password = request.form['password']
            sql = "SELECT * FROM user WHERE email = '%s' AND password = '%s'" % (email, password)
            cursor.execute(sql)
            user = cursor.fetchone()
            if user:
                session['loggedin'] = True
                return redirect(url_for('dashboard'))
    message = 'login salah'
    return render_template('login/Table_login.html', message=message)

### Register Login ## 
@application.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password =  request.form['password']
        openDb()
        sql = "INSERT INTO user (email,password) VALUES (%s, %s)"
        val = (email,password)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('login'))
    else:
        return render_template('login/register.html')
        
## Halaman Utama 
@application.route('/dashboard')
def dashboard():
    openDb()
    #Menjumlahkan Total Mahasiswa 
    sql = "SELECT COUNT(id_mahasiswa) FROM mahasiswa"
    cursor.execute(sql)
    result = cursor.fetchone()  # Membaca hasil perintah SQL
    count_mahasiswa = result[0] if result else 0  # Mendapatkan jumlah mahasiswa dari hasil
    conn.commit()
    closeDb()
    #Tambahkan logika untuk halaman utama disini
    return render_template('dashboard.html', count_mahasiswa=count_mahasiswa)

######################################## DATA MAHASISWA ######################################################
#Fungsi untuk menampilkan DataBase Mahasiswa dari DB_Kampus
@application.route('/viewmahasiswa')
def view():
    openDb()
    container = []
    sql = "SELECT * FROM mahasiswa"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
      container.append(data)
    closeDb()
    return render_template('datamahasiswa/Table_Mahasiswa.html', container=container,)

#Fungsi untuk edit data
@application.route('/editmahasiswa/<id_mahasiswa>', methods=['GET','POST'])
def edit(id_mahasiswa):
   openDb()
   cursor.execute("SELECT * FROM mahasiswa WHERE id_mahasiswa=%s", (id_mahasiswa,))
   data = cursor.fetchone()
   if request.method == 'POST':
      id_mahasiswa = request.form['id_mahasiswa']
      NIM = request.form['nim']
      nama = request.form['nama']
      Fakultas = request.form['fakultas']
      Prodi = request.form['prodi']
      PHONE = request.form['phone']
      Email = request.form['email']
      Alamat = request.form['alamat']
      sql = "UPDATE mahasiswa SET nim=%s,nama_mahasiswa=%s,fakultas=%s,prodi=%s,phone=%s, email=%s, alamat=%s WHERE id_mahasiswa=%s"
      val = (NIM,nama, Fakultas,Prodi,PHONE,Email,Alamat, id_mahasiswa)
      cursor.execute(sql, val)
      conn.commit()
      closeDb()
      return redirect(url_for('viewmahasiswa'))
   else:
      closeDb()
      return render_template('datamahasiswa/Table_edit.html', data=data)
  
#fungsi view tambah() untuk membuat form tambah
# Fungsi view tambah() untuk membuat form tambah
@application.route('/tambahmahasiswa', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        NIM = request.form['nim']
        nama = request.form['nama']
        Fakultas = request.form['fakultas']
        Prodi = request.form['prodi']
        PHONE = request.form['phone']
        Email = request.form['email']
        Alamat = request.form['alamat']
        openDb()
        sql = "INSERT INTO mahasiswa (nim, nama_mahasiswa, fakultas, prodi, phone, email, alamat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (NIM, nama, Fakultas, Prodi, PHONE, Email, Alamat)
        cursor.execute(sql, val)
        conn.commit()

        # Menutup hasil query sebelumnya
        for _ in cursor.stored_results():
            pass

        # Mendapatkan ID dari baris terakhir yang ditambahkan
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]

        closeDb()

        return redirect(url_for('view'))
    else:
        return render_template('datamahasiswa/Table_tambah.html')


#fungsi untuk menghapus data
@application.route('/hapusmahasiswa/<id_mahasiswa>', methods=['GET','POST'])
def hapus(id_mahasiswa):
   openDb()
   cursor.execute('DELETE FROM mahasiswa WHERE id_mahasiswa=%s', (id_mahasiswa,))
   conn.commit()
   closeDb()
   return redirect(url_for('view'))
######################################## DATA MAHASISWA ######################################################
    
######################################## DATA DOSEN ##########################################################
@application.route('/viewdosen')
def viewdosen():
    openDb()
    container = []
    sql = "SELECT * FROM dosen"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
      container.append(data)
    closeDb()
    return render_template('datadosen/index.html', container=container,)
######################################## DATA DOSEN ##########################################################

if __name__ == '__main__':
    application.run(debug=True, port='3000')
    closeDb()