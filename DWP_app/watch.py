# import re
# import os
# import json
# import time
# import pathlib
# import datetime
# from . import watch_dog
# import pdfplumber
# from halo import Halo
# from django.conf import settings
# from django.http.response import JsonResponse
# from rest_framework.decorators import api_view
# import  json
# from django.http import HttpResponse


# ############ Watch dog code################
# import json
# from django.http import HttpResponse
# import os
# import time
# import datetime
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# from os.path import join
# from glob import glob
# from django.conf import settings
# import requests

# list_queue = []
# File_details = {}
# client_paths = settings.CLIENT_PATHS
# client_folders = []
# for i in range(len(client_paths)):
#     unix = str(int(time.mktime(datetime.date.today().timetuple())))
#     client_folders.append(os.path.join(client_paths[i],unix))


# def on_created(events):
#     file_path = events.src_path
#     file_name = os.path.basename(file_path)
#     dir = os.path.dirname(file_path)
#     dirname2 = os.path.split(dir)[1]
#     filename, file_extension = os.path.splitext(file_path)

#     if file_extension == '.pdf':
#         File_details = {
#             'file_path': file_path,
#             'file_name': file_name,
#             'folder_name': dirname2,
#             'file_extension': file_extension
#         }
#         files = []
#         for ext in ('*.pdf', '*.json', '*.xml'):
#             files.extend(glob(join(os.path.dirname(File_details.get('file_path')), ext)))
#         json_file = os.path.join(os.path.dirname(File_details.get('file_path')), os.path.splitext(file_path)[0]+'.json')
#         inp_file = os.path.join(os.path.dirname(File_details.get('file_path')),os.path.splitext(file_path)[0] + '.inp')
#         if (json_file not in files) and (inp_file not in files):
#             if File_details not in list_queue:
#                 for i in client_folders:
#                     client_files = os.listdir(i)
#                     if file_name in client_files:
#                         temp_name = File_details.get('file_name')
#                         inp_extn = temp_name.replace('.pdf', '.inp')
#                         f = open(os.path.join(i, inp_extn), 'w')
#                         f.close()
#                         list_queue.append(File_details)
#             else:
#                 print('Pdf already available in the queue')
#         elif (json_file not in files) and (inp_file in files) :
#             print('Pdf already available in the queue')
#         else:
#             print(json_file,' The pdf is already processed')
#     print(list_queue)
#     if len(list_queue) > 0:
#         if len(list_queue) >= settings.QUEUE_SIZE:
#             print('Multi')
#             # for i in range(len(list_queue)):
#                 # invoice_file.main_parser(list_queue.pop(0))
#             json_obj = json.dumps(list_queue.pop(0))
#             headers = {
#                 'Content-Type': 'application/json'
#             }
#             res = requests.post( url = settings.CLIENT_URL, headers=headers, data=json_obj, allow_redirects=True)
#             return HttpResponse('Successful')
#         if len(list_queue) < settings.QUEUE_SIZE:
#             print('Single')
#             for i in range(len(list_queue)):
#                 json_obj = json.dumps(list_queue.pop(0))
#                 headers = {
#                     'Content-Type': 'application/json'
#                 }
#                 res = requests.post(url=settings.CLIENT_URL,headers=headers, data = json_obj, timeout=10, allow_redirects=True)
#             return HttpResponse('Successful')


# def list_of_files(client_path):
#     dir_files = os.listdir(client_path)
#     dir_files2 = [x for x in dir_files if not x.endswith('.json') and not x.endswith('.inp')]
#     for file in dir_files2:
#         if file.replace('.pdf','.inp') not in dir_files and file.replace('.pdf','.json') not in dir_files:
#             file_path = os.path.join(client_path, file)
#             file_name = os.path.basename(file_path)
#             dir_name = os.path.dirname(file_path)
#             folder_name = os.path.split(dir_name)[1]
#             # filename, file_extension = os.path.splitext(file_path)
#             prev_details = {
#                 'file_path': file_path,
#                 'file_name': file_name,
#                 'folder_name': folder_name,
#                 'file_extension': '.pdf'
#             }
#             temp_name = prev_details.get('file_name')
#             i = temp_name.replace('.pdf', '.inp')
#             f = open(os.path.join(client_path, i), 'w')
#             f.close()
#             list_queue.append(prev_details)

# def remove_inp_files(client_path):
#     files = os.listdir(client_path)
#     dir_files2 = [x for x in files if not x.endswith('.json') and not x.endswith('.inp')]
#     for file in dir_files2:
#         if file.replace('.pdf', '.inp') in files and file.replace('.pdf', '.json') not in files:
#             temp = file.replace('.pdf', '.inp')
#             os.remove(os.path.join(client_path, temp))

# def main_file(request):
#     for i in client_folders:
#         remove_inp_files(i)
#         list_of_files(i)
#     print('*********** List of pdf files which are not recognized by the watchdog ***********\n')
#     if len(list_queue) > 0:
#         print(list_queue)
#     else:
#         print('No pdf files in the list queue')
#     event_handler = FileSystemEventHandler()
#     event_handler.on_created = on_created
#     observer = Observer()
#     if len(list_queue) > 0:
#         if len(list_queue) >= settings.QUEUE_SIZE:
#             print('Multi')
#             # for i in range(len(list_queue)):
#             # invoice_file.main_parser(list_queue.pop(0))
#             json_obj = json.dumps(list_queue.pop(0))
#             headers = {
#                 'Content-Type': 'application/json'
#             }
#             res = requests.post(url=settings.CLIENT_URL, headers=headers, data=json_obj, allow_redirects=True)
#             return HttpResponse('Successful')
#         if len(list_queue) < settings.QUEUE_SIZE:
#             print('Single')
#             for i in range(len(list_queue)):
#                 json_obj = json.dumps(list_queue.pop(0))
#                 headers = {
#                     'Content-Type': 'application/json'
#                 }
#                 res = requests.post(url=settings.CLIENT_URL, headers=headers, data=json_obj, timeout=10,
#                                     allow_redirects=True)
#             return HttpResponse('Successful')
#     for i in client_folders:
#         a = observer.schedule(event_handler, i, recursive=True)

#     observer.start()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print('Thanks for your this appliction')
#         observer.stop()
#     observer.join()

# #####################Watch dog code completed#############################

# def Account_number(text):
#     pass


# def Bill_number(text):
#     pass


# def Customer_code(text):
#     pass


# def Supplier_name(text):
#     pass


# def Supplier_address(text):
#     pass


# def Buyer_name(text):
#     pass


# def Buyer_address(text):
#     pass


# def Convert_Date(text):
#     ''' This function will covert string to date format '''
#     for fmt in ['%d-%b-%Y', '%d-%m-%Y', '%d-%b-%y', '%d-%m-%y']:
#         try:
#             return datetime.datetime.strptime(text, fmt).strftime('%d-%m-%Y')
#         except ValueError:
#             pass


# def Invoice(text):
#     ''' This Function will find Invoice Number in PDF '''
#     keywords = {
#         'invoice_keys': [
#             'invoice #', 'invoice number :', 'invoice number', 'tax invoice copynumber', 'tax invoice', 'tax invoice:',
#             'invoice no', 'tax invoice #', 'original invoice', 'invoice no:', 'nutrienagsolutions', 'invoice #:',
#             'invoicenumber', 'see over for details', 'Tax Credit', 'inv no.', 'invoice no.', 'tax adjustment note:',
#             'invoice number:', 'invoice no :', 'invoice no.:', 'invoice id ....................:',
#             'credit adjustment note', 'account number'
#         ]
#     }
#     for i, j in keywords.items():
#         for name in j:
#             Tran_lang = name
#             try:
#                 n = {3}
#                 invoice_re = re.compile(
#                     fr"({Tran_lang}\)\s+\d+)|({Tran_lang}\s+\w\d+\-\d+\-\d+)|({Tran_lang}\s+\d{n}\d+)|({Tran_lang}\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+)|({Tran_lang}\s+\w+\-\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+\-\d+)")
#                 keyword_invoice = invoice_re.search(text).group()

#                 if Tran_lang in keyword_invoice:
#                     find_word = Tran_lang
#                     main_invoice = keyword_invoice.replace(Tran_lang, '').strip()
#                     return main_invoice, find_word
#             except:
#                 pass


# def Abn(text):
#     '''The Australian Business Number (ABN) is a unique 11-digit identifier issued by the Australian Business Register (ABR) which is operated by the Australian Taxation Office (ATO). The ABN was introduced on 1 July 2000 by John Howard's Liberal government as part of a major tax reform, which included the introduction of a GST.'''
#     try:
#         abn_number = re.search(r"(abn\d+)|(abn:\d+)|(a.b.n.\d+)", text)
#         abn = ""
#         for m in abn_number.group():
#             if m.isdigit():
#                 abn += m
#         return int(abn)
#     except:
#         pass


# def Due_date(text):
#     '''This Function will get Due Date in pdf'''
#     try:
#         date = ""
#         due_date = re.search(
#             'due date:\s+\d+\s+\w+\s+\d+|due date:\s+\d+-\w+-\d+|due date: by\s+\d+\s+\w+\s+\d+|due date:\s+\d+/\w+/\d+|due date:\s+\d+.\d+.\d+|due date:\s+\d+/\d+/\d+|\d+/\d+/\d+\s+mainfreight',
#             text)
#         date = due_date.group().replace('due date:', '').replace('.', '-').replace(' ', '-').replace('/', '-').replace(
#             'by--', '')
#         due_date_parser = Convert_Date(text=date)
#         return due_date_parser
#     except:
#         pass


# def Due(text):
#     '''This Function will find Due days in pdf and send to Invoice_Date Function'''
#     day = 0
#     try:
#         days = ""
#         due_number = re.search(r"(\d+\s+days)|(month\s+\d{2})", text)
#         for m in due_number.group():
#             if m.isdigit():
#                 days += m
#         return int(days)
#     except:
#         pass


# def Invoice_Date(text):
#     ''' This Function Will get Invoice Date  from PDF after Covert into Date Format if we have Deu days it'll calculte Due Date and return '''

#     pattern_list = ['\d+([/]|[.])\d+([/]|[.])([2][0][0-9][0-9]|[0-9][0-9])',
#                     '([0-9]|[0-9][0-9])([\s]|[]|[-])(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)([\s]|[]|[-])([2][0][0-9][0-9]|[0-9][0-9])']

#     temp = []
#     for regex in pattern_list:
#         try:
#             find_date = re.search(regex, text)
#             replce_data = find_date.group().replace('.', '-').replace(' ', '-').replace('/', '-')
#             convert_date = Convert_Date(text=replce_data)
#             temp.append(convert_date)
#             return temp[0]
#         except:
#             pass


# def Invoice_Details(data):
#     invoice_unmissing_count = invoice_missing_count = invoice_missing_date = invoice_unmissing_date = invoice_missing_due_date = invoice_unmissing_due_date = invoice_missing_abn = invoice_unmissing_abn = 0
#     for i, j in data.items():

#         if j['Invoice_number'] == 'N/A':
#             invoice_missing_count += 1
#         else:
#             invoice_unmissing_count += 1

#         if j['Invoice_date'] == 'N/A':
#             invoice_missing_date += 1
#         else:
#             invoice_unmissing_date += 1

#         if j['Due_date'] == 'N/A':
#             invoice_missing_due_date += 1
#         else:
#             invoice_unmissing_due_date += 1

#         if j['ABN'] == 'N/A':
#             invoice_missing_abn += 1
#         else:
#             invoice_unmissing_abn += 1

#     Invoice_counts = {
#         'Missing Invoice': invoice_missing_count,
#         'Ubnv nmissing Invocie': invoice_unmissing_count,
#         'Missing Invoice Date': invoice_missing_date,
#         'Unmissing Invoice Date': invoice_unmissing_date,
#         'Missing Invoice Due Date': invoice_missing_due_date,
#         'UnMissing Invoice Due Date': invoice_unmissing_due_date,
#         'Missing Invoice ABN': invoice_missing_abn,
#         'Unmissing Invoice ABN': invoice_unmissing_abn
#     }

#     output_file = os.path.abspath('output/')
#     pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#     with open(os.path.join(output_file, 'Invoice_counts.json'), 'w') as finalfile:
#         json.dump(Invoice_counts, finalfile)


# client_paths = settings.CLIENT_PATHS
# client_folders = []
# for i in range(len(client_paths)):
#     unix = str(int(time.mktime(datetime.date.today().timetuple())))
#     client_folders.append(os.path.join(client_paths[i],unix))

# @api_view(['GET','POST'])
# def main_parser(request):
#     if request.method == 'POST':
#         path_data = request.data
#         print(path_data)
#         # return HttpResponse('Successful')
#         try:
#             for i, j in path_data.items():
#                 if i == 'file_name':
#                     file_name = j
#                 if i == 'file_path':
#                     path = os.path.dirname(j)
#             # spinner = Halo(text='Read PDF to Find Invoice', spinner='dot')
#             # spinner.start()

#             file_list = {}
#             bulk_data = {}
#             single_data = {}
#             count = 0
#             # lists = os.listdir(path)

#             # for file_name in lists:
#             file_json = file_name.replace('.pdf', '.json')
#             file_xml = file_name.replace('.pdf', '.xml')
#             file_list[f'file_{count}'] = file_name
#             file_path = os.path.join(path,file_name)
#             text = ""

#             with pdfplumber.open(file_path) as pdf:
#                 total_pages = len(pdf.pages)
#                 test = pdf.pages[0 - total_pages]
#                 text += test.extract_text().replace('\n', ' ').lower()
#                 text1 = text.replace(' ', '')
#             pdf.close()

#             if len(text) > 0:

#                 if Invoice_Date(text) is not None:
#                     in_date = Invoice_Date(text)
#                 else:
#                     in_date = 'N/A'

#                 if Due(text) is not None:
#                     day = Due(text)
#                 else:
#                     day = 'N/A'

#                 if Due_date(text) is not None:
#                     if in_date == Due_date(text):
#                         if day != 'N/A' and in_date != 'N/A':
#                             du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y') + datetime.timedelta(days=day)).strftime(
#                                 '%d-%m-%Y')

#                 elif Due_date(text) is None:
#                     if day != 'N/A' and in_date != 'N/A':
#                         du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y') + datetime.timedelta(days=day)).strftime(
#                             '%d-%m-%Y')
#                     else:
#                         du_date = 'N/A'

#                 if Invoice(text) is not None:
#                     Invoice_number, Invoice_Keyword = Invoice(text)
#                 else:
#                     Invoice_number = Invoice_Keyword = 'N/A'

#                 if Abn(text1) is not None:
#                     abn = Abn(text1)
#                 else:
#                     abn = 'N/A'

#                 '''single json  File Remove '[fie_name]' in data and uncomment code same as else also'''

#                 # bulk_data[file_name]= {
#                 #     'File_name':file_name,
#                 #     'Invoice_number': Invoice_number,
#                 #     'Invoice_Keyword': Invoice_Keyword,
#                 #     'Invoice_date': in_date,
#                 #     'Due_date':du_date,
#                 #     'ABN':abn,
#                 #     'Account_number':'soon',
#                 #     'Bill_number':'soon',
#                 #     'Customer_number':'soon',
#                 #     'Supplier_name':'soon',
#                 #     'Supplier_address':'soon',
#                 #     'Buyer_name':'soon',
#                 #     'Buyer_address':'soon'
#                 # }

#                 single_data = {
#                     'File_name': file_name,
#                     'Invoice_number': Invoice_number,
#                     'Invoice_Keyword': Invoice_Keyword,
#                     'Invoice_date': in_date,
#                     'Due_date': du_date,
#                     'ABN': abn,
#                     'Account_number': 'soon',
#                     'Bill_number': 'soon',
#                     'Customer_number': 'soon',
#                     'Supplier_name': 'soon',
#                     'Supplier_address': 'soon',
#                     'Buyer_name': 'soon',
#                     'Buyer_address': 'soon'
#                 }

#                 '''For singledata Json file Uncomment this '''

#                 output_file = os.path.abspath(path)
#                 pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#                 with open(os.path.join(output_file, file_json), 'w') as finalfile:
#                     json.dump(single_data, finalfile)

#                 '''For singledata XML file Uncomment this '''

#                 # output_file = os.path.abspath(path)
#                 # pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#                 # xml = dicttoxml(single_data)
#                 # with open(os.path.join(output_file, file_xml), 'w') as xmlfile:
#                 #     xmlfile.write(xml.decode())
#                 #     xmlfile.close()

#                     # '''N/R Measn non readable pdf'''
#             else:

#                 # bulk_data[file_name] = {
#                 #     'File_name':file_name,
#                 #     'Invoice_number': 'N/R',
#                 #     'Invoice_Keyword': 'N/R',
#                 #     'Invoice_date': 'N/R',
#                 #     'Due_date':'N/R',
#                 #     'ABN':'N/R',
#                 #     'Account_number':'N/R',
#                 #     'Bill_number':'N/R',
#                 #     'Customer_number':'N/R',
#                 #     'Supplier_name':'N/R',
#                 #     'Supplier_address':'N/R',
#                 #     'Buyer_name':'N/R',
#                 #     'Buyer_address':'N/R'
#                 # }

#                 single_data = {
#                     'File_name': file_name,
#                     'Invoice_number': 'N/R',
#                     'Invoice_Keyword': 'N/R',
#                     'Invoice_date': 'N/R',
#                     'Due_date': 'N/R',
#                     'ABN': 'N/R',
#                     'Account_number': 'N/R',
#                     'Bill_number': 'N/R',
#                     'Customer_number': 'N/R',
#                     'Supplier_name': 'N/R',
#                     'Supplier_address': 'N/R',
#                     'Buyer_name': 'N/R',
#                     'Buyer_address': 'N/R'
#                 }

#                 '''For singledata Json file Uncomment this '''
#                 output_file = os.path.abspath(path)
#                 pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#                 with open(os.path.join(output_file, file_json), 'w') as finalfile:
#                     json.dump(single_data, finalfile)

#                 '''For singledata XML file Uncomment this '''
#                 output_file = os.path.abspath(path)
#                 pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#                 # xml = dicttoxml(single_data)
#                 # with open(os.path.join(output_file, file_xml), 'w') as xmlfile:
#                 #     xmlfile.write(xml.decode())
#                 #     xmlfile.close()

#             # Invoice_Details(bulk_data)

#             # output_file  = os.path.abspath('output/Bulk_file_json/')
#             # pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

#             # with open(os.path.join(output_file,'invoice.json'), 'w') as finalfile:
#             #     json.dump(bulk_data, finalfile)

#             # '''For bulkdata XML file Uncomment this '''
#             # output_file  = os.path.abspath('output/Bulk_file_xml/')
#             # pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)
#             # xml=dicttoxml(bulk_data)
#             # with open(os.path.join(output_file,file_xml), 'w') as xmlfile:
#             #     xmlfile.write(xml.decode())
#             #     xmlfile.close()
#         except Exception as e:
#             print('Exception details',e)
#         finally:
#             for i in client_folders:
#                 client_files = os.listdir(i)
#                 file = file_name
#                 if file in client_files:
#                     if file.replace('.pdf', '.inp') in client_files:
#                         temp = file.replace('.pdf', '.inp')
#                         os.remove(os.path.join(i, temp))
#     return HttpResponse('Successful')































from audioop import reverse
import os
import re
import json
import time
import pathlib
import datetime
import requests
import pdfplumber
from DWP_app import Business_Logic
from django.conf import settings
from watchdog.observers import Observer
from rest_framework.request import Request
from watchdog.events import FileSystemEventHandler

list_Queue=[]
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        main_path = event.src_path
        file_name = os.path.basename(main_path)
        file_path = os.path.dirname(main_path)
        _,file_extension  = os.path.splitext(file_name)
        data = {
         'main_path' : main_path,
        'file_name' : file_name,
        'file_path' : file_path,
        'file_exe':  file_extension
        }
        print(main_path)
        rr = requests.post( requests.__build__(reverse(Business_Logic.main)),data={'file_path':main_path}
    )
        # rr = requests.post(url='https://172.0.0.1:8000/',params={'file_path':main_path},Business_Logic.main)
        # rr = Request.query_params('https://172.0.0.1:8000/', data = {Business_Logic.main:main_path})
        print(rr.json())
            # t = threading.Thread(target=Business_Logic.main, args=(main_path,))
            # t.start()
            # t.join()
            # Business_Logic.main(main_path)
        # if data not in list_Queue:
        #     list_Queue.append(data)
        # open(os.path.join(file_path,file_name.replace('.pdf','.temp')),'a').close()

def main():
    print('\n Welcome TO I-PDF-WATCHER\n')
    handler = Handler()
    observer = Observer()
    n = int(input("Number Of clinet folder : "))
    unix = str(int(time.mktime(datetime.date.today().timetuple())))
    for i in range(0, n):
        folder = input("\nEnter The Clinet folder path: ")
        path = os.path.join(folder,unix)
        observer.schedule(handler, path=path, recursive=True)
        list_files = os.listdir(path)
        only_pdf = [x for x in list_files if not x.endswith('.json') and not x.endswith('.temp')]
        for pdf_file in only_pdf:
            if pdf_file.replace('.pdf','.temp') not in list_files and pdf_file.replace('.pdf','.json') not in list_files:
                main_path = os.path.join(path,pdf_file)
                file_name = os.path.basename(main_path)
                file_path = os.path.dirname(main_path)
                _,file_extension  = os.path.splitext(file_name)
                data = {
                'main_path' : main_path,
                'file_name' : file_name,
                'file_path' : file_path,
                'file_exe':  file_extension
                }
                # open(os.path.join(path,pdf_file.replace('.pdf','.temp')),'a').close()
        #         if data not in list_Queue:
        #             list_Queue.append(data)
                    
        # for re_file in only_pdf:
        #     if re_file.replace('.pdf', '.temp') in list_files and re_file.replace('.pdf', '.json') not in list_files:
        #         temp = re_file.replace('.pdf', '.temp')
        #         os.remove(os.path.join(path, temp))
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()




# # # ------------------------------------------------------- Watchdog Logic Start Here -------------------------------------------------------

# # # list_queue = []
# # # File_details = {}
# # # client_paths = settings.CLIENT_PATHS
# # # client_folders = []

# # # for i in range(len(client_paths)):
# # #     unix = str(int(time.mktime(datetime.date.today().timetuple())))
# # #     client_folders.append(os.path.join(client_paths[i],unix))

# # # def on_created(events):
# # #     file_path = events.src_path
# # #     file_name = os.path.basename(file_path)
# # #     dir = os.path.dirname(file_path)
# # #     dirname2 = os.path.split(dir)[1]
# # #     filename, file_extension = os.path.splitext(file_path)

# # #     if file_extension == '.pdf':
# # #         File_details = {
# # #             'file_path': file_path,
# # #             'file_name': file_name,
# # #             'folder_name': dirname2,
# # #             'file_extension': file_extension
# # #         }
# # #         files = []
# # #         for ext in ('*.pdf', '*.json'):
# # #             files.extend(glob(os.path.join(os.path.dirname(File_details.get('file_path')), ext)))
# # #         json_file = os.path.join(os.path.dirname(File_details.get('file_path')), os.path.splitext(file_path)[0]+'.json')
# # #         inp_file = os.path.join(os.path.dirname(File_details.get('file_path')),os.path.splitext(file_path)[0] + '.inp')
# # #         if (json_file not in files) and (inp_file not in files):
# # #             if File_details not in list_queue:
# # #                 for i in client_folders:
# # #                     client_files = os.listdir(i)
# # #                     if file_name in client_files:
# # #                         temp_name = File_details.get('file_name')
# # #                         inp_extn = temp_name.replace('.pdf', '.inp')
# # #                         f = open(os.path.join(i, inp_extn), 'w')
# # #                         f.close()
# # #                         list_queue.append(File_details)
# # #             else:
# # #                 print('Pdf already available in the queue')
# # #         elif (json_file not in files) and (inp_file in files) :
# # #             print('Pdf already available in the queue')
# # #         else:
# # #             print(json_file,' The pdf is already processed')
# # #     print(list_queue)
# # #     if len(list_queue) > 0:
# # #         if len(list_queue) >= settings.QUEUE_SIZE:
# # #             print('Multi')
# # #             json_obj = json.dumps(list_queue.pop(0))
# # #             headers = {
# # #                 'Content-Type': 'application/json'
# # #             }
# # #             res = requests.post( url = settings.CLIENT_URL, headers=headers, data=json_obj, allow_redirects=True)
# # #             return HttpResponse('Successful')
# # #         if len(list_queue) < settings.QUEUE_SIZE:
# # #             print('Single')
# # #             for i in range(len(list_queue)):
# # #                 json_obj = json.dumps(list_queue.pop(0))
# # #                 headers = {
# # #                     'Content-Type': 'application/json'
# # #                 }
# # #                 res = requests.post(url=settings.CLIENT_URL,headers=headers, data = json_obj, timeout=10, allow_redirects=True)
# # #             return HttpResponse('Successful')

# # # def list_of_files(client_path):
# # #     dir_files = os.listdir(client_path)
# # #     dir_files2 = [x for x in dir_files if not x.endswith('.json') and not x.endswith('.inp')]
# # #     for file in dir_files2:
# # #         if file.replace('.pdf','.inp') not in dir_files and file.replace('.pdf','.json') not in dir_files:
# # #             file_path = os.path.join(client_path, file)
# # #             file_name = os.path.basename(file_path)
# # #             dir_name = os.path.dirname(file_path)
# # #             folder_name = os.path.split(dir_name)[1]
# # #             prev_details = {
# # #                 'file_path': file_path,
# # #                 'file_name': file_name,
# # #                 'folder_name': folder_name,
# # #                 'file_extension': '.pdf'
# # #             }
# # #             temp_name = prev_details.get('file_name')
# # #             i = temp_name.replace('.pdf', '.inp')
# # #             f = open(os.path.join(client_path, i), 'w')
# # #             f.close()
# # #             list_queue.append(prev_details)

# # # def remove_inp_files(client_path):
# # #     files = os.listdir(client_path)
# # #     dir_files2 = [x for x in files if not x.endswith('.json') and not x.endswith('.inp')]
# # #     for file in dir_files2:
# # #         if file.replace('.pdf', '.inp') in files and file.replace('.pdf', '.json') not in files:
# # #             temp = file.replace('.pdf', '.inp')
# # #             os.remove(os.path.join(client_path, temp))

# # # def main_file():
# # #     print('-'*5,'Main File Running','-'*5)
# # #     for i in client_folders:
# # #         remove_inp_files(i)
# # #         list_of_files(i)
# # #     print('*********** List of pdf files which are not recognized by the watchdog ***********\n')
# # #     if len(list_queue) > 0:
# # #         print(list_queue)
# # #     else:
# # #         print('No pdf files in the list queue')
# # #     event_handler = FileSystemEventHandler()
# # #     event_handler.on_created = on_created
# # #     observer = Observer()
# # #     if len(list_queue) > 0:
# # #         if len(list_queue) >= settings.QUEUE_SIZE:
# # #             print('Multi')
# # #             json_obj = json.dumps(list_queue.pop(0))
# # #             headers = {
# # #                 'Content-Type': 'application/json'
# # #             }
# # #             # res = requests.post(url=settings.CLIENT_URL, headers=headers, data=json_obj, allow_redirects=True)
# # #             # return HttpResponse('Successful')
# # #         if len(list_queue) < settings.QUEUE_SIZE:
# # #             print('Single')
# # #             for i in range(len(list_queue)):
# # #                 json_obj = json.dumps(list_queue.pop(0))
# # #                 headers = {
# # #                     'Content-Type': 'application/json'
# # #                 }
# # #             #     res = requests.post(url=settings.CLIENT_URL, headers=headers, data=json_obj, timeout=10,
# # #             #                         allow_redirects=True)
# # #             # return HttpResponse('Successful')
# # #     for i in client_folders:
# # #         a = observer.schedule(event_handler, i, recursive=True)

# # #     observer.start()
# # #     try:
# # #         while True:
# # #             time.sleep(1)
# # #     except KeyboardInterrupt:
# # #         print('Thanks for your this appliction')
# # #         observer.stop()
# # #     observer.join()

# # # # ------------------------------------------------------- Business Logic  Start Here -------------------------------------------------------

# # # def Account_number(text):
# # #     pass

# # # def Bill_number(text):
# # #     pass

# # # def Customer_code(text):
# # #     pass

# # # def Supplier_name(text):
# # #     pass

# # # def Supplier_address(text):
# # #     pass

# # # def Buyer_name(text):
# # #     pass

# # # def Buyer_address(text):
# # #     pass

# # # def Convert_Date(text):
# # #     ''' This function will covert string to date format '''
# # #     for fmt in ['%d-%b-%Y', '%d-%m-%Y', '%d-%b-%y', '%d-%m-%y']:
# # #         try:
# # #             return datetime.datetime.strptime(text, fmt).strftime('%d-%m-%Y')
# # #         except ValueError:
# # #             pass

# # # def Invoice(text):
# # #     ''' This Function will find Invoice Number in PDF '''
# # #     keywords = {
# # #         'invoice_keys': [
# # #             'invoice #', 'invoice number :', 'invoice number', 'tax invoice copynumber', 'tax invoice', 'tax invoice:',
# # #             'invoice no', 'tax invoice #', 'original invoice', 'invoice no:', 'nutrienagsolutions', 'invoice #:',
# # #             'invoicenumber', 'see over for details', 'Tax Credit', 'inv no.', 'invoice no.', 'tax adjustment note:',
# # #             'invoice number:', 'invoice no :', 'invoice no.:', 'invoice id ....................:',
# # #             'credit adjustment note', 'account number'
# # #         ]
# # #     }
# # #     for i, j in keywords.items():
# # #         for name in j:
# # #             Tran_lang = name
# # #             try:
# # #                 n = {3}
# # #                 invoice_re = re.compile(
# # #                     fr"({Tran_lang}\)\s+\d+)|({Tran_lang}\s+\w\d+\-\d+\-\d+)|({Tran_lang}\s+\d{n}\d+)|({Tran_lang}\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+)|({Tran_lang}\s+\w+\-\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+\-\d+)")
# # #                 keyword_invoice = invoice_re.search(text).group()

# # #                 if Tran_lang in keyword_invoice:
# # #                     find_word = Tran_lang
# # #                     main_invoice = keyword_invoice.replace(Tran_lang, '').strip()
# # #                     return main_invoice, find_word
# # #             except:
# # #                 pass

# # # def Abn(text):
# # #     '''The Australian Business Number (ABN) is a unique 11-digit identifier issued by the Australian Business Register (ABR) which is operated by the Australian Taxation Office (ATO). The ABN was introduced on 1 July 2000 by John Howard's Liberal government as part of a major tax reform, which included the introduction of a GST.'''
# # #     try:
# # #         abn_number = re.search(r"(abn\d+)|(abn:\d+)|(a.b.n.\d+)", text)
# # #         abn = ""
# # #         for m in abn_number.group():
# # #             if m.isdigit():
# # #                 abn += m
# # #         return int(abn)
# # #     except:
# # #         pass

# # # def Due_date(text):
# # #     '''This Function will get Due Date in pdf'''
# # #     try:
# # #         date = ""
# # #         due_date = re.search(
# # #             'due date:\s+\d+\s+\w+\s+\d+|due date:\s+\d+-\w+-\d+|due date: by\s+\d+\s+\w+\s+\d+|due date:\s+\d+/\w+/\d+|due date:\s+\d+.\d+.\d+|due date:\s+\d+/\d+/\d+|\d+/\d+/\d+\s+mainfreight',
# # #             text)
# # #         date = due_date.group().replace('due date:', '').replace('.', '-').replace(' ', '-').replace('/', '-').replace(
# # #             'by--', '')
# # #         due_date_parser = Convert_Date(text=date)
# # #         return due_date_parser
# # #     except:
# # #         pass

# # # def Due(text):
# # #     '''This Function will find Due days in pdf and send to Invoice_Date Function'''
# # #     try:
# # #         days = ""
# # #         due_number = re.search(r"(\d+\s+days)|(month\s+\d{2})", text)
# # #         for m in due_number.group():
# # #             if m.isdigit():
# # #                 days += m
# # #         return int(days)
# # #     except:
# # #         pass

# # # def Invoice_Date(text):
# # #     ''' This Function Will get Invoice Date  from PDF after Covert into Date Format if we have Deu days it'll calculte Due Date and return '''

# # #     pattern_list = ['\d+([/]|[.])\d+([/]|[.])([2][0][0-9][0-9]|[0-9][0-9])',
# # #                     '([0-9]|[0-9][0-9])([\s]|[]|[-])(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)([\s]|[]|[-])([2][0][0-9][0-9]|[0-9][0-9])']

# # #     temp = []
# # #     for regex in pattern_list:
# # #         try:
# # #             find_date = re.search(regex, text)
# # #             replce_data = find_date.group().replace('.', '-').replace(' ', '-').replace('/', '-')
# # #             convert_date = Convert_Date(text=replce_data)
# # #             temp.append(convert_date)
# # #             return temp[0]
# # #         except:
# # #             pass

# # # def Invoice_Details(data):
# # #     invoice_unmissing_count = invoice_missing_count = invoice_missing_date = invoice_unmissing_date = invoice_missing_due_date = invoice_unmissing_due_date = invoice_missing_abn = invoice_unmissing_abn = 0
# # #     for i, j in data.items():

# # #         if j['Invoice_number'] == 'N/A':
# # #             invoice_missing_count += 1
# # #         else:
# # #             invoice_unmissing_count += 1

# # #         if j['Invoice_date'] == 'N/A':
# # #             invoice_missing_date += 1
# # #         else:
# # #             invoice_unmissing_date += 1

# # #         if j['Due_date'] == 'N/A':
# # #             invoice_missing_due_date += 1
# # #         else:
# # #             invoice_unmissing_due_date += 1

# # #         if j['ABN'] == 'N/A':
# # #             invoice_missing_abn += 1
# # #         else:
# # #             invoice_unmissing_abn += 1

# # #     Invoice_counts = {
# # #         'Missing Invoice': invoice_missing_count,
# # #         'Ubnv nmissing Invocie': invoice_unmissing_count,
# # #         'Missing Invoice Date': invoice_missing_date,
# # #         'Unmissing Invoice Date': invoice_unmissing_date,
# # #         'Missing Invoice Due Date': invoice_missing_due_date,
# # #         'UnMissing Invoice Due Date': invoice_unmissing_due_date,
# # #         'Missing Invoice ABN': invoice_missing_abn,
# # #         'Unmissing Invoice ABN': invoice_unmissing_abn
# # #     }

# # #     output_file = os.path.abspath('output/')
# # #     pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

# # #     with open(os.path.join(output_file, 'Invoice_counts.json'), 'w') as finalfile:
# # #         json.dump(Invoice_counts, finalfile)

# # # client_paths = settings.CLIENT_PATHS
# # # client_folders = []
# # # for i in range(len(client_paths)):
# # #     unix = str(int(time.mktime(datetime.date.today().timetuple())))
# # #     client_folders.append(os.path.join(client_paths[i],unix))


# # # def main_parser(request):
# #     # if request.method == 'POST':
# #     #     path_data = request.data
# #     #     print(path_data)
        
# #     #     try:
# #     #         for i, j in path_data.items():
# #     #             if i == 'file_name':
# #     #                 file_name = j
# #     #             if i == 'file_path':
# #     #                 path = os.path.dirname(j)
                    
# #     #         file_list = {}
# #     #         single_data = {}
# #     #         count = 0

# #     #         file_json = file_name.replace('.pdf', '.json')
# #     #         file_xml = file_name.replace('.pdf', '.xml')
# #     #         file_list[f'file_{count}'] = file_name
# #     #         file_path = os.path.join(path,file_name)
# #     #         text = ""

# #     #         with pdfplumber.open(file_path) as pdf:
# #     #             total_pages = len(pdf.pages)
# #     #             test = pdf.pages[0 - total_pages]
# #     #             text += test.extract_text().replace('\n', ' ').lower()
# #     #             text1 = text.replace(' ', '')
# #     #         pdf.close()

# #     #         if len(text) > 0:

# #     #             if Invoice_Date(text) is not None:
# #     #                 in_date = Invoice_Date(text)
# #     #             else:
# #     #                 in_date = 'N/A'

# #     #             if Due(text) is not None:
# #     #                 day = Due(text)
# #     #             else:
# #     #                 day = 'N/A'

# #     #             if Due_date(text) is not None:
# #     #                 if in_date == Due_date(text):
# #     #                     if day != 'N/A' and in_date != 'N/A':
# #     #                         du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y') + datetime.timedelta(days=day)).strftime(
# #     #                             '%d-%m-%Y')

# #     #             elif Due_date(text) is None:
# #     #                 if day != 'N/A' and in_date != 'N/A':
# #     #                     du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y') + datetime.timedelta(days=day)).strftime(
# #     #                         '%d-%m-%Y')
# #     #                 else:
# #     #                     du_date = 'N/A'

# #     #             if Invoice(text) is not None:
# #     #                 Invoice_number, Invoice_Keyword = Invoice(text)
# #     #             else:
# #     #                 Invoice_number = Invoice_Keyword = 'N/A'

# #     #             if Abn(text1) is not None:
# #     #                 abn = Abn(text1)
# #     #             else:
# #     #                 abn = 'N/A'

# #     #             single_data = {
# #     #                 'File_name': file_name,
# #     #                 'Invoice_number': Invoice_number,
# #     #                 'Invoice_Keyword': Invoice_Keyword,
# #     #                 'Invoice_date': in_date,
# #     #                 'Due_date': du_date,
# #     #                 'ABN': abn,
# #     #                 'Account_number': 'soon',
# #     #                 'Bill_number': 'soon',
# #     #                 'Customer_number': 'soon',
# #     #                 'Supplier_name': 'soon',
# #     #                 'Supplier_address': 'soon',
# #     #                 'Buyer_name': 'soon',
# #     #                 'Buyer_address': 'soon'
# #     #             }

# #     #             '''For singledata Json file Uncomment this '''

# #     #             output_file = os.path.abspath(path)
# #     #             pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

# #     #             with open(os.path.join(output_file, file_json), 'w') as finalfile:
# #     #                 json.dump(single_data, finalfile)
                    
# #     #         else:

# #     #             single_data = {
# #     #                 'File_name': file_name,
# #     #                 'Invoice_number': 'N/R',
# #     #                 'Invoice_Keyword': 'N/R',
# #     #                 'Invoice_date': 'N/R',
# #     #                 'Due_date': 'N/R',
# #     #                 'ABN': 'N/R',
# #     #                 'Account_number': 'N/R',
# #     #                 'Bill_number': 'N/R',
# #     #                 'Customer_number': 'N/R',
# #     #                 'Supplier_name': 'N/R',
# #     #                 'Supplier_address': 'N/R',
# #     #                 'Buyer_name': 'N/R',
# #     #                 'Buyer_address': 'N/R'
# #     #             }

# #     #             '''For singledata Json file Uncomment this '''
# #     #             output_file = os.path.abspath(path)
# #     #             pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

# #     #             with open(os.path.join(output_file, file_json), 'w') as finalfile:
# #     #                 json.dump(single_data, finalfile)

# #     #     except Exception as e:
# #     #         print('Exception details',e)
# #     #     finally:
# #     #         for i in client_folders:
# #     #             client_files = os.listdir(i)
# #     #             file = file_name
# #     #             if file in client_files:
# #     #                 if file.replace('.pdf', '.inp') in client_files:
# #     #                     temp = file.replace('.pdf', '.inp')
# #     #                     os.remove(os.path.join(i, temp))
# #     # return HttpResponse('Successful')