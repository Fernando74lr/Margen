from .data.secret.credentials import server, username, password
from django.http.response import HttpResponse
from openpyxl.utils import get_column_letter
from .functions.tools import format_date, thin_border, enterprises
from openpyxl.styles import Alignment, Font, PatternFill
from django.shortcuts import render
from .models import SqlServerConn
from openpyxl import Workbook
import pyodbc

query_cache = []


def table(request):
    return render(request, 'report/table_filter.html')

def reports(request):
    return render(request, 'report/reports.html')

def get_clients(request):
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
           
            # cursor.execute("SELECT "+
            #             "CIDCLIENTEPROVEEDOR, CRAZONSOCIAL, CRFC,"+
            #             "CFECHAALTA, CESTATUS, CIDAGENTEVENTA "+
            #             "FROM admClientes")

            # cursor.execute("SELECT CIDCLIENTEPROVEEDOR FROM admDocumentos")

            cursor.execute("SELECT "+
                        "CSERIEDOCUMENTO, CFOLIO, CFECHA, "+
                        "CIDCLIENTEPROVEEDOR, CRAZONSOCIAL, CRFC, "+
                        "CIDAGENTE, COBSERVACIONES, CCANCELADO, "+
                        "CNETO, CIMPUESTO1, CTOTAL, "+
                        "CMETODOPAG, CGUIDDOCUMENTO, CUSUARIO, CIDDOCUMENTO "+
                        "FROM admDocumentos " +
                        "WHERE CFECHA BETWEEN '20200427' AND '20200624'")
            
            temp = []
            for query in cursor.fetchall():            
                query = list(query)
                query.insert(0, database.replace('adCOM_', '').replace('_', ' '))
                query.insert(0, database)
                temp.append(query)
            result.append(temp)
        
        query_cache = result
    else:
        print("\nUSING CACHE\n")
        result = query_cache
    
    if len(result) == len(enterprises):
        print("\nALL RIGHT\n")
        # print(result[0])
        print("\n\n")
    else:
        print("SOMETHING WENT WRONG")

    return render(request, 'report/reports.html', {'SqlServerConn' : result})

def clients_report(request):
    # OPEN WORKBOOK AND HEADER DETAILS
    wb = Workbook()
    ws = wb.active
    ws['A1'] = f'REPORTE DE CLIENTES - {format_date()}'
    ws.merge_cells('A1:C1')

    # HEADERS
    ws['A2'] = 'ID CLIENTE'
    ws['B2'] = 'CORPORACIÓN'
    ws['C2'] = 'RAZÓN SOCIAL'
    ws['D2'] = 'RFC'
    ws['E2'] = 'ID AGENTE VENTA'
    ws['F2'] = 'FECHA ALTA'
    ws['G2'] = 'ESTATUS'
    ws['H2'] = 'BASE DE DATOS'

    # FILTERS
    FullRange = "A2:" + get_column_letter(ws.max_column) + str(ws.max_row)
    ws.auto_filter.ref = FullRange

    # ALIGNMENTS, COLORS AND DIMENSIONS
    dimensions = [13.71, 23.86, 65, 16.43, 23, 15.43, 11.29, 34]
    
    ws.row_dimensions[1].height = 26.25
    ws.row_dimensions[2].height = 42.75

    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    ws['A1'].font = Font(size="20", color="FF0000")

    for col in range(8):
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
                # ID Cliente
                ws.cell(row=counter, column=1).value = data[2]
                ws.cell(row=counter, column=1).font = Font(size="12")
                ws.cell(row=counter, column=1).border = thin_border
                # Corporación
                ws.cell(row=counter, column=2).value = data[1]
                ws.cell(row=counter, column=2).font = Font(size="12")
                ws.cell(row=counter, column=2).border = thin_border
                # Razón Social
                ws.cell(row=counter, column=3).value = data[3]
                ws.cell(row=counter, column=3).font = Font(size="12")
                ws.cell(row=counter, column=3).border = thin_border
                # RFC
                ws.cell(row=counter, column=4).value = data[4]
                ws.cell(row=counter, column=4).font = Font(size="12")
                ws.cell(row=counter, column=4).border = thin_border
                # ID Agente Venta
                ws.cell(row=counter, column=5).value = data[7]
                ws.cell(row=counter, column=5).font = Font(size="12")
                ws.cell(row=counter, column=5).border = thin_border
                # Fecha Alta
                ws.cell(row=counter, column=6).value = str(data[5]).split(' ')[0]
                ws.cell(row=counter, column=6).font = Font(size="12")
                ws.cell(row=counter, column=6).border = thin_border
                # Estatus
                ws.cell(row=counter, column=7).value = data[6]
                ws.cell(row=counter, column=7).font = Font(size="12")
                ws.cell(row=counter, column=7).border = thin_border
                # Base de datos
                ws.cell(row=counter, column=8).value = data[0]
                ws.cell(row=counter, column=8).font = Font(size="12")
                ws.cell(row=counter, column=8).border = thin_border

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