import pandas as pd
import re
import datetime as dt
import json
import os

def get_df_path(path):
    list_data = []
    periodos_temporada = ['09-10',
                      '10-11',
                      '11-12',
                      '12-13',
                      '13-14',
                      '14-15',
                      '15-16',
                      '16-17',
                      '17-18',
                      '18-19']

    path = "input/dataset"
    contenido = os.listdir(path)

    for i,archivo in enumerate(contenido):
        path2 = path+'/'+archivo
        data = json.load(open(path2))
        
        for x in data:     
            #periodo
            x['SeasonPeriod'] = periodos_temporada[i]
            list_data.append(x)
        
    df = pd.DataFrame.from_dict(list_data, orient='columns')

    return df

def strftime_format(value,format):
    try:       
        dt.datetime.strptime(value, format)
        return True
    except ValueError:
        return False

def clean_datetime(x):
    
    if strftime_format(x,'%d/%m/%y'): 
        fecha = dt.datetime.strptime(x,'%d/%m/%y')
    elif strftime_format(x,'%Y-%m-%d'):
        fecha = dt.datetime.strptime(x,'%Y-%m-%d')
    elif strftime_format(x,'%d/%m/%Y'):
        fecha = dt.datetime.strptime(x,'%d/%m/%Y')
    else:
        fecha = None
    return fecha  

def clean_int_columns(x):
    numeric_pattern = '[0-9]+'
    space_pattern = ' +'
    if x == None:
        return pd.NA
    elif x == "":
        return pd.NA
    elif isinstance(x, str) and re.match(space_pattern, x):
        return pd.NA
    elif isinstance(x, str) and x == 'None':
        return pd.NA
    elif isinstance(x, str) and x == 'NaN':
        return pd.NA
    elif isinstance(x, str) and x == 'NaT':
        return pd.NA
    elif isinstance(x, str) and x == '<NA>':
        return pd.NA
    elif isinstance(x, str) and re.match(numeric_pattern, x):
        x = int(x)
        return x
    elif isinstance(x, float):
        x = int(x)
        return x
    else:
        return x

def clean_str_columns(x):
    space_pattern = ' +'
    if x == 'null':
        return None
    elif isinstance(x, str) and re.match(space_pattern, x):
        return None
    elif x == 'nan':
        return None
    elif x == 'NaN':
        return None
    elif x == 'None':
        return None
    elif x == '<NA>':
        return None
    elif x == 'NaT':
        return None
    elif isinstance(x, int):
        x = str(x)
        return x
    else:
        return x

#funcion que permite setear los valores Nulos que pueda traer el dataset, a valores None y luego asigna los tipos de datos que corresponda
def clean_df(df_ref, dtypes):
    df = df_ref
    for name_column in df.columns:
        
        if dtypes[name_column] == "float64":
            df[name_column] = df[name_column].astype("float")
            df[name_column] = df[name_column].astype(dtypes[name_column])

        if dtypes[name_column] == 'Int64' or dtypes[name_column] == 'int64':
            df[name_column] = df[name_column].apply(lambda x: clean_int_columns(x))

        if dtypes[name_column] == 'string':
            df[name_column] = df[name_column].apply(lambda x: clean_str_columns(x))

        if dtypes[name_column] == 'datetime64[ns]':
            df[name_column] = df[name_column].apply(lambda x: clean_datetime(x))

    #asignar tipos de datos predefinidos en dtypes
    df = df.astype(dtypes)

    return df

def generar_archivos_csv(df,path):
    df.to_csv(path, sep=';', index = False)