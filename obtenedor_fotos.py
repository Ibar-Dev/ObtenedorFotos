import argparse # Esto nos permite que el programa reciba instrucciones cuando lo ejecutemos desde la terminal.
import logging # Esta librería nos ayuda a guardar registros de lo que el programa va haciendo, por si hay algún problema.
import sys # Esta librería nos da acceso a cosas del sistema operativo, como la terminal.
import time # Nos permite medir el tiempo que tarda el programa en hacer cosas.
from concurrent.futures import ThreadPoolExecutor, as_completed # Esto nos ayuda a hacer varias cosas a la vez usando "hilos" (como varios trabajadores haciendo tareas pequeñas).
from multiprocessing import Pool # Similar a lo anterior, pero usa "procesos" que son como programas separados para hacer tareas en paralelo.
from requests import Session, exceptions as excepciones_requests # Esta librería nos permite hacer peticiones a páginas web (APIs en este caso) para obtener información.

# Configuración centralizada
URL_BASE = "https://jsonplaceholder.typicode.com" # Aquí definimos la dirección web principal de donde vamos a sacar la información. Es como la "calle" principal.
URL_FOTOS = f"{URL_BASE}/photos" # Aquí construimos la dirección web específica para obtener información de las fotos. Es como decir "en la calle principal, la sección de fotos".
URL_ALBUMES = f"{URL_BASE}/albums" # Igual que antes, pero para obtener información de los álbumes de fotos. "En la calle principal, la sección de álbumes".
MAX_CONCURRENTES = 50  # Límite seguro para conexiones simultáneas. Esto dice cuántas peticiones podemos hacer a la vez sin que la página web se sature.
TIEMPO_ESPERA = 10  # Segundos para timeout de peticiones. Si tardamos más de 10 segundos en obtener una respuesta, cancelamos la petición para no quedarnos esperando indefinidamente.
FOTOS_POR_DEFECTO = 5000  # Valor de respaldo si no se obtiene el total. Si por alguna razón no podemos saber cuántas fotos hay en total, usamos este número como referencia.

# Configuración inicial del logging
logging.basicConfig( # Aquí configuramos cómo queremos que se guarden los registros del programa.
    level=logging.INFO, # Indicamos que queremos guardar información importante (INFO), advertencias (WARNING) y errores (ERROR).
    format='%(asctime)s - %(levelname)s - %(message)s', # Definimos cómo se va a mostrar cada línea del registro: la fecha y hora, el tipo de mensaje (INFO, ERROR, etc.) y el mensaje en sí.
    handlers=[ # Aquí decimos dónde queremos guardar esos registros.
        logging.StreamHandler(sys.stdout), # Queremos que los mensajes importantes se muestren también en la pantalla (la terminal).
        logging.FileHandler('obtenedor_fotos.log') # Y también queremos que se guarden en un archivo llamado 'obtenedor_fotos.log' para poder revisarlos después.
    ]
)
logger = logging.getLogger(__name__) # Creamos una herramienta para poder escribir esos registros.

class ObtenedorFotos: # Creamos una "clase", que es como un molde para crear objetos que nos ayudarán a obtener las fotos.
    def __init__(self): # Este es un "constructor", que se ejecuta automáticamente cuando creamos un objeto de la clase ObtenedorFotos.
        self.sesion = Session() # Creamos una "sesión" para poder hacer varias peticiones a la misma página web de forma más eficiente. Es como abrir un navegador web.
        self.sesion.headers.update({'User-Agent': 'ObtenedorFotos/1.0'}) # Le decimos a la página web quiénes somos para que nos identifique. Es como decir "hola, soy el programa ObtenedorFotos versión 1.0".

    def obtener_datos_foto(self, id_foto): # Esta función se encarga de obtener la información de una foto específica, usando su ID (número de identificación).
        """Obtiene datos de una foto y su álbum asociado.""" # Este es un comentario que explica qué hace esta función. Está bien.
        try: # Intentamos hacer lo siguiente, y si algo sale mal, vamos a la parte que dice "except".
            # Obtener datos de la foto
            foto = self._obtener_recurso(f"{URL_FOTOS}/{id_foto}") # Usamos una función interna para ir a la dirección web de la foto con el ID que nos dieron y obtener su información.

            # Obtener datos del álbum
            album = self._obtener_recurso(f"{URL_ALBUMES}/{foto['albumId']}") # Una vez que tenemos la información de la foto, vemos a qué álbum pertenece y usamos otra vez la función interna para obtener la información de ese álbum.

            return { # Devolvemos un "diccionario" (una especie de lista con etiquetas) con la información que obtuvimos.
                'id': foto['id'], # El ID de la foto.
                'titulo': foto['title'], # El título de la foto.
                'url': foto['url'], # La dirección web donde se encuentra la foto.
                'album': { # Dentro de la información de la foto, también incluimos la información del álbum.
                    'id': album['id'], # El ID del álbum.
                    'titulo': album['title'] # El título del álbum.
                }
            }
        except (excepciones_requests.RequestException, KeyError) as e: # Si ocurre algún error al hacer la petición a la web o si falta alguna información importante, hacemos lo siguiente.
            logger.error(f"Error procesando foto {id_foto}: {str(e)}") # Guardamos un mensaje de error en el registro, indicando qué foto falló y cuál fue el error.
            return {'id': id_foto, 'error': str(e)} # Devolvemos un diccionario indicando que hubo un error con esta foto y cuál fue el error.

    def _obtener_recurso(self, url): # Esta es una función interna (por eso empieza con un guion bajo) que se encarga de hacer la petición a una dirección web y obtener la información.
        """Método interno para obtener recursos de la API.""" # Este comentario también está bien.
        try: # Intentamos hacer la petición a la web.
            respuesta = self.sesion.get(url, timeout=TIEMPO_ESPERA) # Usamos la "sesión" que creamos antes para ir a la dirección web que nos dieron y esperamos un máximo de 10 segundos por la respuesta.
            respuesta.raise_for_status() # Si la página web nos dice que hubo algún problema con la petición (por ejemplo, que no encontró la dirección), esto nos avisará.
            return respuesta.json() # Si todo va bien, la página web nos devuelve la información en un formato llamado JSON, y aquí lo convertimos a un formato que Python puede entender (un diccionario o una lista).
        except excepciones_requests.RequestException as e: # Si ocurre algún error al hacer la petición (por ejemplo, si no hay conexión a internet), hacemos lo siguiente.
            logger.debug(f"Error en petición a {url}: {str(e)}") # Guardamos un mensaje de información detallada (DEBUG) en el registro sobre el error.
            raise # Volvemos a lanzar el error para que la función que llamó a esta sepa que algo salió mal.

def obtener_total_fotos(obtenedor): # Esta función intenta obtener el número total de fotos disponibles en la página web.
    """Obtiene el número total de fotos disponibles.""" # Este comentario está bien.
    try: # Intentamos obtener la lista de todas las fotos.
        datos = obtenedor._obtener_recurso(URL_FOTOS) # Usamos la función para obtener información de la dirección web de las fotos. Esto debería devolver una lista con todas las fotos.
        return len(datos) # Contamos cuántos elementos hay en esa lista y ese será el número total de fotos.
    except excepciones_requests.RequestException: # Si no podemos obtener la lista de fotos (por ejemplo, si hay un problema con la conexión), hacemos lo siguiente.
        logger.warning("Usando valor por defecto para total de fotos") # Guardamos una advertencia en el registro indicando que vamos a usar el valor por defecto.
        return FOTOS_POR_DEFECTO # Devolvemos el número que definimos al principio como valor de respaldo (5000).

def ejecutar_secuencial(obtenedor, limite): # Esta función ejecuta el proceso de obtener información de las fotos una por una, en orden.
    """Ejecución secuencial de las peticiones.""" # Este comentario está bien.
    logger.info(f"Iniciando modo secuencial ({limite} fotos)...") # Guardamos un mensaje en el registro indicando que vamos a empezar a procesar las fotos de forma secuencial (una tras otra).
    inicio = time.perf_counter() # Medimos el tiempo justo antes de empezar.
    resultados = [obtenedor.obtener_datos_foto(i+1) for i in range(limite)] # Creamos una lista donde vamos a guardar los resultados de obtener la información de cada foto, desde la foto número 1 hasta el límite que nos hayan indicado.
    return resultados, time.perf_counter() - inicio # Devolvemos la lista de resultados y el tiempo que tardamos en obtenerlos.

def ejecutar_con_hilos(obtenedor, limite): # Esta función intenta obtener la información de las fotos usando "hilos", lo que permite hacer varias cosas a la vez y podría ser más rápido.
    """Ejecución concurrente usando hilos.""" # Este comentario está bien.
    logger.info(f"Iniciando modo multihilos ({limite} fotos)...") # Guardamos un mensaje en el registro indicando que vamos a usar múltiples "hilos" para procesar las fotos al mismo tiempo.
    inicio = time.perf_counter() # Medimos el tiempo justo antes de empezar.

    with ThreadPoolExecutor( # Creamos un grupo de "trabajadores" (hilos) que pueden hacer tareas en paralelo.
        max_workers=min(MAX_CONCURRENTES, limite) # El número máximo de trabajadores será el menor entre el límite que definimos al principio (50) y el número total de fotos que queremos procesar. Así no creamos demasiados trabajadores si no son necesarios.
    ) as ejecutor: # Le damos un nombre a este grupo de trabajadores.
        futuros = [ # Creamos una lista de "tareas" que vamos a darles a los trabajadores.
            ejecutor.submit(obtenedor.obtener_datos_foto, i+1) # Para cada foto desde la 1 hasta el límite, creamos una tarea para obtener su información.
            for i in range(limite)
        ]
        resultados = [f.result() for f in as_completed(futuros)] # Esperamos a que todos los trabajadores terminen sus tareas y recogemos los resultados de cada uno.

    return resultados, time.perf_counter() - inicio # Devolvemos la lista de resultados y el tiempo total que tardamos.

def ejecutar_con_procesos(obtenedor, limite): # Similar a la función anterior, pero en lugar de usar "hilos", usa "procesos", que son como programas separados que se ejecutan al mismo tiempo. Esto también puede ser más rápido en algunos casos.
    """Ejecución paralela usando procesos.""" # Este comentario está bien.
    logger.info(f"Iniciando modo multiprocesos ({limite} fotos)...") # Guardamos un mensaje en el registro indicando que vamos a usar múltiples "procesos" para procesar las fotos en paralelo.
    inicio = time.perf_counter() # Medimos el tiempo justo antes de empezar.

    with Pool(processes=min(MAX_CONCURRENTES, limite)) as grupo: # Creamos un grupo de "procesos" que pueden trabajar en paralelo. El número máximo de procesos será el menor entre el límite que definimos y el número de fotos a procesar.
        resultados = grupo.map(obtenedor.obtener_datos_foto, range(1, limite+1)) # Le damos al grupo de procesos la tarea de obtener la información de cada foto desde la 1 hasta el límite.

    return resultados, time.perf_counter() - inicio # Devolvemos la lista de resultados y el tiempo total que tardamos.

def comparar_modos(obtenedor, limite): # Esta función ejecuta las tres formas de obtener las fotos (secuencial, con hilos y con procesos) para un número limitado de fotos y compara cuánto tiempo tarda cada una.
    """Comparativa de rendimiento entre modos de ejecución.""" # Este comentario está bien.
    modos = { # Creamos un diccionario donde guardamos los nombres de los modos de ejecución y las funciones que los ejecutan.
        'Secuencial': ejecutar_secuencial,
        'Multihilos': ejecutar_con_hilos,
        'Multiprocesos': ejecutar_con_procesos
    }

    resultados = {} # Creamos un diccionario para guardar el tiempo que tarda cada modo.
    for nombre, funcion in modos.items(): # Recorremos cada modo de ejecución.
        logger.info(f"Ejecutando modo {nombre}...") # Guardamos un mensaje en el registro indicando qué modo estamos ejecutando.
        _, tiempo_transcurrido = funcion(obtenedor, limite) # Ejecutamos la función del modo actual para el límite de fotos indicado y obtenemos el tiempo que tardó. No nos interesan los resultados de las fotos en este caso, solo el tiempo.
        resultados[nombre] = tiempo_transcurrido # Guardamos el tiempo que tardó este modo en el diccionario de resultados.
        time.sleep(2)  # Pausa entre ejecuciones. Esperamos 2 segundos entre la ejecución de cada modo para que no se mezclen los resultados en la terminal.

    # Presentación de resultados
    logger.info("\n" + "═" * 50) # Imprimimos una línea de guiones para separar los resultados.
    logger.info(f"COMPARATIVA PARA {limite} FOTOS:") # Indicamos para cuántas fotos se hizo la comparación.
    for nombre, tiempo in resultados.items(): # Recorremos los resultados de cada modo.
        logger.info(f"{nombre:<12}: {tiempo:.2f} segundos") # Imprimimos el nombre del modo y el tiempo que tardó, formateado a dos decimales.

    mas_rapido = min(resultados, key=resultados.get) # Encontramos el nombre del modo que tardó menos tiempo.
    logger.info(f"\nModo más rápido: {mas_rapido} ({resultados[mas_rapido]:.2f}s)") # Imprimimos cuál fue el modo más rápido y cuánto tiempo tardó.

def iniciar(): # Esta es la función principal que se encarga de empezar todo el proceso cuando ejecutamos el programa.
    """Función principal para manejo de línea de comandos.""" # Este comentario está bien.
    informador = argparse.ArgumentParser( # Creamos una herramienta para poder recibir instrucciones del usuario cuando ejecute el programa desde la terminal.
        description="Obtiene datos de fotos y álbumes desde la API" # Le damos una descripción a esta herramienta para que el usuario sepa qué hace el programa.
    )
    informador.add_argument( # Añadimos una opción para que el usuario pueda indicar el modo de ejecución que quiere usar.
        '--modo', # El nombre de la opción será "--modo".
        choices=['secuencial', 'hilos', 'procesos', 'comparar'], # Las opciones válidas para esta opción son 'secuencial', 'hilos', 'procesos' y 'comparar'.
        required=True, # Esta opción es obligatoria, el usuario tiene que elegir un modo.
        help="Modo de ejecución a utilizar" # Le damos una ayuda al usuario explicando qué hace esta opción.
    )
    informador.add_argument( # Añadimos otra opción para que el usuario pueda indicar cuántas fotos quiere procesar.
        '--fotos', # El nombre de la opción será "--fotos".
        type=int, # Esperamos que el valor que dé el usuario sea un número entero.
        help="Cantidad de fotos a procesar (por defecto: todas)" # Explicamos que si no se indica esta opción, se procesarán todas las fotos.
    )
    informador.add_argument( # Añadimos una opción para que el usuario pueda elegir el nivel de detalle de los mensajes que se guardan en el registro.
        '--nivel-log', # El nombre de la opción será "--nivel-log".
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], # Las opciones válidas son los diferentes niveles de registro.
        default='INFO', # Si el usuario no indica nada, el nivel de registro será INFO por defecto.
        help="Nivel de detalle del registro" # Explicamos qué hace esta opción.
    )
    argumentos = informador.parse_args() # Aquí le pedimos a la herramienta que revise las instrucciones que el usuario dio al ejecutar el programa.

    # Configurar nivel de logging
    logger.setLevel(argumentos.nivel_log) # Establecemos el nivel de detalle del registro según lo que haya indicado el usuario (o el valor por defecto).

    # Validar número de fotos
    if argumentos.fotos and argumentos.fotos <= 0: # Verificamos si el usuario indicó un número de fotos y si ese número es menor o igual a cero.
        logger.error("La cantidad de fotos debe ser un número positivo") # Si no es un número positivo, guardamos un mensaje de error en el registro.
        sys.exit(1) # Y terminamos el programa con un código de error (1).

    obtenedor = ObtenedorFotos() # Creamos un objeto de la clase ObtenedorFotos, que nos ayudará a obtener la información de las fotos.
    limite = argumentos.fotos or obtener_total_fotos(obtenedor) # Aquí decidimos cuántas fotos vamos a procesar. Si el usuario indicó un número con la opción "--fotos", usamos ese número. Si no, intentamos obtener el número total de fotos de la página web.

    if argumentos.modo == 'comparar': # Si el usuario eligió el modo "comparar".
        comparar_modos(obtenedor, min(limite, 100))  # Límite para comparativas. Ejecutamos la función para comparar los modos, pero limitamos el número de fotos a 100 para que no tarde demasiado.
    else: # Si el usuario eligió otro modo (secuencial, hilos o procesos).
        modos = { # Creamos un diccionario con los modos y las funciones correspondientes.
            'secuencial': ejecutar_secuencial,
            'hilos': ejecutar_con_hilos,
            'procesos': ejecutar_con_procesos
        }
        resultados, tiempo = modos[argumentos.modo](obtenedor, limite) # Obtenemos la función correspondiente al modo elegido por el usuario y la ejecutamos para el límite de fotos indicado. Guardamos los resultados y el tiempo que tardó.

        # Mostrar resumen final
        exitos = sum(1 for r in resultados if 'error' not in r) # Contamos cuántas fotos se procesaron correctamente (es decir, cuántos resultados no tienen la etiqueta 'error').
        logger.info( # Guardamos un mensaje en el registro con un resumen de lo que pasó.
            f"\nProceso completado: {exitos} correctos, " # Indicamos cuántas fotos se obtuvieron correctamente.
            f"{len(resultados)-exitos} errores\n" # Indicamos cuántas fotos tuvieron algún error.
            f"Tiempo total: {tiempo:.2f} segundos" # Indicamos cuánto tiempo tardó todo el proceso.
        )

if __name__ == '__main__': # Esta línea se asegura de que la función "iniciar" se ejecute solo cuando ejecutamos este archivo directamente (no cuando lo importamos desde otro archivo).
    try: # Intentamos ejecutar la función "iniciar".
        selector_de_fotos = ObtenedorFotos()
        selector_de_fotos.iniciar()
    except KeyboardInterrupt: # Si el usuario presiona Ctrl+C para interrumpir el programa.
        logger.info("\nEjecución interrumpida por el usuario") # Guardamos un mensaje en el registro indicando que el usuario interrumpió el programa.
        sys.exit(0) # Terminamos el programa de forma normal (con código 0).


'''

python pandora1.py --modo secuencial --fotos 100
python pandora1.py --modo secuencial --nivel-log ERROR

python pandora1.py --modo comparar --fotos 100
python pandora1.py --modo comparar --nivel-log WARNING
python pandora1.py --modo comparar --fotos 50 --nivel-log WARNING
python pandora1.py --modo comparar --fotos 50 --nivel-log ERROR

python pandora1.py --modo procesos --nivel-log DEBUG
python pandora1.py --modo procesos --fotos 75 --nivel-log DEBUG

python pandora1.py --modo hilos --nivel-log DEBUG

'''
