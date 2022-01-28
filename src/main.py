import modules.helpers as helpers
import modules.dtypes as dtypes
import modules.process_data as process_data

def main():

    path_input = r"input/dataset"

    try:

        df = helpers.get_df_path(path_input)

        df_clean = helpers.clean_df(df, dtypes.game)

        #1.- generar y obtener data de los partidos
        df_partido = process_data.get_entidad_partido(df_clean)

        #2.- generar y obtener data de partidos
        df_equipos = process_data.get_entidad_equipo(df_clean)

        #3.- generar y obtener data de: tabla de posiciones
        df_tabla_posiciones = process_data.get_tabla_posiciones(df_partido,df_equipos)

        #4.- generar y obtener data de: Equipo con mejor relacion de disparos al arco
        df_equipos_mejor_relacion_disparos_arco = process_data.get_equipos_mejor_relacion_disparos_arco_por_temporada(df_equipos)

        #5.- generar y obtener data de: Equipo más goleado
        df_equipo_mas_goleado = process_data.get_equipo_mas_goleado_por_temporada(df_tabla_posiciones)

        #6.- Generar archivos de salida

        path = 'output'

        #6.1 Tabla de posiciones
        helpers.generar_archivos_csv(df_tabla_posiciones,'output/tabla_posiciones.csv')

        #6.2 Equipo con mejor relacion de disparos al arco
        helpers.generar_archivos_csv(df_equipos_mejor_relacion_disparos_arco,'output/equipo_mejor_relacion_disparos_arco.csv')

        #6.3 Equipo más goleado
        helpers.generar_archivos_csv(df_equipo_mas_goleado,'output/equipo_mas_goleado.csv')

        #eliminar df que ya no se van a usar
        del df_tabla_posiciones,df_equipos_mejor_relacion_disparos_arco,df_equipo_mas_goleado

    except Exception as e:
        print(e)
        raise ValueError(e)

    finally:
        print('')

main()