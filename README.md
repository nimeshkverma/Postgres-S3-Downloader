# Postgres-S3-Downloader

### Aim:
This repository aims to equip user with scripts for downloading all the documents of the customer via HTTP request. The urls for the customer are stored in the tables with following schema.

```
                                Table name: customer_documents
      Column      |           Type           |                            Modifiers                            
------------------+--------------------------+-----------------------------------------------------------------
 id               | integer                  | not null default nextval('customer_documents_id_seq'::regclass)
 created_at       | timestamp with time zone | not null
 updated_at       | timestamp with time zone | not null
 is_active        | boolean                  | not null
 document_1       | character varying(100)   | not null
 document_2       | character varying(100)   | 
 document_3       | character varying(100)   | 
 document_4       | character varying(100)   | 
 document_5       | character varying(100)   | 
 document_6       | character varying(100)   | 
 customer_id      | integer                  | not null
 document_type_id | integer                  | not null
 
                                     Table name: customer_document_types"
   Column   |           Type           |                              Modifiers                               
------------+--------------------------+----------------------------------------------------------------------
 id         | integer                  | not null default nextval('customer_document_types_id_seq'::regclass)
 created_at | timestamp with time zone | not null
 updated_at | timestamp with time zone | not null
 is_active  | boolean                  | not null
 name       | character varying(256)   | not null
 
 ```
 
 If the user has a different schema he/she can change the code in class `DocumentDownloader` in `documents_downloader.py` file as the code is pretty straightforward.
 
### Instructions:
- Clone the repo
- Make a virtual enviroment and install all the packages from `requirements.txt`
  `pip install -r requirements.txt`
- Make a `settings.py` using `settings_sample.py` file with actual values
- Change the code in the class `DocumentDownloader` in `documents_downloader.py` according to ones need

### How to Contribute

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
