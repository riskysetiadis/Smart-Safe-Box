from firebase import firebase
import datetime

firebase = firebase.FirebaseApplication('https://ta-kotlin.firebaseio.com/', None)

def baca_status():
    result = firebase.get('/device_info', None)
    print(result["status_pintu"])
    return result["status_pintu"]

def baca_register():
    result = firebase.get('/device_info', None)
    print(result["status_register"])
    return [result["status_register"], result["pemilik"]]
def pemilik():
    result = firebase.get('/device_info', None)
    print(result["pemilik"])
    return result["pemilik"]

def ubah_status(status):
    result = firebase.put('/device_info', name="status_pintu", data=status, params={'print': 'pretty'})
    tanggal = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    result = firebase.put('/device_info', name="terakhir_dibuka", data=tanggal, params={'print': 'pretty'})
    print(result)

def ubah_status_mode():
    result = firebase.put('/device_info', name="status_register", data=0, params={'print': 'pretty'})
   # result = firebase.put('/device_info', name="pemilik", data="", params={'print': 'pretty'})
    print(result)

def history():
    tanggal = datetime.datetime.now().strftime("%B %d,%Y  %I:%M%p ")
    data = {
        "status": "sistem",
        "username": "sistem",
        "tanggaldanwaktu": tanggal
        }
    result = firebase.post('/History', data)
    #result = firebase.post('/History', name="username",data="", params={'print': 'pretty'})
    print(result)


if __name__ == "__main__":
    try:
        ubah_status(2)
        while True:
            pemilik()
    except KeyboardInterrupt:
        print("[INFO] CLOSED CONNECTION")
