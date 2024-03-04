Script para automatizar carga de horas en clockify

requisitos:
1)Python v3 instalado
2)Instalar si pide dependencias

pip install requests
pip install  pytz
pip install json

Pasos:
1) Generar API KEY desde Clockify. Configuracion -> Api -> GENERATE API KEY
2) Dentro de /internal, buscar el archivo apiToken.json, cambiar el valor de la variable por la api key anterior
3) Desde programador de tareas, armar una tarea que ejecute el .exe dentro de la carpeta /dist

Abrir barra de windows-> Programador de tareas
    a)Crear tarea 
    b)Desencadenadores -> Setear horas
    c)Accion -> ejecutar programa -> Buscar exe dentro de carpeta /dist
Se pueden armar dos tareas que corran a diferentes horas para asegurarse de que corra el programa


---Consideraciones
Si hay horas cargadas para el proyecto, el programa va a finalizar sin cargar nada
Si es feriado o sabado, o domingo, el programa no va a cargar horas
Podria modificarse para agregar el id de tarea, actualmente va vacios



