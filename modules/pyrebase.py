from pusher_push_notifications import PushNotifications
import pyrebase

config = {

    'apiKey': "AIzaSyAtt0Xq5Zx-pFb0gAeKJa_web4aAwLgZBs",
    'authDomain': "ta-kotlin.firebaseapp.com",
    'databaseURL': "https://ta-kotlin.firebaseio.com",
    'projectId': "ta-kotlin",
    'storageBucket': "ta-kotlin.appspot.com",
    'messagingSenderId': "1000178022249",
}

firebase = pyrebase.initialize_app(config)

db=firebase.database()
pn_client = PushNotification(
    instance_id='39e6ff2d-c739-45f1-a998-e583eb395f5e',
    secret_key='19126D628E620E3829B176B32CEC37D55B649E6F42A834DABAAA0500FE989D66',
)


def stream_handler(message):
    print(massage)
    if(message['data'] is 1):
        response = pn_client.publish(
            interests=['hello'],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': 'Hello!',
                        },
                    },
                    'fcm': {
                        'notification': {
                                'title': 'Hello',
                                'body': 'Hello, world!',
                                },
                                },
                                },
)
print(response['publishId'])

my_stream = db.child("device_info/status_brankas").stream(stream_handler,None)
