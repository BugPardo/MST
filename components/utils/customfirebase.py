import firebase_admin
from firebase_admin import credentials, firestore, db


# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(credentials.Certificate('<path>'), {
    'databaseURL': 'https://apysys-project-default-rtdb.firebaseio.com/'
})

ref = db.reference('restricted_access/secret_document')
ref.get()