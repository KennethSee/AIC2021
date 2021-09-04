import firebase_admin
from firebase_admin import credentials, firestore


class DB:
    def __init__(self, credential_path):
        if not firebase_admin._apps:
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
        if ref.get().exists:
            return ref.get().to_dict()
        else:
            return None

    def insert_financials(self, company_id: str, date: str, financials: dict):
        ref = self.companies.document(company_id)
        doc = ref.get()
        if doc.exists:
            ref.update({
                date: financials
            })
        else:
            self.companies.document(company_id).create({
                date: financials
            })

    def update_mappings(self, company_id, mappings: dict):
        ref = self.companies.document(company_id)
        doc = ref.get()
        if doc.exists:
            if 'mapping' in doc.to_dict():
                old_mapping = doc.to_dict()['mapping']
                # update mapping
                for key, val in mappings.items():
                    old_mapping[key] = val
                final_mapping = old_mapping
            else:
                final_mapping = mappings

            ref.update({'mapping': final_mapping})
        else:
            self.companies.document(company_id).create({
                'mapping': mappings
            })


# db = DB('secrets/aic2021-b72a6-firebase-adminsdk-cs1gs-777235e9ad.json')
# financials = {'test': 2}
# db.insert_financials('TestCompany', '3/9/21', financials)
# print(db.get_company_financials('TestCompany'))