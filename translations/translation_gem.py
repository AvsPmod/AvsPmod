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

# Übersetzt von Henrik . AvsP 1.4.0  Danke an Forum Gleitz für die Hilfe, besonders LigH ,doxville,Brother John, Selur und Rippraff !

version = "2.2.1"

messages = {
    "Find" : u"Suchen",
    "Replace" : u"Ersetzen",
    "Cannot find \"%(text)s\"." : u"Nicht gefunden \"%(text)s\".",
    "Information" : u"Information",
    "Replace Information" : u"Information ersetzten",
    "Replaced %(count)i times" : u"Ersetzt %(count)i mal",
    "AviSynth fonts and colors" : u"Avisynthschriftarten und Farben",
    "Background" : u"Hintergrund",
    "Font" : u"Schriftarten",
    "Text color" : u"Textfarbe",
    "OK" : u"OK",
    "Cancel" : u"Abbrechen",
    "Scrap Window" : u"Ablagefenster",
    "Undo" : u"Rückgängig",
    "Redo" : u"Wiederherstellen",
    "Cut" : u"Ausschneiden",
    "Copy" : u"Kopieren",
    "Paste" : u"Einfügen",
    "Select all" : u"Alles auswählen",
    "Refresh" : u"Erneuern",
    "Insert frame #" : u"Eingabe Einzelbild #",
    "Save to file..." : u"Datei speichern als...",
    "Clear all" : u"Alles löschen",
    "Toggle scrap window" : u"Ablage Fenster umschalten",
    "Save script" : u"Speichere Script",
    "Error: no contextMenu variable defined for window" : u"Fehler: Keine contextMenu-Variable definiert für Window",
    "Text document (*.txt)|*.txt|All files (*.*)|*.*" : u"Textdokument (*.txt)|*.txt|Alle Dateien (*.*)|*.*",
    "Save scrap text" : u"Ablagetext speichern",
    "This field must contain a value!" : u"Dieses Feld muss einen Wert enthalten!",
    "This slider label already exists!" : u"Bezeichnung für den Schieberegler existiert schon",
    "Invalid slider label modulo syntax!" : u"Ungültiger Syntax des Modulo im Schiebereglertitel!",
    "This field must contain a number!" : u"Dieses Feld muss eine Zahl enthalten!",
    "The min value must be less than the max!" : u"Der Min Wert muss weniger als der Max sein!",
    "The initial value must be between the min and the max!" : u"Der anfängliche Wert muss zwischen dem Min und dem Max sein!",
    "The min value must be a multiple of %(mod)s!" : u"Der min Wert muss ein Vielfaches sein von %(mod)s!",
    "The max value must be a multiple of %(mod)s!" : u"Der max Wert muss ein Vielfaches sein von %(mod)s!",
    "The initial value must be a multiple of %(mod)s!" : u"",
    "The difference between the min and max must be greater than %(mod)s!" : u"Der anfängliche Wert muss ein Vielfaches sein von %(mod)s",
    "Error" : u"Fehler",
    "Define user slider" : u"Definiere Anwenderschieberegler",
    "Slider label:" : u"Schiebereglerbezeichnung",
    "Min value:" : u"Min Wert:",
    "Max value:" : u"Max Wert:",
    "Initial value:" : u"Anfänglicher Wert:",
    "Add or override AviSynth functions in the database" : u"", # New in v2.2.1
    "Core filters" : u"", # New in v2.2.1
    "Plugins" : u"", # New in v2.2.1
    "User functions" : u"", # New in v2.2.1
    "Script functions" : u"", # New in v2.2.1
    "Clip properties" : u"", # New in v2.2.1
    "Include %(title)s in autcompletion lists" : u"", # New in v2.2.1
    "New function" : u"", # New in v2.2.1
    "Edit selected" : u"", # New in v2.2.1
    "Delete selected" : u"", # New in v2.2.1
    "Select installed" : u"", # New in v2.2.1
    "Import from files" : u"", # New in v2.2.1
    "Export customizations" : u"", # New in v2.2.1
    "Clear customizations" : u"", # New in v2.2.1
    "Clear manual presets" : u"", # New in v2.2.1
    "When importing, don't show the choice dialog" : u"", # New in v2.2.1
    "Edit function information" : u"", # New in v2.2.1
    "Name:" : u"", # New in v2.2.1
    "Type:" : u"", # New in v2.2.1
    "clip property" : u"Clipeigenschaft",
    "core filter" : u"", # New in v2.2.1
    "plugin" : u"", # New in v2.2.1
    "script function" : u"", # New in v2.2.1
    "user function" : u"", # New in v2.2.1
    "Arguments:" : u"", # New in v2.2.1
    "define sliders" : u"", # New in v2.2.1
    "reset to default" : u"", # New in v2.2.1
    "Slider information" : u"", # New in v2.2.1
     "Preset:" : u"Voreinstellungen",
    "Auto-generate" : u"", # New in v2.2.1
    "Filter name already exists!" : u"", # New in v2.2.1
    "Invalid filter name!" : u"", # New in v2.2.1
    "Renaming not allowed!" : u"", # New in v2.2.1
    "You must use dllname_function naming format for plugins!" : u"", # New in v2.2.1
    "Open Customization files, Avisynth scripts or Avsp options files" : u"", # New in v2.2.1
    "All supported|*.txt;*.avsi;*.avs;*.dat|Customization file (*.txt)|*.txt|AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|AvsP data (*.dat)|*.dat|All files (*.*)|*.*" : u"", # New in v2.2.1
    "Unrecognized files" : u"", # New in v2.2.1
    "Select import functions" : u"", # New in v2.2.1
    "select all" : u"", # New in v2.2.1
    "select none" : u"", # New in v2.2.1
    "select all (file only)" : u"", # New in v2.2.1
    "select none (file only)" : u"", # New in v2.2.1
    "Red - a customized function already exists." : u"", # New in v2.2.1
    "No customizations to export!" : u"", # New in v2.2.1
    "Save filter customizations" : u"", # New in v2.2.1
    "Customization file (*.txt)|*.txt|All files (*.*)|*.*" : u"", # New in v2.2.1
    "This will delete all filter customizations. Continue?" : u"", # New in v2.2.1
    "Warning" : u"Warnung",
    "This will delete all manually defined presets. Continue?" : u"", # New in v2.2.1
    "Do you want to delete this custom filter entirely?" : u"", # New in v2.2.1
    "Edit filter database" : u"Filterdatenbank bearbeiten",
    "Default" : u"Standard",
    "Min value" : u"Mindestwert",
    "Max value" : u"Maximalwert",
    "Step size" : u"Schrittgröße",
    "Value list (comma separated)" : u"Werteliste (durch Komma getrennt)",
    "Value must be True or False!" : u"Wert muß zutreffend (wahr), oder falsch sein!",
    "Must enter a value list!" : u"Eine Werteliste muß eingetragen werden!",
    "Export filter customizations" : u"Filteranpassungen exportieren",
    "Import filter customizations" : u"Filteranpassungen importieren",
    "Select filters to export:" : u"Filterauswahl exportieren:",
    "Select filters to import from the file:" : u"Filterauswahl von/aus der Datei importieren:",
    "Overwrite all data" : u"Überschreibe alle Daten",
    "You must select at least one filter!" : u"Mindestens ein Filter muß ausgewählt werden",
    "Error: minValue must be less than maxValue" : u"Fehler: Min Wert muss weniger sein als Max Wert",
    "New File" : u"Datei neu",
    "Windows Bitmap (*.bmp)" : u"",
    "Animation (*.gif)" : u"", # New in v2.2.1
    "JPEG (*.jpg)" : u"",
    "Zsoft Paintbrush (*.pcx)" : u"", # New in v2.2.1
    "Portable Network Graphics (*.png)" : u"",
    "Netpbm (*.pnm)" : u"", # New in v2.2.1
    "Tagged Image File (*.tif)" : u"", # New in v2.2.1
    "ASCII Text Array (*.xpm)" : u"", # New in v2.2.1
    "Windows Icon (*.ico)" : u"", # New in v2.2.1
    "fps" : u"fps (Bilder pro Sekunde)",
    "Frame" : u"Einzelbild",
    "A crash detected at the last running!" : u"", # New in v2.2.1
    "&Zoom" : u"", # New in v2.2.1
    "%s translation file updated with new messages to translate" : u"", # New in v2.2.1
    "Translation updated" : u"", # New in v2.2.1
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.2.1
    "%s language couldn't be loaded" : u"", # New in v2.2.1
    "Paths" : u"", # New in v2.2.1
    "AvsP help directory:" : u"AvsP Hilfe-Verzeichnis",
    "Location of the AvsP help directory" : u"Ort des AvsP Hilfe-Verzeichnis",
    "Avisynth directory:" : u"Avisynthverzeichnis:",
    "Location of the avisynth installation directory" : u"Installationverzeichnis von Avisynth",
    "Avisynth help file/url:" : u"Avisynth-Hilfedatei/url",
    "Location of the avisynth help file or url" : u"Avisynthverzeichnis der Hilfedatei oder url",
    "External player:" : u"Externer Player:",
    "Location of external program for script playback" : u"Verzeichnis des externen Programms für Scriptplayback",
    "Additional arguments when running the external player" : u"Zusätzliche Parameter zum Abspielen im externen Player ",
    "External player extra args:" : u"Zusätzliche Parameter ext.Player",
    "Documentation search paths:" : u"Suchpfad für Dokumentation",
    "Specify which directories to search for docs when you click on a filter calltip" : u"In welchem Verzeichnis sollen DOCS-Dateien gesucht werden, wenn Filtercalltips angeklickt werden",
    "Documentation search url:" : u"", # New in v2.2.1
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"", # New in v2.2.1
    "Text" : u"", # New in v2.2.1
    "Show filter calltips" : u"Zeige Filtercalltips",
    "Turn on/off automatic tips when typing filter names" : u"Ein/Aus von automatischen Tips ,während Filternamen geschrieben werden",
    "Always show calltips any time the cursor is within the filter's arguments" : u"Immer und zu jeder Zeit Calltips zeigen,wenn der Cursor innerhalb der Filterargumente steht",
    "Frequent calltips" : u"Häufigste Calltips",
    "Syntax highlighting" : u"Syntaxhervorhebung",
    "Turn on/off avisynth-specific text colors and fonts" : u"Ein/Aus von Avisynth spezifischen Textenfarben und Schriftarten",
    "Show autocomplete on capital letters" : u"", # New in v2.2.1
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"Ein/Aus von Autovervollständigungsliste beim Wortanfang mit Grossbuchstaben",
    "Show autocomplete list when typing a certain amount of letters" : u"", # New in v2.2.1
    "Don't allow lines wider than the window" : u"Zeilen auf Fenstergröße begrenzen", 
    "Wrap text" : u"Textumbruch",
    "Draw lines at fold points" : u"", # New in v2.2.1
    "For code folding, draw a line underneath if the fold point is not expanded" : u"", # New in v2.2.1
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Kontrollie des Tabulatorenschlüssel ,um aktuelle Tabulatoren anstatt Zwischenräume einzufügen",
    "Use tabs instead of spaces" : u"Tabulatoren statt Leerzeichen verwenden",
    "Set the size of the tabs in spaces" : u"Einstellung der Grösse für Zwischenräume",
    "Tab width" : u"Tab Breite",
    "Initial space to reserve for the line margin in terms of number of digits" : u"Wieviel Stellen von Leerzeichen für den Seitenrandabstand der Zeile ",
    "Line margin width" : u"Zeilenrand Grösse",
    "Autocomplete" : u"Autovervollständigung",
    "Add user defined variables into autocomplete list" : u"", # New in v2.2.1
    "Show autocomplete with variables" : u"", # New in v2.2.1
    "Show autocomplete on single matched lowercase variable" : u"", # New in v2.2.1
    "When typing a lowercase variable name, show autocomplete if there is only one item matched in keyword list" : u"", # New in v2.2.1
    "Add icons into autocomplete list. Using different type to indicate how well a filter's presets is defined" : u"", # New in v2.2.1
    "Show autocomplete with icons" : u"", # New in v2.2.1
    "Don't show autocomplete when calltip is active" : u"", # New in v2.2.1
    "When calltip is active, autocomplete will not be activate automatically. You can still show autocomplete manually" : u"", # New in v2.2.1
    "Customize autocomplete keyword list..." : u"", # New in v2.2.1
    "Customize the keyword list shown in the autocomplete choice box" : u"", # New in v2.2.1
    "Autoparentheses level" : u"Stufe der Auto-Klammervervollständigung",
    "Close \"()\"" : u"Schliessen \"()\"",
    "Determines parentheses to insert upon autocompletion" : u"Beendet Auto-Klammervervollständigung um Autovervollständigung einzufügen",
    "None \" \"" : u"Nichts \" \"",
    "Open \"(\"" : u"Öffnen",
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"", # New in v2.2.1
    "None" : u"", # New in v2.2.1
    "Preset activation key" : u"", # New in v2.2.1
    "Return" : u"", # New in v2.2.1
    "Tab" : u"", # New in v2.2.1
    "Video" : u"Video",
    "Constantly update video while dragging" : u"Ständiges updaten des Videos durch Computermouseaktionen (dragging)",
    "Update the video constantly when dragging the frame slider" : u"Ständiges updaten des des Schiebereglers durch Computermouseaktionen(dragging)",
    "Enable line-by-line update" : u"Erlaube Zeile für Zeile Update",
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"Erlaube den Zeile für Zeile Video Updatemodus (Update bei jeder Cursoränderung in der Zeile)",
    "Focus the video preview upon refresh" : u"Fokussieren der Video-Vorschaufunktion bei Neuanzeige",
    "Switch focus to the video preview window when using the refresh command" : u"Schaltet den Fokus auf das Video-Vorschaufunktionsfenster um, wenn der Neuanzeigenbefehl verwenden wird",
    "Refresh preview automatically" : u"", # New in v2.2.1
    "Refresh preview when switch focus on video window or change a value in slider window" : u"", # New in v2.2.1
    "Seeking to a certain frame will seek to that frame on all tabs" : u"", # New in v2.2.1
    "Shared timeline" : u"", # New in v2.2.1
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"", # New in v2.2.1
    "Allow AvsPmod to resize the window" : u"", # New in v2.2.1
    "Separate video preview window" : u"Separiere Video-Vorschaufunktionsfenster",
    "Use a separate window for the video preview" : u"Ein separates Fenster für die Video-Vorschaufunktion benutzen", 
    "Min text lines on video preview" : u"Min Textzeilen der Video-Vorschaufunktion",
    "Minimum number of lines to show when displaying the video preview" : u"Minimalanzahl von Zeilen der Video-Vorschaufunktion",
    "Customize the video information shown in the program status bar" : u"Anpassen der Videoinformationen , die in der Programm-Status-Bar gezeigt werden",
    "Customize video status bar..." : u"Anpassen der Video-Status-Bar",
    "User Sliders" : u"Benutzer-Schieberegler",
    "Hide slider window by default" : u"", # New in v2.2.1
    "Keep the slider window hidden by default when previewing a video" : u"", # New in v2.2.1
    "Create user sliders automatically" : u"Benutzer-Schieberegler automatisch erstellen",
    "Create user sliders automatically using the filter database" : u"Benutzer-Schieberegler, der die Filterdatenbank verwendet, automatisch erstellen, ",
    "Create user sliders for int and float arguments" : u"Benutzer-Schieberegler für int und float Argumente erstellen",
    "type int/float (numerical slider)" : u"Eingabe int/float (numerischer Schieberegler)",
    "Create color pickers for hex color arguments" : u"Farb-Pipette für Hex Argumente erstellen",
    "type int (hex color)" : u"Eingabe int (hex Farbe)",
    "Create radio boxes for bool arguments" : u"Radio boxen (Dialogfeld) für boolsche Argumente erstellen",
    "type bool" : u"Eingabe bool",
    "Create listboxes for string list arguments" : u"Listboxen für Stringlisten Argumente erstellen",
    "type string (list)" : u"Eingabe string (Liste)",
    "Create filename pickers for string filename arguments" : u"Dateinamenausleser erstellen, zur Ausgabe von Dateinamen als String Argument",
    "type string (filename)" : u"Eingabe string  (Dateiname)",
    "Create placeholders for arguments which have no database information" : u"Platzhalter für Argumente erstellen, die keine Datenbankinformationen haben",
    "undocumented" : u"Undokumentiert",
    "Determines which filters will initially have hidden arguments in the slider window" : u"Stellt zuerst fest, welche Filter versteckt Argumente im Schiebereglerfenster haben",
    "Fold all" : u"Alle eingeklappt",
    "Fold non-numbers" : u"Nichtnumerische eingeklappt",
    "Fold none" : u"Alle ausgeklappt",
    "Fold startup setting" : u"Filterparameter Ein-/Ausklappen",
    "Filter exclusion list:" : u"Filterausschlußliste",
    "Specify filters never to build automatic sliders for" : u"Spezifiziert Filter, für die kein automatischer Schieberegler erstellt wird.",
    "Save/Load" : u"", # New in v2.2.1
    "Automatically save the session on shutdown and load on next startup" : u"Automatisches speichern bei Sessionende und laden beim nächsten Start",
    "Save session for next launch" : u"Speichere Session für den nächsten Start",
    "Always load startup session" : u"Immer Startup Sessions laden",
    "Always load the auto-saved session before opening any other file on startup" : u"Immer automatisch gespeicherte Sessions laden,anstelle einer anderen Datei.",
    "Always hide the video preview window when loading a session" : u"", # New in v2.2.1
    "Don't preview when loading a session" : u"", # New in v2.2.1
    "Backup session when previewing" : u"", # New in v2.2.1
    "If checked, the current session is backed up prior to previewing any new script" : u"Die aktuelle Session wird gespeichert ehe ein neues Script gezeigt wird",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"Eingabeaufforderung zum Speichern eines Scripts vor der Vorschau (Inaktiv bei Script-Vorschaufunktion mit ungesicherten Änderungen)",
    "Prompt to save when previewing" : u"Eingabeaufforderung zum Speichern wenn die Vorschaufunktion läuft",
    "Create a temporary preview script with unsaved changes when previewing the video" : u"Erstellen einer Script Vorschau mit ungesicherten Änderungen ,während der Video-Vorschaufunktion", 
    "Preview scripts with unsaved changes" : u"", # New in v2.2.1
    "Prompt to save each script with unsaved changes when exiting the program" : u"Eingabeaufforderung beim verlassen des Programms, zum Speichern jedes Scripts, bei ungesicherten Änderungen,",
    "Prompt to save scripts on program exit" : u"Eingabeaufforerung zum Speichern des Scripts bei Programmende.",
    "Save *.avs scripts with AvsPmod markings" : u"", # New in v2.2.1
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"", # New in v2.2.1
    "Misc" : u"Sonstiges",
    "Choose the language used for the interface" : u"", # New in v2.2.1
    "Language *" : u"", # New in v2.2.1
    "Show keyboard images in the script tabs when video has focus" : u"", # New in v2.2.1
    "Use keyboard images in tabs" : u"", # New in v2.2.1
    "Show tabs in multiline style" : u"", # New in v2.2.1
    "There can be several rows of tabs" : u"", # New in v2.2.1
    "All tabs will have same width" : u"", # New in v2.2.1
    "Show tabs in fixed width" : u"", # New in v2.2.1
    "Enable scroll wheel through similar tabs" : u"", # New in v2.2.1
    "Mouse scroll wheel cycles through tabs with similar videos" : u"", # New in v2.2.1
    "Only allow a single instance of AvsPmod" : u"", # New in v2.2.1
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"", # New in v2.2.1
    "Show warning for bad plugin naming at startup" : u"", # New in v2.2.1
    "Max number of recent filenames" : u"Max.Anzahl neuer Dateinamen",
    "This number determines how many filenames to store in the recent files menu" : u"Diese Zahl stellt fest wieviele Dateinamen im FileMenue gespeichert werden", 
    "Custom jump size:" : u"Eigene Sprungweite ",
    "Jump size used in video menu" : u"Sprungweite beim Videomenue",
    "Custom jump size units" : u"Spungweiten-Einheiten",
    "Units of custom jump size" : u"Einheiten der Sprungweiten",
    "hours" : u"Stunden",
    "minutes" : u"Minuten", 
    "seconds" : u"Sekunden",
    "frames" : u"Einzelbilder",
    "Extend selection to line down position" : u"", # New in v2.2.1
    "Scroll down" : u"", # New in v2.2.1
    "Extend rectangular selection to line down position" : u"", # New in v2.2.1
    "Extend selection to line up position" : u"", # New in v2.2.1
    "Scroll up" : u"", # New in v2.2.1
    "Extend rectangular selection to line up position" : u"", # New in v2.2.1
    "Go to previous paragraph" : u"", # New in v2.2.1
    "Extend selection to previous paragraph" : u"", # New in v2.2.1
    "Go to next paragraph" : u"", # New in v2.2.1
    "Extend selection to next paragraph" : u"", # New in v2.2.1
    "Extend selection to previous character" : u"", # New in v2.2.1
    "Go to previous word" : u"", # New in v2.2.1
    "Extend selection to previous word" : u"", # New in v2.2.1
    "Extend rectangular selection to previous character" : u"", # New in v2.2.1
    "Extend selection to next character" : u"", # New in v2.2.1
    "Go to next word" : u"", # New in v2.2.1
    "Extend selection to next word" : u"", # New in v2.2.1
    "Extend rectangular selection to next character" : u"", # New in v2.2.1
    "Go to previous word part" : u"", # New in v2.2.1
    "Extend selection to previous word part" : u"", # New in v2.2.1
    "Go to next word part" : u"", # New in v2.2.1
    "Extend selection to next word part" : u"", # New in v2.2.1
    "Extend selection to start of line" : u"", # New in v2.2.1
    "Go to start of document" : u"", # New in v2.2.1
    "Extend selection to start of document" : u"", # New in v2.2.1
    "Go to start of line" : u"", # New in v2.2.1
    "Extend selection to end of line" : u"", # New in v2.2.1
    "Go to end of document" : u"", # New in v2.2.1
    "Extend selection to end of document" : u"", # New in v2.2.1
    "Go to end of line" : u"", # New in v2.2.1
    "Extend selection to previous page" : u"", # New in v2.2.1
    "Extend rectangular selection to previous page" : u"", # New in v2.2.1
    "Extend selection to next page" : u"", # New in v2.2.1
    "Extend rectangular selection to next page" : u"", # New in v2.2.1
    "Delete to end of word" : u"", # New in v2.2.1
    "Delete to end of line" : u"", # New in v2.2.1
    "Delete back" : u"", # New in v2.2.1
    "Delete to start of word" : u"", # New in v2.2.1
    "Delete to start of line" : u"", # New in v2.2.1
    "Cancel autocomplete or calltip" : u"", # New in v2.2.1
    "Indent selection" : u"Auswahl Text einrücken",
    "Unindent selection" : u"Auswahl Text nicht einrücken",
    "Newline" : u"", # New in v2.2.1
    "Zoom in" : u"", # New in v2.2.1
    "Zoom out" : u"", # New in v2.2.1
    "Reset zoom level to normal" : u"", # New in v2.2.1
    "Line cut" : u"", # New in v2.2.1
    "Line delete" : u"", # New in v2.2.1
    "Line copy" : u"", # New in v2.2.1
    "Transpose line with the previous" : u"", # New in v2.2.1
    "Line or selection duplicate" : u"", # New in v2.2.1
    "Convert selection to lowercase" : u"", # New in v2.2.1
    "Convert selection to uppercase" : u"", # New in v2.2.1
    "Sort bookmarks ascending" : u"", # New in v2.2.1
    "sort ascending" : u"", # New in v2.2.1
    "Show bookmarks with timecode" : u"", # New in v2.2.1
    "show time" : u"", # New in v2.2.1
    "Show bookmarks with title" : u"", # New in v2.2.1
    "show title" : u"", # New in v2.2.1
    "Rec601" : u"", # New in v2.2.1
    "PC.601" : u"", # New in v2.2.1
    "Rec709" : u"", # New in v2.2.1
    "PC.709" : u"", # New in v2.2.1
    "Progressive" : u"", # New in v2.2.1
    "Interlaced" : u"", # New in v2.2.1
    "Swap UV" : u"", # New in v2.2.1
    "25%" : u"25%",
    "50%" : u"50%",
    "100% (normal)" : u"100% (Normal)",
    "200%" : u"200%",
    "300%" : u"300%",
    "400%" : u"400%",
    "Fill window" : u"Fenster ausfüllen",
    "Fit inside window" : u"Im Fenster anpassen", 
    "Vertically" : u"", # New in v2.2.1
    "Horizontally" : u"", # New in v2.2.1
    "&File" : u"&Datei",
    "Create a new tab" : u"Neuen Tab erstellen",
    "New tab" : u"Neuer Tab",
    "Open an existing script" : u"Öffne ein vorhandenes Script",
    "Open..." : u"Öffnen...",
    "Close tab" : u"Tab schließen",
    "Close the current tab" : u"Aktuellen Tab schließen",
    "Close all tabs" : u"", # New in v2.2.1
    "Close every tab" : u"", # New in v2.2.1
    "Rename tab" : u"", # New in v2.2.1
    "Rename the current tab. If script file is existing, also rename it" : u"", # New in v2.2.1
    "Save the current script" : u"Speichere aktuelles Script",
    "Choose where to save the current script" : u"Speicherverzeichnis des aktuellen Scripts",
    "Save script as..." : u"Speichere Script als...",
    "Load a session into the tabs" : u"Lade eine Session in Tabs",
    "Load session..." : u"Lade Session...",
    "Save all the scripts as a session, including slider info" : u"Speichern aller Scripte einer Session, inclusive Info des Schiebereglers",
    "Save session..." : u"Speichere Session...",
    "Backup current session" : u"Aktuelle Session speichern",
    "Backup the current session for next program run" : u"Aktuelle Session für nächsten Programmlauf speichern", 
    "Next tab" : u"Nächster Tab",
    "Switch to next script tab" : u"Schalte zum nächsten Script-Tab",
    "Previous tab" : u"Vorheriger Tab",
    "Switch to previous script tab" : u"Schalte zum vorherigen Sript-Tab",
    "Show the scrap window" : u"Zeige das Ablage Fenster",
    "&Exit" : u"Beenden",
    "Exit the program" : u"Programm beenden",
    "&Edit" : u"&Bearbeiten",
    "Undo last text operation" : u"Rückgängig der letzten Textbearbeitung",
    "Redo last text operation" : u"Wiederholen der letzten Textbearbeitung",
    "Cut the selected text" : u"Ausgewählen Text ausschneiden",
    "Copy the selected text" : u"Ausgewählten Text kopieren",
    "Paste the selected text" : u"Ausgewählten Text einfügen",
    "Find..." : u"Suchen...",
    "Open a find text dialog box" : u"Öffne Text-Dialogbox Finden",
    "Find next" : u"Weitersuchen",
    "Find the next instance of given text" : u"Nächste Instanz in diesem Text suchen",
    "Open a replace text dialog box" : u"Öffen der Dialogbox Ersetzen",
    "Replace..." : u"Ersetzen...",
    "Select All" : u"Alles auswählen",
    "Select all the text" : u"Gesammten Text auswählen",
    "&Insert" : u"", # New in v2.2.1
    "Choose a source file to insert into the text" : u"Sourcedatei auswählen, um sie in den Text einzufügen",
    "Insert source..." : u"Eingabe Source...",
    "Get a filename from a dialog box to insert into the text" : u"Einen Dateinamen von der Dialogbox im Text einfügen",
    "Insert filename..." : u"Eingabe Dateiname...",
    "Choose a plugin dll to insert into the text" : u"Plugin-dll-Datei auswählen um sie in den Text einzufügen",
    "Insert plugin..." : u"Eingabe Plugin...",
    "Insert a user-scripted slider into the text" : u"Eingabe eines Schiebreglerscripts im Text",
    "Insert user slider..." : u"Eingabe Schieberegler...",
    "Insert a tag which indicates a separator in the user slider window" : u"Eingabe einer Kennzeichnung (tag),welche ein Begrenzungszeichen im Anwender-Schiebereglerfenster anzeigt",
    "Insert user slider separator" : u"Eingabe Schieberegler-Begrenzungszeichen",
    "Insert the current frame number into the text" : u"Eingabe der aktuellen Einzelbildnummer im Text",
    "Add tags surrounding the selected text for toggling with the video preview" : u"Ergänze tags die den ausgewählten Text umgeben, um zur Video-Vorschaufunktion zu schalten",
    "Tag selection for toggling" : u"Umschalten Tag Auswahl",
    "Clear all tags" : u"Lösche alle Tags",
    "Clear all toggle tags from the text" : u"Lösche alle geschalteten tags vom diesem Text",
    "Indent the selected lines" : u"Ausgewählte Zeilen einrücken",
    "Unindent the selected lines" : u"Ausgewählte Zeilen nicht einrücken",
    "Block comment" : u"Blockkommentar",
    "Comment or uncomment selected lines" : u"Komentiere oder umkomentiere ausgewählte Zeilen",
    "Comment at start of a text style or uncomment" : u"", # New in v2.2.1
    "Style comment" : u"", # New in v2.2.1
    "Toggle current fold" : u"", # New in v2.2.1
    "Toggle the fold point On/OFF at the current line" : u"", # New in v2.2.1
    "Toggle all fold points On/OFF" : u"", # New in v2.2.1
    "Toggle all folds" : u"Umschalten aller ausklappbaren Einstellungen",
    "&AviSynth function" : u"", # New in v2.2.1
    "Show list of filternames matching the partial text at the cursor" : u"Zeige Liste von Filternamen, die im  aktuellen Text (beim Cursor) angepasst werden",
    "Autocomplete all" : u"", # New in v2.2.1
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"", # New in v2.2.1
    "Show calltip" : u"Zeige Calltips",
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"Zeige Filtercalltips (arbeitet nur wenn der Cursor innerhalb der Argumente steht)",
    "Show function definition" : u"Zeige Funktionsdefinition",
    "Show the AviSynth function definition dialog for the filter" : u"Zeige den Avisynth-Funktionsdefinitionsdialog für den Filter",
    "Filter help file" : u"Filter-Hilfedatei", 
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"Starte die Hilfedatei für die Filter (arbeitet nur wenn der Cursor innerhalb der Argumente steht oder Name hervorgehoben ist)",
    "&Miscellaneous" : u"", # New in v2.2.1
    "Move line up" : u"Zeile hochrücken",
    "Move the current line or selection up by one line" : u"Zeile oder Auswahl um eine Zeile hochrücken",
    "Move line down" : u"Zeile nach unten rücken",
    "Move the current line or selection down by one line" : u"Zeile oder Auswahl um eine Zeile nach unten rücken",
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"Kopieren des aktuellen Scripts, ohne irgendwelche AvsP Kennzeichnungen (Benutzer Schieberegler ,Umschalter tags)",
    "Copy unmarked script to clipboard" : u" Kopiere ungekennzeichnetes Script zum Clipboard", 
    "Copy avisynth error to clipboard" : u"", # New in v2.2.1
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"", # New in v2.2.1
    "&Video" : u"Video",
    "Add/Remove bookmark" : u"", # New in v2.2.1
    "Mark the current frame on the frame slider" : u"Markiere das aktuelle Einzelbild am Eizeldbild-Schieberegler",
    "Clear all bookmarks" : u"Lösche alle Lesezeichen",
    "Titled &bookmarks" : u"", # New in v2.2.1
    "Move the nearest titled bookmark to the current position. A historic title will be restored if it matches the condition." : u"", # New in v2.2.1
    "Move titled bookmark" : u"", # New in v2.2.1
    "Restore all historic titles" : u"", # New in v2.2.1
    "Restore historic titles" : u"", # New in v2.2.1
    "Clear all historic titles" : u"", # New in v2.2.1
    "Clear historic titles" : u"", # New in v2.2.1
    "Generate titles for untitled bookmarks by the pattern - 'Chapter %02d'" : u"", # New in v2.2.1
    "Set title (auto)" : u"", # New in v2.2.1
    "Edit title for bookmarks in a list table" : u"", # New in v2.2.1
    "Set title (manual)" : u"", # New in v2.2.1
    "&Navigate" : u"", # New in v2.2.1
    "Go to &bookmark" : u"", # New in v2.2.1
    "Go to next bookmarked frame" : u"Gehe zum nächsten,als Lesezeichen markierten, Einzelbild",
    "Next bookmark" : u"Nächstes Lesezeichen",
    "Go to previous bookmarked frame" : u"Gehe zum vorherigen,als Lesezeichen markierten, Einzelbild ",
    "Previous bookmark" : u"Vorheriges Lesezeichen",
    "Forward 1 frame" : u"Vorwärts 1 Einzelbild",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"Zeige nächstes Videobild (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Backward 1 frame" : u"Zürück    1 Einzelbild",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"Zeige vorheriges Videobild (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Forward 1 second" : u"Vorwärts 1 Sekunde",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"Zeige Video 1 Sekunde vorwärts (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Backward 1 second" : u"Zurück     1 Sekunde",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"Zeige Video 1 Sekunde zurück (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Forward 1 minute" : u"Vorwärts 1 Minute",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"Zeige Video 1 Minute vorwärts (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Backward 1 minute" : u"Zurück    1 Minute",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"Zeige Video 1 Minute zurück (Tastaturkurzbefehle aktiv, sobald Videofenster fokussiert)",
    "Forward x units" : u"Vorwärts x Einheiten",
    "Jump forward by x units (you can specify x in the options dialog)" : u"Vorwärtsspringen mit x Einheiten (x kann im Optionsdialog angegeben werden)",
    "Backwards x units" : u"Zurück x Einheiten",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"Zurüchspringen mit x Einheiten (x kann im Optionsdialog angegeben werden)",
    "Go to first frame" : u"Zum ersten Einzelbild",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"Zum ersten Video-Einzelbild (Kurzbefehle aktiv,sobald Videofenster fokussiert hat) ",
    "Go to last frame" : u"Zum letzten Einzelbild",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"Zum letzten Video-Einzelbild (Kurzbefehle aktiv,sobald Videofenster fokussiert hat)", 
    "Go to last scrolled frame" : u"Gehe zum letzten gescrollten Einzelbild",
    "Last scrolled frame" : u"Letztes gescrolltes Einzelbild",
    "Enter a video frame or time to jump to" : u"Eingabe eines Videoeinzelbilds oder Zeit um dort hin zu springen",
    "Go to frame..." : u"Gehe zum Einzelbild...",
    "Crop editor..." : u"Crop-Editor...",
    "Show the crop editor dialog" : u"Zeige den Crop-Editor-Dialog",
    "&Trim selection editor" : u"", # New in v2.2.1
    "Show the trim selection editor dialog" : u"Zeige den Auswahldialog des Trim-Editors",
    "Show trim selection editor" : u"Zeige den Trim-Auswahl-Editor ",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"Auswahl eines Startpunkts (Angezeigt im Trim-Editor,falls nicht sichtbar)",
    "Set selection startpoint" : u"Auswahl Startpunkt",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"Auswahl eines Endpunkts (Angezeigt im Trim-Editor,falls nicht sichtbar)",
    "Set selection endpoint" : u"Auswahl Endpunkt",
    "Zoom video preview to 25%" : u"Zoom Video-Vorschaufunktion auf 25%",
    "Zoom video preview to 50%" : u"Zoom Video-Vorschaufunktion auf 50%",
    "Zoom video preview to 100% (normal)" : u"Zoom Video-Vorschaufunktion auf 100%",
    "Zoom video preview to 200%" : u"Zoom Video-Vorschaufunktion auf 200%",
    "Zoom video preview to 300%" : u"Zoom Video-Vorschaufunktion auf 300%",
    "Zoom video preview to 400%" : u"Zoom Video-Vorschaufunktion auf 400%",
    "Zoom video preview to fill the entire window" : u"Zoomen der Videovorschau-Funktion, um das ganze Fenster zu füllen",
    "Zoom video preview to fit inside the window" : u"Zoomen der Videovorschau-Funktion, für Anpassung innerhalb des Fensters.",
    "Enlarge preview image to next zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.2.1
    "Shrink preview image to previous zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.2.1
    "&Flip" : u"", # New in v2.2.1
    "Flip video preview upside down" : u"", # New in v2.2.1
    "Flip video preview from left to right" : u"", # New in v2.2.1
    "&YUV -> RGB" : u"", # New in v2.2.1
    "Swap chroma channels (U and V)" : u"", # New in v2.2.1
    "For YUV source, assume it is Rec601 (default)" : u"", # New in v2.2.1
    "For YUV source, assume it is PC.601" : u"", # New in v2.2.1
    "For YUV source, assume it is Rec709" : u"", # New in v2.2.1
    "For YUV source, assume it is PC.709" : u"", # New in v2.2.1
    "For YV12 only, assume it is progressive (default)" : u"", # New in v2.2.1
    "For YV12 only, assume it is interlaced" : u"", # New in v2.2.1
    "Save image as..." : u" Speichere Bild als...",
    "Save the current frame as a bitmap" : u"Speicher das aktuelle Einzelbild als Bitmap-Datei",
    "Force the script to reload and refresh the video frame" : u"Erzwinge durch Skript, erneutes laden und erneuern des Videoeinzelbilds",
    "Refresh preview" : u"Erneuere Vorschaufunktion",
    "Show/Hide the preview" : u"", # New in v2.2.1
    "Toggle the video preview" : u"Umschalten Video-Vorschaufunktion",
    "Release all open videos from memory" : u"Freigabe aller offenen Videos im Speicher", 
    "Release all videos from memory" : u"Freigabe aller Videos im Speicher", 
    "Switch focus between the video preview and the text editor" : u"Schalten des Fokus zwischen der Video-Vorschaufunktion und dem Texteditor",
    "Switch video/text focus" : u"Schalte Video/Textfocus",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"",
    "Toggle the slider sidebar" : u"Umschalten der Schieberegler Sidebar ", 
    "External player" : u"Externer Player",
    "Play the current script in an external program" : u"Wiedergabe des aktuellen Skripts in einem externen Programm",
    "Show information about the video in a dialog box" : u"Zeige Informationen über das Video in der Dialogbox.",
    "Video information" : u"Videoinformation",
    "&Options" : u"&Optionen",
    "Always on top" : u"Immer im Vordergrund",
    "Keep this window always on top of others" : u"Dieses Fenster vor allen anderen im Vordergrund",
    "Disable video preview" : u"Abschalten der Video-Vorschaufunktion",
    "If checked, the video preview will not be shown under any circumstances" : u"Wenn angehakt, wird unter keinen Umständen die Video-Vorschaufunktion gezeigt werden",
    "Associate .avs files with AvsP" : u"Assoziiere .avs-Dateien mit AvsP",
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"Konfiguriert den Computer so, dass ein Doppelklick .avs Dateien mit AvsP öffnet. ",
    "AviSynth function definition..." : u"AviSynth-Funktionsdefinition",
    "Edit the various AviSynth script fonts and colors" : u"Bearbeite die verschiedenen Schriftarten und Farben im Avisynthscript",
    "Fonts and colors..." : u"Schriftarten und Farben",
    "Edit the extension-based templates for inserting sources" : u"Bearbeite die Beispiel basierenden Vorlagen um die Sources einzufügen",
    "Extension templates..." : u"Beispiel basierenden Vorlagen...", 
    "Configure the program keyboard shortcuts" : u"Programmkonfiguration der Tastatur Kurzbefehle",
    "Keyboard shortcuts..." : u"", # New in v2.2.1
    "Configure program settings" : u"Programmeinstellungen konfigurieren",
    "Program settings..." : u"Programmeinstellungen",
    "&Help" : u"&Hilfe",
    "Animated tutorial" : u"Filmische Anleitung",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"Filmische Anleitung von AvsP anschauen (von der AvsP Webseite)",
    "Learn more about AvsP text features (from the AvsP website)" : u"Lerne mehr über AvsP Textfunktionen (von der AvsP Webseite)",
    "Text features" : u"Textfunktionen",
    "Learn more about AvsP video features (from the AvsP website)" : u"Lerne mehr über AvsP Videofunktionen (von der AvsP Webseite)",
    "Video features" : u"Videofunktionen",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"Lerne mehr über AvsP Benutzer-Schieberegler (von der AvsP Webseite)",
    "User sliders" : u"Benutzer-Schieberegler",
    "Learn more about AvsP macros (from the AvsP website)" : u"Lerne mehr über AvsP Macros (von der AvsP Webseite)",
    "Macros" : u"Macros",
    "Avisynth help" : u"Avisynth Hilfe",
    "Open the avisynth help html" : u"Öffne Avisynth-HTML-Hilfe",
    "Open Avisynth plugins folder" : u"", # New in v2.2.1
    "Open the avisynth plugins folder" : u"", # New in v2.2.1
    "About this program" : u"Über dieses Programm",
    "About AvsPmod" : u"", # New in v2.2.1
    "Previous frame" : u"Vorheriges Einzelbild",
    "Next frame" : u"Nächstes Einzelbild",
    "Run the script with an external program" : u"Starte Spript mit einem externen Programm",
    "Run the selected tool" : u"", # New in v2.2.1
    "&Tools" : u"&Werkzeuge",
    "a macro check item" : u"", # New in v2.2.1
    "a macro radio item" : u"", # New in v2.2.1
    "Run selected macro" : u"Starte ausgewähltes Macro",
    "View the readme for making macros" : u"Siehe Readme für Macro Erstellung",
    "Open the macros folder" : u"", # New in v2.2.1
    "&Macros" : u"", # New in v2.2.1
     "Close" : u"Schließen",
    "Rename" : u"", # New in v2.2.1
    "Save" : u"Speichern",
    "Save as..." : u"Speichere als...",
    "Copy to new tab" : u"", # New in v2.2.1
    "Reposition to" : u"", # New in v2.2.1
    "Crop editor" : u"Cropeditor",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"Bei diesem Dialog ,kann die Cropfunktion auch mittels linker Maustaste im Bild ausgeführt werden.",
    "At script end" : u"Am Scriptende",
    "At script cursor" : u"Am Scriptcursor", 
    "Copy to clipboard" : u"Kopiere zum Clipboard ",
    "Insert Crop() command:" : u"Eingabe Crop() Befehl:",
    "Apply" : u"Übernehmen",
    "Trim editor" : u"",
    "Selection options" : u"Auswahl Optionen",
    "Keep selected regions" : u"Behalte ausgesuchte Bereiche",
    "Keep unselected regions" : u"Behalte freie Bereiche", 
    "Mark video frames inside/outside selection" : u"Video-Frames innerhalb/außerhalb der Auswahl markieren",
    "Use Dissolve() with overlap frames:" : u"", # New in v2.2.1
    "Insert Trim() commands:" : u"Eingabe Trim() Befehle",
    "Insert Dissolve() commands:" : u"", # New in v2.2.1
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"Video-Schieberegler für die Bildauswahl zum trimmen benutzen ",
    "File does not exist!" : u"Datei existiert nicht",
    "All files (*.*)|*.*" : u"Alle Dateien (*.*)|*.*",
    "Select a file" : u"Auswahl einer Datei",
    "Create a separator label" : u"Erstellen einer gesonderten Bezeichnung (label)",
    "Enter separator label" : u"Eingabe einer gesonderten Bezeichnung (label)",
    "Enter tag name:" : u"Eingabe tag Name", 
    "Tag definition" : u"Tag-Definition",
    "Chapter" : u"", # New in v2.2.1
    "Set title for bookmarks" : u"", # New in v2.2.1
    "Title" : u"", # New in v2.2.1
    "Frame No." : u"", # New in v2.2.1
    "Time **" : u"", # New in v2.2.1
    "" : u"", # New in v2.2.1
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"", # New in v2.2.1
    "Frame size:" : u"Einzelbildgröße",
    "Length:" : u"Länge",
    "Frame rate:" : u"Wiederholungsrate der Einzelbilder",
    "Colorspace:" : u"Farbraum",
    "Field or frame based:" : u"Feld oder Einzelbild basierend",
    "Parity:" : u"Parität",
    "Audio" : u"Audio",
    "Channels:" : u"Kanäle",
    "Hz" : u"Hz",
    "Sampling rate:" : u"Abtastrate",
    "Sample type:" : u"Sample-Typ",
    "bits" : u"Bits",
    "samples" : u"Samples", 
    "Could not find the macros folder!" : u"", # New in v2.2.1
    "Could not find %(readme)s!" : u"Kann nicht finden %(readme)s!",
    "Failed to import the selected tool" : u"", # New in v2.2.1
    "You must restart for changes to take effect!" : u"", # New in v2.2.1
    "Basic" : u"Grundlagen",
    "Default:" : u"Standard",
    "Comment:" : u"Kommentar",
    "Block Comment:" : u"", # New in v2.2.1
    "__END__ Comment:" : u"", # New in v2.2.1
    "Number:" : u"Nummer",
    "Operator:" : u"Operator",
    "String:" : u"String:",
    "Triple-quoted string:" : u"Triple-quoted string:",
    "Internal filter:" : u"Interner Filter",
    "External filter:" : u"Externer Filter",
    "Internal function:" : u"Interne Funktionen",
    "User defined function:" : u"Benutzerdefenierte Funkionen", 
    "Clip property:" : u"Clip-Eigenschaften (property)",
    "AviSynth keyword:" : u"AviSynth-Schlüsselwort",
    "AviSynth data type:" : u" AviSynth Datentypen",
    "AvsP user slider:" : u" AvsP Benutzer-Schieberegler",
    "Monospaced font:" : u"Monospaced Schriftart",
    "Advanced" : u"Erweitert",
    "Incomplete string:" : u"Unvollständiger string:",
    "Syntax highlight strings which are not completed in a single line differently" : u"Strings innerhalb der Syntaxhervorhebung die nicht in einer einzelnen Zeile unterschiedlich beendet werden",
    "Brace highlight:" : u"Klammerhervorhebung",
    "Bad brace:" : u"Fehlerhafte Klammer",
    "Bad number:" : u"Fehlerhafte Nummer",
    "Margin line numbers:" : u"",
    "Miscellaneous word:" : u"Rand Zeilennummern", 
    "Calltip:" : u"Calltip",
    "Calltip highlight:" : u"Hervorhebung Calltip",
    "Cursor:" : u"", # New in v2.2.1
    "Selection highlight:" : u"", # New in v2.2.1
    "Current line highlight:" : u"", # New in v2.2.1
    "Highlight the line that the caret is currently in" : u"Zeile mit Einschaltungszeichen hervorheben",
    "Fold margin:" : u"", # New in v2.2.1
    "Scrap window" : u"", # New in v2.2.1
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"", # New in v2.2.1
    "Use monspaced font" : u"", # New in v2.2.1
    "Insert aborted:" : u"Eingabe abgebrochen",
    "No dot required in file extension!" : u"Keine Punktsetzung in der Dateinamenserweiterung erforderlich",
    "Edit extension-based templates" : u"Bearbeite Dateivorlagen",
    "File extension" : u"Dateinamenserweiterung",
    "Template" : u"Schablone",
    "This info is used for inserting sources based on file extensions." : u"Diese Information wird für Source basierende Dateinamenserweiterung benötigt",
    "Any instances of *** in the template are replaced with the filename." : u"Jede Instanz von *** in den Vorlagen wird ersetzt mit den Dateinamen",
    "(If you want relative paths instead of the full filename, use [***].)" : u"", # New in v2.2.1
    "Associating .avs files will write to the windows registry." : u"Assoziation von .avs-Dateien wird in die Windows Registry geschrieben.",
    "Do you wish to continue?" : u"Wollen Sie weitermachen ?",
    "Could not find the Avisynth plugins folder!" : u"", # New in v2.2.1
    "AvsPmod version %(version)s " : u"", # New in v2.2.1
    "An AviSynth script editor" : u"Ein AviSynth Sripteditor",
    "AvsP Website" : u"AvsP Webseite",
    "Active thread on Doom9's forum" : u"", # New in v2.2.1
    "This program is freeware under the GPL license." : u"", # New in v2.2.1
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"", # New in v2.2.1
    "copy as time" : u"", # New in v2.2.1
    "copy" : u"", # New in v2.2.1
    "paste" : u"", # New in v2.2.1
    "clear history" : u"", # New in v2.2.1
    "Cannot switch tabs while crop editor is open!" : u"Kann keine Tabs schalten,weil der Cropeditor noch geöffnet ist",
    "Cannot switch tabs while trim editor is open!" : u"Tabs können nicht geschaltet werden,solange der Trim editor geöffnet ist.",
    "pos" : u"pos",
    "rgb" : u"RGB",
    "rgba" : u"rgba",
    "yuv" : u"yuv",
    "hex" : u"hex",
    "Invalid crop values detected.  Continue?" : u"", # New in v2.2.1
    "You must create at least one frame selection first!" : u"Zumindestens eine Bildauswahl muß gemacht werden.",
    "Select autocomplete keywords" : u"", # New in v2.2.1
    "exclude long names" : u"", # New in v2.2.1
    "Customize the video status bar message" : u"Anpassen der Nachricht in der Video-Status-Bar",
    "Video status bar message:" : u"Video-Status-Bar Nachricht",
    "Legend" : u"Legende",
    "Current frame" : u"Aktuelles Einzelbild",
    "Framecount" : u"",
    "Current time" : u"Aktuelle Zeit",
    "Total time" : u"Zeit Total",
    "Width" : u"Breite",
    "Height" : u"Höhe",
    "Aspect ratio" : u"Aspect Ratio (AR)",
    "Framerate" : u"Bildwiederholgungsrate",
    "Framerate numerator" : u"Zähler Bildwiederholgungsrate",
    "Framerate denominator" : u"Nenner Bildwiederholgungsrate ",
    "Colorspace" : u"Farbraum",
    "Field or frame based" : u"Feld oder Einzelbild basierend",
    "Parity" : u"Parität",
    "Parity short (BFF or TFF)" : u"Parität kurz (BFF or TFF)",
    "Audio rate" : u"Audiorate",
    "Audio length" : u"Audiolänge",
    "Audio channels" : u"Audiokanäle",
    "Audio bits" : u"Audiobits",
    "Audio type (Integer or Float)" : u"Audiotyp (Integer or Float)",
    "Pixel position (cursor based)" : u"Pixelposition (Cursor basierend)",
    "Pixel hex color (cursor based)" : u"Pixelfarbe hex (Cursor basierend)",
    "Pixel rgb color (cursor based)" : u"Pixelfarbe RGB (Cursor basierend)",
    "Pixel yuv color (cursor based)" : u"Pixelfarbe yuv (Cursor basierend)",
    "Pixel color (auto-detect colorspace)" : u"Pixelfarbe (Automatisch gefundener Farbraum)",
    "Program zoom" : u"Programm-Zoom",
    "Save changes before closing?" : u"Änderungen vor dem Beenden speichern?",
    "Cannot create a new tab while crop editor is open!" : u"Kein neuer Tab kann erstellt werden,solange der Crop-Editor geöfnnet ist!",
    "Cannot create a new tab while trim editor is open!" : u"Kein neuer Tab kann erstellt werden,solange der Trim-Editor geöfnnet ist!",
    "AviSynth script (avs, avsi)|*.avs;*.avsi|Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"AviSynth script (avs, avsi)|*.avs;*.avsi|Source-Dateien (%(extlist1)s)|*.%(extlist2)s|Alle Dateien (*.*)|*.*",
    "Open a script or source" : u"Öffne ein Script oder Source",
    "Reload the file and lose the current changes?" : u"Die Datei neu laden und die gegenwärtigen Änderungen verlieren?",
    "Open this file" : u"Öffne die Datei",
    "Save session before closing all tabs?" : u"", # New in v2.2.1
    "AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|All files (*.*)|*.*" : u"AviSynthscript (*.avs, *.avsi)|*.avs;*.avsi|Alle Dateien (*.*)|*.*",
    "Save current script" : u"Speichere aktuelles Script",
    "Directory %(dirname)s does not exist!" : u"Verzeichnis %(dirname)s existiert nicht!",
    "Load a session" : u"Lade eine Session",
    "File has been modified since the session was saved. Reload?" : u"Datei wurde verändert, seit die letzte Sitzung gespeichert wurde.",
    "Save the session" : u"Speichere die Session",
    "Save current frame" : u"Speichere aktuelles Einzelbild",
    "No image to save" : u"Kein Bild zum speichern",
    "Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"Source Dateien (%(extlist1)s)|*.%(extlist2)s|Alle Dateien (*.*)|*.*",
    "Insert a source" : u"Eingabe Source",
    "AviSynth plugin (*.dll)|*.dll|All files (*.*)|*.*" : u"", # New in v2.2.1
    "Insert a plugin" : u"Eingabe Plugin",
    "No bookmarks defined!" : u"Keine Lesezeichen definiert",
    "There must be more than one unique bookmark to use this feature!" : u"Es muß mehr als ein eindeutiges Lesezeichen geben, um diese Funktion zu nutzen",
    "Jump to specified bookmark" : u"Springe zu bestimmten Lesezeichen",
    "Line: %(line)i  Col: %(col)i" : u"Zeile: %(line)i  Col: %(col)i",
    "Frame Based" : u"Einzelbild basierend",
    "Field Based" : u"Feld basierend",
    "Bottom Field First" : u"Bottom Field zuerst",
    "BFF" : u"BFF",
    "Top Field First" : u"Top Field zuerst",
    "TFF" : u"TFF",
    "Integer" : u"Integer",
    "Float" : u"Float",
    "Edit AviSynth function information" : u"Bearbeite Information der Avisynthfunktionen ",
    "  Function name" : u"Funktiosname",
    "Function arguments" : u"Funktionsargumente", 
    "Open filter customization file" : u"Öffnen Fileranpassungsdatei",
    "Calltip-only text file (*.txt)|*.txt" : u"Calltips- nur als Textdatei (*.txt)|*.txt",
    "Filter customization file (*.tag)|*.tag" : u"Öffnen Fileranpassungsdatei(*.tag)|*.tag",
    "Invalid filter customization file!" : u"Falsche Fileranpassungsdatei",
    "Save filter customization file" : u"Speichern Fileranpassungsdatei",
    "Invalid argument!" : u"Falsches Argument",
    "Error loading AviSynth!" : u"Fehler beim laden von AviSynth",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"", # New in v2.2.1
    "Save changes before previewing?" : u"Speichern der Änderungen vor der Vorschau",
    "Executable files (*.exe)|*.exe|All files (*.*)|*.*" : u"Ausführbare  Dateien (*.exe)|*.exe|All Dateien (*.*)|*.*",
    "Select an external player" : u"Wähle einen externen Player",
    "A program must be specified to use this feature!" : u"Ein Programm muss angegeben werden um dieses Eigenschaften zu nutzen",
    "General settings..." : u"Allgemeine Einstellungen...",
    "Invalid slider text: min > max" : u"Ungültiger Schiebereglertext: min > max",
    "Invalid slider text: value not in bounds" : u"Ungültiger Schiebereglertext: Wert nicht in Grenzen",
    "Invalid slider text: bad modulo label" : u"Ungültiger Schiebereglertext: Fehl modulo Kennzeichnung",
    "Invalid slider text: slider label already exists" : u"Ungültiger Schiebereglertext: Bezeichnung des Schiebereglers existiert schon",
    "Invalid slider text: invalid number" : u"Ungültiger Schiebereglertext: Ungültige Nummer",
    "Reset to initial value: %(value_formatted)s" : u"Zurückstellen zum Ausgangswert %(value_formatted)s",
    "Reset to initial value: %(value2_formatted)s" : u"", # New in v2.2.1
    "Reset to default value: %(value_formatted)s" : u"", # New in v1.4.0
    "Invalid hexadecimal color!" : u"Ungültiger hexadecimal Farbwert",
    "Must specify a max value!" : u"Ein Maximalwert muß spezifiziert werden!",
    "Must specify a min value!" : u"Ein Minimalwert muß spezifiziert werden!",
    "Min value must be a number!" : u"Minimalwert muß eine Zahl sein!",
    "Max value must be a number!" : u"Maximalwert muß eine Zahl sein!",
    "Default value must be a number!" : u"Standartwet muß eine Zahl sein!",
    "Step size value must be a number!" : u"", # New in v2.2.1
    "Left-click to select a color, right click to reset to default" : u"Links-click um eine Farbe zu wählen, Rechts-click setzt auf Standard zurück.",
    "Source files (%(extlist1)s)|*.%(extlist2)s" : u"Source-Dateien(%(extlist1)s)|*.%(extlist2)s",
    "Toggle \"%(label)s\" section" : u"Umschalten \"%(label)s\" Abschnitt",
    "Don't show me this again" : u"", # New in v2.2.1
    "Save as" : u"Speicher als", 
    "Select a directory" : u"Verzeichnis auswählen",
    "Enter information" : u"Informationen eintragen",
    "Progress" : u"Bearbeitung",
    "Error loading the script" : u"Fehlerhaft geladenes Script",
    "Error in the macro:" : u"Fehler im Macro",
    "Couldn't find %(macrofilename)s" : u"Konnte nicht finden %(macrofilename)s",
    "Failed to open the AVI file" : u"Konnte die AVI-Datei nicht öffnen",
    "Failed to open the AVI frame" : u"Konnte das AVI-Einzelbild nicht öffnen",
    "Failed to retrieve AVI frame" : u"Konnte das AVI-Einzelbild nicht wiederherstellen",
    "Ctrl" : u"Ctrl",
    "Alt" : u"Alt",
    "Shift" : u"Shift",
    "Program Settings" : u"Programm Einstellungen",
    "Browse" : u"Browse",
    "* Requires program restart for full effect" : u"* Erfordert Programm Neustart für vollen Effekt",
    "Invalid directory!" : u"Ungültiges Verzeichnis",
    "Invalid filename!" : u"Ungültiger Dateiname",
    "Edit shortcuts" : u"Bearbeite Kurzbefehle",
    "Menu label" : u" Menue Titel",
    "Keyboard shortcut" : u"Tastaur Kurzbefehl",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"Doppelklick/Enter auf einen Begriff in der Liste um einen Kurzbefehl zu bearbeiten",
    "Shortcut" : u"", # New in v2.2.1
    "Action" : u"", # New in v2.2.1
    "Edit the keyboard shortcut" : u"Bearbeite Tastatur Kurzbefehl",
    "Key:" : u"Key",
    "Clear" : u"Löschen",
    "%(keyString)s not found in key string list" : u"%(keyString)s konnte nicht in der key Sring Liste gefunden werden",
    "This shortcut is being used by:" : u"Diese Kurzbefehl wird benutzt von",
    "Insert" : u"Eingabe",
    "Delete" : u"Löschen",
    "Error: key %(key)s does not exist!" : u"Fehler: key %(key)s existiert nicht!",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"Sind Sie sicher das Sie umbenennen möchten%(oldName)s zu %(newName)s?",
    "Question" : u"Frage",
     "Insert a new item" : u"Ein neues Element einfügen",
    "Must enter a name!" : u"Es muss ein Name vergeben werden",
    "Item %(newKey)s already exists!" : u"Element %(newKey)s existiert schon!",
    "Warning: no value entered for item %(newKey)s!" : u"Warnung: Für das Element wurde kein Wert eingetragen %(newKey)s!",
    "Message" : u"Meldung",
    "Select an item to delete first" : u"Erst ein Element auswählen um zu löschen",
    "Are you sure you want to delete item %(key)s?" : u"Das Element wirklich löschen %(key)s?",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"Resize-Calculator...",
    "Calculate an appropriate resize for the video" : u"", # New in v2.2.1
    "Resize calculator" : u"", # New in v2.2.1
    "Input" : u"", # New in v2.2.1
    "Video resolution:" : u"", # New in v2.2.1
    "Pixel aspect ratio:" : u"", # New in v2.2.1
    "Results" : u"", # New in v2.2.1
    "Aspect ratio error:" : u"", # New in v2.2.1
    "Settings" : u"", # New in v2.2.1
    "Target pixel aspect ratio:" : u"", # New in v2.2.1
    "Resize block constraints:" : u"", # New in v2.2.1
    "Resize percent ranges:" : u"", # New in v2.2.1
    "Max search aspect ratio error:" : u"", # New in v2.2.1
    "Configure" : u"", # New in v2.2.1
    "compute from .d2v" : u"", # New in v2.2.1
    "Configure options" : u"", # New in v2.2.1
    "Avisynth resize:" : u"", # New in v2.2.1
    "The current Avisynth script contains errors." : u"", # New in v2.2.1

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"", # New in v2.2.1
    "Encode the current script using x264" : u"", # New in v2.2.1
    "Encode video" : u"", # New in v2.2.1
    "System settings" : u"", # New in v2.2.1
    "Input file:" : u"", # New in v2.2.1
    "Output file:" : u"", # New in v2.2.1
    "Compression settings" : u"", # New in v2.2.1
    "Bitrate (kbits/sec):" : u"", # New in v2.2.1
    "calculate" : u"", # New in v2.2.1
    "Quality CRF (0-51):" : u"", # New in v2.2.1
    "Quality CQ (1-31):" : u"", # New in v2.2.1
    "Additional settings" : u"", # New in v2.2.1
    "Credits start frame:" : u"", # New in v2.2.1
    "Command line settings" : u"", # New in v2.2.1
    "Run" : u"Start",
    "First time using this compression preset!" : u"", # New in v2.2.1
    "Please enter the exe paths in the following dialog." : u"", # New in v2.2.1
    "Exe pathnames" : u"", # New in v2.2.1
    "Open an AviSynth script" : u"AviSynthscript öffnen",
    "AviSynth script (*.avs)|*.avs" : u"AviSynthscript (*.avs)|*.avs",
    "Save the video as" : u"", # New in v2.2.1
    "Select a program" : u"", # New in v2.2.1
    "Program (*.exe)|*.exe" : u"", # New in v2.2.1
    "Unreplaced items remain in the command line:" : u"", # New in v2.2.1
    "Unknown exe paths!" : u"", # New in v2.2.1
    "General" : u"Allgemein",
    "Credits warning minutes:" : u"", # New in v2.2.1
    "Automatically compute bitrate value on startup" : u"", # New in v2.2.1
    "Automatically compute pixel aspect ratio from d2v on startup" : u"", # New in v2.2.1
    "Append batch commands to the avs script as comments" : u"", # New in v2.2.1
    "Encoder priority:" : u"", # New in v2.2.1
    "Path to %(name)s:" : u"", # New in v2.2.1
    "Extra arguments:" : u"", # New in v2.2.1
    "Bitrate Calculator" : u"", # New in v2.2.1
    "Output info" : u"", # New in v2.2.1
    "Total size:" : u"", # New in v2.2.1
    "Container:" : u"", # New in v2.2.1
    "(None)" : u"", # New in v2.2.1
    "Video info" : u"", # New in v2.2.1
    "Framecount:" : u"", # New in v2.2.1
    "FPS:" : u"", # New in v2.2.1
    "Audio info" : u"", # New in v2.2.1
    "Audio file:" : u"", # New in v2.2.1
    "Compress audio" : u"", # New in v2.2.1
    "Audio bitrate:" : u"", # New in v2.2.1
    "Format:" : u"", # New in v2.2.1
    "Subtitles info" : u"", # New in v2.2.1
    "Subtitles file:" : u"", # New in v2.2.1
    "Total time:" : u"", # New in v2.2.1
    "Video size:" : u"", # New in v2.2.1
    "Audio size:" : u"", # New in v2.2.1
    "Subtitles size:" : u"", # New in v2.2.1
    "Overhead size:" : u"", # New in v2.2.1
    "Bitrate:" : u"", # New in v2.2.1
    "Open the audio file" : u"", # New in v2.2.1
    "Open the subtitles file" : u"", # New in v2.2.1
    "%(h)i hr and %(m)i min" : u"", # New in v2.2.1

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"", # New in v2.2.1
    "Use avs2avi to save the current script as an avi" : u"", # New in v2.2.1
    "Please select the path to avs2avi.exe" : u"", # New in v2.2.1
    "Error: avs2avi is required to save an avi!" : u"Fehler: avs2avi wird zum Speichern einer AVI-Datei benötigt",
    "Pass: %(pass)s / %(passes)s" : u"Pass: %(pass)s / %(passes)s",
    "Frame: %(frame)i / %(frames)i" : u"Einzelbild: %(frame)i / %(frames)i",
    "Size: %(size).2f MB" : u"Grösse: %(size).2f MB",
    "FPS: %(fps).1f fps" : u"FPS: %(fps).1f fps",
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"Zeit abgelaufen: %(hr)02i:%(min)02i:%(sec)02i",
    "Input file (.avs):" : u"Eingabedatei (.avs):",
    "Output file (.avi):" : u"Ausgabedatei (.avi):",
    "# of passes:" : u"# of passes:",
    "Priority:" : u"Priorität",
    "Error: Unknown button" : u"Fehler: Unkekannte Schaltfläche",
    "Save the avi as" : u"AVI-Datei speichern als",
    "Avi file (*.avi)|*.avi" : u"AVI-Datei (*.avi)|*.avi",
    "Input file does not exist!" : u"Eingabedatei existiert nicht!",
    "Input file must be an avisynth script!" : u"Eingabedatei muss ein AviSynthscript sein!",
    "Output path does not exist!" : u"Ausgangspfad existiert nicht!",
    "# of passes must be an integer!" : u"# of passes (Durchläufe) muß eine Ganzzahl (integer) sein !",
    "Priority must be an integer!" : u"Priorität muss eine Ganzzahl sein!",
    "Stop" : u"Stop",
    "Done" : u"Erledigt",
    "Process stopped." : u"Vorgang gestoppt.",
    "Processing..." : u"Bearbeitung...",
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"Beendet in %(hr)i Stunde(n) and %(min)i Minute(n).",
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"Beendet in %(min)i Minute(n) and %(sec)i Sekunde(n).",
    "Finished in %(time).1f seconds." : u"Beendet in %(time).1f Sekunden.",
    "Filesize: %(size).2f MB" : u"Dateigrösse: %(size).2f MB",
    "The current script contains errors, exiting." : u"", # New in v2.2.1
    "Save as AVI" : u"Speichern als AVI-Datei",
}