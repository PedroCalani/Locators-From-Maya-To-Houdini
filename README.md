# Locators-From-Maya-To-Houdini

"Tool in development"

## *Archivos en el repositorio:*

import_locators.shelf (va en la carpeta toolbar de houdini ubicada en documentos)

shelf_Locators_Exporter.mel (va en la carpeta prefs\shelves de Maya ubicada en documentos)

## *Archivos Adicionales:*

Export_locators_code.py (es el codigo de la tool de Maya colocado en un .py)

Import_locators_code (es el codigo de la tool de Houdini colocado en un .py)

Test_Export_locators.json (es el json del ejemplo explicado más abajo en este documento)


## *Cómo funciona?*

Desde una interfaz en maya podemos exportar un json con uno o más locators.

Desde otra tool en houdini podemos leer ese json e importar todos esos locators en un nodo Add, o cada uno en diferentes nodos Add


### EJEMPLO:

Cree una escena vacía en maya y coloqué varios locators en diferentes ubicaciones aleatorias:

![image](https://github.com/user-attachments/assets/80aee527-dbb0-4c64-86fd-49e36c481608)

Después abrí la tool. Inmediatamente aparecen todos los locators de la escena.
Es posible ir seleccionando los que queremos exportar o seleccionar todos de una desde el check.
También, en la parte superior debemos configurar dónde se exportará el json.

![image](https://github.com/user-attachments/assets/8970269b-138f-4be2-8b46-5d9a4278418f)

Una vez damos al botón la ventana se cierra y aparece la confirmación de que el json fue creado.

![image](https://github.com/user-attachments/assets/15d338e3-0b08-4c08-babe-2ed27ac179d3)

Una vez en Houdini, abrimos la shelftool y se abre una ventana similar a la usada en Maya.

![image](https://github.com/user-attachments/assets/778039d7-5431-4b44-ac65-bf86ca3ad146)

Tendremos que seleccionar el archivo json creado anteriormente e inmediatamente aparecerán todos los locators que habíamos exportado.
Además, tenemos la posibilidad de decidir cuales queremos importar. Lo hacemos con la misma forma de selección que en maya.
También, antes de pulsar el botón de importar, podemos configurar modo de importación entre 2 opciones:
* Importar todos los locators como puntos en un nodo Add.
* Importar cada locator como un punto en nodos Add diferentes.
* 
![image](https://github.com/user-attachments/assets/00e7a284-2f7d-41d2-8ece-7a3a1fbac39f)

Una vez exportamos, recibimos mensaje de confirmación la ventana se cierra y tendremos el nodo creado:

![image](https://github.com/user-attachments/assets/3520c04c-7100-49df-9d6b-f694bbb2ffe8)
![image](https://github.com/user-attachments/assets/3bb2eddf-35c5-479e-89fc-761465b4dd7b)

Si hubiéramos importado con la otra opción:

![image](https://github.com/user-attachments/assets/6e1f6022-8af7-48d4-a27c-417eb8c1be3c)
![image](https://github.com/user-attachments/assets/c3be3c56-23fe-4624-8e8d-74cdaa00476e)



