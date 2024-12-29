# test_database_connection.py
from backend.utils.database import Database
from sqlalchemy import text  # Burada text modülünü ekliyoruz

def test_database_connection():
    # Database nesnesini oluştur
    db = Database()

    # Veritabanına bağlan
    session = db.connect()
    print("Bağlantı başarılı!")

    # Test amacıyla basit bir işlem yapılabilir (örneğin, veri eklemek veya sorgulamak)
    # Burada örnek olarak bir sorgu yapılabilir, mesela:
    try:
        result = session.execute(text("SELECT 1"))  # Burada sorguyu text() ile sarıyoruz
        print("Sorgu başarılı:", result.fetchall())
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    # Bağlantıyı kapat
    db.close(session)
    print("Bağlantı kapatıldı.")

if __name__ == '__main__':
    test_database_connection()
