import firebase_admin
from firebase_admin import credentials, firestore


class DB:
    def __init__(self, credential_path):
        cd = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cd)
        self.db = firestore.client()
        self.companies = self.db.collection(u'companies')

    def get_all(self):
        docs = self.companies.stream()
        for doc in docs:
            print(doc.id, doc.to_dict())

    def get_company_financials(self, company_id: str):
        ref = self.companies.document(company_id)
        return ref.get().to_dict()

    def insert_financials(self, company_id: str, date: str, financials: dict):
        ref = self.companies.document(company_id)
        ref.update({
            date: financials
        })


# db = DB('secrets/aic2021-b72a6-firebase-adminsdk-cs1gs-777235e9ad.json')
# financials = {'test': 2}
# db.insert_financials('TestCompany', '3/9/21', financials)
# print(db.get_company_financials('TestCompany'))