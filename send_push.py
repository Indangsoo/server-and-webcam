import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

CRED_PATH = ""
cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)

REGISTRATION_TOKEN = ""

def send_notification(title, body):
    message = messaging.Message(
            notification = messaging.Notification(
                title=title,
                body=body
            ),
            token = REGISTRATION_TOKEN,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)

if __name__ == "__main__":
    print("test")
    send_notification("테스트", "테스트메세지")
