from .data.secret.credentials import server, username, password
from django.http.response import HttpResponse
from openpyxl.utils import get_column_letter
from .functions.tools import format_date, thin_border, enterprises, get_time
from openpyxl.styles import Alignment, Font, PatternFill
from django.shortcuts import render
from .models import SqlServerConn
from openpyxl import Workbook
import pyodbc

query_cache = []
beginDateG = ''
endDateG = ''

def table(request):
    return render(request, 'report/table_filter.html')

def reports(request):
    return render(request, 'report/reports.html')

def get_clients(request, beginDate, endDate):
    global beginDateG
    global endDateG

    beginDateG = beginDate.replace('-', '/')
    endDateG = endDate.replace('-', '/')

    beginDate = list(beginDate.split("/"))
    endDate = list(endDate.split("/"))

    print(f"\n{beginDateG} - {endDateG}\n")
    print(f"\n{beginDate} - {endDate}\n")

    global query_cache
    result = []

    if len(query_cache) == 0:
        print("\nGETTING DATA\n")

        for database in enterprises:
            conn = pyodbc.connect('DRIVER={SQL Server};'+
                                'SERVER=' + server + ';'+
                                'DATABASE=' + database + ';'+
                                'UID=' + username + ';'+
                                'PWD=' + password + ';')
            cursor = conn.cursor()
           
            cursor.execute("SELECT "+
                        "CSERIEDOCUMENTO, CFOLIO, CFECHA, "+
                        "CIDCLIENTEPROVEEDOR, CRAZONSOCIAL, CRFC, "+
                        "CCANCELADO, "+
                        "CNETO, CIMPUESTO1, CTOTAL, "+
                        "CMETODOPAG, CGUIDDOCUMENTO, CUSUARIO, CIDDOCUMENTO "+
                        "FROM admDocumentos " +
                        f"WHERE CFECHA BETWEEN '{''.join(beginDate)}' AND '{''.join(endDate)}'")
            # 20200623 | 20200624
            dataDocumentos = cursor.fetchall()
            temp = []
            observTemp = []
            sentence = ''
            for query in dataDocumentos:            
                query = list(query)
                query.insert(0, database.replace('adCOM_', '').replace('_', ' '))
                query.insert(0, database)
                observations = cursor.execute(f"SELECT COBSERVAMOV FROM admMovimientos WHERE CIDDOCUMENTO='{query[len(query)-1]}'")
                for observ in observations:
                    if str(observ[0]) != 'None':
                        observTemp.append(str(observ[0]))
                for word in observTemp:
                    sentence+=word+' \n'
                    sentence+=' \n'
                query.append(sentence)
                cursor.fetchall()
                temp.append(query)

            observTemp = [] # reset observations temp.
            sentence = '' # reset sentence.
            result.append(temp)
        
        query_cache = result
    else:
        print("\nUSING CACHE\n")
        result = query_cache
    
    if len(result) == len(enterprises):
        print("\nALL RIGHT\n")
    else:
        print("SOMETHING WENT WRONG")

    return render(request, 'report/reports.html', {'SqlServerConn' : result})

def clients_report(request):
    # OPEN WORKBOOK AND HEADER DETAILS
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"
    ws['A1'] = f'REPORTE DE CLIENTES - {format_date()} - {get_time()}'
    ws['E1'] = f'Rango: {beginDateG} - {endDateG}'
    ws.merge_cells('A1:D1')
    ws.merge_cells('E1:F1')

    # HEADERS
    ws['A2'] = 'SERIE DOCUMENTO'
    ws['B2'] = 'CORPORACIÓN'
    ws['C2'] = 'FOLIO'
    ws['D2'] = 'FECHA'
    ws['E2'] = 'RFC'
    ws['F2'] = 'ID CLIENTE PROVEEDOR'
    ws['G2'] = 'RAZÓN SOCIAL'
    ws['H2'] = 'CANCELADO'
    ws['I2'] = 'NETO'
    ws['J2'] = 'IMPUESTO1'
    ws['K2'] = 'TOTAL'
    ws['L2'] = 'MÉTODO DE PAGO'
    ws['M2'] = 'GUID DOCUMENTO'
    ws['N2'] = 'USUARIO'
    ws['O2'] = 'ID DOCUMENTO'
    ws['P2'] = 'OBSERV. MOVIM.'

    # FILTERS
    FullRange = "A2:" + get_column_letter(ws.max_column) + str(ws.max_row)
    ws.auto_filter.ref = FullRange

    # ALIGNMENTS, COLORS AND DIMENSIONS
    dimensions = [29.43, 23.57, 12.57, 19.43, 15.14, 34.57, 68.14, 20.43, 12, 19.71, 13, 28.57, 40.43, 16.29, 25.43, 60]
    
    ws.row_dimensions[1].height = 26.25
    ws.row_dimensions[2].height = 42.75

    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['A1'].font = Font(size="18", color="FF0000")

    ws['E1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['E1'].font = Font(size="18", color="FF0000")

    for col in range(16):
        ws.cell(row=2, column=col+1).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=2, column=col+1).fill = PatternFill(start_color="2F75B5", end_color="2F75B5", fill_type = "solid")
        ws.cell(row=2, column=col+1).font = Font(size="16", color="FFFFFF")
        ws.cell(row=2, column=col+1).border = thin_border

    # Column size
    for i, column_width in enumerate(dimensions):
        ws.column_dimensions[get_column_letter(i+1)].width = column_width + 1

    global query_cache
    counter = 3

    # CREATE EXCEL
    if len(query_cache) > 0:
        print("\nCREATING EXCEL\n")
        for enterprise in query_cache:
            for data in enterprise:
                # Serie Documento
                ws.cell(row=counter, column=1).value = data[2]
                ws.cell(row=counter, column=1).font = Font(size="12")
                ws.cell(row=counter, column=1).border = thin_border
                # Corporación
                ws.cell(row=counter, column=2).value = data[1]
                ws.cell(row=counter, column=2).font = Font(size="12")
                ws.cell(row=counter, column=2).border = thin_border
                # Folio
                ws.cell(row=counter, column=3).value = data[3]
                ws.cell(row=counter, column=3).font = Font(size="12")
                ws.cell(row=counter, column=3).border = thin_border
                # Fecha
                ws.cell(row=counter, column=4).value = data[4]
                ws.cell(row=counter, column=4).font = Font(size="12")
                ws.cell(row=counter, column=4).border = thin_border
                # RFC
                ws.cell(row=counter, column=5).value = data[7]
                ws.cell(row=counter, column=5).font = Font(size="12")
                ws.cell(row=counter, column=5).border = thin_border
                # ID Cliente Proveedor
                ws.cell(row=counter, column=6).value = str(data[5]).split(' ')[0]
                ws.cell(row=counter, column=6).font = Font(size="12")
                ws.cell(row=counter, column=6).border = thin_border
                # Razón Social
                ws.cell(row=counter, column=7).value = data[6]
                ws.cell(row=counter, column=7).font = Font(size="12")
                ws.cell(row=counter, column=7).border = thin_border
                # Cancelado
                ws.cell(row=counter, column=8).value = data[8]
                ws.cell(row=counter, column=8).font = Font(size="12")
                ws.cell(row=counter, column=8).border = thin_border
                # Neto
                ws.cell(row=counter, column=9).value = data[9]
                ws.cell(row=counter, column=9).font = Font(size="12")
                ws.cell(row=counter, column=9).border = thin_border
                # Impuesto1
                ws.cell(row=counter, column=10).value = data[10]
                ws.cell(row=counter, column=10).font = Font(size="12")
                ws.cell(row=counter, column=10).border = thin_border
                # Total
                ws.cell(row=counter, column=11).value = data[11]
                ws.cell(row=counter, column=11).font = Font(size="12")
                ws.cell(row=counter, column=11).border = thin_border
                # Método de pago
                ws.cell(row=counter, column=12).value = str(data[12]).split(' ')[0]
                ws.cell(row=counter, column=12).font = Font(size="12")
                ws.cell(row=counter, column=12).border = thin_border
                # GUID Documento
                ws.cell(row=counter, column=13).value = data[13]
                ws.cell(row=counter, column=13).font = Font(size="12")
                ws.cell(row=counter, column=13).border = thin_border
                # Usuario
                ws.cell(row=counter, column=14).value = data[14]
                ws.cell(row=counter, column=14).font = Font(size="12")
                ws.cell(row=counter, column=14).border = thin_border
                # ID Documento
                ws.cell(row=counter, column=15).value = str(data[15]).split(' ')[0]
                ws.cell(row=counter, column=15).font = Font(size="12")
                ws.cell(row=counter, column=15).border = thin_border
                # Observ. Movim.
                ws.cell(row=counter, column=16).value = data[16]
                ws.cell(row=counter, column=16).font = Font(size="12")
                ws.cell(row=counter, column=16).border = thin_border

                counter+=1
    else:
        print("\nCACHE EMPTY\n")

    # FILE DETAILS AND FORMAT
    filename = 'Reporte_Clientes.xlsx'
    response = HttpResponse(content_type = 'application/ms-excel')
    content = 'attachment; filename = {0}'.format(filename)
    response['Content-Disposition'] = content
    wb.save(response)

    return response