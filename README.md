# Obtenedor de Fotos API 🖼️

Cliente Python para obtener datos de fotos y álbumes desde JSONPlaceholder.

<!-- # Instalación -->
```bash
git clone https://github.com/Ibar-Dev/ObtenedorFotos.git
cd ObtenedorFotos
pip install -r requirements.txt


📸 ¡Cazador de Fotos con Estilo! 🚀
¡Hola, amigos! 👋 Les presento este proyecto súper interesante que llamaremos Cazador de Fotos con Estilo. Este código está diseñado para cazar datos sobre fotos y sus álbumes desde una API llamada JSONPlaceholder y, ¡lo hace a la velocidad del rayo! ⚡

Si alguna vez han querido probar cómo funciona el mundo de las APIs o la magia de la programación concurrente (o sea, hacer muchas cosas a la vez), este proyecto les va a encantar. 😎

¿Qué hace este código? 🧐
Busca fotos y álbumes: Usa la API de JSONPlaceholder para traer información sobre fotos y los álbumes en los que están.

Modos para todos los gustos: Permite procesar fotos de distintas maneras, desde el modo más tranquilo y secuencial hasta el modo turbo con hilos o procesos paralelos. 💨

Comparativa de velocidad: ¿Quién ganará la carrera? Este código puede comparar qué tan rápido funcionan los distintos modos de ejecución.

¿Qué necesitamos? 🛠️
Antes de empezar, asegúrate de tener instalado Python 3.8 o superior. También deberás instalar algunas dependencias para que todo funcione de maravilla (puedes hacerlo con pip install requests).

Instrucciones de uso 🏃‍♂️
Ejecuta el código desde la terminal:

bash
python tu_codigo.py --modo [secuencial|hilos|procesos|comparar] --fotos NUMERO_FOTOS --nivel-log [DEBUG|INFO|WARNING|ERROR]
--modo: Elige cómo quieres procesar las fotos:

secuencial: Un paso a la vez (¡ideal si eres zen! 🧘).

hilos: Múltiples tareas al mismo tiempo (como un pulpo 🐙).

procesos: Similar a los hilos, pero aún más avanzado.

comparar: ¡Veamos quién es el más rápido! 🏁

--fotos: El número de fotos a procesar (por defecto, se procesarán todas las disponibles). 📸

--nivel-log: Decide el nivel de chismes (digo, información) que quieres en los logs.

Ejemplo práctico: Si quieres procesar 1000 fotos con hilos:

bash
python tu_codigo.py --modo hilos --fotos 1000 --nivel-log INFO
¿Qué hay bajo el capó? 🚗
Este proyecto está lleno de pequeñas genialidades:

Clase ObtenedorFotos: Es como nuestro detective principal. Usa requests para traer los datos de las fotos y álbumes.

Concurrencia total: Aprovecha la potencia de Python con hilos (ThreadPoolExecutor) y procesos (multiprocessing.Pool).

Logs elegantes: Registra todo lo que pasa, para que nunca te pierdas ningún detalle. 🕵️‍♂️

¡A ponerse manos a la obra! ✨
Espero que este código les inspire a seguir explorando el universo de la programación y APIs. ¡Anímense a modificarlo, probarlo y hacerlo aún más suyo!

Y recuerden: programar es como cocinar, hay que experimentar, divertirse y, de vez en cuando, echarle una pizca de locura. 😄 ¡Que lo disfruten!


# Uso Básico

# Modo secuencial
python obtenedor_fotos.py --modo secuencial --fotos 50

# Modo comparativo
python obtenedor_fotos.py --modo comparar --fotos 100

# Ver todos los parámetros
python obtenedor_fotos.py --help
