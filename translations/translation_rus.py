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
# translate any words inside formatted strings (ie, any portions of the 
# text which look like %(...)s, %(...)i, etc.)
#
# Данный файл используется для перевода сообщений, используемых в интерфейсе AvsP.
# Чтобы использовать его, убедитесь, что он назван "translation.py" и лежит в той же папке,
# что и AvsP.exe.  Просто добавьте переведенные сообщения после каждого сообщения
# (любое непереведенное сообщение будет показано на английском).  Вы можете вводить
# текст в кодировке unicode прямо в этом документе - если так, будьте уверены сохранить его
# в соответствующем формате (кодировке). Если требуется, вы можете изменить кодировку 
# в первой сточке данного документа на кодировку подходящую для вашего языка перевода.
# (Фактически для русского языка можно использовать редакторы типа Блокнот в Win2000 и WinXP.) 
# НЕ ПЕРЕВОДИТЕ любые слова внутри форматированных строк (то есть, любые части
# текста, которые выглядят подобно %(...)s, %(...)i, и т.п.)

# Russian interface file for AvsP editor by qwerpoi, http://www.avisynth.org/qwerpoi
# Translated by Fizick 19.09.2006-11.03.2007 for AvsP v1.3.7, http://avisynth.org.ru/avsp

version = "2.2.1"

messages = {
    "Find" : u"Найти",
    "Replace" : u"Заменить",
    "Cannot find \"%(text)s\"." : u"Не могу найти \"%(text)s\".",
    "Information" : u"Информация",
    "Replace Information" : u"Заменить информацию",
    "Replaced %(count)i times" : u"Заменено %(count)i раз(а)",
    "AviSynth fonts and colors" : u"Шрифты и цвета", 
    "Background" : u"Фон", 
    "Font" : u"Шрифт", 
    "Text color" : u"Цвет текста", 
    "OK" : u"Да", 
    "Cancel" : u"Отменить ",
    "Scrap Window" : u"Окно заметок",
    "Undo" : u"Отмена",
    "Redo" : u"Повтор",
    "Cut" : u"Вырезать",
    "Copy" : u"Копировать",
    "Paste" : u"Вставить",
    "Select all" : u"Выделить все",
    "Refresh" : u"Обновить",
    "Insert frame #" : u"Вставить номер кадра",
    "Save to file..." : u"Сохранить в файл...",
    "Clear all" : u"Очистить все",
    "Toggle scrap window" : u"Переключить окно заметок",
    "Save script" : u"Сохранить скрипт",
    "Error: no contextMenu variable defined for window" : u"Ошибка: переменная contextMenu не определена для окна",
    "Text document (*.txt)|*.txt|All files (*.*)|*.*" : u"Текстовый документ (*.txt)|*.txt|Все файлы (*.*)|*.*",
    "Save scrap text" : u"Сохранить текст заметок",
    "This field must contain a value!" : u"Данное поле должно содержать величину!",
    "This slider label already exists!" : u"Данная метка ползунка уже существует!",
    "Invalid slider label modulo syntax!" : u"Неверный синтаксис метки модуля ползунка",
    "This field must contain a number!" : u"Данное поле дожно содержать число!",
    "The min value must be less than the max!" : u"Минимальная величина должна быть меньше максимальной!",
    "The initial value must be between the min and the max!" : u"Начальная величина должна быть между минимумом и максимумом!",
    "The min value must be a multiple of %(mod)s!" : u"Мин. значение должно быть кратно %(mod)s!",
    "The max value must be a multiple of %(mod)s!" : u"Макс. значение должно быть кратно %(mod)s!",
    "The initial value must be a multiple of %(mod)s!" : u"Начальное значение должно быть кратно %(mod)s!",
    "The difference between the min and max must be greater than %(mod)s!" : u"Разница между мин. и макс. должна быть больше чем %(mod)s!",
    "Error" : u"Ошибка",
    "Define user slider" : u"Определить пользовательский ползунок",
    "Slider label:" : u"Метка ползунка:",
    "Min value:" : u"Минимальное значение:",
    "Max value:" : u"Максимальное значение:",
    "Initial value:" : u"Начальное значение:",
    "Add or override AviSynth functions in the database" : u"Добавить или изменить функции AviSynth в базе данных",
    "Core filters" : u"Фильтры ядра",
    "Plugins" : u"Плагины",
    "User functions" : u"Пользовательские функции",
    "Script functions" : u"", # New in v2.0.2
    "Clip properties" : u"Свойства клипа",
    "Include %(title)s in autcompletion lists" : u"Добавить %(title)s в список автозавершения ввода",
    "New function" : u"Новая функция",
    "Edit selected" : u"Редактировать",
    "Delete selected" : u"Удалить",
    "Select installed" : u"В папке AviSynth",
    "Import from files" : u"Импорт",
    "Export customizations" : u"Экспорт",
    "Clear customizations" : u"", # New in v2.0.2
    "Clear manual presets" : u"", # New in v2.0.2
    "When importing, don't show the choice dialog" : u"", # New in v2.0.7
    "Edit function information" : u"", # New in v2.0.2
    "Name:" : u"Имя:",
    "Type:" : u"Тип:",
    "clip property" : u"свойство клипа", 
    "core filter" : u"", # New in v2.0.2
    "plugin" : u"", # New in v2.0.2
    "script function" : u"", # New in v2.0.2
    "user function" : u"пользовательская функция",
    "Arguments:" : u"Аргументы",
    "define sliders" : u"параметры ползунков",
    "reset to default" : u"сброс",
    "Slider information" : u"Параметры ползунков",
    "Preset:" : u"Предустановка",
    "Auto-generate" : u"Создать автоматически",
    "Filter name already exists!" : u"Фильтр с таким именем уже существует!",
    "Invalid filter name!" : u"Неверное имя фильтра!",
    "Renaming not allowed!" : u"Невозможно переименовать!",
    "You must use dllname_function naming format for plugins!" : u"", # New in v2.0.2
    "Open Customization files, Avisynth scripts or Avsp options files" : u"", # New in v2.0.7
    "All supported|*.txt;*.avsi;*.avs;*.dat|Customization file (*.txt)|*.txt|AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|AvsP data (*.dat)|*.dat|All files (*.*)|*.*" : u"", # New in v2.0.7
    "Unrecognized files" : u"", # New in v2.0.7
    "Select import functions" : u"", # New in v2.0.7
    "select all" : u"", # New in v2.0.7
    "select none" : u"", # New in v2.0.7
    "select all (file only)" : u"", # New in v2.0.7
    "select none (file only)" : u"", # New in v2.0.7
    "Red - a customized function already exists." : u"", # New in v2.1.6
    "No customizations to export!" : u"", # New in v2.0.2
    "Save filter customizations" : u"", # New in v2.0.2
    "Customization file (*.txt)|*.txt|All files (*.*)|*.*" : u"", # New in v2.0.2
    "This will delete all filter customizations. Continue?" : u"", # New in v2.0.2
    "Warning" : u"Предупреждение",
    "This will delete all manually defined presets. Continue?" : u"", # New in v2.0.2
    "Do you want to delete this custom filter entirely?" : u"", # New in v2.0.2
    "Edit filter database" : u"", # New in v2.0.2
    "Default" : u"По умолчанию",
    "Min value" : u"Минимум",
    "Max value" : u"Максимум",
    "Step size" : u"Шаг",
    "Value list (comma separated)" : u"Список значений (через запятую)",
    "Value must be True or False!" : u"Значение может быть только True или False!",
    "Must enter a value list!" : u"Необходимо указать список значений!",
    "Export filter customizations" : u"Экспорт настроенных фильтров",
    "Import filter customizations" : u"Импорт настроенных фильтров",
    "Select filters to export:" : u"Выбрать фильтры для экспорта:",
    "Select filters to import from the file:" : u"Выбрать фильтры для импорта из файла:",
    "Overwrite all data" : u"Переписать все данные",
    "You must select at least one filter!" : u"Вы должны быбрать по крайней мере один фильтр",
    "Error: minValue must be less than maxValue" : u"Ошибка: мин. величина должна быть меньше чем макс. величина",
    "New File" : u"Новый файл",
    "Windows Bitmap (*.bmp)" : u"",
    "Animation (*.gif)" : u"", # New in v2.0.7
    "JPEG (*.jpg)" : u"",
    "Zsoft Paintbrush (*.pcx)" : u"", # New in v2.0.7
    "Portable Network Graphics (*.png)" : u"",
    "Netpbm (*.pnm)" : u"", # New in v2.0.7
    "Tagged Image File (*.tif)" : u"", # New in v2.0.7
    "ASCII Text Array (*.xpm)" : u"", # New in v2.0.7
    "Windows Icon (*.ico)" : u"", # New in v2.0.7
    "fps" : u"кадр/с",
    "Frame" : u"Кадр",
    "A crash detected at the last running!" : u"", # New in v2.1.6
    "&Zoom" : u"", # New in v2.2.0
    "%s translation file updated with new messages to translate" : u"", # New in v2.2.1
    "Translation updated" : u"", # New in v2.2.1
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.2.1
    "%s language couldn't be loaded" : u"", # New in v2.2.1
    "Paths" : u"", # New in v2.2.0
    "AvsP help directory:" : u"Папка справки AvsP",
    "Location of the AvsP help directory" : u"Расположение папки справки AvsP",
    "Avisynth directory:" : u"Папка Avisynth:",
    "Location of the avisynth installation directory" : u"Расположение директории установенного Avisynth",
    "Avisynth help file/url:" : u"Файл/ссылка помощи Avisynth",
    "Location of the avisynth help file or url" : u"Расположение файла справки Avisynth или ссылки",
    "External player:" : u"Внешний проигрыватель:",
    "Location of external program for script playback" : u"Расположение внешней программы для проигрывания скриптов",
    "Additional arguments when running the external player" : u"Дополнительные аргументы при выполнении внешнего проигрывателя", 
    "External player extra args:" : u"Доп. аргументы внешнего проигрывателя", 
    "Documentation search paths:" : u"Пути поиска документации",
    "Specify which directories to search for docs when you click on a filter calltip" : u"Укажите в каких папках искать документы, когда Вы щелкните на подсказке для фильтра",
    "Documentation search url:" : u"Поиск через интернет",
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"", # New in v2.0.2
    "Text" : u"", # New in v2.2.0
    "Show filter calltips" : u"Показывать подсказки для фильтра",
    "Turn on/off automatic tips when typing filter names" : u"Включить/выключить автоматические подсказки при наборе имен фильтров",
    "Always show calltips any time the cursor is within the filter's arguments" : u"Всегда показывать подсказки во время нахождения курсора на аргументах фильтра", 
    "Frequent calltips" : u"Частые подсказки",
    "Syntax highlighting" : u"Подсветка синтаксиса",
    "Turn on/off avisynth-specific text colors and fonts" : u"Включить/выключить  цвета и шрифты специфичного для Avisynth текста",
    "Show autocomplete on capital letters" : u"Показывать список автозавершения слов",
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"Включить показ списка автозавершения при наборе слов, начинающихся с заглавных букв",
    "Show autocomplete list when typing a certain amount of letters" : u"", # New in v2.1.6
    "Don't allow lines wider than the window" : u"Не допускать строки шире чем окно", 
    "Wrap text" : u"Перенос текста",
    "Draw lines at fold points" : u"", # New in v2.1.6
    "For code folding, draw a line underneath if the fold point is not expanded" : u"", # New in v2.1.6
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Отметьте, чтобы вставлять табуляцию вместо пробелов при использовании клавиши Tab",
    "Use tabs instead of spaces" : u"Использовать табуляцию вместо пробелов",
    "Set the size of the tabs in spaces" : u"Установить размер табуляции в пробелах",
    "Tab width" : u"Ширина табуляции",
    "Initial space to reserve for the line margin in terms of number of digits" : u"Начальный пробел, зарезервированный для отступа строк, число цифр", 
    "Line margin width" : u"Ширина отступа строк",
    "Autocomplete" : u"Автозавершение",
    "Add user defined variables into autocomplete list" : u"", # New in v2.1.6
    "Show autocomplete with variables" : u"", # New in v2.1.6
    "Show autocomplete on single matched lowercase variable" : u"", # New in v2.2.0
    "When typing a lowercase variable name, show autocomplete if there is only one item matched in keyword list" : u"", # New in v2.2.0
    "Add icons into autocomplete list. Using different type to indicate how well a filter's presets is defined" : u"", # New in v2.1.6
    "Show autocomplete with icons" : u"", # New in v2.1.6
    "Don't show autocomplete when calltip is active" : u"", # New in v2.2.0
    "When calltip is active, autocomplete will not be activate automatically. You can still show autocomplete manually" : u"", # New in v2.2.0
    "Customize autocomplete keyword list..." : u"", # New in v2.1.6
    "Customize the keyword list shown in the autocomplete choice box" : u"", # New in v2.1.6
    "Autoparentheses level" : u"Уровень автоскобок",
    "Close \"()\"" : u"Закрытая \"()\"",
    "Determines parentheses to insert upon autocompletion" : u"Определяет скобки для вставки при автозавершении",
    "None \" \"" : u"Никакая \" \"",
    "Open \"(\"" : u"Открытая \"(\"",
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"Определяет, какая кнопка активирует пресет фильтра при использовании списка автозавершения",
    "None" : u"Не определена",
    "Preset activation key" : u"Активировать пресет кнопкой",
    "Return" : u"", # New in v2.0.2
    "Tab" : u"", # New in v2.0.2
    "Video" : u"Видео",
    "Constantly update video while dragging" : u"Непрерывно обновлять видео при перетаскивании",
    "Update the video constantly when dragging the frame slider" : u"Обновлять видео непрерывно при перемещении ползунка кадров",
    "Enable line-by-line update" : u"Разрешить обновление построчно", 
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"Разрешить режим построчного обновления видео (обновлять каждый раз при смене позиции строки курсора)", 
    "Focus the video preview upon refresh" : u"Фокус на видеопросмотр при обновлении",
    "Switch focus to the video preview window when using the refresh command" : u"Переключить фокус на окне видео просмотра при использовании команды обновления",
    "Refresh preview automatically" : u"", # New in v2.2.0
    "Refresh preview when switch focus on video window or change a value in slider window" : u"", # New in v2.2.0
    "Seeking to a certain frame will seek to that frame on all tabs" : u"", # New in v2.2.0
    "Shared timeline" : u"", # New in v2.2.0
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"", # New in v2.2.0
    "Allow AvsPmod to resize the window" : u"", # New in v2.2.0
    "Separate video preview window" : u"Отдельное окно просмотра видео",
    "Use a separate window for the video preview" : u"Использоваить отдельное окно для просмотра видео",
    "Min text lines on video preview" : u"Мин. число строк при просмотре видео",
    "Minimum number of lines to show when displaying the video preview" : u"Минимальное число строк текста при просмотре видео",
    "Customize the video information shown in the program status bar" : u"Настроить видео информацию показываемую в полосе статуса",
    "Customize video status bar..." : u"Настроить полосу статуса",
    "User Sliders" : u"Ползунки",
    "Hide slider window by default" : u"Не показывать колонку ползунков",
    "Keep the slider window hidden by default when previewing a video" : u"Не открывать колонку ползунков при открытии окна превью",
    "Create user sliders automatically" : u"Автоматически создавать ползунки",
    "Create user sliders automatically using the filter database" : u"Автоматически создавать ползунки, используя известные параметры фильтров",
    "Create user sliders for int and float arguments" : u"", # New in v2.0.2
    "type int/float (numerical slider)" : u"", # New in v2.0.2
    "Create color pickers for hex color arguments" : u"", # New in v2.0.2
    "type int (hex color)" : u"", # New in v2.0.2
    "Create radio boxes for bool arguments" : u"", # New in v2.0.2
    "type bool" : u"", # New in v2.0.2
    "Create listboxes for string list arguments" : u"", # New in v2.0.2
    "type string (list)" : u"", # New in v2.0.2
    "Create filename pickers for string filename arguments" : u"", # New in v2.0.2
    "type string (filename)" : u"", # New in v2.0.2
    "Create placeholders for arguments which have no database information" : u"", # New in v2.0.2
    "undocumented" : u"", # New in v2.0.2
    "Determines which filters will initially have hidden arguments in the slider window" : u"", # New in v2.0.2
    "Fold all" : u"", # New in v2.0.2
    "Fold non-numbers" : u"", # New in v2.0.2
    "Fold none" : u"", # New in v2.0.2
    "Fold startup setting" : u"", # New in v2.0.2
    "Filter exclusion list:" : u"Список исключений:",
    "Specify filters never to build automatic sliders for" : u"Укажите фильтры, для которых не следует автоматически создавать ползунки",
    "Save/Load" : u"", # New in v2.2.0
    "Automatically save the session on shutdown and load on next startup" : u"Автоматически сохранять сеанс при закрытии и загружать при следующем запуске",
    "Save session for next launch" : u"Сохранять сеанс для следующего запуска",
    "Always load startup session" : u"Всегда загружать стартовый сеанс", 
    "Always load the auto-saved session before opening any other file on startup" : u"Всегда загружать авто-сохраненный сеанс до открытия другого файла при запуске", 
    "Always hide the video preview window when loading a session" : u"", # New in v2.1.6
    "Don't preview when loading a session" : u"", # New in v2.1.6
    "Backup session when previewing" : u"", # New in v2.2.0
    "If checked, the current session is backed up prior to previewing any new script" : u"Если включен, текущий сеанс сохраняется перед просмотром любого скрипта",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"Предлагать сохранить скрипт перед просмотром (неактивно если просмотр с несохраненными изменениями)", 
    "Prompt to save when previewing" : u"Предлагать сохранить перед просмотром", 
    "Create a temporary preview script with unsaved changes when previewing the video" : u"Создавать временный скрипт просмотра с несохраненными изменениями при просмотре видео", 
    "Preview scripts with unsaved changes" : u"", # New in v2.2.0
    "Prompt to save each script with unsaved changes when exiting the program" : u"Приглашение сохранять каждый скрипт с несохраненными изменениями при выходе из программы",
    "Prompt to save scripts on program exit" : u"Приглашение сохранять скрипты при выходе",
    "Save *.avs scripts with AvsPmod markings" : u"", # New in v2.2.0
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"", # New in v2.2.0
    "Misc" : u"Разное", 
    "Choose the language used for the interface" : u"", # New in v2.2.1
    "Language *" : u"", # New in v2.2.1
    "Show keyboard images in the script tabs when video has focus" : u"Показывать в заголовках вкладок кнопки клавиатуры (для переключения вкладок), когда окно превью под фокусом",
    "Use keyboard images in tabs" : u"Кнопки клавиатуры в заголовках вкладок",
    "Show tabs in multiline style" : u"", # New in v2.1.6
    "There can be several rows of tabs" : u"", # New in v2.1.6
    "All tabs will have same width" : u"", # New in v2.2.0
    "Show tabs in fixed width" : u"", # New in v2.2.0
    "Enable scroll wheel through similar tabs" : u"", # New in v2.2.0
    "Mouse scroll wheel cycles through tabs with similar videos" : u"Вращение колесика мышки будет по очереди переключать вкладки",
    "Only allow a single instance of AvsPmod" : u"", # New in v2.2.0
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"", # New in v2.1.6
    "Show warning for bad plugin naming at startup" : u"", # New in v2.1.6
    "Max number of recent filenames" : u"Макс. число имен последних файлов", 
    "This number determines how many filenames to store in the recent files menu" : u"Это число определяет, сколько имен файлов сохраняется в меню последних файлов", 
    "Custom jump size:" : u"Задаваемый размер шага",
    "Jump size used in video menu" : u"Размер шага используемый в меню видео",
    "Custom jump size units" : u"Единицы задаваемого размера шага",
    "Units of custom jump size" : u"Единицы задаваемого размера шага",
    "hours" : u"часы",
    "minutes" : u"минуты",
    "seconds" : u"секунды",
    "frames" : u"кадры",
    "Extend selection to line down position" : u"", # New in v2.1.6
    "Scroll down" : u"", # New in v2.1.6
    "Extend rectangular selection to line down position" : u"", # New in v2.1.6
    "Extend selection to line up position" : u"", # New in v2.1.6
    "Scroll up" : u"", # New in v2.1.6
    "Extend rectangular selection to line up position" : u"", # New in v2.1.6
    "Go to previous paragraph" : u"", # New in v2.1.6
    "Extend selection to previous paragraph" : u"", # New in v2.1.6
    "Go to next paragraph" : u"", # New in v2.1.6
    "Extend selection to next paragraph" : u"", # New in v2.1.6
    "Extend selection to previous character" : u"", # New in v2.1.6
    "Go to previous word" : u"", # New in v2.1.6
    "Extend selection to previous word" : u"", # New in v2.1.6
    "Extend rectangular selection to previous character" : u"", # New in v2.1.6
    "Extend selection to next character" : u"", # New in v2.1.6
    "Go to next word" : u"", # New in v2.1.6
    "Extend selection to next word" : u"", # New in v2.1.6
    "Extend rectangular selection to next character" : u"", # New in v2.1.6
    "Go to previous word part" : u"", # New in v2.1.6
    "Extend selection to previous word part" : u"", # New in v2.1.6
    "Go to next word part" : u"", # New in v2.1.6
    "Extend selection to next word part" : u"", # New in v2.1.6
    "Extend selection to start of line" : u"", # New in v2.1.6
    "Go to start of document" : u"", # New in v2.1.6
    "Extend selection to start of document" : u"", # New in v2.1.6
    "Go to start of line" : u"", # New in v2.1.6
    "Extend selection to end of line" : u"", # New in v2.1.6
    "Go to end of document" : u"", # New in v2.1.6
    "Extend selection to end of document" : u"", # New in v2.1.6
    "Go to end of line" : u"", # New in v2.1.6
    "Extend selection to previous page" : u"", # New in v2.1.6
    "Extend rectangular selection to previous page" : u"", # New in v2.1.6
    "Extend selection to next page" : u"", # New in v2.1.6
    "Extend rectangular selection to next page" : u"", # New in v2.1.6
    "Delete to end of word" : u"", # New in v2.1.6
    "Delete to end of line" : u"", # New in v2.1.6
    "Delete back" : u"", # New in v2.1.6
    "Delete to start of word" : u"", # New in v2.1.6
    "Delete to start of line" : u"", # New in v2.1.6
    "Cancel autocomplete or calltip" : u"", # New in v2.1.6
    "Indent selection" : u"Отступ выбранного",
    "Unindent selection" : u"Убрать отступ выбранного",
    "Newline" : u"", # New in v2.1.6
    "Zoom in" : u"", # New in v2.1.6
    "Zoom out" : u"", # New in v2.1.6
    "Reset zoom level to normal" : u"", # New in v2.1.6
    "Line cut" : u"", # New in v2.1.6
    "Line delete" : u"", # New in v2.1.6
    "Line copy" : u"", # New in v2.1.6
    "Transpose line with the previous" : u"", # New in v2.1.6
    "Line or selection duplicate" : u"", # New in v2.1.6
    "Convert selection to lowercase" : u"", # New in v2.1.6
    "Convert selection to uppercase" : u"", # New in v2.1.6
    "Sort bookmarks ascending" : u"Сортировать закладки по возрастанию",
    "sort ascending" : u"по возрастанию",
    "Show bookmarks with timecode" : u"Показывать время",
    "show time" : u"показать время",
    "Show bookmarks with title" : u"Показывать подпись",
    "show title" : u"показать подпись",
    "Rec601" : u"", # New in v2.0.7
    "PC.601" : u"", # New in v2.0.7
    "Rec709" : u"", # New in v2.0.7
    "PC.709" : u"", # New in v2.0.7
    "Progressive" : u"", # New in v2.0.7
    "Interlaced" : u"", # New in v2.0.7
    "Swap UV" : u"", # New in v2.1.6
    "25%" : u"", # New in v1.3.8
    "50%" : u"", # New in v1.3.8
    "100% (normal)" : u"", # New in v1.3.8
    "200%" : u"", # New in v1.3.8
    "300%" : u"", # New in v1.3.8
    "400%" : u"", # New in v1.3.8
    "Fill window" : u"Заполнить окно",
    "Fit inside window" : u"Подогнать внутрь окна",
    "Vertically" : u"", # New in v2.1.6
    "Horizontally" : u"", # New in v2.1.6
    "&File" : u"&Файл",
    "Create a new tab" : u"Создать новую вкладку",
    "New tab" : u"Новая вкладка",
    "Open an existing script" : u"Открыть существующий скрипт",
    "Open..." : u"Открыть...",
    "Close tab" : u"Закрыть вкладку",
    "Close the current tab" : u"Закрыть текущую вкладку",
    "Close all tabs" : u"Закрыть все вкладки",
    "Close every tab" : u"Закрыть каждую вкладку",
    "Rename tab" : u"", # New in v2.2.0
    "Rename the current tab. If script file is existing, also rename it" : u"", # New in v2.2.0
    "Save the current script" : u"Сохранить текущий скрипт",
    "Choose where to save the current script" : u"Выбрать где сохранить текущий скрипт",
    "Save script as..." : u"Сохранить скрипт как...",
    "Load a session into the tabs" : u"Загрузить сеанс во вкладки",
    "Load session..." : u"Загрузить сеанс...",
    "Save all the scripts as a session, including slider info" : u"Сохранить все скрипты как сеанс, включая информацию ползунков",
    "Save session..." : u"Сохранить сеанс...",
    "Backup current session" : u"Архивировать текущий сеанс",
    "Backup the current session for next program run" : u"Архивировать текущий сеанс (состояние) для последующего запуска программы",
    "Next tab" : u"Следующая вкладка",
    "Switch to next script tab" : u"Переключиться к следующей скриптовой вкладке",
    "Previous tab" : u"Предыдущая вкладка",
    "Switch to previous script tab" : u"Переключиться к предыдущей скриптовой вкладке",
    "Show the scrap window" : u"Показать окно заметок",
    "&Exit" : u"&Выход",
    "Exit the program" : u"Выйти из программы",
    "&Edit" : u"&Правка",
    "Undo last text operation" : u"Отменить последнюю текстовую операцию",
    "Redo last text operation" : u"Повторить последнюю текстовую операцию",
    "Cut the selected text" : u"Вырезать выбранный текст",
    "Copy the selected text" : u"Скопировать выбранный текст",
    "Paste the selected text" : u"Вставить выбранный текст",
    "Find..." : u"Найти...",
    "Open a find text dialog box" : u"Открыть диалог поиска текста",
    "Find next" : u"Найти следующее",
    "Find the next instance of given text" : u"Найти следующий образец заданного текста",
    "Open a replace text dialog box" : u"Открыть диалог замены текста",
    "Replace..." : u"Заменить...",
    "Select All" : u"Выбрать все",
    "Select all the text" : u"Выбрать весь текст",
    "&Insert" : u"", # New in v2.2.0
    "Choose a source file to insert into the text" : u"Задать файл (видео) источника для вставки в текст",
    "Insert source..." : u"Вставить источник...",
    "Get a filename from a dialog box to insert into the text" : u"Получить имя файла в диалоге для вставки в текст",
    "Insert filename..." : u"Вставить имя файла...",
    "Choose a plugin dll to insert into the text" : u"Задать DLL плагина для вставки в текст",
    "Insert plugin..." : u"Вставить плагин...",
    "Insert a user-scripted slider into the text" : u"Вставить определяемый пользователем ползунок в текст",
    "Insert user slider..." : u"Вставить пользовательский ползунок...",
    "Insert a tag which indicates a separator in the user slider window" : u"Вставить метку, обозначающую разделитель в окне пользовательских ползунков",
    "Insert user slider separator" : u"Вставить разделитель пользовательских ползунков",
    "Insert the current frame number into the text" : u"Вставить номер текущего кадра в текст",
    "Add tags surrounding the selected text for toggling with the video preview" : u"Добавить метки, окружающие блок текста, для отключения-включения при просмотре видео",
    "Tag selection for toggling" : u"Пометить выбранное для переключения",
    "Clear all tags" : u"Убрать все метки",
    "Clear all toggle tags from the text" : u"Убрать все метки отключения блоков из текста",
    "Indent the selected lines" : u"Увеличить отступ выбранных строк",
    "Unindent the selected lines" : u"Уменьшить отступ выбранных строк",
    "Block comment" : u"Блоковый комментарий",
    "Comment or uncomment selected lines" : u"Закомментировать или раскомментировать выбранные строки",
    "Comment at start of a text style or uncomment" : u"", # New in v2.1.6
    "Style comment" : u"", # New in v2.1.6
    "Toggle current fold" : u"", # New in v2.1.6
    "Toggle the fold point On/OFF at the current line" : u"", # New in v2.1.6
    "Toggle all fold points On/OFF" : u"", # New in v2.1.6
    "Toggle all folds" : u"", # New in v2.0.2
    "&AviSynth function" : u"", # New in v2.2.0
    "Show list of filternames matching the partial text at the cursor" : u"Показать список имен фильтров, соответствующих части текста, выделенной курсором",
    "Autocomplete all" : u"", # New in v2.1.6
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"", # New in v2.1.6
    "Show calltip" : u"Показать подсказку", 
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"Показать подсказку по фильтру (работает только если курсор на аргументах)", 
    "Show function definition" : u"Показать определение функции",
    "Show the AviSynth function definition dialog for the filter" : u"Показать диалог опрелеления функции AviSynth для фильтра",
    "Filter help file" : u"Файл справки по фильтру", 
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"Вызвать файл справки по фильтру (работает только если курсор на аргументах или имя подсвечено)", 
    "&Miscellaneous" : u"", # New in v2.2.0
    "Move line up" : u"Передвинуть строку вверх", 
    "Move the current line or selection up by one line" : u"Передвинуть текущую строку или выбранное на одну позицию вверх", 
    "Move line down" : u"Передвинуть строку вниз", 
    "Move the current line or selection down by one line" : u"Передвинуть текущую строку или выбранное на одну позицию вниз", 
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"Копировать текущий скрипт без AvsP разметки (ползунков, меток) в буфер обмена", 
    "Copy unmarked script to clipboard" : u"Копировать неразмеченный скрипт в буфер обмена", 
    "Copy avisynth error to clipboard" : u"", # New in v2.1.6
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"", # New in v2.1.6
    "&Video" : u"&Видео",
    "Add/Remove bookmark" : u"Добавить/Удалить закладку",
    "Mark the current frame on the frame slider" : u"Пометить текущий кадр на ползунке кадров",
    "Clear all bookmarks" : u"Очистить все закладки",
    "Titled &bookmarks" : u"", # New in v2.2.0
    "Move the nearest titled bookmark to the current position. A historic title will be restored if it matches the condition." : u"", # New in v2.0.7
    "Move titled bookmark" : u"", # New in v2.0.7
    "Restore all historic titles" : u"", # New in v2.0.7
    "Restore historic titles" : u"", # New in v2.0.7
    "Clear all historic titles" : u"", # New in v2.0.7
    "Clear historic titles" : u"", # New in v2.0.7
    "Generate titles for untitled bookmarks by the pattern - 'Chapter %02d'" : u"Подписать закладку как 'Chapter %02d'", # New in v2.0.7
    "Set title (auto)" : u"Подписать (авто)",
    "Edit title for bookmarks in a list table" : u"Подписать закладку вручную",
    "Set title (manual)" : u"Подписать (вручную)",
    "&Navigate" : u"", # New in v2.2.0
    "Go to &bookmark" : u"", # New in v2.2.0
    "Go to next bookmarked frame" : u"Перейти к следующей закладке на кадрах",
    "Next bookmark" : u"Следующая закладка",
    "Go to previous bookmarked frame" : u"Перейти к предыдущей закдадке на кадрах",
    "Previous bookmark" : u"Предыдущая закладка",
    "Forward 1 frame" : u"Вперед на 1 кадр",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"Показать следующий видео кадр (горячая клавиша активна когда видео окно в фокусе)",
    "Backward 1 frame" : u"Назад на 1 кадр",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"Показать предыдущий видео кадр (горячая клавиша активна когда видео окно в фокусе)",
    "Forward 1 second" : u"Вперед на 1 секунду",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"Показать видео кадр на 1 секунду вперед (горячая клавиша активна когда видео окно в фокусе)",
    "Backward 1 second" : u"Назад на 1 секунду",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"Показать видео кадр на 1 секунду назад (горячая клавиша активна когда видео окно в фокусе)",
    "Forward 1 minute" : u"Вперед на 1 минуту",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"Показать видео кадр на 1 минуту вперед (горячая клавиша активна когда видео окно в фокусе)",
    "Backward 1 minute" : u"Назад на 1 минуту",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"Показать видео кадр на 1 минуту назад (горячая клавиша активна когда видео окно в фокусе)",
    "Forward x units" : u"Вперед на x единиц",
    "Jump forward by x units (you can specify x in the options dialog)" : u"Шаг вперед на x единиц (вы можете задать x в диалоге настроек)",
    "Backwards x units" : u"Назад на x единиц",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"Шаг назад на x единиц (вы можете задать x в диалоге настроек)",
    "Go to first frame" : u"К первому кадру",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"Идти к первому кадру (сочетание клавиш активно, если видео в фокусе)",
    "Go to last frame" : u"К последнему кадру",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"Идти к последнему кадру (сочетание клавиш активно, если видео в фокусе)",
    "Go to last scrolled frame" : u"Перейти к последнему прокрученному кадру",
    "Last scrolled frame" : u"Последний прокрученный кадр",
    "Enter a video frame or time to jump to" : u"Введите видео кадр или время для перемещения",
    "Go to frame..." : u"Перейти к кадру...",
    "Crop editor..." : u"Редактор обрезки Crop...",
    "Show the crop editor dialog" : u"Показать диалог редактора обрезки размеров кадра Crop",
    "&Trim selection editor" : u"", # New in v2.2.0
    "Show the trim selection editor dialog" : u"Показать диалог редактора выборки кадров Trim",
    "Show trim selection editor" : u"Показать редактор выборки Trim",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"Установить начало выборки (показывает редактор вырезки, если невидим)",
    "Set selection startpoint" : u"Установить начало выборки",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"Установить конец выборки (показывает редактор вырезки, если невидим)",
    "Set selection endpoint" : u"Установить конец выборки",
    "Zoom video preview to 25%" : u"Масштаб видео просмотра 25%", 
    "Zoom video preview to 50%" : u"Масштаб видео просмотра 50%", 
    "Zoom video preview to 100% (normal)" : u"Масштаб видео просмотра 100% (нормальный)",
    "Zoom video preview to 200%" : u"Масштаб видео просмотра 200%",
    "Zoom video preview to 300%" : u"Масштаб видео просмотра 300%",
    "Zoom video preview to 400%" : u"Масштаб видео просмотра 400%",
    "Zoom video preview to fill the entire window" : u"Изменить масштаб видео просмотра до заполнения полного окна",
    "Zoom video preview to fit inside the window" : u"Изменить масштаб видео просмотра до помещения внутри окна всего окна",
    "Enlarge preview image to next zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.1.6
    "Shrink preview image to previous zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.1.6
    "&Flip" : u"", # New in v2.2.0
    "Flip video preview upside down" : u"", # New in v2.1.6
    "Flip video preview from left to right" : u"", # New in v2.1.6
    "&YUV -> RGB" : u"", # New in v2.2.0
    "Swap chroma channels (U and V)" : u"", # New in v2.1.6
    "For YUV source, assume it is Rec601 (default)" : u"", # New in v2.0.7
    "For YUV source, assume it is PC.601" : u"", # New in v2.0.7
    "For YUV source, assume it is Rec709" : u"", # New in v2.0.7
    "For YUV source, assume it is PC.709" : u"", # New in v2.0.7
    "For YV12 only, assume it is progressive (default)" : u"", # New in v2.0.7
    "For YV12 only, assume it is interlaced" : u"", # New in v2.0.7
    "Save image as..." : u"Сохранить изображение как...",
    "Save the current frame as a bitmap" : u"Сохранить текущий кадр как файл картинки",
    "Force the script to reload and refresh the video frame" : u"Перезагрузить скрипт и обновить видео кадр",
    "Refresh preview" : u"Обновить просмотр",
    "Show/Hide the preview" : u"", # New in v2.2.0
    "Toggle the video preview" : u"Переключить просмотр видео",
    "Release all open videos from memory" : u"Выгрузить все открытые видео из памяти",
    "Release all videos from memory" : u"Выгрузить все видео из памяти",
    "Switch focus between the video preview and the text editor" : u"Переключить фокус между окнами видео просмотра и текстового редактора",
    "Switch video/text focus" : u"Переключить фокус видео/текст",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"Показать/скрыть колонку ползунков (двойной щелчок на разделителе имеет тот же эффект)", 
    "Toggle the slider sidebar" : u"Переключить колонку ползунков", 
    "External player" : u"Внешний проигрыватель",
    "Play the current script in an external program" : u"Проиграть текущий скрипт во внешней программе",
    "Show information about the video in a dialog box" : u"Показать информацию о видео в диалоговом окне",
    "Video information" : u"Информация о видео",
    "&Options" : u"&Опции",
    "Always on top" : u"Поверх других окон",
    "Keep this window always on top of others" : u"Всегда удерживать это окно поверх других окон",
    "Disable video preview" : u"Отключить видео превью", 
    "If checked, the video preview will not be shown under any circumstances" : u"Если отмечено, видео превью не будет показано ни при каких обстоятельствах", 
    "Associate .avs files with AvsP" : u"", # New in v2.1.6
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"", # New in v2.1.6
    "AviSynth function definition..." : u"Определения функций AviSynth...", 
    "Edit the various AviSynth script fonts and colors" : u"Редактировать различные шрифты и цвета скриптов AviSynth", 
    "Fonts and colors..." : u"Шрифты и цвета...", 
    "Edit the extension-based templates for inserting sources" : u"Редактировать шаблоны типов файлов для вставки источников",
    "Extension templates..." : u"Шаблоны расширений...", 
    "Configure the program keyboard shortcuts" : u"Конфигурировать сочетания клавиш быстрого выполнения",
    "Keyboard shortcuts..." : u"", # New in v2.2.0
    "Configure program settings" : u"Конфигурировать настройки программы",
    "Program settings..." : u"Настройки программы...",
    "&Help" : u"&Помощь",
    "Animated tutorial" : u"Анимированный урок",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"Смотреть анимированный урок по AvsP (с сайта AvsP)",
    "Learn more about AvsP text features (from the AvsP website)" : u"Узнать больше об текстовых особенностях AvsP",
    "Text features" : u"Текстовые особенности",
    "Learn more about AvsP video features (from the AvsP website)" : u"Узнать больше о видео особенностях AvsP",
    "Video features" : u"Видео особенности",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"Узнать больше о пользвательских ползунках AvsP",
    "User sliders" : u"Пользовательские ползунки",
    "Learn more about AvsP macros (from the AvsP website)" : u"Узнать больше о макросах AvsP",
    "Macros" : u"Макросы",
    "Avisynth help" : u"Справка AviSynth",
    "Open the avisynth help html" : u"Открыть html файл справки AviSynth",
    "Open Avisynth plugins folder" : u"Открыть папку плагинов AviSynth",
    "Open the avisynth plugins folder" : u"Открыть папку плагинов AviSynth",
    "About this program" : u"Об этой программе",
    "About AvsPmod" : u"О программе AvsPmod",
    "Previous frame" : u"Предыдущий кадр",
    "Next frame" : u"Следующий кадр",
    "Run the script with an external program" : u"Выполнить скрипт внешней программой",
    "Run the selected tool" : u"", # New in v2.0.2
    "&Tools" : u"", # New in v2.1.6
    "a macro check item" : u"", # New in v2.2.0
    "a macro radio item" : u"", # New in v2.2.0
    "Run selected macro" : u"Выполнить выбранный макрос",
    "View the readme for making macros" : u"Посмотреть справку по созданию макросов",
    "Open the macros folder" : u"Открыть папку макросов",
    "&Macros" : u"", # New in v2.1.6
    "Close" : u"Закрыть",
    "Rename" : u"", # New in v2.2.0
    "Save" : u"Сохранить",
    "Save as..." : u"Сохранить как...",
    "Copy to new tab" : u"Копировать в новую вкладку",
    "Reposition to" : u"", # New in v2.2.0
    "Crop editor" : u"Редактор обрезки",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"Вы можете перетаскивать область обрезки левой кнопкой мыши, когда этот диалог видимый, обрезая края ближайшие в начальному щелчку мышкой",
    "At script end" : u"В конце скрипта",
    "At script cursor" : u"В позиции курсора",
    "Copy to clipboard" : u"Копировать в буфер",
    "Insert Crop() command:" : u"Вставить команду обрезки Crop():",
    "Apply" : u"Применить ",
    "Trim editor" : u"Редактор вырезок Trim",
    "Selection options" : u"Опции выбора",
    "Keep selected regions" : u"Удерживать выбранные области",
    "Keep unselected regions" : u"Удерживать невыбранные области",
    "Mark video frames inside/outside selection" : u"Пометить видеокадры внути/вне выбранного",
    "Use Dissolve() with overlap frames:" : u"Использовать плавный переход, кадров:",
    "Insert Trim() commands:" : u"Вставить команду:",
    "Insert Dissolve() commands:" : u"Вставить команду:",
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"Используйте кнопки на ползунке превью для создания выборки кадров для вырезки.",
    "File does not exist!" : u"Файл не существует!", 
    "All files (*.*)|*.*" : u"Все файлы (*.*)|*.*",
    "Select a file" : u"Выбрать файл",
    "Create a separator label" : u"Создать метку разделителя",
    "Enter separator label" : u"Введите метку разделителя",
    "Enter tag name:" : u"Введите имя метки", 
    "Tag definition" : u"Определение метки", 
    "Chapter" : u"", # New in v2.0.7
    "Set title for bookmarks" : u"", # New in v2.0.7
    "Title" : u"", # New in v2.0.7
    "Frame No." : u"", # New in v2.0.7
    "Time **" : u"", # New in v2.0.7
    "" : u"", # New in v2.0.7
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"", # New in v2.1.6
    "Frame size:" : u"Размер кадра",
    "Length:" : u"Длина",
    "Frame rate:" : u"Частота кадров",
    "Colorspace:" : u"Цветовое пространство",
    "Field or frame based:" : u"Поля или целые кадры",
    "Parity:" : u"Четность",
    "Audio" : u"Аудио",
    "Channels:" : u"Каналов:",
    "Hz" : u"Гц",
    "Sampling rate:" : u"Частота отсчетов",
    "Sample type:" : u"Тип отсчетов",
    "bits" : u"бит",
    "samples" : u"отсчетов",
    "Could not find the macros folder!" : u"Не могу найти папку макросов!",
    "Could not find %(readme)s!" : u"Не могу найти %(readme)s!",
    "Failed to import the selected tool" : u"", # New in v2.0.2
    "You must restart for changes to take effect!" : u"Чтобы изменения вступили в силу, необходим перезапуск!",
    "Basic" : u"Базовые",
    "Default:" : u"По умолчанию:", 
    "Comment:" : u"Комментарий:", 
    "Block Comment:" : u"", # New in v2.1.6
    "__END__ Comment:" : u"", # New in v2.1.6
    "Number:" : u"Число:", 
    "Operator:" : u"Оператор:", 
    "String:" : u"Строка:", 
    "Triple-quoted string:" : u"Строка в тройных кавычках:", 
    "Internal filter:" : u"Внутренний фильтр:", 
    "External filter:" : u"Внешний фильтр:", 
    "Internal function:" : u"Внутренняя функция:", 
    "User defined function:" : u"Функция определенная пользователем:",
    "Clip property:" : u"Свойство клипа:", 
    "AviSynth keyword:" : u"Ключевое слово AviSynth:",
    "AviSynth data type:" : u"Тип данных AviSynth:",
    "AvsP user slider:" : u"AvsP пользовательский ползунок:",
    "Monospaced font:" : u"Моноширинный шрифт:", 
    "Advanced" : u"Дополнительные",
    "Incomplete string:" : u"Незавершенная строка:", 
    "Syntax highlight strings which are not completed in a single line differently" : u"Подсвечивать синтаксис строк, которые незавершены в одной строке другим образом", 
    "Brace highlight:" : u"Подсветка скобок:",
    "Bad brace:" : u"Плохая скобка:",
    "Bad number:" : u"Плохое число:",
    "Margin line numbers:" : u"Номера строк границы:",
    "Miscellaneous word:" : u"Различные слова:",
    "Calltip:" : u"Подсказка:",
    "Calltip highlight:" : u"Подстветка подсказки:",
    "Cursor:" : u"Курсор:",
    "Selection highlight:" : u"", # New in v2.2.0
    "Current line highlight:" : u"", # New in v2.2.0
    "Highlight the line that the caret is currently in" : u"Подсвечивать строку, на которой сейчас каретка", 
    "Fold margin:" : u"", # New in v2.1.6
    "Scrap window" : u"", # New in v2.2.0
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"", # New in v2.2.0
    "Use monspaced font" : u"", # New in v2.2.0
    "Insert aborted:" : u"Вставка прервана:",
    "No dot required in file extension!" : u"Точка не требуется в раcширении файла!",
    "Edit extension-based templates" : u"Редактировать основанные на расширении шаблоны",
    "File extension" : u"Расширение файла",
    "Template" : u"Шаблон",
    "This info is used for inserting sources based on file extensions." : u"Эта информация используется для вставки источников, основываясь на расширениях.",
    "Any instances of *** in the template are replaced with the filename." : u"Любое нахождение *** в шаблоне заменяется именем файла + полный путь к нему.",
    "(If you want relative paths instead of the full filename, use [***].)" : u"Если вы хотите использовать только имя файла, укажите [***] вместо ***.",
    "Associating .avs files will write to the windows registry." : u"", # New in v2.1.6
    "Do you wish to continue?" : u"Хотите продолжить?",
    "Could not find the Avisynth plugins folder!" : u"Не могу найти папку плагинов AviSynth!",
    "AvsPmod version %(version)s " : u"AvsPmod версия %(version)s ",
    "An AviSynth script editor" : u"Редактор скриптов AviSynth \n (автор qwerpoi, переводчик Fizick)",
    "AvsP Website" : u"AvsP WWW-сайт",
    "Active thread on Doom9's forum" : u"", # New in v2.1.6
    "This program is freeware under the GPL license." : u"Эта бесплатная программа распространяется на условиях GPL лицензии.",
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"", # New in v2.1.6
    "copy as time" : u"", # New in v2.1.6
    "copy" : u"", # New in v2.1.6
    "paste" : u"", # New in v2.1.6
    "clear history" : u"", # New in v2.1.6
    "Cannot switch tabs while crop editor is open!" : u"Не могу переключить вкладки если редактор обрезки активен!",
    "Cannot switch tabs while trim editor is open!" : u"Не могу переключить вкладки, если открыт редактор вырезок!",
    "pos" : u"поз",
    "rgb" : u"", # New in v1.3.7
    "rgba" : u"", # New in v1.3.8
    "yuv" : u"", # New in v1.3.7
    "hex" : u"", # New in v1.3.7
    "Invalid crop values detected.  Continue?" : u"Обнаружены недопустимые значения. Продолжить?",
    "You must create at least one frame selection first!" : u"Вы должны сначала создать по крайней мере одну выборку кадров!",
    "Select autocomplete keywords" : u"", # New in v2.1.6
    "exclude long names" : u"", # New in v2.2.0
    "Customize the video status bar message" : u"Настроить сообщение в полосе статуса видео",
    "Video status bar message:" : u"Сообщение статуса видео",
    "Legend" : u"Метка",
    "Current frame" : u"Текущий кадр",
    "Framecount" : u"Число кадров",
    "Current time" : u"Текущий кадр",
    "Total time" : u"Общее время",
    "Width" : u"Ширина",
    "Height" : u"Высота",
    "Aspect ratio" : u"Отношение сторон",
    "Framerate" : u"Частота кадров",
    "Framerate numerator" : u"Делимое частоты кадров",
    "Framerate denominator" : u"Делитель частоты кадров",
    "Colorspace" : u"Цветовое пространство",
    "Field or frame based" : u"Поля или целые кадры",
    "Parity" : u"Четность",
    "Parity short (BFF or TFF)" : u"Четность кратко (BFF или TFF)",
    "Audio rate" : u"Поток аудио",
    "Audio length" : u"Длина аудио",
    "Audio channels" : u"Каналов аудио:",
    "Audio bits" : u"Бит аудио",
    "Audio type (Integer or Float)" : u"Тип аудио (целый или вещественный)",
    "Pixel position (cursor based)" : u"Позиция пиксела (курсором)",
    "Pixel hex color (cursor based)" : u"16-ный цвет пиксела (курсором)",
    "Pixel rgb color (cursor based)" : u"RGB цвет (курсором)",
    "Pixel yuv color (cursor based)" : u"YUV цвет (курсором)",
    "Pixel color (auto-detect colorspace)" : u"Цвет пиксела (автоопределение формата)",
    "Program zoom" : u"Программный зум",
    "Save changes before closing?" : u"Сохранить изменения перед закрытием?",
    "Cannot create a new tab while crop editor is open!" : u"Не могу создать новую вкладку при открытом редакторе обрезки",
    "Cannot create a new tab while trim editor is open!" : u"Не могу создать новую вкладку при открытом редакторе вырезок",
    "AviSynth script (avs, avsi)|*.avs;*.avsi|Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"", # New in v2.0.2
    "Open a script or source" : u"Открыть скрипт или источник",
    "Reload the file and lose the current changes?" : u"Открыть файл заново с потерей всех внесенных изменений?",
    "Open this file" : u"Открыть этот файл",
    "Save session before closing all tabs?" : u"Сохранить сеанс перед закрытием всех вкладок?",
    "AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|All files (*.*)|*.*" : u"AviSynth скрипт (*.avs, *.avsi)|*.avs;*.avsi|Все файлы (*.*)|*.*",
    "Save current script" : u"Сохранить текущий скрипт",
    "Directory %(dirname)s does not exist!" : u"Папка %(dirname)s не существует",
    "Load a session" : u"Загрузить сеанс",
    "File has been modified since the session was saved. Reload?" : u"Файл был изменен с момента сохранения сеанса. Загрузить заново?",
    "Save the session" : u"Сохранить сеанс",
    "Save current frame" : u"Сохранить текущий кадр",
    "No image to save" : u"Нет изображения для сохранения",
    "Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"Файлы источников (%(extlist1)s)|*.%(extlist2)s|Все файлы (*.*)|*.*",
    "Insert a source" : u"Вставить источник",
    "AviSynth plugin (*.dll)|*.dll|All files (*.*)|*.*" : u"AviSynth плагин (*.dll)|*.dll|All files (*.*)|*.*",
    "Insert a plugin" : u"Вставить плагин",
    "No bookmarks defined!" : u"Нет определенных закладок!",
    "There must be more than one unique bookmark to use this feature!" : u"Должно быть более чем одна закладка для использования этой функции!",
    "Jump to specified bookmark" : u"Прыгнуть к указанной закладке",
    "Line: %(line)i  Col: %(col)i" : u"Строка: %(line)i  Колонка: %(col)i",
    "Frame Based" : u"Полные кадры",
    "Field Based" : u"Поля",
    "Bottom Field First" : u"Нижнее поле первое",
    "BFF" : u"BFF",
    "Top Field First" : u"Верхнее поле первое",
    "TFF" : u"TFF",
    "Integer" : u"Целое",
    "Float" : u"Вещественное",
    "Edit AviSynth function information" : u"Редактировать информацию по функции AviSynth", 
    "  Function name" : u"   Имя функции", 
    "Function arguments" : u"Аргументы функции", 
    "Open filter customization file" : u"Открыть файл настроек фильтра",
    "Calltip-only text file (*.txt)|*.txt" : u"", # New in v2.0.2
    "Filter customization file (*.tag)|*.tag" : u"Файл настроек фильтра (*.tag)|*.tag",
    "Invalid filter customization file!" : u"Негодный файл настроек фильтра!",
    "Save filter customization file" : u"Сохранить файл настроек фильтра",
    "Invalid argument!" : u"Неверный аргумент!",
    "Error loading AviSynth!" : u"Ошибка при запуске AviSynth!",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"Убедитесь, что AviSynth установлен, и что в папке плагинов AviSynth не находятся сбойные/нестабильные плагины или avsi-скрипты.",
    "Save changes before previewing?" : u"Сохранить изменения перед просмотром?", 
    "Executable files (*.exe)|*.exe|All files (*.*)|*.*" : u"Выполняемые файлы (*.exe)|*.exe|Все файлы (*.*)|*.*",
    "Select an external player" : u"Выберете внешний проигрыватель",
    "A program must be specified to use this feature!" : u"Для использования этой функции должна быть указана программа!",
    "General settings..." : u"Основные настройки...",
    "Invalid slider text: min > max" : u"Негодный текст ползунка:  min > max",
    "Invalid slider text: value not in bounds" : u"Негодный текст ползунка: величина вне диапазона",
    "Invalid slider text: bad modulo label" : u"Негодный текст ползунка: плохая метка",
    "Invalid slider text: slider label already exists" : u"Негодный текст ползунка: метка уже существует",
    "Invalid slider text: invalid number" : u"Негодный текст ползунка:",
    "Reset to initial value: %(value_formatted)s" : u"Сброс к начальному значению: %(value_formatted)s",
    "Reset to initial value: %(value2_formatted)s" : u"", # New in v2.2.0
    "Reset to default value: %(value_formatted)s" : u"Сброс к начальному значению: %(value_formatted)s",
    "Invalid hexadecimal color!" : u"Неправильный код цвета!",
    "Must specify a max value!" : u"Необходимо указать максимум!",
    "Must specify a min value!" : u"Необходимо указать минимум!",
    "Min value must be a number!" : u"Минимум - значение должно быть цифрой!",
    "Max value must be a number!" : u"Максимум - значение должно быть цифрой!",
    "Default value must be a number!" : u"Дефолтное значение должно быть цифрой!",
    "Step size value must be a number!" : u"Размер шага - значение должно быть цифрой!",
    "Left-click to select a color, right click to reset to default" : u"Левый клик - выбор цвета, правый клик - сброс на дефолт",
    "Source files (%(extlist1)s)|*.%(extlist2)s" : u"Исходные файлы (%(extlist1)s)|*.%(extlist2)s",
    "Toggle \"%(label)s\" section" : u"Блок \"%(label)s\" включен",
    "Don't show me this again" : u"", # New in v2.1.6
    "Save as" : u"Сохранить как",
    "Select a directory" : u"Выберите папку",
    "Enter information" : u"Введите информацию",
    "Progress" : u"Выполнение",
    "Error loading the script" : u"Ошибка загрузки скрипта",
    "Error in the macro:" : u"Ошибка в макросе:",
    "Couldn't find %(macrofilename)s" : u"Не могу найти %(macrofilename)s",
    "Failed to open the AVI file" : u"Ошибка при открытии AVI файла",
    "Failed to open the AVI frame" : u"Ошибка при открытии кадра из AVI файла",
    "Failed to retrieve AVI frame" : u"Ошибка при получении кадра из AVI файла",
    "Ctrl" : u"",
    "Alt" : u"",
    "Shift" : u"",
    "Program Settings" : u"Настройки программы",
    "Browse" : u"Обзор",
    "* Requires program restart for full effect" : u"* Требуется перезапуск программы",
    "Invalid directory!" : u"Негодная папка!",
    "Invalid filename!" : u"Негодное имя файла!",
    "Edit shortcuts" : u"Редактировать сочетания клавиш",
    "Menu label" : u"Пункт меню",
    "Keyboard shortcut" : u"Сочетание клавиш",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"Для изменения - двойной щелчок или нажмите Enter на пункте",
    "Shortcut" : u"", # New in v2.1.6
    "Action" : u"", # New in v2.1.6
    "Edit the keyboard shortcut" : u"Редактировать сочетание клавиш быстрого запуска",
    "Key:" : u"Клавиша:",
    "Clear" : u"Очистить",
    "%(keyString)s not found in key string list" : u"%(keyString)s не найдена в списке сочетаний клавиш",
    "This shortcut is being used by:" : u"Это сочетание клавиш используется как:",
    "Insert" : u"Вставить",
    "Delete" : u"Удалить",
    "Error: key %(key)s does not exist!" : u"Ошибка: пункт %(key)s не существует!",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"Вы уверены, что хотите переименовать %(oldName)s в %(newName)s?",
    "Question" : u"Вопрос",
    "Insert a new item" : u"Вставьте новый пункт",
    "Must enter a name!" : u"Должны ввести имя!",
    "Item %(newKey)s already exists!" : u"Пункт %(newKey)s уже существует",
    "Warning: no value entered for item %(newKey)s!" : u"Предупреждение: не введедена величина для пункта  %(newKey)s!",
    "Message" : u"Сообщение",
    "Select an item to delete first" : u"Для удаления сначала выберете пункт",
    "Are you sure you want to delete item %(key)s?" : u"Вы уверены, что хотите удалить пункт %(key)s?",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"", # New in v2.0.7
    "Calculate an appropriate resize for the video" : u"", # New in v2.0.7
    "Resize calculator" : u"", # New in v2.0.7
    "Input" : u"", # New in v2.0.7
    "Video resolution:" : u"", # New in v2.0.7
    "Pixel aspect ratio:" : u"", # New in v2.0.7
    "Results" : u"", # New in v2.0.7
    "Aspect ratio error:" : u"", # New in v2.0.7
    "Settings" : u"", # New in v2.0.7
    "Target pixel aspect ratio:" : u"", # New in v2.0.7
    "Resize block constraints:" : u"", # New in v2.0.7
    "Resize percent ranges:" : u"", # New in v2.0.7
    "Max search aspect ratio error:" : u"", # New in v2.0.7
    "Configure" : u"", # New in v2.0.7
    "compute from .d2v" : u"", # New in v2.0.7
    "Configure options" : u"", # New in v2.0.7
    "Avisynth resize:" : u"", # New in v2.0.7
    "The current Avisynth script contains errors." : u"", # New in v2.0.7

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"Сохранить в MP4...",
    "Encode the current script using x264" : u"Кодировать текущий скрипт используя x264",
    "Encode video" : u"Кодировать",
    "System settings" : u"Системные настройки",
    "Input file:" : u"", # New in v2.0.7
    "Output file:" : u"", # New in v2.0.7
    "Compression settings" : u"Настройки сжатия",
    "Bitrate (kbits/sec):" : u"", # New in v2.0.7
    "calculate" : u"", # New in v2.0.7
    "Quality CRF (0-51):" : u"", # New in v2.0.7
    "Quality CQ (1-31):" : u"", # New in v2.0.7
    "Additional settings" : u"", # New in v2.0.7
    "Credits start frame:" : u"", # New in v2.0.7
    "Command line settings" : u"", # New in v2.0.7
    "Run" : u"", # New in v2.0.7
    "First time using this compression preset!" : u"", # New in v2.0.7
    "Please enter the exe paths in the following dialog." : u"", # New in v2.0.7
    "Exe pathnames" : u"", # New in v2.0.7
    "Open an AviSynth script" : u"", # New in v2.0.7
    "AviSynth script (*.avs)|*.avs" : u"", # New in v2.0.7
    "Save the video as" : u"", # New in v2.0.7
    "Select a program" : u"", # New in v2.0.7
    "Program (*.exe)|*.exe" : u"", # New in v2.0.7
    "Unreplaced items remain in the command line:" : u"", # New in v2.0.7
    "Unknown exe paths!" : u"", # New in v2.0.7
    "General" : u"Общие",
    "Credits warning minutes:" : u"", # New in v2.0.7
    "Automatically compute bitrate value on startup" : u"", # New in v2.0.7
    "Automatically compute pixel aspect ratio from d2v on startup" : u"", # New in v2.0.7
    "Append batch commands to the avs script as comments" : u"", # New in v2.0.7
    "Encoder priority:" : u"", # New in v2.0.7
    "Path to %(name)s:" : u"", # New in v2.0.7
    "Extra arguments:" : u"", # New in v2.0.7
    "Bitrate Calculator" : u"", # New in v2.0.7
    "Output info" : u"", # New in v2.0.7
    "Total size:" : u"", # New in v2.0.7
    "Container:" : u"", # New in v2.0.7
    "(None)" : u"", # New in v2.0.7
    "Video info" : u"", # New in v2.0.7
    "Framecount:" : u"", # New in v2.0.7
    "FPS:" : u"", # New in v2.0.7
    "Audio info" : u"", # New in v2.0.7
    "Audio file:" : u"", # New in v2.0.7
    "Compress audio" : u"", # New in v2.0.7
    "Audio bitrate:" : u"", # New in v2.0.7
    "Format:" : u"", # New in v2.0.7
    "Subtitles info" : u"", # New in v2.0.7
    "Subtitles file:" : u"", # New in v2.0.7
    "Total time:" : u"", # New in v2.0.7
    "Video size:" : u"", # New in v2.0.7
    "Audio size:" : u"", # New in v2.0.7
    "Subtitles size:" : u"", # New in v2.0.7
    "Overhead size:" : u"", # New in v2.0.7
    "Bitrate:" : u"", # New in v2.0.7
    "Open the audio file" : u"", # New in v2.0.7
    "Open the subtitles file" : u"", # New in v2.0.7
    "%(h)i hr and %(m)i min" : u"", # New in v2.0.7

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"", # New in v2.0.7
    "Use avs2avi to save the current script as an avi" : u"", # New in v2.0.7
    "Please select the path to avs2avi.exe" : u"", # New in v2.0.7
    "Error: avs2avi is required to save an avi!" : u"", # New in v2.0.7
    "Pass: %(pass)s / %(passes)s" : u"", # New in v2.0.7
    "Frame: %(frame)i / %(frames)i" : u"", # New in v2.0.7
    "Size: %(size).2f MB" : u"", # New in v2.0.7
    "FPS: %(fps).1f fps" : u"", # New in v2.0.7
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"", # New in v2.0.7
    "Input file (.avs):" : u"", # New in v2.0.7
    "Output file (.avi):" : u"", # New in v2.0.7
    "# of passes:" : u"", # New in v2.0.7
    "Priority:" : u"", # New in v2.0.7
    "Error: Unknown button" : u"", # New in v2.0.7
    "Save the avi as" : u"", # New in v2.0.7
    "Avi file (*.avi)|*.avi" : u"", # New in v2.0.7
    "Input file does not exist!" : u"", # New in v2.0.7
    "Input file must be an avisynth script!" : u"", # New in v2.0.7
    "Output path does not exist!" : u"", # New in v2.0.7
    "# of passes must be an integer!" : u"", # New in v2.0.7
    "Priority must be an integer!" : u"", # New in v2.0.7
    "Stop" : u"", # New in v2.0.7
    "Done" : u"", # New in v2.0.7
    "Process stopped." : u"", # New in v2.0.7
    "Processing..." : u"", # New in v2.0.7
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"", # New in v2.0.7
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"", # New in v2.0.7
    "Finished in %(time).1f seconds." : u"", # New in v2.0.7
    "Filesize: %(size).2f MB" : u"", # New in v2.0.7
    "The current script contains errors, exiting." : u"", # New in v2.0.7
    "Save as AVI" : u"", # New in v2.0.7
}