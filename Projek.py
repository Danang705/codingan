import psycopg2

def koneksi_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="dbBarbercrown",
        user="postgres",
        password="12345"
    )

def login():
    print("=== Menu Login ===")
    print("1. Login Admin")
    print("2. Login Pengguna")
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
        username = input("Masukkan Username Pengguna: ")
        password = input("Masukkan Password: ")

        try:
            conn = koneksi_db()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customer WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                print(f"Login berhasil sebagai Pengguna: {user[1]}")
                MenuPengguna(user[0])
            else:
                print("Username atau password pengguna salah.")

            cursor.close()
            conn.close()
        except Exception as e:
            print("Terjadi kesalahan:", e)
    else:
        print("Input tidak valid.")

def MenuAdmin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat Data Kapster")
        print("2. Lihat Semua Booking & Ubah Status")
        print("3. Logout")
        pilihan = input("Masukkan Pilihan: ")

        if pilihan == "1":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()

                while True:
                    cursor.execute("SELECT id_kapster, nama, status FROM kapster")
                    rows = cursor.fetchall()
                    print("\n=== Data Kapster ===")
                    for row in rows:
                        print(f"ID: {row[0]}, Nama: {row[1]}, Status: {row[2]}")

                    print("\nSubmenu Kapster:")
                    print("1. Tambah Kapster")
                    print("2. Ubah Status Kapster")
                    print("3. Hapus Kapster")
                    print("4. Kembali")
                    sub_pilihan = input("Pilih: ")

                    if sub_pilihan == "1":
                        try:
                            nama = input("Nama Kapster: ")
                            status = input("Status (Tersedia/Tidak): ")
                            no_telp = input("No. Telp: ")
                            id_admin = input("ID Admin: ")

                            cursor.execute("""
                                INSERT INTO kapster (nama, status, no_telp, id_admin)
                                VALUES (%s, %s, %s, %s)
                            """, (nama, status, no_telp, id_admin))
                            conn.commit()
                            print("Kapster berhasil ditambahkan.")
                        except Exception as e:
                            print("Gagal menambahkan kapster:", e)

                    elif sub_pilihan == "2":
                        try:
                            id_kapster = input("ID Kapster: ")
                            status = input("Status Baru (Tersedia/Tidak): ")

                            cursor.execute("UPDATE kapster SET status = %s WHERE id_kapster = %s", (status, id_kapster))
                            conn.commit()
                            print("Status kapster berhasil diperbarui.")
                        except Exception as e:
                            print("Gagal mengubah status kapster:", e)

                    elif sub_pilihan == "3":
                        try:
                            id_kapster = input("ID Kapster yang ingin dihapus: ")
                            cursor.execute("DELETE FROM kapster WHERE id_kapster = %s", (id_kapster,))
                            conn.commit()
                            print("Kapster berhasil dihapus.")
                        except Exception as e:
                            print("Gagal menghapus kapster:", e)

                    elif sub_pilihan == "4":
                        break
                    else:
                        print("Pilihan tidak valid.")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Terjadi kesalahan:", e)

        elif pilihan == "2":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT b.id_booking, b.tanggal_booking, c.nama, k.nama, sb.nama_status
                    FROM booking b
                    JOIN customer c ON b.id_cust = c.id_cust
                    JOIN kapster k ON b.id_kapster = k.id_kapster
                    JOIN status_booking sb ON b.id_status = sb.id_status
                """)
                bookings = cursor.fetchall()

                print("=== Daftar Booking ===")
                for b in bookings:
                    print(f"ID: {b[0]}, Tanggal: {b[1]}, Customer: {b[2]}, Kapster: {b[3]}, Status: {b[4]}")

                ubah = input("Ubah status booking? (y/n): ").lower()
                if ubah == "y":
                    id_booking = input("ID Booking: ")

                    cursor.execute("SELECT * FROM status_booking")
                    statuses = cursor.fetchall()
                    print("\n=== Pilihan Status Baru ===")
                    for s in statuses:
                        print(f"{s[0]}. {s[1]}")
                    id_status = input("Masukkan ID Status Baru: ")

                    cursor.execute("UPDATE booking SET id_status = %s WHERE id_booking = %s",
                                   (id_status, id_booking))
                    conn.commit()
                    print("Status booking berhasil diubah.")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Gagal memproses booking:", e)

        elif pilihan == "3":
            print("Logout Admin...")
            break
        else:
            print("Pilihan tidak valid.")

def MenuPengguna(id_cust):
    while True:
        print("\n=== Menu Pengguna ===")
        print("1. Lihat Riwayat Booking")
        print("2. Logout")
        pilihan = input("Pilih: ")

        if pilihan == "1":
            try:
                conn = koneksi_db()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT b.id_booking, b.tanggal_booking, sb.nama_status, k.nama
                    FROM booking b
                    JOIN status_booking sb ON b.id_status = sb.id_status
                    JOIN kapster k ON b.id_kapster = k.id_kapster
                    WHERE b.id_cust = %s
                """, (id_cust,))
                riwayat = cursor.fetchall()

                print("=== Riwayat Booking ===")
                for r in riwayat:
                    print(f"ID: {r[0]}, Tanggal: {r[1]}, Status: {r[2]}, Kapster: {r[3]}")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Gagal menampilkan riwayat:", e)

        elif pilihan == "2":
            print("Logout Pengguna...")
            break
        else:
            print("Pilihan tidak valid.")

# Program Utama
if __name__ == "__main__":
    login()
