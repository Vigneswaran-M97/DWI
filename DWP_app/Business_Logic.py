import re
import os
import json
import pathlib
import datetime
import pdfplumber
from rest_framework.response import Response
from rest_framework.decorators import api_view

def Account_number(text):
    pass

def Bill_number(text):
    pass

def Customer_code(text):
    pass

def Supplier_name(text):
    pass

def Supplier_address(text):
    pass

def Buyer_name(text):
    pass

def Buyer_address(text):
    pass

def Convert_Date(text):
    ''' This function will covert string to date format '''
    for fmt in ['%d-%b-%Y','%d-%m-%Y','%d-%b-%y','%d-%m-%y']:
        try:
            return datetime.datetime.strptime(text, fmt).strftime('%d-%m-%Y')
        except ValueError:
            pass

def Invoice(text):
    ''' This Function will find Invoice Number in PDF '''
    keywords = {
        'invoice_keys' : [
            'invoice #','invoice number :','invoice number','tax invoice copynumber','tax invoice','tax invoice:', 'invoice no','tax invoice #','original invoice','invoice no:','nutrienagsolutions','invoice #:','invoicenumber','see over for details','Tax Credit','inv no.','invoice no.','tax adjustment note:','invoice number:','invoice no :','invoice no.:','invoice id ....................:','credit adjustment note','account number'
        ]
    }
    for i,j in keywords.items():
        for name in j:
            Tran_lang = name
            try:
                n={3}
                invoice_re = re.compile(fr"({Tran_lang}\)\s+\d+)|({Tran_lang}\s+\w\d+\-\d+\-\d+)|({Tran_lang}\s+\d{n}\d+)|({Tran_lang}\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+)|({Tran_lang}\s+\w+\-\d{n}\d+)|({Tran_lang}\s+\w+\d{n}\d+\-\d+)")
                keyword_invoice = invoice_re.search(text).group()

                if Tran_lang in keyword_invoice:
                    find_word = Tran_lang                
                    main_invoice = keyword_invoice.replace(Tran_lang,'').strip()
                    return main_invoice , find_word
            except:
                pass

def Abn(text):
    '''The Australian Business Number (ABN) is a unique 11-digit identifier issued by the Australian Business Register (ABR) which is operated by the Australian Taxation Office (ATO). The ABN was introduced on 1 July 2000 by John Howard's Liberal government as part of a major tax reform, which included the introduction of a GST.'''
    try:    
        abn_number = re.search(r"(abn\d+)|(abn:\d+)|(a.b.n.\d+)", text)
        abn = ""
        for m in abn_number.group():
            if m.isdigit():
                abn += m
        return int(abn)
    except:
        pass
    
def Due_date(text):
    '''This Function will get Due Date in pdf'''
    try:
        date =""
        due_date = re.search('due date:\s+\d+\s+\w+\s+\d+|due date:\s+\d+-\w+-\d+|due date: by\s+\d+\s+\w+\s+\d+|due date:\s+\d+/\w+/\d+|due date:\s+\d+.\d+.\d+|due date:\s+\d+/\d+/\d+|\d+/\d+/\d+\s+mainfreight',text)
        date = due_date.group().replace('due date:','').replace('.','-').replace(' ','-').replace('/','-').replace('by--','')
        due_date_parser = Convert_Date(text = date)
        return due_date_parser
    except:
        pass

def Due(text):
    '''This Function will find Due days in pdf and send to Invoice_Date Function'''
    try:           
        days ="" 
        due_number = re.search(r"(\d+\s+days)|(month\s+\d{2})",text)
        for m in due_number.group():
            if m.isdigit():
                days += m
        return int(days)
    except:
        pass

def Invoice_Date(text):
    ''' This Function Will get Invoice Date  from PDF after Covert into Date Format if we have Deu days it'll calculte Due Date and return '''
    
    pattern_list = ['\d+([/]|[.])\d+([/]|[.])([2][0][0-9][0-9]|[0-9][0-9])','([0-9]|[0-9][0-9])([\s]|[]|[-])(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)([\s]|[]|[-])([2][0][0-9][0-9]|[0-9][0-9])']
    
    temp = []
    for regex in pattern_list:
            try:
                find_date = re.search(regex,text)
                replce_data = find_date.group().replace('.','-').replace(' ','-').replace('/','-')
                convert_date = Convert_Date(text = replce_data)
                temp.append(convert_date)
                return temp[0]
            except:
                pass

def Invoice_Details(data):
    
    invoice_unmissing_count = invoice_missing_count = invoice_missing_date = invoice_unmissing_date = invoice_missing_due_date = invoice_unmissing_due_date = invoice_missing_abn = invoice_unmissing_abn = 0
    for i,j in data.items():
        
        if j['Invoice_number'] == 'N/A':
            invoice_missing_count += 1
        else:
            invoice_unmissing_count += 1
            
        if j['Invoice_date'] == 'N/A':
            invoice_missing_date += 1
        else:
            invoice_unmissing_date += 1
            
        if j['Due_date'] == 'N/A':
            invoice_missing_due_date += 1
        else:
            invoice_unmissing_due_date += 1
            
        if j['ABN'] == 'N/A':
            invoice_missing_abn += 1
        else:
            invoice_unmissing_abn += 1
            
    Invoice_counts = {
        'Missing Invoice':invoice_missing_count,
        'Unmissing Invocie':invoice_unmissing_count,
        'Missing Invoice Date':invoice_missing_date,
        'Unmissing Invoice Date':invoice_unmissing_date,
        'Missing Invoice Due Date':invoice_missing_due_date,
        'UnMissing Invoice Due Date':invoice_unmissing_due_date,
        'Missing Invoice ABN':invoice_missing_abn,
        'Unmissing Invoice ABN':invoice_unmissing_abn
    }
    
    output_file  = os.path.abspath('output/')
    pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(output_file,'Invoice_counts.json'), 'w') as finalfile:
        json.dump(Invoice_counts,finalfile)

@api_view(['POST'])
def main(request):
    if request.method == 'POST':
        file_path = request.data['file_path']
        single_data={}
        file_name = os.path.basename(file_path)
        path = os.path.dirname(file_path)
        file_json = file_name.replace('.pdf','.json')
        text = ""
        
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            test = pdf.pages[0-total_pages]
            text += test.extract_text().replace('\n',' ').lower()
            text1 = text.replace(' ','')
        pdf.close()
        
        if len(text) > 0:
            
            if Invoice_Date(text) is not None:
                in_date = Invoice_Date(text)
            else:
                in_date = 'N/A'
                
            if Due(text) is not None:
                day = Due(text)
            else:
                day = 'N/A'
                        
            if Due_date(text) is not None:
                if in_date == Due_date(text):
                    if day != 'N/A'and in_date !='N/A':
                        du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y')+ datetime.timedelta(days=day)).strftime('%d-%m-%Y')
                                
            elif Due_date(text) is None:
                if day != 'N/A' and in_date !='N/A':
                    du_date = (datetime.datetime.strptime(in_date, '%d-%m-%Y')+ datetime.timedelta(days=day)).strftime('%d-%m-%Y')
                else:
                    du_date = 'N/A'
                    
            if Invoice(text) is not None:
                Invoice_number, Invoice_Keyword = Invoice(text)
            else:
                Invoice_number = Invoice_Keyword = 'N/A'
            
            if Abn(text1) is not None:
                abn = Abn(text1)
            else:
                abn = 'N/A'
            
            single_data= {
                'File_name':file_name,
                'Invoice_number': Invoice_number,
                'Invoice_Keyword': Invoice_Keyword,
                'Invoice_date': in_date,
                'Due_date':du_date,
                'ABN':abn,
                'Account_number':'soon',
                'Bill_number':'soon',
                'Customer_number':'soon',
                'Supplier_name':'soon',
                'Supplier_address':'soon',
                'Buyer_name':'soon',
                'Buyer_address':'soon'
            }
        
            with open(os.path.join(path,file_json), 'w') as finalfile:
                json.dump(single_data, finalfile)
            
        else:
                    
            single_data = {
                    'File_name':file_name,
                    'Invoice_number': 'N/R',
                    'Invoice_Keyword': 'N/R',
                    'Invoice_date': 'N/R',
                    'Due_date':'N/R',
                    'ABN':'N/R',
                    'Account_number':'N/R',
                    'Bill_number':'N/R',
                    'Customer_number':'N/R',
                    'Supplier_name':'N/R',
                    'Supplier_address':'N/R',
                    'Buyer_name':'N/R',
                    'Buyer_address':'N/R'
                }
            
            with open(os.path.join(path,file_json), 'w') as finalfile:
                json.dump(single_data, finalfile)
            print(file_name,'=',single_data)        
        return Response(single_data)
        