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

![image](https://github.com/user-attachments/assets/9e652c3c-3ee8-405d-8b2b-7cf31e509781)

Después abrí la tool. Inmediatamente aparecen todos los locators de la escena.
Es posible ir seleccionando los que queremos exportar o seleccionar todos de una desde el check.
También, en la parte superior debemos configurar dónde se exportará el json.

![image](https://github.com/user-attachments/assets/a1463ab8-698d-419e-ae12-ab0ba44d42a7)

Una vez damos al botón la ventana se cierra y aparece la confirmación de que el json fue creado.

![image](https://github.com/user-attachments/assets/72a56b64-49fa-4603-b679-bf13daa3f7a4)

Una vez en Houdini, abrimos la shelftool y se abre una ventana similar a la usada en Maya.

![image](https://github.com/user-attachments/assets/eeaea635-6feb-4590-a0d1-b9f3f6d14869)

Tendremos que seleccionar el archivo json creado anteriormente e inmediatamente aparecerán todos los locators que habíamos exportado.
Además, tenemos la posibilidad de decidir cuales queremos importar. Lo hacemos con la misma forma de selección que en maya.
También, antes de pulsar el botón de importar, podemos configurar modo de importación entre 2 opciones:
* Importar todos los locators como puntos en un nodo Add.
* Importar cada locator como un punto en nodos Add diferentes.
* 
![image](https://github.com/user-attachments/assets/2968a677-67fb-4764-933c-e39d9f32cfdd)

Una vez exportamos, recibimos mensaje de confirmación la ventana se cierra y tendremos el nodo creado:

![image](https://github.com/user-attachments/assets/d25a6706-8efb-4225-8fa9-6eb507dd194f)
![image](https://github.com/user-attachments/assets/c5f77f65-6339-42bd-b177-9405155fbb13)

Si hubiéramos importado con la otra opción:

![image](https://github.com/user-attachments/assets/824e8c43-30c3-46ff-b8b0-708fc4dbf72a)
![image](https://github.com/user-attachments/assets/6ef09458-25ac-4174-911d-b199823d4563)


