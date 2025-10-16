#   Este programa busca recursivamente y loguea archivos duplicados.
#   Copyright (C) 2024 Cristian Tocci
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   Contacto : toccicristian@hotmail.com / toccicristian@protonmail.ch


licencias = dict()
licencias['gplv3'] = """    duplipy.py  Copyright (C) 2024  Cristian Tocci
    This program comes with ABSOLUTELY NO WARRANTY; for details use -w argument.
    This is free software, and you are welcome to redistribute it
    under certain conditions; See COPYING.odt file for further details.
"""
licencias['gplv3logo'] = """
+----------------------------------------------------------------------------------------------------+
|oooooooo+~~~+~~~~~~+~~~~~+~~~~+~~~~~~+~~~~+~~~~~~+~~+~~~~+~~~~~+~~~~+~~~~~~++~~+~~+~~~~~~:  ::::::~+|
|oooooooo :::::::::::::::::::::::::::::::::::::::::::~::::::::::::::::::::::::::::::::. ~~~++ooooo+:.|
|ooooooo~::::::~:::::::::::::::::::::::::::::::::::::+::::::::::::::::::::::::~~.~:~:~+oooooooooooo:.|
|ooooooo :~:~~~~~~~~~~+~::: +~~~~~~~~~~~~~::++ :::::~+~:::::::::::::::::::~...~:::~ooooooooooooooo~.+|
|oooooo~~:~oo~~~~~~~~~oo~:~+oo ~~~~~~.ooo.~oo+~::::.+o ::::::::::::::::~  .~::::+oo+~:   +ooooooo::+o|
|oooooo::.+o+~::::::~+oo : oo~::::::::oo~:~oo~::::: oo~:::::::::::::: ~ ~::::.++~ ~:::::.+oooo+~ ~ooo|
|ooooo+~:~oo~:::::::::::::~oo::::::::+oo :+oo~:::::~oo+.::::::::::.:~ ~:::::: .:::::::~~oooo+:~ +oooo|
|ooooo::~+o+.:::::::::::: oo+~:::::: oo~~:oo~::::::~ooo~::::::::.~~.::::::::::::::::~~+oooooo+~::oooo|
|oooo+~::oo~:::~:~:~~::::~oo~       ~oo::+oo.::::::~ooo+~::::: ~~.:::::::::::::::: ~+oooooooooo~~oooo|
|oooo~::+oo :::~   +oo::.ooo~~~~~~~~~:.: oo+:::::::~oooo~:::~~+:::::::::::::::: ~+++~~~~oooooo+.~oooo|
|ooo+.: oo~:::::::.oo+.:~oo~::::::::::::~oo:::::::::oooo+~::++~::::::::::::::~   .::::::ooooo~.~ooooo|
|ooo~::~oo::::::::~oo~:~+o+~::::::::::: oo+~:::::::.+ooo~.~o+:::::::::::::::::::::::: +oooo+: +oooooo|
|ooo.: oo+.~~~~~~ +oo.::oo~::::::::::::~oo~~~~~~~:::+oo~ +oo ::::::::::::::::::::.:~ooooo+: ~oooooooo|
|oo~::.~~~~~~~~~~~~~ ::~+~.::::::::::::~+~~~~~~~~~:::o~ +ooo:::::::::::::::::: ~+oooooo~::~oooooooooo|
|o+ :~   ~::::::::::::.  ~::::: ..:::::::::::::::::::~ ~oooo~~::::::::::~. ~~+oooooo+~::+oooooooooooo|
|o~~:~~: ~ :~~. ~~.::~~~~. ::.~~~~::~:: :~~.~::~~ ::::.oooooo+~~::::~~~~ooooooooo+~::~+oooooooooooooo|
|o::~~~~:::~~~ ~~~.:: ::~.~:~.~~~: ~~~ :~~~: ~~~~~:::: oooooooooooooooooooooo++~::~+ooooooooooooooooo|
|+:::~::::::~~::::::::~~:::~::~:::::::::::~::::~:::::::~ooooooooooooooooo++~::~~+oooooooooooooooooooo|
|::::::::::::::::::::::::::::::::::::::::::::::::::::::: ~oooooooooo+~~~::~~+oooooooooooooooooooooooo|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:~~~~~:    ::::::::~~~ooooooooooooooooooooooooooooo|
+----------------------------------------------------------------------------------------------------+
"""
licencias['textow'] = """ 
    15. Disclaimer of Warranty.
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY 
    APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT 
    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT 
    WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
    PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE 
    OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU 
    ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
    
    16. Limitation of Liability.
    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING 
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR 
    CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR 
    DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL 
    DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM 
    (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED 
    INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF 
    THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER 
    OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    17. Interpretation of Sections 15 and 16.
    If the disclaimer of warranty and limitation of liability provided above 
    cannot be given local legal effect according to their terms, 
    reviewing courts shall apply local law that most closely approximates 
    an absolute waiver of all civil liability in connection with the Program, 
    unless a warranty or assumption of liability accompanies a copy of 
    the Program in return for a fee.
    """



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

ayuda=f"""
    {sys.argv[0]}
    Descripción: Busca y loguea archivos duplicados recursivamente.
    Dado un tamaño (configurable en la variable DETALLE) compara los contenidos
    de los archivos que superen ese tamaño, sino sólo compara el espacio que ocupan.

    Es posible definir una serie de extensiones de nombres de archivo para que {sys.argv[0]}
    indexe y compare sólo los archivos que posean esa extensión.

    SINTAXIS:
    {sys.argv[0]} directorio[{os.path.join('/','directorio2')}[...]][ .extension1[ .extension2 [ ...]]]

    argumentos:
        -h/--help/--ayuda       esta ayuda
        -w                      disclaimer of warranty
        -c                      copiright info
        -g                      gplv3 ascii logo
"""

if len(sys.argv)>1:
    for a in sys.argv[1:]:
        if len([x for x in ["--help","-h","--ayuda"] if x == a.rstrip()])>0:
            print(f"{ayuda}")
            sys.exit()

        if a.rstrip() == "-w":
            print(licencias['textow'])
            sys.exit()

        if a.rstrip() == "-c":
            print(licencias['gplv3'])
            sys.exit()

        if a.rstrip() == "-g":
            print(licencias['gplv3logo'])
            sys.exit()


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






