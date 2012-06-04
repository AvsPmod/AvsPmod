# -*- coding: utf-8 -*-

# This file is used to translate the messages used in the AvsPmod interface.
# To use it, make sure it is named "translation_lng.py" where "lng" is the 
# three-letter code corresponding to the language that is translated to 
# (see <http://www.loc.gov/standards/iso639-2/php/code_list.php>), 
# and is placed in the "translations" subdirectory.
# 
# Simply add translated messages next to each message (any untranslated 
# messages will be shown in English).  You can type unicode text directly 
# into this document - if you do, make sure to save it in the appropriate 
# format.  If required, you can change the coding on the first line of this 
# document to a coding appropriate for your translated language. DO NOT 
# touch line breaks (\n) and any words inside formatted strings (ie, any 
# portions of the text which look like %(...)s, %(...)i, etc.)

# Spanish translation authors:
#   zemog v2.0.1
#   Overdrive80 v2.2.0

version = "2.3.0"

messages = {
    "Find" : u"Buscar",
    "Replace" : u"Reemplazar",
    "Cannot find \"%(text)s\"" : u"", # New in v2.3.0
    "Replaced %(count)i times" : u"Reemplazada %(count)i veces",
    "AviSynth fonts and colors" : u"Fuentes y colores script AviSynth",
    "Background" : u"Fondo",
    "Font" : u"Fuente",
    "Text color" : u"Color texto",
    "OK" : u"OK",
    "Cancel" : u"Cancelar",
    "Scrap Window" : u"Ventana para notas",
    "Undo" : u"Deshacer",
    "Redo" : u"Rehacer",
    "Cut" : u"Cortar",
    "Copy" : u"Copiar",
    "Paste" : u"Pegar",
    "Select all" : u"Marcar todos",
    "Refresh" : u"Actualizar",
    "Insert frame #" : u"Insertar número fotograma activo",
    "Save to file..." : u"Guardar archivo...",
    "Clear all" : u"Desmarcar todos",
    "Toggle scrap window" : u"Abrir/Cerrar ventana para notas",
    "Save script" : u"Guardar script",
    "Error: no contextMenu variable defined for window" : u"Error: Variable de menú contextual no definida para esta ventana",
    "Text document" : u"", # New in v2.3.0
    "All files" : u"", # New in v2.3.0
    "Save scrap text" : u"Guardar estas notas como",
    "This field must contain a value!" : u"Este campo debe contener un valor",
    "This slider label already exists!" : u"¡Esta etiqueta ya existe!",
    "Invalid slider label modulo syntax!" : u"¡Sintaxis errónea para el Control de Ajuste!",
    "This field must contain a number!" : u"¡Este campo debe contener un número!",
    "The min value must be less than the max!" : u"¡El valor mínimo debe ser menor que el máximo",
    "The initial value must be between the min and the max!" : u"¡El valor inicial debe estar entre el mínimo y el máximo!",
    "The min value must be a multiple of %(mod)s!" : u"¡El valor mínimo debe ser múltiplo de %(mod)s!",
    "The max value must be a multiple of %(mod)s!" : u"¡El valor máximo debe ser múltiplo de %(mod)s!",
    "The initial value must be a multiple of %(mod)s!" : u"¡El valor inicial debe ser múltiplo de %(mod)s!",
    "The difference between the min and max must be greater than %(mod)s!" : u"¡La diferencia entre el valor mínimo y el máximo debe ser mayor de %(mod)s!",
    "Error" : u"Error",
    "Define user slider" : u"Control de Ajuste de  Filtro",
    "Slider label:" : u"Etiqueta:",
    "Min value:" : u"Valor mínimo:",
    "Max value:" : u"Valor máximo:",
    "Initial value:" : u"Valor inicial:",
    "Add or override AviSynth functions in the database" : u"Añadir o sustituir funciones AviSynth en la base de datos",
    "Core filters" : u"Filtros esenciales",
    "Plugins" : u"Plugins",
    "User functions" : u"Funciones de usuario",
    "Script functions" : u"Funciones script",
    "Clip properties" : u"Propiedades del Clip",
    "Include %(title)s in autcompletion lists" : u"Incluir %(title)s en la lista para autocompletar",
    "New function" : u"Nueva función",
    "Edit selected" : u"Editar seleccionado",
    "Delete selected" : u"Borrar seleccionado",
    "Select installed" : u"Marcar solo los instalados",
    "Import from files" : u"Importar desde archivos",
    "Export customizations" : u"Exportar personalizaciones",
    "Clear customizations" : u"Borrar personalizaciones",
    "Clear manual presets" : u"Borrar valores iniciales manuales",
    "When importing, don't show the choice dialog" : u"Al importar, no mostrar diálogo de selección",
    "Edit function information" : u"Editar información de la función",
    "Name:" : u"Nombre:",
    "Type:" : u"Tipo:",
    "clip property" : u"Propiedades del clip",
    "core filter" : u"Filtro esencial",
    "plugin" : u"plugin",
    "script function" : u"Función script",
    "user function" : u"Función de usuario",
    "Arguments:" : u"Argumentos:",
    "define sliders" : u"Definir Controles",
    "reset to default" : u"Volver a los valores por defecto",
    "Slider information" : u"Información del Control",
    "Preset:" : u"Valores iniciales:",
    "Auto-generate" : u"Auto generar",
    "Filter name already exists!" : u"¡Nombre del filtro ya existe!",
    "Invalid filter name!" : u"¡Nombre de filtro no válido!",
    "Renaming not allowed!" : u"¡No puede renombrarse!",
    "You must use dllname_function naming format for plugins!" : u"Para los plugins debe usar el formato nombredll_función",
    "Open Customization files, Avisynth scripts or Avsp options files" : u"Abrir archivos personalizados, scripts de Avisynth o archivos de opciones de AvsP",
    "All supported" : u"", # New in v2.3.0
    "Customization file" : u"", # New in v2.3.0
    "AvsP data" : u"", # New in v2.3.0
    "AviSynth script" : u"", # New in v2.3.0
    "Unrecognized files" : u"Archivos no reconocidos",
    "Select import functions" : u"Seleccione las funciones a importar",
    "select all" : u"Seleccionar todos",
    "select none" : u"No seleccionar ninguno",
    "select all (file only)" : u"Seleccionar todo (sólo archivo)",
    "select none (file only)" : u"No seleccionar ninguno (sólo archivo)",
    "Red - a customized function already exists." : u"Rojo - ya existe una función personalizada.",
    "No customizations to export!" : u"¡No hay personalizaciones para exportar!",
    "Save filter customizations" : u"Guardar personalizaciones de filtros",
    "This will delete all filter customizations. Continue?" : u"Se borraran todas las personalizaciones de filtros. ¿Continuar?",
    "Warning" : u"Aviso",
    "This will delete all manually defined presets. Continue?" : u"Se borraran todos los valores iniciales definidos manualmente. ¿Continuar?",
    "Do you want to delete this custom filter entirely?" : u"¿Borrar completamente la personalización de este filtro?",
    "Edit filter database" : u"Editar base de datos del filtro",
    "Default" : u"Por defecto",
    "Min value" : u"Valor mínimo",
    "Max value" : u"Valor máximo",
    "Step size" : u"Intervalo",
    "Value list (comma separated)" : u"Lista de valores (separados por comas)",
    "Value must be True or False!" : u"¡El valor debe ser True o False!",
    "Must enter a value list!" : u"¡Debe teclearse una lista de valores!",
    "Export filter customizations" : u"Exportar configuraciones de filtros",
    "Import filter customizations" : u"Importar configuraciones de filtros",
    "Select filters to export:" : u"Seleccionar filtros para exportar:",
    "Select filters to import from the file:" : u"Seleccionar filtros para importar desde el fichero:",
    "Overwrite all data" : u"Sobreescribir todos los datos",
    "You must select at least one filter!" : u"¡Debe seleccionarse al menos un filtro!",
    "Error: minValue must be less than maxValue" : u"Error: Valor mínimo debe ser menor que valor máximo",
    "New File" : u"Archivo nuevo",
    "Windows Bitmap" : u"", # New in v2.3.0
    "Animation" : u"", # New in v2.3.0
    "JPEG" : u"", # New in v2.3.0
    "Zsoft Paintbrush" : u"", # New in v2.3.0
    "Portable Network Graphics" : u"", # New in v2.3.0
    "Netpbm" : u"", # New in v2.3.0
    "Tagged Image File" : u"", # New in v2.3.0
    "ASCII Text Array" : u"", # New in v2.3.0
    "Windows Icon" : u"", # New in v2.3.0
    "fps" : u"FPS",
    "Frame" : u"Fotograma",
    "A crash detected at the last running!" : u"¡Un fallo detectado en la última ejecución",
    "&Zoom" : u"&Zoom",
    "%s translation file updated with new messages to translate" : u"", # New in v2.3.0
    "Translation updated" : u"", # New in v2.3.0
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.3.0
    "%s language couldn't be loaded" : u"", # New in v2.3.0
    "Paths" : u"Directorios",
    "AvsP help directory:" : u"Directorio ayuda AvsP:",
    "Location of the AvsP help directory" : u"Localización de la carpeta en la que se encuentran los ficheros de ayuda de AvsP",
    "Avisynth directory:" : u"Directorio AviSynth:",
    "Location of the avisynth installation directory" : u"Localización de la carpeta en la que se encuentra el archivo AviSynth.exe",
    "Avisynth help file/url:" : u"Ayuda AviSynth, archivo/url: ",
    "Location of the avisynth help file or url" : u"Localización ayuda AviSinth (archivo/URL)",
    "External player:" : u"Reproductor externo:",
    "Location of external program for script playback" : u"Localización del archivo .exe del reproductor externo predefinido",
    "Additional arguments when running the external player" : u"Argumentos adicionales para el reproductor externo",
    "External player extra args:" : u"Argumentos para reprod. externo:",
    "Documentation search paths:" : u"Directorio Documentación filtros:",
    "Specify which directories to search for docs when you click on a filter calltip" : u"Localización de los archivos de documentación de los filtros AviSynth",
    "Documentation search url:" : u"URL búsqueda documentación:",
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"Dirección web para búsqueda si la documentación no es encontrada en el directorio (el nombre del filtro reemplaza %filtername%)",
    "Text" : u"Texto",
    "Show filter calltips" : u"Mostrar ventana argumentos función",
    "Turn on/off automatic tips when typing filter names" : u"Activar/desactivar ventana ayuda al teclear los nombres de funciones",
    "Always show calltips any time the cursor is within the filter's arguments" : u"Mostrar ventana ayuda siempre que el cursor este situado en los argumentos de un filtro",
    "Frequent calltips" : u"Mostrar siempre ventana argumentos función",
    "Syntax highlighting" : u"Resaltar sintaxis",
    "Turn on/off avisynth-specific text colors and fonts" : u"Activar/Desactivar la utilización de un específico color y fuente en el texto",
    "Show autocomplete on capital letters" : u"Mostrar lista para autocompletar al teclear Mayusculas",
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"Activar/desactivar lista para autocompletar al teclear palabras que empiecen con letra mayúscula",
    "Amount of letters typed" : u"", # New in v2.3.0
    "Show autocomplete list when typing a certain amount of letters" : u"Mostrar lista de autocompletado, al escribir cierta cantidad de letras",
    "Don't allow lines wider than the window" : u"No permitir líneas más anchas que la ventana",
    "Wrap text" : u"Ajustar texto al ancho de la ventana",
    "Draw lines at fold points" : u"Dibujar líneas en puntos de plegado ",
    "For code folding, draw a line underneath if the fold point is not expanded" : u"Para código plegado, dibuja una línea debajo si el punto de pliegue no se expande",
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Insertar tabulador en lugar de espacios al teclear Tab",
    "Use tabs instead of spaces" : u"Usar tabuladores en lugar de espacios",
    "Set the size of the tabs in spaces" : u" Defina el tamaño de los tabuladores en espacios",
    "Tab width" : u"Anchura tabulador",
    "Initial space to reserve for the line margin in terms of number of digits" : u"Margen inicial para la línea expresado en un numero de espacios",
    "Line margin width" : u"Ancho del margen de línea",
    "Autocomplete" : u"Autocompletar",
    "Add user defined variables into autocomplete list" : u"Añadir variables definidas por el usuario en lista de autocompletado",
    "Show autocomplete with variables" : u"Mostrar autocompletado con variables",
    "Show autocomplete on single matched lowercase variable" : u"Mostrar autocompletado solo en variables escritas en minúscula",
    "When typing a lowercase variable name, show autocomplete if there is only one item matched in keyword list" : u"Al escribir un nombre de variable en minúscula, mostrar autocompletado si hay solo un elemento que coincida en la lista",
    "Add icons into autocomplete list. Using different type to indicate how well a filter's presets is defined" : u"Añadir iconos en la lista de autocompletado. Usando diferentes tipos para indicar cómo están definidos, al igual que los ajustes de los filtros. ",
    "Show autocomplete with icons" : u"Mostrar autocompletar con iconos",
    "Don't show autocomplete when calltip is active" : u"No mostrar autocompletado cuando se activa calltip",
    "When calltip is active, autocomplete will not be activate automatically. You can still show autocomplete manually" : u"Cuando calltip esta activo, el autocompletado no se activará automaticamente. También puedes mostrar manualmente el autocompletado.",
    "Customize autocomplete keyword list..." : u"Personalizar lista de palabras claves del autocompletado...",
    "Customize the keyword list shown in the autocomplete choice box" : u"Personalizar lista de palabras claves a mostrar en la caja de opciones ",
    "Autoparentheses level" : u"Nivel autoparéntesis",
    "Close \"()\"" : u"Cerrar \"()\"", # New in v1.3.2
    "Determines parentheses to insert upon autocompletion" : u"Número de paréntesis a insertar en la opción de autocompletar",
    "None \" \"" : u"Ninguno \" \"", # New in v1.3.2
    "Open \"(\"" : u"Abrir \"(\"", # New in v1.3.2
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"Tecla para incorporar los valores inicales del filtro cuando el cuadro autocompletar este visible",
    "None" : u"Ninguna",
    "Preset activation key" : u"Tecla activación valores iniciales",
    "Return" : u"Enter",
    "Tab" : u"Tabular",
    "Video" : u"Vídeo",
    "Constantly update video while dragging" : u"Previsualización continuada al arrastrar la barra de desplazamiento",
    "Update the video constantly when dragging the frame slider" : u"Actualizar la previsualización del vídeo de forma continuada cuando se arratre la barra de desplazamiento",
    "Enable line-by-line update" : u"Habilitar previsualización línea a línea",
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"Si está marcada esta opción, la previsualización se actualizará cada vez que el cursor cambie de línea",
    "Focus the video preview upon refresh" : u"Focalizar la previsualización de vídeo al actualizarla",
    "Switch focus to the video preview window when using the refresh command" : u"Cambiar la focalización a la ventana del vídeo cuando se use el comando actualizar previsualización",
    "Refresh preview automatically" : u"Actualizar automáticamente la vista previa",
    "Refresh preview when switch focus on video window or change a value in slider window" : u"Actualizar vista previa al cambiar el foco en la ventana de vídeo o cambiar un valor en la ventana deslizante",
    "Seeking to a certain frame will seek to that frame on all tabs" : u"La búsqueda de un cierto fotograma que se realizará en los frames de todas las pestañas ",
    "Shared timeline" : u"Linea de tiempo compartida",
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"Permitir a AvsPmod reescalar y/o mover la ventana del programa cuando se actualice la vista previa del video",
    "Allow AvsPmod to resize the window" : u"Permitir a AvsPmod reescalar la ventana",
    "Separate video preview window" : u"Previsualización en ventana independiente",
    "Use a separate window for the video preview" : u"Abrir ventana independiente para previsualización del vídeo",
    "Min text lines on video preview" : u"Mínimo líneas de texto en modo previsualización",
    "Minimum number of lines to show when displaying the video preview" : u"Mínimo número de líneas de texto que deben mostrarse cuando se active la previsualización del vídeo",
    "Customize the video information shown in the program status bar" : u"Personalización de la información que acerca del vídeo debe mostrarse en la barra de estado",
    "Customize video status bar..." : u"Personalización de la información del vídeo en la barra de estado...",
    "User Sliders" : u"Controles de Ajuste",
    "Hide slider window by default" : u"Ocultar, por defecto, los Controles de Ajuste de filtros",
    "Keep the slider window hidden by default when previewing a video" : u"Ocultar, por defecto, la ventana de Controles de Ajuste de filtros en la previsualización del vídeo",
    "Create user sliders automatically" : u"Crear automáticamente Controles de Ajuste de Filtros",
    "Create user sliders automatically using the filter database" : u"Crear automáticamente Controles de Ajuste a partir de la base de datos de filtros",
    "Create user sliders for int and float arguments" : u"Crear barras de desplazamiento para argumentos numéricos (enteros y decimales)",
    "type int/float (numerical slider)" : u"Tipo numérico (entero/decimal)",
    "Create color pickers for hex color arguments" : u"Crear entrada para argumentos de color",
    "type int (hex color)" : u"Tipo entero (Hex color) ",
    "Create radio boxes for bool arguments" : u"Crear botones para argumentos booleanos",
    "type bool" : u"Tipo booleano",
    "Create listboxes for string list arguments" : u"Crear entrada para argumentos de texto",
    "type string (list)" : u"Tipo texto (lista)",
    "Create filename pickers for string filename arguments" : u"Crear entrada para argumentos de nombres de ficheros",
    "type string (filename)" : u"Tipo texto (nombre de fichero)",
    "Create placeholders for arguments which have no database information" : u"Crear entrada para argumentos no documentados",
    "undocumented" : u"No documentados",
    "Determines which filters will initially have hidden arguments in the slider window" : u"Determina que filtros tendrán plegados inicialmente sus argumentos en la ventana de Controles de Ajuste",
    "Fold all" : u"Plegar todos",
    "Fold non-numbers" : u"Plegar los no numéricos",
    "Fold none" : u"Desplegar todos",
    "Fold startup setting" : u"Especificaciones de presentación",
    "Filter exclusion list:" : u"Lista de exclusión de filtros:",
    "Specify filters never to build automatic sliders for" : u"Especificar los filtros para los que no deben crearse nunca automáticamente Controles de Ajuste",
    "Save/Load" : u"Guardar/Cargar",
    "Automatically save the session on shutdown and load on next startup" : u"Guardar la sesión automáticamente al salir y abrirla en el próximo arranque del progrma.",
    "Save session for next launch" : u"Guardar la sesión para el próximo arranque del programa",
    "Always load startup session" : u"Abrir siempre la sesión autoguardada",
    "Always load the auto-saved session before opening any other file on startup" : u"Al arrancar, abrir siempre la sesión autoguardada antes que ningún otro archivo",
    "Always hide the video preview window when loading a session" : u"Ocultar siempre la vista previa del video al iniciar una sesión",
    "Don't preview when loading a session" : u"No mostrar vista previa al iniciar una sesión",
    "Backup session periodically (minutes)" : u"", # New in v2.3.0
    "Backup the session every X minutes, if X > 0" : u"", # New in v2.3.0
    "Backup session when previewing" : u"Copia de la sesión al previsualizar",
    "If checked, the current session is backed up prior to previewing any new script" : u"Si está marcada esta opción, se efectúa backup de la sesión actual antes de previsualizar cualquier nuevo script",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"Preguntar si ha de guardarse el script antes de ejecutar el reproductor externo (inactivo si está marcado 'ejecutar sin guardar los cambios')",
    "Prompt to save when previewing" : u"Preguntar si se guardan los cambios antes de ejecutar el reproductor externo",
    "Create a temporary preview script with unsaved changes when previewing the video" : u" Se creará el archivo 'preview.avs' con los cambios no guardados para la ejecución del reproductor externo",
    "Preview scripts with unsaved changes" : u"Vista previa de los scripts con cambios sin guardar",
    "Don't prompt to save scripts without file" : u"", # New in v2.3.0
    "When closing a tab, don't prompt to save the script if it doesn't already exist on the filesystem" : u"", # New in v2.3.0
    "Prompt to save each script with unsaved changes when exiting the program" : u"Preguntar sobre guardar cada script no guardado previamente al salir del programa",
    "Prompt to save scripts on program exit" : u"Preguntar sobre guardar scripts al salir del programa",
    "Save *.avs scripts with AvsPmod markings" : u"Guardar los *.avs scripts con las marcas de AvsPmod",
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"Guardar marcas especificas de AvsPmod (control de usuario, etiquetas, etc) como una sección comentada en el archivo *.avs",
    "Misc" : u"Miscelánea",
    "Choose the language used for the interface" : u"", # New in v2.3.0
    "Language *" : u"", # New in v2.3.0
    "Show keyboard images in the script tabs when video has focus" : u"Mostrar las teclas de acceso rápido en las pestañas cuando se focalice el vídeo",
    "Use keyboard images in tabs" : u"Mostrar teclas acceso rápido en las pestañas",
    "Show tabs in multiline style" : u"Mostrar tabulaciones en múltiples estilos",
    "There can be several rows of tabs" : u"Puede haber varias filas de pestañas",
    "All tabs will have same width" : u"Todas las pestañas tendrán el mismo ancho",
    "Show tabs in fixed width" : u"Mostrar pestañas con ancho fijo",
    "Enable scroll wheel through similar tabs" : u"Activar la rueda de desplazamiento a través de pestañas similares",
    "Mouse scroll wheel cycles through tabs with similar videos" : u"Habilitar la rueda del ratón para moverse a través de las pestañas que contengan videos similares",
    "Only allow a single instance of AvsPmod" : u"Permitir una única instancia de AvsPmod",
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"Mostrar advertencia al inicio si hay dlls con un mal nombre en la carpeta de plugins",
    "Show warning for bad plugin naming at startup" : u"Mostrar advertencia al inicio, por un mal nombre de un plugin",
    "Max number of recent filenames" : u"Número máximo de archivos recientes",
    "This number determines how many filenames to store in the recent files menu" : u"Este número determina cuantos archivos se almacenan en el menu 'Archivos Recientes'", # New in v1.2.1
    "Custom jump size:" : u"Valor del salto predefinido en la previsualización:",
    "Jump size used in video menu" : u"Valor del salto (avance/retroceso en la previsualización) predefinido usado en el menu \"vídeo\"", # New in v1.3.3
    "Custom jump size units" : u"Unidad en la que se expresa el salto predefinido",
    "Units of custom jump size" : u"Unidad en la que se expresa el salto predefinido (avance/retroceso en la previsualización)",
    "hours" : u"Horas",
    "minutes" : u"Minutos",
    "seconds" : u"Segundos",
    "frames" : u"Fotogramas",
    "Extend selection to line down position" : u"Ampliar la selección a la línea inferior",
    "Scroll down" : u"Desplazarse hacia abajo",
    "Extend rectangular selection to line down position" : u"Ampliar selección rectángular a la linea inferior",
    "Extend selection to line up position" : u"Ampliar selección a la línea superior",
    "Scroll up" : u"Desplazarse hacia arriba",
    "Extend rectangular selection to line up position" : u"Ampliar selección rectángular a la linea superior",
    "Go to previous paragraph" : u"Ir al párrafo anterior",
    "Extend selection to previous paragraph" : u"Ampliar selección al párrafo anterior",
    "Go to next paragraph" : u"Ir al siguiente párrafo",
    "Extend selection to next paragraph" : u"Ampliar selección al siguiente párrafo",
    "Extend selection to previous character" : u"Ampliar selección al carácter previo",
    "Go to previous word" : u"Ir a la palabra anterior",
    "Extend selection to previous word" : u"Ampliar selección a la palabra anterior",
    "Extend rectangular selection to previous character" : u"Ampliar selección rectángular a la linea superior al carácter anterior",
    "Extend selection to next character" : u"Ampliar selección al siguiente carácter",
    "Go to next word" : u"Ir a la siguiente palabra",
    "Extend selection to next word" : u"Ampliar selección a la siguiente palabra",
    "Extend rectangular selection to next character" : u"Ampliar selección rectángular al siguiente carácter",
    "Go to previous word part" : u"Ir a la parte anterior a la palabra",
    "Extend selection to previous word part" : u"Ampliar selección a la parte previa de la palabra",
    "Go to next word part" : u"Ir a la siguiente parte de la palabra",
    "Extend selection to next word part" : u"Ampliar selección a la siguiente parte de la palabra",
    "Extend selection to start of line" : u"Ampliar selección al inicio de la línea",
    "Go to start of document" : u"Ir al inicio del documento",
    "Extend selection to start of document" : u"Ampliar selección al inicio del documento",
    "Go to start of line" : u"Ir al inicio de la línea",
    "Extend selection to end of line" : u"Ampliar selección al final de la línea",
    "Go to end of document" : u"Ir al final del documento",
    "Extend selection to end of document" : u"Ampliar selección al final del documento",
    "Go to end of line" : u"Ir al final de la línea",
    "Extend selection to previous page" : u"Ampliar selección a la página anterior",
    "Extend rectangular selection to previous page" : u"Ampliar selección rectángular a la página anterior",
    "Extend selection to next page" : u"Ampliar selección a la siguiente página",
    "Extend rectangular selection to next page" : u"Ampliar selección rectángular a la siguiente página",
    "Delete to end of word" : u"Borrar hasta el final de la palabra",
    "Delete to end of line" : u"Borrar hasta el final de la línea",
    "Delete back" : u"Volver a borrar",
    "Delete to start of word" : u"Borrar hasta el inicio de la palabra",
    "Delete to start of line" : u"Borrar hasta el final de la línea",
    "Cancel autocomplete or calltip" : u"Cancelar autocomplar o calltip",
    "Indent selection" : u"Indentar línea(s) seleccionada(s)",
    "Unindent selection" : u"Desindentar línea(s) seleccionada(s)",
    "Newline" : u"Nueva línea",
    "Zoom in" : u"Acercar",
    "Zoom out" : u"Alejar",
    "Reset zoom level to normal" : u"Ajustar zoom al nivel normal",
    "Line cut" : u"Cortar línea",
    "Line delete" : u"Borrar línea",
    "Line copy" : u"Copiar línea",
    "Transpose line with the previous" : u"Transposición de la línea con la anterior",
    "Line or selection duplicate" : u"Duplicar línea o selección",
    "Convert selection to lowercase" : u"Convertir selección a minúsculas",
    "Convert selection to uppercase" : u"Convertir selección a mayúsculas",
    "Sort bookmarks ascending" : u"Marcadores de orden ascendente",
    "sort ascending" : u"orden ascendente",
    "Show bookmarks with timecode" : u"Mostrar marcadores con código de tiempo",
    "show time" : u"mostrar tiempo",
    "Show bookmarks with title" : u"Mostrar marcadores con título",
    "show title" : u"mostrar título",
    "Resolution-based" : u"", # New in v2.3.0
    "BT.709" : u"", # New in v2.3.0
    "BT.601" : u"", # New in v2.3.0
    "TV levels" : u"", # New in v2.3.0
    "PC levels" : u"", # New in v2.3.0
    "Progressive" : u"Progresivo",
    "Interlaced" : u"Entrelazado",
    "Swap UV" : u"Intercambio UV",
    "25%" : u"25%",
    "50%" : u"50%",
    "100% (normal)" : u"100% (normal)",
    "200%" : u"200%",
    "300%" : u"300%",
    "400%" : u"400%",
    "Fill window" : u"Ocupar toda la ventana",
    "Fit inside window" : u"Ajustar dentro de la ventana",
    "Vertically" : u"Verticalmente",
    "Horizontally" : u"Horizontalmente",
    "&File" : u"&Archivo",
    "Create a new tab" : u"Abrir una nueva pestaña",
    "New tab" : u"Nueva pestaña",
    "Open an existing script" : u"Abrir un script o fichero fuente existente",
    "Open..." : u"Abrir...",
    "Close tab" : u"Cerrar pestaña",
    "Close the current tab" : u"Cerrar la pestaña activa",
    "Close all tabs" : u"Cerrar todas las pestañas",
    "Close every tab" : u"Cerrar todas las pestañas existentes",
    "Rename tab" : u"Renombra pestaña",
    "Rename the current tab. If script file is existing, also rename it" : u"Renombrar la actual pestaña. Si el archio de script existe, renombralo también",
    "Save the current script" : u"Guardar el scrip activo",
    "Choose where to save the current script" : u"Elegir donde y con que nombre guardar el scrip activo",
    "Save script as..." : u"Guardar script como...",
    "Load a session into the tabs" : u"Abrir una sesión,previamente guardada, con todos sus scripts, Controles de Ajuste de filtros, etiquetas AvsP. etc.",
    "Load session..." : u"Abrir sesión...",
    "Save all the scripts as a session, including slider info" : u"Guardar todos los scripts como una sesión. incluyendo Controles de Ajuste de Filtros, etiquetas AvsP, etc.",
    "Save session..." : u"Guardar sesión como...",
    "Backup current session" : u"Hacer backup de la sesión actual",
    "Backup the current session for next program run" : u"Hacer backup de la sesión actual para la próxima vez que se ejecute AvsP",
    "Next tab" : u"Pestaña siguiente",
    "Switch to next script tab" : u"Pasar a la pestaña siguiente",
    "Previous tab" : u"Pestaña anterior",
    "Switch to previous script tab" : u"Pasar a la pestaña anterior",
    "Show the scrap window" : u"Mostrar Ventana para notas",
    "&Exit" : u"&Salir",
    "Exit the program" : u"Cerrar la aplicación",
    "&Edit" : u"&Edición",
    "Undo last text operation" : u"Deshacer el último cambio efectuado en el texto",
    "Redo last text operation" : u"Rehacer el último cambio deshecho",
    "Cut the selected text" : u"Cortar el texto seleccionado",
    "Copy the selected text" : u"Copiar el texto seleccionado",
    "Paste the selected text" : u"Pegar el texto seleccionado",
    "Find..." : u"Buscar...",
    "Open a find text dialog box" : u"Abrir cuadro de diálogo para la búsqueda de una(s) palabra(s)",
    "Find next" : u"Buscar siguiente",
    "Find the next instance of given text" : u"Buscar la siguiente ocurrencia de una(s) palabra(s)",
    "Open a replace text dialog box" : u"Abrir cuadro de diálogo para reemplazar una(s) palabra(s)",
    "Replace..." : u"Reemplazar...",
    "Select All" : u"Seleccionar todo",
    "Select all the text" : u"Seleccionar todo el texto del script",
    "&Insert" : u"&Insertar",
    "Choose a source file to insert into the text" : u"Elegir un archivo de vídeo, audio, imagen o script para insertarlo en el texto",
    "Insert source..." : u"Insertar vídeo, imagen, audio o script...",
    "Get a filename from a dialog box to insert into the text" : u"Elegir el nombre de un archivo para insertarlo, junto con su ruta, en el texto",
    "Insert filename..." : u"Insertar ruta y nombre de archivo...",
    "Choose a plugin dll to insert into the text" : u"Elegir un plugin .dll para insertarlo en el texto",
    "Insert plugin..." : u"Invocar plugin...",
    "Insert a user-scripted slider into the text" : u"Insertar en el texto las variables de un parámetro para crear un Control de Ajuste de Filtro",
    "Insert user slider..." : u"Crear Control de Ajuste de Filtro...",
    "Insert a tag which indicates a separator in the user slider window" : u"Insertar una etiqueta para crear un separador entre Controles de Ajuste de Filtros",
    "Insert user slider separator" : u"Insertar separador de Controles de Ajuste...",
    "Insert the current frame number into the text" : u"Insertar el número del fotograma activo en el texto",
    "Add tags surrounding the selected text for toggling with the video preview" : u"Añadir etiquetas para que el texto seleccionado pueda ser activado/desactivado en la ventana de previsualización del vídeo",
    "Tag selection for toggling" : u"Insertar etiquetas sección activable/desactivable...",
    "Clear all tags" : u"Borrar etiquetas secciones activables/desactivables",
    "Clear all toggle tags from the text" : u"Borrar todas las etiquetas de secciones activables/desactivables",
    "Indent the selected lines" : u"Desplazar la(s) línea(s) selecionadas a la derecha (4 espacios)",
    "Unindent the selected lines" : u"Desplazar la(s) línea(s) seleccionada(s) a la izquierda -solo en línea(s) indentada(s)-",
    "Block comment" : u"Insertar/Eliminar signo de comentario (#)",
    "Comment or uncomment selected lines" : u"Insertar/eliminar el signo de comentario (#) en la línea o líneas seleccionadas",
    "Comment at start of a text style or uncomment" : u"Comentar en el inicio de un estilo de texto o descomentar",
    "Style comment" : u"Estilo del comentario",
    "Toggle current fold" : u"Activar el pliegue actual",
    "Toggle the fold point On/OFF at the current line" : u"Activar el punto de pliege On/Off de la línea actual",
    "Toggle all fold points On/OFF" : u"Activar todos los puntos de pligue On/Off",
    "Toggle all folds" : u"Desplegar todo",
    "&AviSynth function" : u"Funciones &AviSynth",
    "Show list of filternames matching the partial text at the cursor" : u"Mostrar lista de filtros cuyo nombre coincida parcialmente con el texto seleccionado",
    "Autocomplete all" : u"Autocompletar todo",
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"Haga caso omiso de configuración del usuario, mostrar la lista completa de nombres de filtros coinciden con el texto parcial en el cursor",
    "Show calltip" : u"Motrar argumentos",
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"Mostrar los argumentos del filtro (Solo funciona si el cursor esta posicionado en la zona de argumentos)",
    "Show function definition" : u"Editar información función",
    "Show the AviSynth function definition dialog for the filter" : u"Mostrar cuadro de diálogo de edición de la información de la función existente en la base de datos",
    "Filter help file" : u"Mostrar archivo ayuda",
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"Abrir archivo ayuda para el filtro (Solo funciona si el cursor está en zona de los argumentos o si el nombre esta resaltado)",
    "&Miscellaneous" : u"&Misceláneas",
    "Move line up" : u"Mover línea(s) arriba",
    "Move the current line or selection up by one line" : u"Mover la(s) línea(s) activa(s) o seleccionada(s) una posición hacia arriba",
    "Move line down" : u"Mover línea(s) abajo",
    "Move the current line or selection down by one line" : u"Mover la(s) línea(s) activa(s) o seleccionada(s) una posición hacia abajo",
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"Copiar el script activo sin marcas AvsP (Controles de Ajuste y etiquetas) en el portapapeles",
    "Copy unmarked script to clipboard" : u"Copiar script sin marcas AvsP en el portapapeles",
    "Copy avisynth error to clipboard" : u"Copiar errro de avisynth al portapapeles",
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"Copiar el mensaje de error mostrado de avisynth en la ventana de vista previa en el portapapeles",
    "&Video" : u"&Vídeo",
    "Add/Remove bookmark" : u"Añadi/Borrar marcador",
    "Mark the current frame on the frame slider" : u"Marcar el fotograma actual en la barra de desplazamiento del vídeo",
    "Clear all bookmarks" : u"Borrar todos los marcadores",
    "Titled &bookmarks" : u"&Marcadores titulados",
    "Move the nearest titled bookmark to the current position. A historic title will be restored if it matches the condition." : u"Mover al marcador titulado mas cercano a la posición actual. Un titulo historico será restaurado si coincide al condición.",
    "Move titled bookmark" : u"Mover marcador titulado",
    "Restore all historic titles" : u"Restaurar todos los titulos historicos",
    "Restore historic titles" : u"Restaurar titulos históricos",
    "Clear all historic titles" : u"Limpiar todos los títulos históricos",
    "Clear historic titles" : u"Limpiar títulos históricos",
    "Generate titles for untitled bookmarks by the pattern - 'Chapter %02d'" : u"Generar títulos para marcadores sin nombrar mediante el patrón - 'Chapter %02d'", # New in v2.2.0.1215
    "Set title (auto)" : u"Establecer título (auto)",
    "Edit title for bookmarks in a list table" : u"Editar título para marcadores en una lista de tablas ",
    "Set title (manual)" : u"Establecer título (manual)",
    "&Navigate" : u"&Navegar",
    "Go to &bookmark" : u"Ir al &Marcador",
    "Go to next bookmarked frame" : u"Ir al siguiente fotograma marcado",
    "Next bookmark" : u"Marcador siguiente",
    "Go to previous bookmarked frame" : u"Ir al anterior fotograma marcado",
    "Previous bookmark" : u"Marcador previo",
    "Forward 1 frame" : u"Avanzar un fotograma",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"Mostrar el siguiente fotograma (acceso rápido solo con previsualización focalizada)",
    "Backward 1 frame" : u"Retroceder un fotograma",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"Mostrar el fotograma anterior (acceso rápido solo con previsualizaciòn focalizada)",
    "Forward 1 second" : u"Avanzar 1 segundo",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"Avanzar 1 segundo la barra desplazamiento y mostrar fotograma correspondiente (acceso rápido solo con previsualización focalizada)",
    "Backward 1 second" : u"Retroceder 1 segundo",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"Retrceder 1 segundo la barra desplazamiento y mostrar fotograma correspondiente (acceso rápido solo con previsualización focalizada)",
    "Forward 1 minute" : u"Avanzar 1 minuto",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"Avanzar 1 minuto la barra desplazamiento y mostrar fotograma correspondiente (acceso rápido solo con previsualización focalizada)",
    "Backward 1 minute" : u"Retroceder 1 minuto",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"Retrceder 1 minuto la barra desplazamiento y mostrar fotograma correspondiente (acceso rápido solo con previsualización focalizada)",
    "Forward x units" : u"Avanzar salto predefinido",
    "Jump forward by x units (you can specify x in the options dialog)" : u"Salto predefinido hacia adelante en la barra de desplazamiento (especificado en Opciones->Parámetros del programa->vídeo)",
    "Backwards x units" : u"Retroceder salto predefinido",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"Salto predefinido hacia atrás en la barra de desplazamiento (especificado en Opciones->Parámetros del programa->vídeo)",
    "Go to first frame" : u"Ir al primer fotograma",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"Ir al primer fotograma (acceso rapido solo con previsualización focalizada)",
    "Go to last frame" : u"Ir al último fotograma ",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"Ir al último fotograma (acceso rapido solo con previsualización focalizada)",
    "Go to last scrolled frame" : u"Volver a la posición anterior en la barra de desplazamiento",
    "Last scrolled frame" : u"Anterior posición",
    "Enter a video frame or time to jump to" : u"Saltar a un fotograma o espacio temporal concreto",
    "Go to frame..." : u"Ir al fotograma...",
    "Crop editor..." : u"Recortar...",
    "Show the crop editor dialog" : u"Mostrar cuadro de diálogo para recortar el ancho y/o alto del vídeo",
    "&Trim selection editor" : u"Edi&tor de selección de ajuste",
    "Show the trim selection editor dialog" : u"Mostrar cuadro de diálogo para seleccionar los fotogramas que se deseen suprimir o conservar",
    "Show trim selection editor" : u"Mostrar cuadro de diálogo para selección de puntos de corte",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"Marcar el inicio de la selección (Se abre el cuadro de diálogo para selección de cortes si no esta visible)",
    "Set selection startpoint" : u"Marcar el inicio de la selección",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"Marcar el final de la selección (Se abre el cuadro de diálogo para selección de cortes si no esta visible)",
    "Set selection endpoint" : u"Marcar el final de la selección",
    "Zoom video preview to 25%" : u"Previsualizar el vídeo al 25% de su tamaño",
    "Zoom video preview to 50%" : u"Previsualizar el vídeo a la mitad de su tamaño",
    "Zoom video preview to 100% (normal)" : u"Previsualizar el vídeo en su formato real",
    "Zoom video preview to 200%" : u"Previsualizar el vídeo al doble de su tamaño",
    "Zoom video preview to 300%" : u"Previsualizar el vídeo al 300% de su tamaño",
    "Zoom video preview to 400%" : u"Previsualizar el vídeo al 400% de su tamaño",
    "Zoom video preview to fill the entire window" : u"Ajustar la previsualización del vídeo hasta ocupar toda la ventana",
    "Zoom video preview to fit inside the window" : u"Ajustar la previsualización del vídeo dentro de la ventana",
    "Enlarge preview image to next zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"Ampliar imagen de la vista previa hasta el siguiente nivel de zoom. No funciona 'ventana completa' o 'encajada'", # New in v2.2.0.1215
    "Shrink preview image to previous zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"Reducir imagen de la vista previa al anterior nivel de zoom. No funciona 'ventana completa' o 'encajada'", # New in v2.2.0.1215
    "&Flip" : u"Voltear",
    "Flip video preview upside down" : u"Vista previa del video, al revés",
    "Flip video preview from left to right" : u"Vista previa del video invertido verticalmente",
    "&YUV -> RGB" : u"", # New in v2.2.0.1215
    "Swap chroma channels (U and V)" : u"Intercambiar canales del croma (U y V)",
    "Use BT.709 coefficients for HD, BT.601 for SD (default)" : u"", # New in v2.3.0
    "Use BT.709 coefficients" : u"", # New in v2.3.0
    "Use BT.601 coefficients" : u"", # New in v2.3.0
    "Use limited range (default)" : u"", # New in v2.3.0
    "Use full range" : u"", # New in v2.3.0
    "For YV12 only, assume it is progressive (default)" : u"Sólo para YV12, asume que es progresivo",
    "For YV12 only, assume it is interlaced" : u"Sólo para YV12, asume que es entrelazado",
    "Save image as..." : u"Guardar imagen como...",
    "Save the current frame as a bitmap" : u"Guardar el fotograma actual como... (.bmp/.jpg/.pcx/.png)",
    "Force the script to reload and refresh the video frame" : u"Forzar la ejecución del scrip para actualizar la previsualización del fotograma actual",
    "Refresh preview" : u"Actualizar previsualización",
    "Show/Hide the preview" : u"Mostrar/Ocultar la vista previa",
    "Toggle the video preview" : u"Mostrar/ocultar previsualización",
    "Release all open videos from memory" : u"Liberar de la memoria todos los vídeos abiertos",
    "Release all videos from memory" : u"Liberar todos los vídeos de la memoria",
    "Switch focus between the video preview and the text editor" : u"Alternar la focalización entre la previsualización del vídeo y la edición del texto",
    "Switch video/text focus" : u"Focalizar vídeo/texto",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"Mostrar/ocultar sección de Controles de Ajuste fr Filtros (el mismo efecto se tiene con doble-click en la división)",
    "Toggle the slider sidebar" : u"Mostrar/ocultar sección Controles de Ajuste de Filtros",
    "Request every video frame once (analysis pass for two-pass filters)" : u"", # New in v2.3.0
    "Run analysis pass" : u"", # New in v2.3.0
    "External player" : u"Reproductor externo",
    "Play the current script in an external program" : u"Reproducir el scrip activo con el programa externo definido en Opciones-Parámetros del programa",
    "Show information about the video in a dialog box" : u"Mostrar la información acerca del clip (vídeo y audio) en un cuadro de díálogo",
    "Video information" : u"Información del clip (Vídeo y Audio)",
    "&Options" : u"&Opciones",
    "Always on top" : u"Siempre al frente",
    "Keep this window always on top of others" : u"Mantener esta ventana siempre al frente de las demás",
    "Disable video preview" : u"Deshabilitar previsualización vídeo",
    "If checked, the video preview will not be shown under any circumstances" : u"Si está marcada esta opción, el vídeo no se previsualizará bajo ninguna circunstancia",
    "Associate .avs files with AvsP" : u"Asociar archivos .avs con AvsP",
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"Configurar el ordenador para que los archivos .avs sean abiertos por AvsP",
    "AviSynth function definition..." : u"Información funciones AviSynth...",
    "Edit the various AviSynth script fonts and colors" : u"Editar fuentes y colores usados en el script AviSynth",
    "Fonts and colors..." : u"Fuentes y colores...",
    "Edit the extension-based templates for inserting sources" : u"Editar las extensiones de ficheros predefinidas para añadir ficheros de vídeo, etc.",
    "Extension templates..." : u"Extensiones predefinidas...",
    "Configure the program keyboard shortcuts" : u"Configurar las teclas de acceso rápido para uso en este programa",
    "Keyboard shortcuts..." : u"Atajos de teclado...",
    "Configure program settings" : u"Configuarar los parámetros de este programa",
    "Program settings..." : u"Parámetros del programa...",
    "&Help" : u"&Ayuda",
    "Animated tutorial" : u"Tutorial animado",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"Ver un tutorial animado (desde la página web de AVsP)",
    "Learn more about AvsP text features (from the AvsP website)" : u"Aprenda más acerca de las opciones de edición de texto (desde la página web de AvsP)",
    "Text features" : u"Texto. Opciones edición",
    "Learn more about AvsP video features (from the AvsP website)" : u"Aprenda más acerca de las opciones de previsualización de vídeo (desde la página web de AvsP)",
    "Video features" : u"vídeo. Opciones de previsualización",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"Aprenda más acerca de los Controles de Ajuste de Filtros (desde la página web de AvsP)",
    "User sliders" : u"Controles de Ajuste de Filtros",
    "Learn more about AvsP macros (from the AvsP website)" : u"Aprenda más acerca de las macros de AvsP (desde la página web de AvsP)",
    "Macros" : u"",
    "Avisynth help" : u"Ayuda de AviSynth",
    "Open the avisynth help html" : u"Abrir archivo .html de ayuda para AviSynth",
    "Open Avisynth plugins folder" : u"Abrir carpeta de plugins de Avisynth",
    "Open the avisynth plugins folder" : u"Abrir la carpeta de plugins de Avisynth",
    "About this program" : u"Acerca de este programa",
    "About AvsPmod" : u"Sobre AvsPmod",
    "Previous frame" : u"Fotograma anterior",
    "Next frame" : u"Fotograma siguiente",
    "Run the script with an external program" : u"Ejecutar el script activo con el programa externo predefinido en Opciones-Parámetros del programa",
    "Run the selected tool" : u"Ejecutar la herramienta seleccionada",
    "&Tools" : u"&Herramientas",
    "A macro check item" : u"", # New in v2.3.0
    "A macro radio item" : u"", # New in v2.3.0
    "Run selected macro" : u"Ejecutar la Macro seleccionada",
    "View the readme for making macros" : u"Abrir el archivo Leeme.txt sobre como crear Macros",
    "Open macros folder" : u"", # New in v2.3.0
    "Open the macros folder" : u"Abrir carpeta de macros",
    "&Macros" : u"&Macros",
    "Close" : u"Cerrar",
    "Rename" : u"Renombrar",
    "Save" : u"Guardar",
    "Save as..." : u"Guardar como...",
    "Copy to new tab" : u"Copiar en una nueva pestaña",
    "Reposition to" : u"Reposicionar a",
    "Crop editor" : u"Recortar",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"Cuando este cuadro de diálogo está abierto, puede recortarse, la anchura o altura del vídeo, pulsando y arrastrando con el botón izquierdo del ratón sobre la previsualización",
    "At script end" : u"Al final del script",
    "At script cursor" : u"En la posición del cursor",
    "Copy to clipboard" : u"Copiar al portapapeles",
    "Insert Crop() command:" : u"Insertar comando Crop():",
    "Apply" : u"Aplicar",
    "Trim editor" : u"Troceado",
    "Selection options" : u"Opciones",
    "Keep selected regions" : u"Conservar los fotogramas seleccionados",
    "Keep unselected regions" : u"Conservar los fotogramas no seleccionados",
    "Mark video frames inside/outside selection" : u"Visualizar marca en los fotogramas dentro/fuera de la selección",
    "Use Dissolve() with overlap frames:" : u"Usar Dissolve() con fotogramas solapados:",
    "Insert Trim() commands:" : u"Insertar comando(s) Trim():",
    "Insert Dissolve() commands:" : u"Insertar comando(s) Dissolve()",
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"Usar los botones que aparecen junto al arrastre de la barra de desplazamiento del vídeo para efectuar la selección",
    "File does not exist!" : u"¡El archivo no existe!",
    "Select a file" : u"Seleccionar un archivo",
    "Create a separator label" : u"Separador de controles de ajuste de filtros",
    "Enter separator label" : u"Teclear el nombre del separador:",
    "Enter tag name:" : u"Teclear el nombre de la etiqueta:",
    "Tag definition" : u"Etiqueta sección activable/desacivable",
    "Chapter" : u"Capítulo",
    "Set title for bookmarks" : u"Establecer título para marcadores",
    "Title" : u"Título",
    "Frame No." : u"Fotograma No.",
    "Time **" : u"Tiempo **",
    "Left-click on a selected item or double-click to edit.\n\n*  RED - a historic title, not a real bookmark.\n** Time may be unavailable or incorrect before preview refreshed." : u"", # New in v2.3.0
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"No puede usar editor de recorte (crop) a menos que el zoom esté al 100% y no volteado ",
    "Error loading the script" : u"Error abriendo el script",
    "Starting analysis pass..." : u"", # New in v2.3.0
    "Frame size:" : u"Dimensiones fotograma:",
    "Length:" : u"Tamaño:",
    "Frame rate:" : u"Velocidad fotogramas:",
    "Colorspace:" : u"Espacio de color:",
    "Field or frame based:" : u"Escaneado (Field or frame based):",
    "Parity:" : u"Paridad:",
    "Audio" : u"Audio",
    "Channels:" : u"Canales:",
    "Hz" : u"", # New in v1.3.8
    "Sampling rate:" : u"Frecuencia:",
    "Sample type:" : u"Resolución:",
    "bits" : u"", # New in v1.3.8
    "samples" : u"Ciclos",
    "Could not find the macros folder!" : u"¡No se ha podido encontrar la carpeta de las macros!",
    "Could not find %(readme)s!" : u"¡No se pudo encontrar %(readme)s!",
    "Failed to import the selected tool" : u"Fallo al importar la herramienta seleccionada",
    "You must restart for changes to take effect!" : u"¡Debe reiniciarse el programa para que los cambios tengan efecto!",
    "Basic" : u"Básico",
    "Default:" : u"Por defecto:",
    "Comment:" : u"Comentarios:",
    "Block Comment:" : u"Comentar bloque:",
    "__END__ Comment:" : u"Comentar __END__ :",
    "Number:" : u"Números:",
    "Operator:" : u"Operadores:",
    "String:" : u"Cadenas:",
    "Triple-quoted string:" : u"Cadenas tres veces entrecomilladas:",
    "Internal filter:" : u"Filtros internos:",
    "External filter:" : u"Filtros externos:",
    "Internal function:" : u"Funciones internas:",
    "User defined function:" : u"Funciones definidas por el usuario:",
    "Clip property:" : u"Propiedades del clip:",
    "AviSynth keyword:" : u"Palabras clave de AviSynth:",
    "AviSynth data type:" : u"Tipos de datos de AviSynth:",
    "AvsP user slider:" : u"Controles de ajuste de AvsP:",
    "Monospaced font:" : u"Fuente monoespacio:",
    "Advanced" : u"Avanzado",
    "Incomplete string:" : u"Cadenas incompletas:",
    "Syntax highlight strings which are not completed in a single line differently" : u"Resaltar cadenas de texto incompletas al pasar el cursor a otra línea",
    "Brace highlight:" : u"Paréntesis y corchetes resaltados:",
    "Bad brace:" : u"Paréntesis y corchetes sin cerrar:",
    "Bad number:" : u"Números erróneos:",
    "Margin line numbers:" : u"Margen de números de línea:",
    "Miscellaneous word:" : u"Miscelaneos:",
    "Calltip:" : u"Ayuda argumentos función:",
    "Calltip highlight:" : u"Ayuda argumentos función resaltada:",
    "Cursor:" : u"", # New in v2.0.0
    "Selection highlight:" : u"Selección resaltada:",
    "Current line highlight:" : u"Actual línea resaltada:",
    "Highlight the line that the caret is currently in" : u"Resaltar la línea en la que está posicionado el cursor",
    "Fold margin:" : u"Pliegue del margen:",
    "Scrap window" : u"Desechar ventana",
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"Anular todas las fuentes a utilizar si una fuente monoespacio es especificada (sin efecto en la ventana de desechos)",
    "Use monspaced font" : u"Usar fuentes monoespacio",
    "Insert aborted:" : u"No se pudo añadir:",
    "No dot required in file extension!" : u"¡La extensión debe teclearse sin punto!",
    "Edit extension-based templates" : u"Edición de valores predefinidos para extensiones de archivos",
    "File extension" : u"Extensión del archivo",
    "Template" : u"Valor predefinido",
    "This info is used for inserting sources based on file extensions." : u"Esta información se utiliza para añadir archivos en base a su extensión",
    "Any instances of *** in the template are replaced with the filename." : u"Los tres asteriscos serán reemplazados por la ruta y nombre del archivo",
    "(If you want relative paths instead of the full filename, use [***].)" : u"(Si desea rutas relativas en lugar del nombre completo, use [***].)",
    "Associating .avs files will write to the windows registry." : u"Asociar los archivos .avs supondrá una nueva entrada en el registro de Windows",
    "Do you wish to continue?" : u"¿Desea continuar?",
    "Above keys are built-in editing shortcuts. If item is checked,\nit will not be overrided by a menu shortcut in script window." : u"", # New in v2.3.0
    "* This shortcut is active only when video window has focus.\n~ This shortcut is active only when script window has focus." : u"", # New in v2.3.0
    "Could not find the Avisynth plugins folder!" : u"¡No se ha podido encontrar la carpeta de plugins de Avisynth!",
    "AvsPmod version %(version)s " : u"Versión de AvsPmod  %(version)s ",
    "An AviSynth script editor" : u"Un editor de scripts AviSynth",
    "AvsP Website" : u"AvsP Website",
    "Active thread on Doom9's forum" : u"Activar hilo en foro Doom9",
    "This program is freeware under the GPL license." : u"Este programa se distribuye gratuitamente bajo Licencia General Pública",
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"Introduzca un número de fotograma o tiempo (hr: min: sec) y pulsa Enter. Haga clic derecho para recuperar la historia.",
    "copy as time" : u"copiar con tiempo",
    "copy" : u"copiar",
    "paste" : u"pegar",
    "clear history" : u"limpiar historia",
    "Cannot switch tabs while crop editor is open!" : u"¡No puede cambiarse de pestaña con la ventana Recortar abierta!",
    "Cannot switch tabs while trim editor is open!" : u"¡No puede cambiarse de pestaña mientras esté abierta la ventana Trocear!",
    "Invalid crop values detected.  Continue?" : u"Valores para recortar no válidos. ¿Continuar? ",
    "You must create at least one frame selection first!" : u"¡Debe efectuarse al menos una selección de fotogramas!",
    "Select autocomplete keywords" : u"Seleccionar palabras claves el autocompletado",
    "exclude long names" : u"excluir nombres largos",
    "Customize the video status bar message" : u"Personalización de la información del vídeo en la barra de estado",
    "Video status bar message:" : u"Información del vídeo en la barra de estado:",
    "Legend" : u"Leyenda",
    "Current frame" : u"Fotograma actual",
    "Framecount" : u"Total fotogramas",
    "Current time" : u"Tiempo actual",
    "Total time" : u"Tiempo total",
    "Width" : u"Ancho",
    "Height" : u"Alto",
    "Aspect ratio" : u"Relación ancho/alto",
    "Framerate" : u"Fotogramas por segundo",
    "Framerate numerator" : u"Numerador Velocidad fotogramas",
    "Framerate denominator" : u"Denominador Velocidad fotogramas",
    "Colorspace" : u"Espacio de color",
    "Field or frame based" : u"Escaneado (Field or frame based)",
    "Parity" : u"Paridad",
    "Parity short (BFF or TFF)" : u"Paridad (acrónimos BFF o TFF)",
    "Audio rate" : u"AUdio. Frecuencia",
    "Audio length" : u"Audio. Longitud",
    "Audio channels" : u"Audio. Canales",
    "Audio bits" : u"Audio. Bits",
    "Audio type (Integer or Float)" : u"Audio. Tipo",
    "Pixel position (cursor based)" : u"Pixel. Posición (Base: cursor)",
    "Pixel hex color (cursor based)" : u"Pixel. Hex color (Base: cursor)",
    "Pixel rgb color (cursor based)" : u"Pixel. RGB color (Base: cursor)",
    "Pixel yuv color (cursor based)" : u"Pixel. YUV color (Base: cursor)",
    "Pixel color (auto-detect colorspace)" : u"Pixel. Color (Colorspace autodetectado)",
    "Program zoom" : u"Zoom",
    "Note: The \"\\t\\t\" or \"\\T\\T\" is used to separate the left and right portions of the status bar\n         message." : u"", # New in v2.3.0
    "A macro is still running. Close anyway?" : u"", # New in v2.3.0
    "Save changes before closing?" : u"¿Guardar los cambios antes de cerrar?",
    "Cannot create a new tab while crop editor is open!" : u"¡No puede crearse una pestaña nueva mientras la ventana Recortar esté abierta!",
    "Cannot create a new tab while trim editor is open!" : u"¡No puede crearse una pestaña nueva mientras la ventana Trocear esté abierta!",
    "Source files" : u"", # New in v2.3.0
    "Open a script or source" : u"Abrir un script",
    "Reload the file and lose the current changes?" : u"¿Reabrir el fichero y perder los cambios efectuados?",
    "Open this file" : u"Abrir este archivo",
    "Save session before closing all tabs?" : u"¿Guardar la sesión antes de cerrar todas las pestañas?",
    "Save current script" : u"Guardar Script",
    "Directory %(dirname)s does not exist!" : u"¡La carpeta %(dirname)s no existe!",
    "Load a session" : u"Abrir sesión",
    "File has been modified since the session was saved. Reload?" : u"El fichero se ha modificado despues de guardar la Sesión.  ¿Recargar?",
    "Save the session" : u"Guardar la sesión como archivo .ses",
    "No image to save" : u"No hay imagen que guardar",
    "Save current frame" : u"Guardar el fotograma activo",
    "Insert a source" : u"Seleccionar un archivo",
    "All supported plugins" : u"", # New in v2.3.0
    "AviSynth plugins" : u"", # New in v2.3.0
    "VirtualDub plugins" : u"", # New in v2.3.0
    "VFAPI plugins" : u"", # New in v2.3.0
    "Insert a plugin" : u"Selecionar un archivo .dll",
    "No bookmarks defined!" : u"¡No existen marcadores! ",
    "There must be more than one unique bookmark to use this feature!" : u"¡Debe haber más de un marcador para usar esta funcionalidad!",
    "Jump to specified bookmark" : u"Saltar al fotograma con una marca especificada",
    "Line: %(line)i  Col: %(col)i" : u"línea: %(line)i  Columna: %(col)i",
    "Frame Based" : u"Basado en fotogramas (Frame Based)",
    "Field Based" : u"Basado en campos (Field Based)",
    "Bottom Field First" : u"Primero campo inferior",
    "BFF" : u"", # New in v1.3.8
    "Top Field First" : u"Primero campo superior",
    "TFF" : u"", # New in v1.3.8
    "Integer" : u"Entero",
    "Float" : u"Decimal",
    "pos" : u"", # New in v1.3.8
    "hex" : u"", # New in v1.3.7 
    "rgb" : u"", # New in v1.3.7 
    "rgba" : u"", # New in v1.3.8
    "yuv" : u"", # New in v1.3.7 
    "Edit AviSynth function information" : u"Información de funciones AviSynth",
    "  Function name" : u"Nombre de la función",
    "Function arguments" : u"Argumentos de la función",
    "Open filter customization file" : u"Abrir fichero de configuraciones de filtros",
    "Filter customization file" : u"", # New in v2.3.0
    "Calltip-only text file" : u"", # New in v2.3.0
    "Invalid filter customization file!" : u"¡Fichero de configuraciones de filtros no válido!",
    "Save filter customization file" : u"Guardar fichero de configuraciones de filtros",
    "Invalid argument!" : u"¡Argumento no válido!",
    "Error loading AviSynth!" : u"¡Error al cargar AviSynth!",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"Asegúrese de tener AviSynth instalado y que no hay plugins o archivos .avs corruptos en la carpeta de plugins de AviSynth",
    "Save changes before previewing?" : u"¿Guardar los cambios antes de ejecutar el reproductor externo?",
    "Executable files" : u"", # New in v2.3.0
    "Select an external player" : u"Seleccionar un reproductor externo",
    "A program must be specified to use this feature!" : u"¡Debe especificarse un programa para usar esta funcionalidad!", 
    "General settings..." : u"Especificaciones generales...",
    "Invalid slider text: min > max" : u"Sintaxis Control de Ajuste no válida: Valor mínimo > máximo",
    "Invalid slider text: value not in bounds" : u"Sintaxis Control de Ajuste no válida: Valor fuera del rango mín-máx",
    "Invalid slider text: bad modulo label" : u"Sintaxis Control de Ajuste no válida: Etiqueta no válida",
    "Invalid slider text: slider label already exists" : u"Sintaxis Control de Ajuste no válida: La etiqueta ya existe",
    "Invalid slider text: invalid number" : u"Sintaxis Control de Ajuste no válida: Valor no numérico",
    "Invalid slider tag for rescaling!\nAccept only +, -, or an integer." : u"", # New in v2.3.0
    "Reset to initial value: %(value_formatted)s" : u"Volver al valor inicial: %(value_formatted)s",
    "Reset to initial value: %(value2_formatted)s" : u"Reajustar el valor inicial: %(value2_formatted)s",
    "Reset to default value: %(value_formatted)s" : u"Volver al valor por defecto: %(value_formatted)s",
    "Invalid hexadecimal color!" : u"¡valor hexadecimal de color no válido!",
    "Must specify a max value!" : u"¡Debe especificarse un valor máximo!",
    "Must specify a min value!" : u"¡Debe especificarse un valor mínimo!",
    "Min value must be a number!" : u"¡El valor mínimo debe ser un número!",
    "Max value must be a number!" : u"¡El valor máximo debe ser un número!",
    "Default value must be a number!" : u"¡El valor por defecto debe ser un número!",
    "Step size value must be a number!" : u"¡El valor del salto debe ser un número!",
    "Left-click to select a color, right click to reset to default" : u"click con el botón izquierdo para seleccionar un color, click con el botón derecho para volver al color por defecto",
    "Toggle \"%(label)s\" section" : u"Activar/desactivar sección \"%(label)s\"", # New in v1.1.5
    "Above plugin names contain undesirable symbols.\nRename them to only use alphanumeric or underscores,\nor make sure to use them in short name style only." : u"", # New in v2.3.0
    "Don't show me this again" : u"No mostrar este mensaje de nuevo",
    "Save as" : u"Guardar como",
    "Select a directory" : u"Seleccione una carpeta",
    "Enter information" : u"Teclee la información",
    "Progress" : u"Progreso",
    "A get pixel info operation has already started" : u"", # New in v2.3.0
    "Error in the macro:" : u"Error en la macro:",
    "Couldn't find %(macrofilename)s" : u"No se pudo encontrar la macro %(macrofilename)s",
    "Failed to open the AVI file" : u"No se pudo abrir el fichero AVI",
    "Failed to open the AVI frame" : u"No se pudo abrir el fotograma del fichero AVI",
    "Failed to retrieve AVI frame" : u"No se pudo recuperar el fotograma del fichero AVI",
    "Ctrl" : u"", # New in v1.4.0
    "Alt" : u"", # New in v1.4.0
    "Shift" : u"", # New in v1.4.0
    "Program Settings" : u"Parámetros de este programa",
    "Browse" : u"Explorar",
    "* Requires program restart for full effect" : u"* Requiere reinicio",
    "Invalid directory!" : u"¡Directorio no válido!",
    "Invalid filename!" : u"¡Nombre de archivo inválido!",
    "Edit shortcuts" : u"Edición de teclas acceso rápido",
    "Menu label" : u"Opción de menú",
    "Keyboard shortcut" : u"Tecla acceso rápido",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"Doble clic o Enter en una opción de menú para editar las teclas acceso rápido",
    "Shortcut" : u"Atajo teclado",
    "Action" : u"Acción",
    "Edit the keyboard shortcut" : u"Edición de teclas de acceso rápido",    
    "Key:" : u"Tecla:",
    "Clear" : u"Borrar",
    "%(keyString)s not found in key string list" : u"%(keyString)s no encontrada en la lista de cadenas de teclas",
    "This shortcut is being used by:" : u"Este acceso rápido se usa ya para:",
    "Insert" : u"Añadir",
    "Delete" : u"Borrar",
    "Error: key %(key)s does not exist!" : u"Error: !Clave %(key)s no existe!",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"¿Está seguro de que quiere renombrar %(oldName)s como %(newName)s?",
    "Question" : u"Interrogante",
    "Insert a new item" : u"Añadir nuevo item",
    "Must enter a name!" : u"¡Debe teclear un nombre! ",
    "Item %(newKey)s already exists!" : u"¡El item %(newKey)s ya existe!",
    "Warning: no value entered for item %(newKey)s!" : u"Aviso: ¡No se ha tecleado ningun parámetro para el item %(newKey)s!", 
    "Message" : u"Aviso",
    "Select an item to delete first" : u"Seleccione primero el item que quiere borrar",
    "Are you sure you want to delete item %(key)s?" : u"¿Seguro que quiere borrar %(key)s?",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"Calculador de redimensionamiento...",
    "Calculate an appropriate resize for the video" : u"Calcular un redimensionamiento apropiado para el vídeo",
    "Resize calculator" : u"Calculador de redimensionamiento",
    "Input" : u"Entrada",
    "Video resolution:" : u"Resolución del vídeo:",
    "Pixel aspect ratio:" : u"Relación pixel ancho/alto: ",
    "Results" : u"Resultados",
    "Aspect ratio error:" : u"Error relación ancho/alto:",
    "Settings" : u"Especificaciones",
    "Target pixel aspect ratio:" : u"Objetivo relación pixel ancho/alto:",
    "Resize block constraints:" : u"Limitaciones redimensionamiento bloque:",
    "Resize percent ranges:" : u"Porcentajes redimensionamiento:",
    "Max search aspect ratio error:" : u"Máximo error relación ancho/alto tolerado:",
    "Configure" : u"Configurar",
    "compute from .d2v" : u"Calcular desde el archivo .dv2",
    "Configure options" : u"Configurar opciones",
    "Avisynth resize:" : u"Filtro AviSynth para redimensionar:",
    "The current Avisynth script contains errors." : u"El actual script AviSynth contiene errores",

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"Guardar como MP4...",
    "Encode the current script using x264" : u"Codificar el actual script usando x264",
    "Encode video" : u"Codificar vídeo",
    "System settings" : u"Especificaciones de archivos",
    "Input file:" : u"Archivo entrada:",
    "Output file:" : u"Archivo salida:",
    "Compression settings" : u"Especificaciones de compresión",
    "Bitrate (kbits/sec):" : u"Bitraje (kbits/sec):",
    "calculate" : u"Calcular",
    "Quality CRF (0-51):" : u"Calidad CRF (0-51):",
    "Quality CQ (1-31):" : u"Calidad CQ (1-31)",
    "Additional settings" : u"Especificaciones adicionales",
    "Credits start frame:" : u"Primer fotograma de créditos;",
    "Command line settings" : u"Especificaciones de línea de comandos",
    "Run" : u"Ejecutar",
    "First time using this compression preset!" : u"¡Primera vez que se usan estos valores iniciales de compresión!",
    "Please enter the exe paths in the following dialog." : u"Por favor, entre el directorio del archivo .exe en el siguiente cuadro de diálogo",
    "Exe pathnames" : u"Directorio archivo .exe",
    "Open an AviSynth script" : u"Abrir un script AviSynth",
    "AviSynth script (*.avs)|*.avs" : u"AviSynth script (*.avs)|*.avs",
    "Save the video as" : u"Guardar vídeo como",
    "Select a program" : u"Seleccionar un programa",
    "Program (*.exe)|*.exe" : u"Programa (*.exe)|*.exe",
    "Unreplaced items remain in the command line:" : u"Todavía quedan items no reemplazados en la línea de comandos:",
    "Unknown exe paths!" : u"¡Directorio archivo .exe desconocido!",
    "General" : u"",
    "Credits warning minutes:" : u"Minutos de títulos de crédito:",
    "Automatically compute bitrate value on startup" : u"Calcular el bitraje automáticamente al iniciar",
    "Automatically compute pixel aspect ratio from d2v on startup" : u"Calcular la relación ancho/alto del pixel desde el archivo .d2v al iniciar",
    "Append batch commands to the avs script as comments" : u"Añadir comandos batch al Script AviSynth como comentarios",
    "Encoder priority:" : u"Prioridad para el codificador:",
    "Path to %(name)s:" : u"Directorio de %(name)s:",
    "Extra arguments:" : u"Argumentos extras:",
    "Bitrate Calculator" : u"Calculador de bitraje",
    "Output info" : u"Archivo salida",
    "Total size:" : u"Tamaño total:",
    "Container:" : u"Contenedor:",
    "(None)" : u"Ninguno",
    "Video info" : u"vídeo",
    "Framecount:" : u"Total fotogramas:",
    "FPS:" : u"", # New in v2.0.0
    "Audio info" : u"Audio",
    "Audio file:" : u"Archivo:",
    "Compress audio" : u"Compresión",
    "Audio bitrate:" : u"Kbits por segundo",
    "Format:" : u"Formato:",
    "Subtitles info" : u"Subtítulos",
    "Subtitles file:" : u"Archivo:",
    "Total time:" : u"Tiempo total:",
    "Video size:" : u"Tamaño vídeo:",
    "Audio size:" : u"Tamaño audio:",
    "Subtitles size:" : u"Tamaño Subtítulos:",
    "Overhead size:" : u"Tamaño cabecera:",
    "Bitrate:" : u"Bitraje:",
    "Open the audio file" : u"Abrir archivo audio",
    "Open the subtitles file" : u"Abrir archivo subtítulos",
    "%(h)i hr and %(m)i min" : u"%(h)i hr y %(m)i min",

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"Guardar como AVI...",
    "Use avs2avi to save the current script as an avi" : u"Usar avs2avi para guardar el script actual como un avi",
    "Please select the path to avs2avi.exe" : u"Por favor, seleccione el directorio de avs2avi.exe",
    "Error: avs2avi is required to save an avi!" : u"Error: ¡Para guardar como Avi es necesario el programa avs2avi!",
    "Pass: %(pass)s / %(passes)s" : u"Pasadas: %(pass)s / %(passes)s",
    "Frame: %(frame)i / %(frames)i" : u"Fotograma: %(frame)i / %(frames)i",
    "Size: %(size).2f MB" : u"Tamaño: %(size).2f MB",
    "FPS: %(fps).1f fps" : u"FPS: %(fps).1f fps",
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"Tiempo restante: %(hr)02i:%(min)02i:%(sec)02i",
    "Input file (.avs):" : u"Entrada: (.avs):",
    "Output file (.avi):" : u"Salida: (.avi):",
    "# of passes:" : u"Pasadas: ",
    "Priority:" : u"Prioridad: ",
    "Error: Unknown button" : u"Error: botón desconocido",
    "Save the avi as" : u"Guardar archivo .avi",
    "Avi file (*.avi)|*.avi" : u"Archivo AVI (*.avi)|*.avi",
    "Input file does not exist!" : u"¡Archivo .avs no existe!",
    "Input file must be an avisynth script!" : u"¡El archivo debe ser un script AviSynth!",
    "Output path does not exist!" : u"¡La carpeta no existe!",
    "# of passes must be an integer!" : u"¡El número de pasadas debe ser un número entero!",
    "Priority must be an integer!" : u"¡La prioridad debe ser dada con un número entero!",
    "Stop" : u"Detener",
    "Done" : u"Completado",
    "Process stopped." : u"Proceso detenido",
    "Processing..." : u"Procesando...",
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"Completado en %(hr)i hour(s) y %(min)i minuto(s).",
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"Completado en %(min)i minuto(s) y %(sec)i segundo(s).",
    "Finished in %(time).1f seconds." : u"Completado en %(time).1f segundos.",
    "Filesize: %(size).2f MB" : u"Tamaño archivo: %(size).2f MB",
    "The current script contains errors, exiting." : u"El script contiene errores. volver.  ",
    "Save as AVI" : u"Guardar como AVI",

    #--- Macros ---#
    "Bookmarks at Intervals" : u"", # New in v2.3.0
    "Bookmarks from Chapter" : u"", # New in v2.3.0
    "Bookmarks to Chapter" : u"", # New in v2.3.0
    "ConditionalReader file from bookmarks" : u"", # New in v2.3.0
    "DeleteFrame" : u"", # New in v2.3.0
    "DuplicateFrame" : u"", # New in v2.3.0
    "Preview from current point" : u"", # New in v2.3.0
    "Random Clip Order" : u"", # New in v2.3.0
    "Save bookmarks to images" : u"", # New in v2.3.0
    "Save Image Sequence" : u"", # New in v2.3.0
    "Shift Bookmarks by frames" : u"", # New in v2.3.0
    "Example (Resize)" : u"", # New in v2.3.0
    "Examples" : u"", # New in v2.3.0
    "Customized" : u"", # New in v2.3.0
    "bilinear" : u"", # New in v2.3.0
    "bicubic" : u"", # New in v2.3.0
    "lanczos" : u"", # New in v2.3.0
    "spline36" : u"", # New in v2.3.0
    "create new tab" : u"", # New in v2.3.0
    "force mod 2" : u"", # New in v2.3.0
    "Template example" : u"", # New in v2.3.0
    "Batch example" : u"", # New in v2.3.0
    "Image processing" : u"", # New in v2.3.0
    "Manual Telecide" : u"", # New in v2.3.0
    "Secondary preview" : u"", # New in v2.3.0
    "Encoding example" : u"", # New in v2.3.0
    "Encoding example 2" : u"", # New in v2.3.0
    "Optimize Sliders" : u"", # New in v2.3.0

    #--- Macro: Bookmarks at Intervals ---#
    "Choose a frame step or a number of intervals" : u"", # New in v2.3.0
    "Frame step" : u"", # New in v2.3.0
    "Number of intervals" : u"", # New in v2.3.0

    #--- Macro: Bookmarks from Chapter ---#
    "Open a bookmark file" : u"", # New in v2.3.0
    "Supported files" : u"", # New in v2.3.0
    "Chapters Text files" : u"", # New in v2.3.0
    "Matroska XML files" : u"", # New in v2.3.0
    "Celltimes files" : u"", # New in v2.3.0
    "AvsP Session files" : u"", # New in v2.3.0
    "Bookmark file unrecognized!" : u"", # New in v2.3.0

    #--- Macro: Bookmarks to Chapter ---#
    "Text files" : u"", # New in v2.3.0

    #--- Macro: ConditionalReader file from bookmarks ---#
    "There is not bookmarks" : u"", # New in v2.3.0
    "Type" : u"Tipo", # New in v2.0.0
    "Value" : u"", # New in v2.3.0
    "Bookmarks represent..." : u"", # New in v2.3.0
    "Override 'Value' with the bookmark's title" : u"", # New in v2.3.0
    "ConditionalReader file" : u"", # New in v2.3.0
    "Insert the ConditionalReader file path at the current cursor position" : u"", # New in v2.3.0
    "Bool" : u"", # New in v2.3.0
    "String" : u"Cadenas", # New in v1.2.1
    "Int" : u"", # New in v2.3.0
    "False" : u"", # New in v2.3.0
    "True" : u"", # New in v2.3.0
    "Single frames" : u"", # New in v2.3.0
    "Ranges of frames" : u"", # New in v2.3.0
    "Ranges of frames (with interpolation)" : u"", # New in v2.3.0
    "Interpolation only available for Int and Float" : u"", # New in v2.3.0
    "Odd number of bookmarks" : u"", # New in v2.3.0

    #--- Macro: Preview from current point ---#
    "Failed to run the external player!\n\nOpen the macro file in the \"Macros\" subdirectory\nwith a text editor and edit the executable\ndirectory appropriately!" : u"", # New in v2.3.0

    #--- Macro: Save bookmarks to images ---#
    "Select the output directory and basename" : u"", # New in v2.3.0
    "JPEG Quality (0-100):" : u"", # New in v2.3.0
    "JPEG Quality" : u"", # New in v2.3.0
    "%d image files created." : u"", # New in v2.3.0
    "Information" : u"Información",
    "Please save the current script first!" : u"", # New in v2.3.0

    #--- Macro: Save Image Sequence ---#
    "Saving images..." : u"", # New in v2.3.0

    #--- Macro: Shift Bookmarks by frames ---#
    "Introduce the number of frames:" : u"", # New in v2.3.0
    "Shift bookmarks by # frames" : u"", # New in v2.3.0

    #--- Macro: Customized ---#
    "Customized aspect ratio" : u"", # New in v2.3.0
    "Enter a pixel ratio or new size. e.g. 40:33, 1.212 or 640x360" : u"", # New in v2.3.0

    #--- Macro: Image processing ---#
    "Processing images..." : u"", # New in v2.3.0
    "Macro aborted" : u"", # New in v2.3.0

    #--- Macro: Manual Telecide ---#
    "Open a source to Telecide" : u"", # New in v2.3.0
    "Filename was mangled! Get it again!" : u"", # New in v2.3.0
    "Enter the field order:" : u"", # New in v2.3.0
    "Must enter either a 0 or 1!" : u"", # New in v2.3.0
    "Must enter an integer!" : u"", # New in v2.3.0
    "Override filename was mangled! Get it again!" : u"", # New in v2.3.0
    "Not allowed to select base Telecide tab!" : u"", # New in v2.3.0
    "Unknown mode!" : u"", # New in v2.3.0

    #--- Macro: Encoding example ---#
    "Encoding is disabled, please read the \"Encoding example.py\" macro for info" : u"", # New in v2.3.0

    #--- Macro: Encoding example 2 ---#
    "Output filename:" : u"", # New in v2.3.0
    "Output height:" : u"", # New in v2.3.0
    "Output width:" : u"", # New in v2.3.0
    "Enter encoder info" : u"", # New in v2.3.0
    "Encoding is disabled, please read the \"Encoding example 2.py\" macro for info" : u"", # New in v2.3.0

    #--- Macro: Optimize Sliders ---#
    "Generation 0 Progress" : u"", # New in v2.3.0
    "Initial evaluation..." : u"", # New in v2.3.0
    "Initial best score: %.3f, Current best score: %.3f" : u"", # New in v2.3.0
    "Best score: %.2f" : u"", # New in v2.3.0
    "Must configure avs2avi directory to use this macro!" : u"", # New in v2.3.0
    "SSIM log filename:" : u"", # New in v2.3.0
    "max generations:" : u"", # New in v2.3.0
    "population size:" : u"", # New in v2.3.0
    "crossover probability:" : u"", # New in v2.3.0
    "mutation probability:" : u"", # New in v2.3.0
    "selection pressure:" : u"", # New in v2.3.0
    "Enter optimization info    (%i bits, %i possibilities)" : u"", # New in v2.3.0
    "Begin optimization..." : u"", # New in v2.3.0
    "Finished optimization." : u"", # New in v2.3.0
}