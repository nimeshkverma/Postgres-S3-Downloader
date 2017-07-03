#!/usr/bin/python

import sys
import requests
from settings import IMAGE_BASE_URL
from service.database_service import Database


class DocumentDownloader(object):

    def __init__(self, customer_id, db, original_file_name=True):
        self.db = db
        self.customer_id = customer_id
        self.original_file_name = original_file_name
        self.documents_sql_query = self.__documents_sql_query()
        self.document_type_sql_query = self.__document_type_sql_query()
        self.document_type = self.__document_type()
        self.documents = self.__documents()

    def __documents_sql_query(self):
        return """
                     SELECT  document_1, document_2, document_3, document_4, document_5, document_6, document_type_id
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
            documents[self.document_type[row['document_type_id']]] = row
            documents[self.document_type[row['document_type_id']]].pop(
                'document_type_id')
        return documents

    def __file_downloader(self, url, file_name):
        if self.original_file_name:
            file_name = url.split('/')[-1]
        print "Downloading File: {file_name} from URL: {url}".format(file_name=file_name, url=url)
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)

    def download(self):
        for document_type, document_dict in self.documents.iteritems():
            for document_key, document_value in document_dict.iteritems():
                if document_value:
                    file_name = "customer_id_{customer_id}_{document_type}_{document_key}".format(
                        customer_id=str(self.customer_id), document_type=document_type, document_key=document_key)
                    url = IMAGE_BASE_URL + document_value
                    self.__file_downloader(url, file_name)

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
