from os.path import normpath, expanduser, isdir, isfile
import os
import sys
import glob
import hashlib
import copy


def md5sum(url_archivo):
    with open(os.path.expanduser(os.path.normpath(url_archivo)),'rb') as ar:
        return str(hashlib.md5(ar.read()).hexdigest())


def archivos_iguales (url1, url2):
    with open(url1, 'rb') as ar1:
        with open (url2, 'rb') as ar2:
            return ar1.read() == ar2.read()


def acorta_url(url, tam):
    if len(url) > tam:
        exceso=len(url)-tam
        return f"{url[:int(tam/2)-3]}...{os.path.split(url)[1]}"
    return url


def ldir (d, lista=list()):
    try:
        for ruta in os.listdir(d):
            if isfile(os.path.join(d,ruta)):
                print(f"leyendo...{acorta_url(os.path.join(d,ruta),80)}")
                lista.append(os.path.join(d,ruta))
            if isdir(os.path.join(d,ruta)):
                ldir (os.path.join(d,ruta), lista)
    except PermissionError:
        print(f"\nExcepcion en {d}\n")


def busca_duplicados(d):
    lista1=list()
    lista2=list()
    ldir (d, lista1)
    lista1 = sorted(lista1)
    lista2 = copy.copy(lista1)
    cant_elementos= len(lista1)
    cant_procesados=0
    print("Buscando duplicados...")
    for f1 in lista1:
        for f2 in lista2:
            print(f"comparando {cant_procesados}/{cant_elementos}...{os.path.split(f1)[1]} == {os.path.split(f2)[1]}?")
            if archivos_iguales(f1,f2) and str(f1) != str(f2):
                print(f"(duplicados);{f1};{f2}")
        cant_procesados+=1
        del lista2[0]


if len(sys.argv)<2:
    print("faltan parametros")
    sys.exit()

l=list()
busca_duplicados(normpath(expanduser(sys.argv[1])))






