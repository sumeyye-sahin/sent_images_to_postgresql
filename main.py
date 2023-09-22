from config import config
import psycopg2
from create_table import create_tables
from work_blob import write_blob,read_blob
import cv2
import os

def connect():
    conn = None
    try:
        params = config()
        print("Connecting to the PostgreSQL database ...")
        conn =psycopg2.connect(**params)

        #create a cursor
        cur= conn. cursor()

        print('PostgreSQL  database version:')
        cur.execute('SELECT version()')

        #Execute the ps database server version
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__=='__main__':

    connect()

    create_tables()



    cap = cv2.VideoCapture(0)  #camerayı değişkene aktararak işlemlerde kullandım

    yukseklik = 700  # görüntüleri istediğim boyutlarda kayıt etmek için yükseklik ve genişlik değerlerini belrledim
    genislik = 700

    i = 0  # kameradan alınan görüntülerin kayıt edilmesinde 0 dan başlayıp artan(i += 1) isimlendirme için kullanıldı
    while True:  # "q" tuşuna basana kadar devam edecek kameranın çalışmasını sağlayacak döngü oluşturuldu
        ret, frame = cap.read()  # sonsuz döngü içinde kamera frame şeklinde okunuyor

        frame = cv2.resize(frame, (genislik, yukseklik))  # termal kameradan alınan framelerin boyutunu belirledim
        isim = os.path.join("C:\\Users\\sumeyye\\Desktop\\sent_images_postgresql\\images", 'Image' + str(i) + '.jpg')

        cv2.imwrite(isim, frame)  # kameradan aldığımız görüntüleri kayıt etmek için bu satır oluşturuldu


        i += 1

        cv2.imshow("video", frame)  # okunan kamera görüntüsünü ekrana yansıtmak için bu kod satırını yazdım

        if cv2.waitKey(1) & 0xFF == ord("q"):  # q'a basıldığında çalışmayı durduruyor
            break

    cap.release()
    cv2.destroyAllWindows()

    # read_blob ile database de kayıtlı olan görüntüleri projemize getirmiş oluyoruz



    #write_blob ile kameradan alınan görüntüleri database e kayıt ediyoruz
    for i in range(80):
        write_blob(i,'fromCam','C:\\Users\\sumeyye\\Desktop\\sent_images_postgresql\\images\\Image'+str(i)+'.jpg','jpg')
        i+=1

"""
# read_blob ile database de kayıtlı olan görüntüleri projemize getirmiş oluyoruz
    for i in range(80):
        read_blob(i, 'image' + str(i))
        i += 1

"""





















