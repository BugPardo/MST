from typing import Dict

import firebase_admin
from firebase_admin import credentials, firestore, db


class FirebaseAuth:
    def __init__(self, 
                 secret_location:str,
                 databaseurl:str = 'https://apysys-project-default-rtdb.firebaseio.com/', 
                 reference:str = 'test/documents'
                 ) -> None:
        self.secret_location = secret_location
        self.databaseurl = databaseurl
        self.reference = reference
        self.conn = None
        try:
            firebase_admin.initialize_app(credentials.Certificate(secret_location), {
                'databaseURL':databaseurl
            })
            print('Connection established')
        except Exception as e:
            print(e)
        pass

class RealTimeDB(FirebaseAuth):
    def _generate_connection(self, reference:str = None) -> None:
        """Generate connect to the reference (Path)

        Args:
            reference (str, optional): New Reference if it is needed. Defaults to None.
        """
        if reference:
            self.conn = db.reference(reference)
        else:
            self.conn = db.reference(self.reference)

    def insert_record(self, data:Dict, child:str = 'sample', reference:str =None) -> None:
        """Insert new records in RealtimeDatabase by child

        Args:
            data (Dict): Data in Dict format
            child (str, optional): Child to include the data. Defaults to 'sample'.
        """
        if self.conn == None:
            self._generate_connection(reference)

        print(f"Sending data to RealTime | {data}")
        try:
            if child:
                self.conn_object = self.conn.child(child).update(data)
            else:
                self.conn_object = self.conn.update(data)
        except Exception as e:
            print(f'There was an error, please review {e}')
            pass

    def collect_data(self, reference:str = None, child:str = None) -> Dict:
        """Collect results from path

        Args:
            reference (str, optional): Path to get data. Defaults to None.
            child (str, optional): node or key to get data. Defaults to None.

        Returns:
            Dict: Results in dict format by levels
        """
        if self.conn == None:
            self._generate_connection(reference)

        print(f'Collecting data from {self.conn.path}')
        try:
            return self.conn.child(child).get() if child else self.conn.get()
        except Exception as e:
                print(f'There was an error, please review {e}')

class FireStoreDB(FirebaseAuth):
    def _generate_connection(self) -> None:
        """Generate connect to the firebase app
        """
        if self.conn == None:
            self.conn = firestore.client()

    def insert_data(self, collection:str, document:str, data:Dict) -> None:
        """Insert data into firestore database
        Example: self.conn.collection('sample').document('test').set({'Hola':'mundo'})

        Args:
            collection (str): Collection name (new or existing)
            document (str):  document name (new or existing)
            data (Dict): {'Hola':'world'}
        """
        self._generate_connection()
        print(f"Adding data to /{collection}/{document}/")
        
        try:
            self.conn.collection(collection).document(document).set(data)
        except Exception as e:
            print(f'There was an error, please review {e}')

    def collect_data(self, collection:str, document:str) -> Dict:
        """Collect data from document in Dict format

        Args:
            collection (str): Collection name (new or existing)
            document (str):  document name (new or existing)

        Returns:
            Dict: data in dictionary format ->  {'Hola':'world'}
        """
        self._generate_connection()
        try:
            return self.conn.collection(collection).document(document).get().to_dict()
        except Exception as e:
            print(f'There was an error, please review {e}') 