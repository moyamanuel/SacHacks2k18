import pyrebase

config = {
    "apiKey": "AIzaSyB-qKMHUdMC4w0QcZIzmVsjFWJmTrDB_wY",
    "authDomain": "sachacks-2018.firebaseapp.com",
    "databaseURL": "https://sachacks-2018.firebaseio.com",
    "projectId": "sachacks-2018",
    "storageBucket": "sachacks-2018.appspot.com",
    "messagingSenderId": "23141275388"
}

firebase = pyrebase.initialize_app(config)

