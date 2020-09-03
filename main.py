import modules.lcd.lcd_app as lcd_app
import modules.buzzer_app as buzzer_app
import modules.led_app as led_app
import modules.magnetic_app as magnetic_app
import modules.relay as relay_app
import modules.push_app as push_app
import modules.firebase_app as firebase_app
import sys
import os
import numpy as np
import face_recognition_system.VideoCamera as VideoCamera
import face_recognition_system.FaceDetector as FaceDetector
import cv2
import shutil
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as gpio
from cv2 import __version__


gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if (f.verifyPassword() == False):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('Exception message: ' + str(e))
    exit(1)


def check_module(mylcd):
    lcd_app.hapus_lcd(mylcd)
    lcd_app.tulis_lcd(mylcd, "Warm Up", 1)
    lcd_app.tulis_lcd(mylcd, "Module", 2)
    buzzer_app.setup_pin()
    buzzer_app.testing_pin()
    led_app.setup_pin()
    led_app.testing_pin()
    relay_app.setup_relay()
    relay_app.testing_relay()
    lcd_app.hapus_lcd(mylcd)
    lcd_app.tulis_lcd(mylcd, "Brankas Tertutup", 1)
    lcd_app.tulis_lcd(mylcd, "Scan Sidik Jari", 2)
    magnetic_app.setup_pin()
    push_app.setup_pin()
    firebase_app.ubah_status(0)

def enrollFinger():
    print("Enrolling Finger")
    time.sleep(2)
    lcd_app.hapus_lcd(mylcd)
    lcd_app.tulis_lcd(mylcd, "Silahkan", 1)
    lcd_app.tulis_lcd(mylcd, "Tempelkan Sidik jari", 2)
    print('Waiting for finger...')
    print("Place Finger")
    while (f.readImage() == False):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    if (positionNumber >= 0):
        lcd_app.hapus_lcd(mylcd)
        lcd_app.tulis_lcd(mylcd, "Gagal", 1)
        lcd_app.tulis_lcd(mylcd, "Coba Lagi", 2)
        print('Template already exists at position #' + str(positionNumber))
        print("Finger ALready")
        print("   Exists     ")
        time.sleep(2)
        return
    lcd_app.hapus_lcd(mylcd)
    lcd_app.tulis_lcd(mylcd, "Angkat sidik jari", 1)
    lcd_app.tulis_lcd(mylcd, "kemudian  tempel kembali", 2)
    print('Remove finger...')
    print("Remove Finger")
    time.sleep(2)
    print('Waiting for same finger again...')
    print("Place Finger")
    print("   Again    ")
    while (f.readImage() == False):
        pass
    f.convertImage(0x02)
    if (f.compareCharacteristics() == 0):
        print("Fingers do not match")
        print("Finger Did not")
        print("   Mactched   ")
        time.sleep(2)
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print("Stored at Pos:")
    print(str(positionNumber))
    lcd_app.hapus_lcd(mylcd)
    lcd_app.tulis_lcd(mylcd, "Selamat anda", 1)
    lcd_app.tulis_lcd(mylcd, "Teregistrasi", 2)
    print("successfully")
    print('New template position #' + str(positionNumber))
    time.sleep(2)


def searchFinger():
    try:
        PEOPLE_FOLDER = "face_recognition_system/people/"
        SHAPE = "rectangle"

        print('Waiting for finger...')
        while(f.readImage() == False):
            #pass
            time.sleep(.5)
            return
        f.convertImage(0x01)
        result = f.searchTemplate()

        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        print('SHA-2 hash of template: ' +
              hashlib.sha256(characterics).hexdigest())

        positionNumber = result[0]
        accuracyScore = result[1]
        if positionNumber == -1:
            lcd_app.hapus_lcd(mylcd)
            lcd_app.tulis_lcd(mylcd, "Gagal", 1)
            lcd_app.tulis_lcd(mylcd, "Ulangi Lagi", 2)
            print('No match found!')
            print("No Match Found")
            time.sleep(2)
            return False, ""
        else:
            print('Found template at position #' + str(positionNumber))
            print("Found at Pos:")
            print(str(positionNumber))
            lcd_app.hapus_lcd(mylcd)
            lcd_app.tulis_lcd(mylcd, "Berhasil", 1)
            lcd_app.tulis_lcd(mylcd, "Silahkan Menghadap Kamera", 2)
            recognize_people(PEOPLE_FOLDER, SHAPE)
            time.sleep(2)
            return True, str(positionNumber)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        # exit(1)
        return False




def resize(images, size=(100, 100)):
    images_norm = []
    for image in images:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if image.shape < size:
            image_norm = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm
def cut_face_rectangle(image, face_coord):
    images_rectangle = []
    for (x, y, w, h) in face_coord:
        images_rectangle.append(image[y: y + h, x: x + w])
    return images_rectangle

def draw_face_rectangle(image, faces_coord):
    for (x, y, w, h) in faces_coord:
        cv2.rectangle(image, (x, y), (x + w, y + h), (206, 0, 209), 2)
    return image


def get_images(frame, faces_coord, shape):
    faces_img = cut_face_rectangle(frame, faces_coord)
    frame = draw_face_rectangle(frame, faces_coord)
    #faces_img = normalize_intensity(faces_img)
    faces_img = resize(faces_img)
    return (frame, faces_img)

def add_person(people_folder, shape):
    person_name = ("pemilik")
    folder = people_folder + person_name
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
    video = VideoCamera.VideoCamera()
    detector = FaceDetector.FaceDetector('face_recognition_system/haarcascade_frontalface_alt2.xml')
    counter = 1
    timer = 0
    while counter < 21:
        frame = video.get_frame()
        face_coord = detector.detect(frame)
        if len(face_coord):
            frame, face_img = get_images(frame, face_coord, shape)
            if timer % 10 == 5:
                cv2.imwrite(folder + '/' + str(counter) + '.jpg',
                            face_img[0])
                counter += 1

        cv2.imshow('Video Feed', frame)
        cv2.waitKey(50)
        timer += 5
    cv2.destroyAllWindows()

def recognize_people(people_folder, shape):
    people = [person for person in os.listdir(people_folder)]

    print (30 * '-')
    detector = FaceDetector.FaceDetector('face_recognition_system/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    threshold = 85
    images = []
    labels = []
    labels_people = {}
    for i, person in enumerate(people):
        labels_people[i] = person
        for image in os.listdir(people_folder + person):
            images.append(cv2.imread(people_folder + person + '/' + image, 0))
            labels.append(i)
    try:
        recognizer.train(images, np.array(labels))
    except:
        print ("\nOpenCV Error: Do you have at least two people in the database?\n")
        sys.exit()

    video = VideoCamera.VideoCamera()
    while True:
        frame = video.get_frame()
        faces_coord = detector.detect(frame, False)
        if len(faces_coord):
            frame, faces_img = get_images(frame, faces_coord, shape)
            for i, face_img in enumerate(faces_img):
                if __version__ == "3.1.0":
                    collector = cv2.face.MinDistancePredictCollector()
                    recognizer.predict(face_img, collector)
                    conf = collector.getDist()
                    pred = collector.getLabel()
                else:
                    pred, conf = recognizer.predict(face_img)
                if conf < threshold:
                    relay_app.nyalakan_pin()
                    buzzer_app.nyalakan_pin()
                    firebase_app.ubah_status(0)
                    magnetic_app.setup_pin()
                    firebase_app.history()
                    push_app.setup_pin()
                    lcd_app.hapus_lcd(mylcd)
                    lcd_app.tulis_lcd(mylcd, "Berhasil", 1)
                    lcd_app.tulis_lcd(mylcd, "Silahkan masuk", 2)

                else:
                    lcd_app.hapus_lcd(mylcd)
                    lcd_app.tulis_lcd(mylcd, "Gagal", 1)
                    lcd_app.tulis_lcd(mylcd, "Coba Lagi", 2)
                time.sleep(3.0)
                return '__main__'

if __name__ == '__main__':

    try:
        mylcd = lcd_app.get_lcd()
        print("Running Application")
        check_module(mylcd)
        status_alarm = True
        status_buka = False
        status_registrasi = False


        PEOPLE_FOLDER = "face_recognition_system/people/"
        SHAPE = "rectangle"

        while True:

            data_registrasi = firebase_app.baca_register()
            if data_registrasi[0]==1:
                status_registrasi = True
            else:
                status_registrasi = False

            # Kondisi Mode registrasi
            if status_registrasi == True:
                lcd_app.hapus_lcd(mylcd)
                lcd_app.tulis_lcd(mylcd, "Registrasi", 1)
                lcd_app.tulis_lcd(mylcd, "Silahkan scan wajah", 2)
                buzzer_app.nyalakan_pin()
                push_app.setup_pin()
                magnetic_app.setup_pin()
                add_person(PEOPLE_FOLDER, SHAPE)
                enrollFinger()
                firebase_app.ubah_status_mode()

            # Kondisi Mode Keamanan
            else:
                lcd_app.hapus_lcd(mylcd)
                lcd_app.tulis_lcd(mylcd, "Brankas Tertutup", 1)
                lcd_app.tulis_lcd(mylcd, "Scan Sidik Jari dan wajah", 2)

                # Kodisi untuk pintu terbuka
                if magnetic_app.baca_status_pintu() == True:

                    if status_alarm == True:
                        firebase_app.ubah_status(2)
                        lcd_app.tulis_lcd(mylcd, "Brankas Terbuka", 1)
                        lcd_app.tulis_lcd(mylcd, "Dibuka Paksa", 2)
                        led_app.nyalakan_pin()
                        buzzer_app.nyalakan_pin()
                        magnetic_app.setup_pin()
                        push_app.setup_pin()
                    else:
                        lcd_app.tulis_lcd(mylcd, "Brankas Terbuka", 1)
                        lcd_app.tulis_lcd(mylcd, "Tutup kembali", 2)
                else:
                    lcd_app.tulis_lcd(mylcd, "Brankas Tertutup", 1)
                    lcd_app.tulis_lcd(mylcd, "Scan Sidik Jari", 2)
                    searchFinger()

                if firebase_app.baca_status() == 1:
                    status_buka = True
                else:
                    status_buka = False

                if status_buka == True:
                    lcd_app.hapus_lcd(mylcd)
                    lcd_app.tulis_lcd(mylcd, "Berhasil", 1)
                    lcd_app.tulis_lcd(mylcd, "Silahkan masuk", 2)
                    relay_app.nyalakan_pin()
                    buzzer_app.nyalakan_pin()
                    firebase_app.ubah_status(0)
                    time.sleep(3.0)
                    status_buka = False
                    magnetic_app.setup_pin()
                    push_app.setup_pin()
                firebase_app.ubah_status(0)

    except KeyboardInterrupt:
        print("[INFO] WIPE PIN...")
