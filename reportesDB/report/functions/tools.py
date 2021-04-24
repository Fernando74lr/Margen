from openpyxl.styles import Border, Side
from datetime import datetime as dateTimeFormat
import datetime

thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

enterprises = [
    'adCOM_ACEROS_INDUSTRIALES',
    'adCOM_ADECUACION_Y_SERVICI',
    'adCOM_ADMINISTRACION_AMAYA',
    'adCOM_ADMINISTRACION_EMPRE',
    'adCOM_ADMINISTRACION_Y_SER',
    'adCOM_ADMINISTRATIVOS_DUD',
    'adCOM_ADMINISTRATIVOS_FTL',
    'adCOM_AGRICOLA_DON_MARIANO',
    'adCOM_AGRODESARROLLO_BIMI',
    'adCOM_AGRONEGOCIOS_ACEL_S',
    'adCOM_ALIMENTOS_AGRICOLAS',
    'adCOM_ALTERNATIVAS_INTEGRA',
    'adCOM_ASISTENCIA_BONETE_S',
    'adCOM_ASOCIACION_DE_CONSUL',
    'adCOM_ASOCIADOS_BERILOS_S',
    'adCOM_ASPERATUS_GRUPO_IMPU',
    'adCOM_AURA_DESARROLLO_SOCI',
    'adCOM_BARRENA_GRUPO_MINERO',
    'adCOM_BAULA',
    'adCOM_BAULA_SERVICIOS',
    'adCOM_BINAS_ADMINISTRACION',
    'adCOM_BIOGRUPO_TICAR',
    'adCOM_BJ_BONILLA_Y_ASOCIAD',
    'adCOM_BLI_GRUPO_EMPRESARIA',
    'adCOM_BPF_IMPULSE_SA_DE',
    'adCOM_BRESTON_SERVICIOS_S',
    'adCOM_CALCIDIA_DE_OTE_SA',
    'adCOM_CAPITAL_HUMANO_Y_FIN',
    'adCOM_CAVA_INTEGRACION_S',
    'adCOM_CENTRO_DE_RECICLADO',
    'adCOM_CHOSEMA_SA_DE_CV',
    'adCOM_CITIVER_SAPI_DE',
    'adCOM_CIUDAD_CAPITAL_CONSU',
    'adCOM_COMERCIALIZA_MINOR',
    'adCOM_COMERCIALIZADORA_MIN',
    'adCOM_COMERCIO_Y_CONSULTOR',
    'adCOM_COMUNIDAD_CREATIVA',
    'adCOM_CONSTRUCCIONES_TILAC',
    'adCOM_CONSTRUCCIONES_Y_ACA',
    'adCOM_CONSTRUCTOMANIA',
    'adCOM_CONSTRUCTORA_E_INGEN',
    'adCOM_CONSTRUCTORES_OBRAKO',
    'adCOM_CONSTRUGALIA_SA_DE',
    'adCOM_CONSULTORES_NINA_S',
    'adCOM_CONSULTORIA_DE_CARTE',
    'adCOM_CONSULTORIA_DE_GESTI',
    'adCOM_CONSULTORIA_ESTRATEG'
]

def get_time():
    now = dateTimeFormat.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def format_date_prefered(date):
    f_date = str(date).split(' ')[0].split('-')
    return f'{f_date[2]}/{f_date[1]}/{f_date[0]}'

def format_date():
    months = {
        '01' : 'Enero',
        '02' : 'Febrero',
        '03' : 'Marzo',
        '04' : 'Abril',
        '05' : 'Mayo',
        '06' : 'Junio',
        '07' : 'Julio',
        '08' : 'Agosto',
        '09' : 'Septiembre',
        '10' : 'Octubre',
        '11' : 'Noviembre',
        '12' : 'Diciembre'
    }

    today = datetime.datetime.now()
    date = today.strftime('%d')
    month = str(today.strftime('%m'))

    for key, value in months.items():
        if key == month:
            month = value

    year = today.strftime('%Y')

    return f'{date} DE {month.upper()} DEL {year}'