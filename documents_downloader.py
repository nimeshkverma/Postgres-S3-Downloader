#!/usr/bin/python

import os
import sys
import requests
from settings import IMAGE_BASE_URL, WINDOWS
from service.database_service import Database


DOCUMENT_DICT_KEYS = {
    "document_1": "document_1_password",
    "document_2": "document_2_password",
    "document_3": "document_3_password",
    "document_4": "document_4_password",
    "document_5": "document_5_password",
    "document_6": "document_6_password",
}


class DocumentDownloader(object):

    def __init__(self, customer_id, db, original_file_name=True):
        self.db = db
        self.customer_id = customer_id
        self.original_file_name = original_file_name
        self.documents_sql_query = self.__documents_sql_query()
        self.document_type_sql_query = self.__document_type_sql_query()
        self.document_type = self.__document_type()
        self.documents = self.__documents()
        self.directory_name = self.__directory_name()

    def __directory_name(self):
        directory_name = ""
        name_sql_query = """
                            SELECT first_name, last_name 
                            from customer_aadhaar
                            WHERE customer_id={customer_id};
        """.format(customer_id=self.customer_id)
        name_rows = self.db.execute_query(name_sql_query)
        for name_row in name_rows:
            directory_name += name_row.get('first_name', 'NONE') + \
                '_' + name_row.get('last_name', 'NONE')
            break

        loan_sql_query = """
                            SELECT loan_amount, loan_tenure,loan_emi  
                            from loan_product
                            WHERE customer_id={customer_id};
        """.format(customer_id=self.customer_id)
        loan_rows = self.db.execute_query(loan_sql_query)
        for loan_row in loan_rows:
            directory_name += '_{loan_amount}_{loan_emi}_{loan_tenure}'.format(loan_amount=loan_row.get(
                'loan_amount', 'NONE'), loan_tenure=loan_row.get('loan_tenure', 'NONE'), loan_emi=loan_row.get('loan_emi', 'NONE'))
        return directory_name

    def __documents_sql_query(self):
        return """
                     SELECT  document_1, document_2, document_3, document_4, document_5, document_6, document_type_id,
                             document_1_password, document_2_password, document_3_password, document_4_password, document_5_password, document_6_password
                     FROM customer_documents
                     WHERE customer_id={customer_id};
               """.format(customer_id=self.customer_id)

    def __document_type_sql_query(self):
        return """
                    SELECT id, name FROM customer_document_types;
               """

    def __document_type(self):
        rows = self.db.execute_query(self.document_type_sql_query)
        document_type = {}
        for row in rows:
            document_type[row['id']] = row['name']
        return document_type

    def __documents(self):
        rows = self.db.execute_query(self.documents_sql_query)
        documents = {}
        for row in rows:
            documents[self.document_type[row['document_type_id']]] = {}
            for document_name_key, document_password_key in DOCUMENT_DICT_KEYS.iteritems():
                documents[self.document_type[row['document_type_id']]][document_name_key] = {
                    'name': row.get(document_name_key, ''),
                    'password': row.get(document_password_key, ''),
                }
        return documents

    def __file_downloader(self, url, file_data):
        if self.original_file_name:
            file_name = url.split('/')[-1]
            if file_data['password']:
                file_name = file_name.split(
                    '.pdf')[-2] + '_' + file_data['password'] + '.pdf'
        else:
            file_name = file_data['name']
        if WINDOWS:
            file_name = self.directory_name.upper() + "\\" + file_name
        else:
            file_name = self.directory_name.upper() + "/" + file_name
        print "Downloading File: {file_name} from URL: {url}".format(file_name=file_name, url=url)
        r = requests.get(url, timeout=60)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)

    def download(self):
        if self.directory_name:
            os.mkdir(self.directory_name)
        for document_type, document_data in self.documents.iteritems():
            for document_key, document_dict in document_data.iteritems():
                if document_dict and document_dict.get('name'):
                    file_name = "customer_id_{customer_id}_{document_type}_{document_key}_{document_password}".format(
                        customer_id=str(self.customer_id), document_type=document_type, document_key=document_key, document_password=document_dict['password'])
                    url = IMAGE_BASE_URL + document_dict['name']
                    self.__file_downloader(url, document_dict)

if __name__ == '__main__':
    db = Database()
    for customer_id in sys.argv[1:]:
        try:
            print 'Execution Start for the customer_id: ' + customer_id
            customer_id = int(customer_id)
            document_downloader = DocumentDownloader(customer_id, db)
            document_downloader.download()
            print 'Execution End for the customer_id: ' + str(customer_id)
        except Exception as e:
            print "Please provide the correct customer_id"
            print "Error: {error}".format(error=str(e))
    db.close_connection()
