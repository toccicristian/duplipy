#!/usr/bin/python3

from os.path import normpath, expanduser, isdir, isfile
import os
import sys
import glob
import hashlib
import copy

#################     VALORES EDITABLES     ##################

# A partir de cuantos bytes deja de comparar contenido
# y comienza a comprarar tamaños:
DETALLE=20480
LOGFILE="duplilog.txt"

############      FIN DE VALORES EDITABLES    ################


EXTENSIONES_PERMITIDAS=False


buffer=""
archivos_totales=0
buffer_archivos_totales=f"(totales 0)"

def loguea(cadena):
    with open(os.path.normpath(os.path.expanduser(LOGFILE)),"a") as arlog:
        arlog.writelines(cadena+"\n")


def borra_linea(cadena):
    print("",end='\r',flush=True)
    for _ in range(0,len(cadena)):
        print(" ",end='',flush=True)
    print("",end='\r',flush=True)
    return None


def reemplaza_texto(linea_vieja, linea_nueva):
    for x in range (0, len(linea_vieja)):
        print("",end='\b',flush=True)

    print(linea_nueva,end='',flush=True)
    if (len(linea_nueva)<len(linea_vieja)):
        for x in range (0, len(linea_vieja)-len(linea_nueva)):
            print(" ",end='',flush=True)

        for x in range (0, len(linea_vieja)-len(linea_nueva)):
            print("",end='\b',flush=True)

    return None


def reemplaza_linea(linea_vieja, linea_nueva):
    print("",end="\r",flush=True)
    print(linea_nueva,end='',flush=True)
    if (len(linea_nueva)<len(linea_vieja)):
        for x in range (0, len(linea_vieja)-len(linea_nueva)):
            print(" ",end='',flush=True)

        for x in range (0, len(linea_vieja)-len(linea_nueva)):
            print("",end='\b',flush=True)

    return None


# hace una comparacion detallada del contenido si el archivo1 es pequeño (<DETALLE)
# y coincide en tamaño con archivo 2
#artup1 y artup2 son tuplas de url y tamaño en bytes (st_size)
def comparacion_selectiva(artup1, artup2):
    if artup1[1] < DETALLE and artup1[1] == artup2[1]:
        with open(artup1[0], 'rb') as ar1:
            with open (artup2[0], 'rb') as ar2:
                return ar1.read() == ar2.read()

    return artup1[1]== artup2[1]


def acorta_url(url, tam):
    if len(url) > tam:
        exceso=len(url)-tam # TODO: hacer mas copado esto
        return f"{url[:int(tam/2)-3]}...{os.path.split(url)[1]}"
    return url


def restringido(url):
    if not EXTENSIONES_PERMITIDAS:
        return False
    if len([ex for ex in EXTENSIONES_PERMITIDAS if url.endswith(ex)])>0:
        return False
    return True


def ldir (d, lista=list()):
    try:
        for ruta in os.listdir(d):
            if isfile(os.path.join(d,ruta)) and (not restringido(os.path.join(d,ruta))):
                salida=f"leyendo...{acorta_url(os.path.join(d,ruta),80)}"
                global buffer
                reemplaza_linea(buffer, salida)
                buffer=salida
                # print(f"leyendo...{acorta_url(os.path.join(d,ruta),80)}")
                lista.append( (os.path.join(d,ruta),os.stat(os.path.join(d,ruta)).st_size) ) #agrego URL y Tamaño como tupla a la lista
            if isdir(os.path.join(d,ruta)):
                ldir (os.path.join(d,ruta), lista)

            # TODO : Capaz me conviene presentar esto a la izquierda siempre
            # global archivos_totales
            # global buffer_archivos_totales
            # archivos_totales+=1
            # salida=f"(totales {archivos_totales})"
            # reemplaza_texto(buffer_archivos_totales, salida)
            # buffer_archivos_totales=salida

    except (PermissionError, OSError) as e:
        print(f"\nExcepcion {e} en {d}\n")
        loguea(f"Excepcion {e} en {d}")


def busca_duplicados(d):
    lista1=list()
    lista2=list()
    ldir (d, lista1)
    lista1 = sorted(lista1, key= lambda x : x[0])
    lista2 = copy.copy(lista1)
    cant_elementos= len(lista1)
    cant_procesados=0
    print("Buscando duplicados...")
    for f1 in lista1:
        # salida=f"comparando {cant_procesados}/{cant_elementos} ({(cant_procesados*100/cant_elementos):.2f}%)...{os.path.split(f1[0])[1]}"
        salida=f"comparando {cant_procesados}/{cant_elementos} ({(cant_procesados*100/cant_elementos):.2f}%)..."
        print(f"{salida}",end='\r',flush=True)
        #print(f"comparando {cant_procesados}/{cant_elementos} ({(cant_procesados*100/cant_elementos):.2f}%)...{os.path.split(f1[0])[1]}")
        for f2 in lista2:
            # print(f"comparando {cant_procesados}/{cant_elementos} ({(cant_procesados*100/cant_elementos):.2f}%)...{os.path.split(f1[0])[1]} == {os.path.split(f2[0])[1]}?")
            # print(f"comparando {cant_procesados}/{cant_elementos}...{os.path.split(f1[0])[1]} == {os.path.split(f2[0])[1]}?")
            if comparacion_selectiva(f1, f2) and str(f1[0]) != str(f2[0]):
                print(f"\r(duplicados);{f1[0]};{f2[0]}")
                loguea(f"{f1[0]};{f2[0]}")
        borra_linea(salida)
        cant_procesados+=1
        del lista2[0]


if len(sys.argv)<2:
    print("faltan parametros")
    sys.exit()

if len(sys.argv)>2:
    EXTENSIONES_PERMITIDAS=list()
    for arg in sys.argv[2:]:
        EXTENSIONES_PERMITIDAS.append("."+arg)

l=list()

try:
    busca_duplicados(normpath(expanduser(sys.argv[1])))

except KeyboardInterrupt:
    print("Programa finalizado por el usuario (Ctrl+C)")






