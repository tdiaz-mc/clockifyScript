# Clockify Task Scheduler

Este script automatiza la carga de horas en Clockify mediante el uso de una tarea programada en Windows.

## Requisitos

- Python v3 instalado
- Dependencias:
  ```bash
  pip install requests
  pip install pytz
  pip install json
  ```

## Pasos

1. Generar API KEY desde Clockify:
   - Dirígete a Configuración -> API -> Generar API KEY

2. Actualizar el archivo `apiToken.json`:
   - Ubica el archivo `apiToken.json` dentro de `dist/internal`.
   - Cambia el valor de la variable `API_TOKEN` por la API KEY generada anteriormente.

3. Configurar la tarea programada:
   - Abrir el Programador de tareas de Windows: Barra de Windows -> Programador de tareas.
   - Crear una nueva tarea.
   - Configura los desencadenadores para establecer la hora de ejecución.
   - Configura la acción para ejecutar el programa:
     - Selecciona "Ejecutar programa".
     - Busca el ejecutable dentro de la carpeta `/dist`.

   *Nota: Se pueden crear múltiples tareas programadas con diferentes horarios para asegurar la ejecución del programa.*

## Consideraciones

- Si ya hay horas cargadas para el proyecto, el programa finalizará sin cargar nuevas horas.
- El programa no cargará horas en feriados, sábados o domingos.
- El programa tiene hardcodeado el workspace y demas, habria que modificar eso y crear otro ejecutable.
- Se puede modificar el script para agregar el ID de la tarea; actualmente, este campo está vacío.
- Se podria meter un archivo de config para los datos hardcodeados

---

