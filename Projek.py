import psycopg2
from datetime import datetime

def koneksi_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="fixBarbercrown",
        user="postgres",
        password="12345"
    )

def MenuCustomer ():
    print("=== Menu Pengguna ===")
    print("1. Daftar Pengguna Baru")
    print("2. Login Pengguna")
    sub_pilihan = input("Masukkan Pilihan: ")
    if sub_pilihan == "1":
        daftarPenggunaBaru ()
    elif sub_pilihan == "2":
        login_pengguna()
    else:
        print ("Input Tidak Ada")
    


def daftarPenggunaBaru ():
    print("=== Daftar Pengguna Baru ===")
    nama = input("Nama: ")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    no_telp = input("No. Telepon: ")

    try:
        conn = koneksi_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO customer (nama, username, password, email, no_telp)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (nama, username, password, email, no_telp)
        cursor.execute(query, data)
        conn.commit()

        print("Pendaftaran berhasil. Silakan login.")
    except Exception as e:
        print("Terjadi kesalahan saat mendaftar:", e)
    finally:
        cursor.close()
        conn.close()  

def login_pengguna():
    username = input("Masukkan Username Pengguna: ")
    password = input("Masukkan Password: ")

    try:
        conn = koneksi_db()
        cursor = conn.cursor()

        query = "SELECT * FROM customer WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            print(f"Login berhasil sebagai Pengguna: {user[1]}")
            MenuPengguna(user[0])  # Asumsinya user[0] adalah ID user
        else:
            print("Username atau password pengguna salah.")
    except Exception as e:
        print("Terjadi kesalahan:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def login():
    print("=== Menu Login ===")
    print("1. Login Admin")
    print("2. Menu Pengguna")
    pilihan = input("Masukkan Pilihan: ")

    if pilihan == "1":
        username = input("Masukkan Username Admin: ")
        password = input("Masukkan Password: ")

        try:
            conn = koneksi_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
            admin = cursor.fetchone()

            if admin:
                print(f"Login berhasil sebagai Admin: {admin[1]}")
                MenuAdmin()
            else:
                print("Username atau password admin salah.")

            cursor.close()
            conn.close()
        except Exception as e:
            print("Terjadi kesalahan:", e)

    elif pilihan == "2":
        MenuCustomer()

def MenuAdmin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat & Kelola Kapster")
        print("2. Lihat & Ubah Status Booking")
        print("3. Riwayat & Status Pembayaran")
        print("4. Logout")
        pilihan = input("Masukkan Pilihan: ")

        if pilihan == "1":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()
                while True:
                    cursor.execute("SELECT id_kapster, nama, status FROM kapster")
                    kapsters = cursor.fetchall()
                    print("\n=== Data Kapster ===")
                    for k in kapsters:
                        print(f"ID: {k[0]}, Nama: {k[1]}, Status: {k[2]}")

                    print("\nSubmenu Kapster:")
                    print("1. Tambah Kapster")
                    print("2. Ubah Status Kapster")
                    print("3. Hapus Kapster")
                    print("4. Kembali")
                    sub = input("Pilih: ")

                    if sub == "1":
                        nama = input("Nama Kapster: ")
                        status = input("Status (Aktif/Tidak Aktif): ")
                        no_telp = input("No. Telp: ")
                        cursor.execute("""
                            INSERT INTO kapster (nama, status, no_telp)
                            VALUES (%s, %s, %s)
                        """, (nama, status, no_telp))
                        conn.commit()
                        print("Kapster berhasil ditambahkan.")

                    elif sub == "2":
                        id_kapster = input("ID Kapster: ")
                        status_baru = input("Status Baru (Aktif/Tidak Aktif): ")
                        cursor.execute("""
                            UPDATE kapster SET status = %s WHERE id_kapster = %s
                        """, (status_baru, id_kapster))
                        conn.commit()
                        print("Status kapster berhasil diperbarui.")

                    elif sub == "3":
                        id_kapster = input("ID Kapster yang ingin dihapus: ")
                        cursor.execute("DELETE FROM kapster WHERE id_kapster = %s", (id_kapster,))
                        conn.commit()
                        print("Kapster berhasil dihapus.")

                    elif sub == "4":
                        break
                    else:
                        print("Pilihan tidak valid.")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Terjadi kesalahan saat mengelola kapster:", e)

        elif pilihan == "2":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.id_booking, b.tanggal_booking, c.nama, k.nama, sb.nama_status
                    FROM booking b
                    JOIN customer c ON b.id_cust = c.id_cust
                    JOIN kapster k ON b.id_kapster = k.id_kapster
                    JOIN status_booking sb ON b.id_booking = sb.id_booking
                """)
                bookings = cursor.fetchall()

                print("\n=== Data Booking ===")
                for b in bookings:
                    print(f"ID: {b[0]}, Tanggal: {b[1]}, Customer: {b[2]}, Kapster: {b[3]}, Status: {b[4]}")

                ubah = input("Ubah status booking? (y/n): ").lower()
                if ubah == "y":
                    id_booking = input("ID Booking yang ingin diubah: ")
                    print("Pilihan Status Baru:")
                    print("1. Menunggu\n2. Terkonfirmasi\n3. Selesai\n4. Batal")
                    status_input = input("Pilih (1/2/3/4): ")
                    mapping = {"1": "Menunggu", "2": "Terkonfirmasi", "3": "Selesai", "4": "Batal"}
                    status_baru = mapping.get(status_input)

                    if status_baru:
                        cursor.execute("""
                            UPDATE status_booking SET nama_status = %s WHERE id_booking = %s
                        """, (status_baru, id_booking))
                        conn.commit()
                        print("Status booking berhasil diubah.")
                    else:
                        print("Input status tidak valid.")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Gagal memproses data booking:", e)

        elif pilihan == "3":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id_pembayaran, p.tanggal_pembayaran, p.jumlah_pembayaran, p.status_pembayaran,
                           c.nama, b.id_booking
                    FROM pembayaran p
                    JOIN booking b ON p.id_pembayaran = b.id_pembayaran
                    JOIN customer c ON b.id_cust = c.id_cust
                """)
                pembayaran = cursor.fetchall()

                print("\n=== Riwayat Pembayaran ===")
                for p in pembayaran:
                    print(f"ID: {p[0]}, Tanggal: {p[1]}, Jumlah: {p[2]}, Status: {p[3]}, Customer: {p[4]}, ID Booking: {p[5]}")

                ubah = input("Ubah status pembayaran? (y/n): ").lower()
                if ubah == "y":
                    id_pembayaran = input("ID Pembayaran: ")
                    print("1. Lunas\n2. Belum Lunas")
                    status_input = input("Pilih Status Baru (1/2): ")
                    status_baru = "Lunas" if status_input == "1" else "Belum Lunas"

                    cursor.execute("""
                        UPDATE pembayaran SET status_pembayaran = %s WHERE id_pembayaran = %s
                    """, (status_baru, id_pembayaran))
                    conn.commit()
                    print("Status pembayaran berhasil diubah.")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Terjadi kesalahan saat memproses pembayaran:", e)

        elif pilihan == "4":
            print("Logout Admin...")
            break
        else:
            print("Pilihan tidak valid.")



def MenuPengguna(id_cust):
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Pesan Booking")
        print("2. Lihat Riwayat Booking")
        print("3. Logout")
        pilihan = input("Pilih: ")

        if pilihan == "1":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()

                # Tampilkan kapster aktif
                cursor.execute("SELECT id_kapster, nama FROM kapster WHERE status = 'Aktif'")
                kapsters = cursor.fetchall()
                if not kapsters:
                    print("Maaf, tidak ada kapster aktif saat ini.")
                    continue
                print("\n=== Kapster Aktif ===")
                for k in kapsters:
                    print(f"{k[0]}. {k[1]}")

                id_kapster = int(input("Pilih ID Kapster: "))

                # Tampilkan layanan
                cursor.execute("SELECT id_layanan, nama_layanan, deskripsi, harga FROM layanan")
                layanans = cursor.fetchall()
                print("\n=== Daftar Layanan ===")
                for l in layanans:
                    print(f"{l[0]}. {l[1]} - {l[2]} - Rp{l[3]:,}")

                id_layanan = int(input("Pilih ID Layanan: "))
                kuantitas = int(input("Jumlah layanan (kuantitas): "))
                tanggal_input = input("Masukkan Tanggal Booking (YYYY-MM-DD HH:MM): ")
                tanggal_booking = datetime.strptime(tanggal_input, "%Y-%m-%d %H:%M")

                # Ambil harga layanan
                cursor.execute("SELECT harga FROM layanan WHERE id_layanan = %s", (id_layanan,))
                harga = cursor.fetchone()[0]
                total_harga = harga * kuantitas

                # Insert pembayaran dengan status_pembayaran 'Belum Lunas'
                cursor.execute("""
                    INSERT INTO pembayaran (tanggal_pembayaran, jumlah_pembayaran, status_pembayaran)
                    VALUES (%s, %s, %s) RETURNING id_pembayaran
                """, (datetime.now(), total_harga, 'Belum Lunas'))
                id_pembayaran = cursor.fetchone()[0]

                # Ambil id_admin default (misal 1)
                id_admin = 1

                # Insert booking
                cursor.execute("""
                    INSERT INTO booking (tanggal_booking, id_cust, id_kapster, id_pembayaran, id_admin)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id_booking
                """, (tanggal_booking, id_cust, id_kapster, id_pembayaran, id_admin))
                id_booking = cursor.fetchone()[0]

                # Insert detail_booking
                cursor.execute("""
                    INSERT INTO detail_booking (id_booking, id_layanan, kuantitas, total_harga)
                    VALUES (%s, %s, %s, %s)
                """, (id_booking, id_layanan, kuantitas, total_harga))

                # Insert status booking default 'Menunggu'
                cursor.execute("""
                    INSERT INTO status_booking (nama_status, id_booking)
                    VALUES (%s, %s)
                """, ('Menunggu', id_booking))

                conn.commit()
                print("Booking berhasil dilakukan!")

                cursor.close()
                conn.close()

            except Exception as e:
                print("Gagal memproses booking:", e)

        elif pilihan == "2":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()

                # Menampilkan riwayat booking dengan status terakhir
                cursor.execute("""
                    SELECT b.id_booking, b.tanggal_booking, sb.nama_status, k.nama
                    FROM booking b
                    JOIN status_booking sb ON b.id_booking = sb.id_booking
                    JOIN kapster k ON b.id_kapster = k.id_kapster
                    WHERE b.id_cust = %s
                    ORDER BY b.tanggal_booking DESC
                """, (id_cust,))
                riwayat = cursor.fetchall()

                if riwayat:
                    print("\n=== Riwayat Booking ===")
                    for r in riwayat:
                        print(f"ID Booking: {r[0]}, Tanggal: {r[1]}, Status: {r[2]}, Kapster: {r[3]}")
                else:
                    print("Belum ada riwayat booking.")

                cursor.close()
                conn.close()

            except Exception as e:
                print("Gagal menampilkan riwayat:", e)

        elif pilihan == "3":
            print("Logout Pengguna...")
            break

        else:
            print("Pilihan tidak valid.")

# Program Utama
# if __name__ == "__main__":
login()