import pandas as pd
  
def set_equipo_local(df):
    df_equipo_local = df[['SeasonPeriod','Date','HomeTeam','HC','HF','HR','HS','HST','HY','HTHG','FTHG','FTR']]

    #homologar nombres de columnas
    df_equipo_local = df_equipo_local.rename(columns={'HomeTeam':'Name',
                                                    'HF':'Faults',
                                                    'HC':'Cards',
                                                    'HR':'CardsRed',
                                                    'HY': 'CardsYellow',
                                                    'HS': 'Shot',
                                                    'HST': 'ShotTarget',
                                                    'HTHG': 'HalfTimeGoals',
                                                    'FTHG': 'FullTimeGoals'
                                                    })

    #agregar tipo de equipo: local o visita
    df_equipo_local['Type'] = 'Home'

    #agregar resultado del juego
    df_equipo_local['Result'] = df_equipo_local['FTR'].apply(lambda x: 'Win' if x == 'H' else ('Lose' if x == 'A' else 'Draw') )

    return df_equipo_local

def set_equipo_visita(df):
    df_equipo_visita = df[['SeasonPeriod','Date','AwayTeam','AC','AF','AR','AS','AST','AY','FTAG','HTAG','FTR']]

    #homologar nombres de columnas
    df_equipo_visita = df_equipo_visita.rename(columns={'AwayTeam':'Name',
                                                    'AF':'Faults',
                                                    'AC':'Cards',
                                                    'AR':'CardsRed',
                                                    'AY': 'CardsYellow',
                                                    'AS': 'Shot',
                                                    'AST': 'ShotTarget',
                                                    'HTAG': 'HalfTimeGoals',
                                                    'FTAG': 'FullTimeGoals'
                                                    })

    #agregar tipo de equipo: local o visita
    df_equipo_visita['Type'] = 'Away'

    #agregar resultado del juego
    df_equipo_visita['Result'] = df_equipo_visita['FTR'].apply(lambda x: 'Win' if x == 'A' else ('Lose' if x == 'H' else 'Draw') )

    return df_equipo_visita

def get_entidad_equipo(df):

    df_equipo_local = set_equipo_local(df)
    df_equipo_visita = set_equipo_visita(df)

    df_equipos = pd.concat([df_equipo_local,df_equipo_visita])

    #eliminar df que ya no se van a usar
    del df_equipo_local, df_equipo_visita

    return df_equipos

def get_entidad_partido(df):
    df_partido = df[['SeasonPeriod','Date','Div','Referee','AwayTeam','HomeTeam','FTR','HTR']]

    #cambiar nombres de columnas
    df_partido = df_partido.rename(columns={'FTR':'FullTimeResult',
                                            'HTR':'HalfTimeResult'
                                            })
    
    return df_partido

def set_resultados_partidos(df_equipos):
    #agrupar y contar los datos por resultado: Win, Lose y Draw
    df_partidos_resultados = df_equipos.groupby(
                                                ['SeasonPeriod', 'Name','Result']
                                            ).size().reset_index(name='Count')

    #trasponer resultados anteriores, y pasar de filas a columnas, luego se cambian los nombres de columnas, para el reporte
    df_partidos_resultados = df_partidos_resultados.pivot_table(
                                                                'Count', ['SeasonPeriod', 'Name'], 'Result'
                                                            ).rename(columns={'Win':'Won',
                                                                                'Lose':'Lost',
                                                                                'Draw':'Drawn'
                                                                                }
                                                                    )

    #crear nuevo campo calculado: Played, con la suma de los 3 resultados
    df_partidos_resultados['Played'] = df_partidos_resultados['Won']+df_partidos_resultados['Lost']+df_partidos_resultados['Drawn']

    return df_partidos_resultados

def set_goles_a_favor(df_equipos):
    #agrupar datos por periodo y equipo y sumar los goles, luego se modifica el nombre del campo, para el reporte
    df_goles_favor = df_equipos.groupby(
                                   ['SeasonPeriod', 'Name'], as_index=False
                                   )['FullTimeGoals'].sum().rename(columns={'FullTimeGoals':'GF'})
    
    return df_goles_favor

def set_goles_en_contra(df_partido,df_equipos):

    '''
    trikiñuela para ir a buscar la suma de goles que me hicieron los equipos con los que jugué,
    a: tomando los equipos locales
    b.tomando los equipos de visita
    '''
    #a. a partir de los equipos locales, se busca la suma de los goles que me hicieron los equipos de visita
    df_goles_contra_hometeam = (df_partido.merge(
                                                df_equipos,how='inner',
                                                left_on=['SeasonPeriod','Date','AwayTeam'],
                                                right_on=['SeasonPeriod','Date','Name'])
                                                ).groupby(
                                                        ['SeasonPeriod', 'HomeTeam'], as_index=False
                                                        )['FullTimeGoals'].sum().rename(columns={'HomeTeam':'Name'}
                                                                                                                                    )
    #b. a partir de los equipos visitas, se busca la suma de los goles que me hicieron los equipos locales
    df_goles_contra_awayteam =(df_partido.merge(
                                                df_equipos,how='inner',
                                                left_on=['SeasonPeriod','Date','HomeTeam'],
                                                right_on=['SeasonPeriod','Date','Name'])
                                                ).groupby(
                                                        ['SeasonPeriod', 'AwayTeam'], as_index=False
                                                        )['FullTimeGoals'].sum().rename(columns={'AwayTeam':'Name'})

    # ahora juntar y sumar todo: a+b

    #juntar a y b
    df_goles_contra = pd.concat(
                            [df_goles_contra_hometeam,df_goles_contra_awayteam]
                            ).rename(columns={'FullTimeGoals':'GA'})

    #sumar los valores, para que quede una sola fila por equipo
    df_goles_contra = df_goles_contra.groupby(
                                            ['SeasonPeriod', 'Name'], as_index=False
                                            )['GA'].sum()

    #eliminar df que ya no se van a usar
    del df_goles_contra_hometeam,df_goles_contra_awayteam

    return df_goles_contra

def get_tabla_posiciones(df_partido,df_equipos):

    #1. set resultados partidos: Played, Won, Lost, Drawn
    df_partidos_resultados = set_resultados_partidos(df_equipos)

    #2. set goles a favor
    df_goles_favor = set_goles_a_favor(df_equipos)

    #3. set goles en contra
    df_goles_contra = set_goles_en_contra(df_partido,df_equipos)

    #Tabla de posiciones, ahora cruzar todo lo anterior: 1+2+3

    #0. crear df principal con season y equipo
    df_season_club = df_equipos[['SeasonPeriod', 'Name']].drop_duplicates()

    #a.resultados juego
    df_aux1 = df_season_club.merge(
                                df_partidos_resultados,how='inner',on=['SeasonPeriod','Name']
                                )

    #b.goles a favor
    df_aux2 = df_aux1.merge(
                            df_goles_favor, how='inner', on=['SeasonPeriod','Name']
                            )

    #c.goles en contra 
    df_tabla_posiciones = df_aux2.merge(
                                    df_goles_contra, how='inner', on=['SeasonPeriod','Name']
                                        )
    #d.diferencia de goles
    df_tabla_posiciones['GD'] = df_tabla_posiciones['GF'] - df_tabla_posiciones['GA']

    #e.puntos
    df_tabla_posiciones['Points'] = (df_tabla_posiciones['Won'] * 3)+(df_tabla_posiciones['Drawn'] * 1)

    #ordenar
    df_tabla_posiciones = df_tabla_posiciones.sort_values(
                                                        ['SeasonPeriod', 'Points'], ascending=[True, False]
                                                        )

    #agregar numero de posicion
    df_tabla_posiciones['Position'] = df_tabla_posiciones.groupby(
                                                                ['SeasonPeriod']
                                                                ).cumcount()+1

    #mostrar columnas ordenadas
    df_tabla_posiciones = df_tabla_posiciones[['Position',
                                            'SeasonPeriod',
                                            'Name',
                                            'Played',
                                            'Won',
                                            'Lost',
                                            'Drawn',
                                            'GF',
                                            'GA',
                                            'GD',
                                            'Points']]

    #eliminar df que ya no se van a usar
    del df_aux1,df_aux2,df_season_club,df_partidos_resultados,df_goles_favor,df_goles_contra

    return df_tabla_posiciones

def get_equipos_mejor_relacion_disparos_arco_por_temporada(df_equipos):

    #obtener suma de tiros al arco y de goles por temporada y equipo
    df_aux1 = df_equipos.groupby(
                                ['SeasonPeriod','Name'], as_index=False
                                ).agg(
                                    {
                                    'FullTimeGoals':'sum',
                                    'ShotTarget':'sum'
                                    })

    #crear nuevo campo, con la división/relacion de campos anteriores
    df_aux1['ShotsGoals'] = df_aux1['FullTimeGoals']/df_aux1['ShotTarget']

    #agrupar por periodo y sacar el maximo valor de relacion anterior, luego se obtiene el equipo asociado a ese máximo
    df_equipos_mejor_relacion_arco = df_aux1.groupby(
                                                    'SeasonPeriod', as_index=False
                                                    )['ShotsGoals'].agg(
                                                    'max').merge(
                                                                df_aux1, how='inner', on=['SeasonPeriod','ShotsGoals']
                                                                )[['SeasonPeriod','Name','ShotsGoals']]

    #eliminar df que ya no se van a usar
    del df_aux1

    return df_equipos_mejor_relacion_arco

def get_equipo_mas_goleado_por_temporada(df_tabla_posiciones):
    #agrupar por periodo y sacar el maximo valor de los goles en contra, luego se obtiene el equipo asociado a ese maximo
    df_equipo_mas_goleado = df_tabla_posiciones.groupby(
                                                        'SeasonPeriod', as_index=False)['GA'].agg(
                                                        'max').merge(
                                                                    df_tabla_posiciones, how='inner', on=['SeasonPeriod','GA']
                                                                    )[['SeasonPeriod','Name','GA']]
    
    return df_equipo_mas_goleado