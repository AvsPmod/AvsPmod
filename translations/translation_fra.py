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

# French traslation authors:
#   André v2.0.2

version = "2.2.1"

messages = {
    "Find" : u"Rechercher",
    "Replace" : u"Remplacer",
    "Cannot find \"%(text)s\"." : u"\"%(text)s\". est introuvable !",
    "Information" : u"",
    "Replace Information" : u"Remplacer l'information",
    "Replaced %(count)i times" : u"Remplacé %(count)i fois",
    "AviSynth fonts and colors" : u"APolices et couleurs AvsP",
    "Background" : u"Arrière-plan",
    "Font" : u"Police",
    "Text color" : u"Couleur",
    "OK" : u"", # New in v1.2.1
    "Cancel" : u"Annuler",
    "Scrap Window" : u"Bloc-note",
    "Undo" : u"Annuler",
    "Redo" : u"Refaire",
    "Cut" : u"Couper",
    "Copy" : u"Copier",
    "Paste" : u"Coller",
    "Select all" : u"Sélectionner tout",
    "Refresh" : u"Rafraîchir",
    "Insert frame #" : u"Insérer No frame",
    "Save to file..." : u"Enregistrer dans le fichier...",
    "Clear all" : u"Désélectionner tout",
    "Toggle scrap window" : u"Afficher bloc-note",
    "Save script" : u"Enregistrer le script",
    "Error: no contextMenu variable defined for window" : u"Erreur : variable du menu contextuel non définie pour cette fenêtre",
    "Text document (*.txt)|*.txt|All files (*.*)|*.*" : u"Document texte (*.txt)|*.txt|Tous (*.*)|*.*",
    "Save scrap text" : u"Enregistrer le bloc-note",
    "This field must contain a value!" : u"Ce champ doit être rempli !",
    "This slider label already exists!" : u"Un appel vers ce curseur existe déjà !",
    "Invalid slider label modulo syntax!" : u"Syntaxe du modulo dans l'appel du curseur incorrecte !",
    "This field must contain a number!" : u"Ce champ doit contenir un nombre !",
    "The min value must be less than the max!" : u"La valeure min doit être inférieure à la valeur max !",
    "The initial value must be between the min and the max!" : u"La valeur intiale doit être comprise entre le min et le max !",
    "The min value must be a multiple of %(mod)s!" : u"La valeur min doit être un multiple de %(mod)s!",
    "The max value must be a multiple of %(mod)s!" : u"La valeur max doit être un multiple de %(mod)s!",
    "The initial value must be a multiple of %(mod)s!" : u"La valeur initiale doit être un multiple de %(mod)s!",
    "The difference between the min and max must be greater than %(mod)s!" : u"La différence entre le min et le max doit être >= %(mod)s!",
    "Error" : u"Erreur",
    "Define user slider" : u"Définir un curseur utilisateur",
    "Slider label:" : u"Nom du curseur :",
    "Min value:" : u"Valeure min :",
    "Max value:" : u"Valeure max :",
    "Initial value:" : u"Valeur initiale:",
    "Add or override AviSynth functions in the database" : u"Ajoute ou modifie des fonctions de la base de données",
    "Core filters" : u"Filtres internes",
    "Plugins" : u"", # New in v2.0.0
    "User functions" : u"Scripts utilisateur",
    "Script functions" : u"Fonctions",
    "Clip properties" : u"Propriétés clip",
    "Include %(title)s in autcompletion lists" : u"Inclure %(title)s dans les listes déroulantes automatiques",
    "New function" : u"Nouvelle fonction",
    "Edit selected" : u"Editer sélection",
    "Delete selected" : u"Supprimer sélection",
    "Select installed" : u"Sél. installées",
    "Import from files" : u"", # New in v2.2.1
    "Export customizations" : u"Exporter personnalisation",
    "Clear customizations" : u"Supprimer personnalisation",
    "Clear manual presets" : u"Supprimer presets manuels",
    "When importing, don't show the choice dialog" : u"", # New in v2.2.1
    "Edit function information" : u"Editer les informations de la fonction",
    "Name:" : u"Nom:",
    "Type:" : u"", # New in v2.0.0
    "clip property" : u"propriété clip",
    "core filter" : u"filtre interne",
    "plugin" : u"", # New in v2.0.0
    "script function" : u"fonction",
    "user function" : u"script utilisateur",
    "Arguments:" : u"Paramètres :",
    "define sliders" : u"définir les curseurs",
    "reset to default" : u"réinitialiser les paramètres",
    "Slider information" : u"Edition des curseurs",
    "Preset:" : u"Texte automatique :",
    "Auto-generate" : u"Générer automatiquement",
    "Filter name already exists!" : u"Ce nom de filtre existe déjà !",
    "Invalid filter name!" : u"Nom de filtre invalide !",
    "Renaming not allowed!" : u"Renommage refusé !",
    "You must use dllname_function naming format for plugins!" : u"Vous devez utiliser le format nomDeFicherDll_fonction pour nommer les plugins!",
    "Open Customization files, Avisynth scripts or Avsp options files" : u"", # New in v2.2.1
    "All supported|*.txt;*.avsi;*.avs;*.dat|Customization file (*.txt)|*.txt|AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|AvsP data (*.dat)|*.dat|All files (*.*)|*.*" : u"", # New in v2.2.1
    "Unrecognized files" : u"", # New in v2.2.1
    "Select import functions" : u"", # New in v2.2.1
    "select all" : u"", # New in v2.2.1
    "select none" : u"", # New in v2.2.1
    "select all (file only)" : u"", # New in v2.2.1
    "select none (file only)" : u"", # New in v2.2.1
    "Red - a customized function already exists." : u"", # New in v2.2.1
    "No customizations to export!" : u"Aucune personnalisation à exporter !",
    "Save filter customizations" : u"Enregistrer les personnalisations des filtres",
    "Customization file (*.txt)|*.txt|All files (*.*)|*.*" : u"Fichier personnalisation (*.txt)|Tout (*.*)|*.*",
    "This will delete all filter customizations. Continue?" : u"Supprimer toute les personnalisations (*) ?",
    "Warning" : u"Attention",
    "This will delete all manually defined presets. Continue?" : u"Supprimer les presets manuels (~) ?",
    "Do you want to delete this custom filter entirely?" : u"Supprimer completement ce filtre personnalisé ?",
    "Edit filter database" : u"Editer la base de donnée des filtres",
    "Default" : u"Par défaut ",
    "Min value" : u"Min",
    "Max value" : u"Max",
    "Step size" : u"Taille de pas",
    "Value list (comma separated)" : u"Liste de paramètres (séparés par ,)",
    "Value must be True or False!" : u"Paramètre doit etre True ou False !",
    "Must enter a value list!" : u"Une liste de paramètres est requise !",
    "Export filter customizations" : u"Exporter les filtres utilisateurs",
    "Import filter customizations" : u"Importer les filtres utilisateurs",
    "Select filters to export:" : u"Sélectionner les filtres à exporter :",
    "Select filters to import from the file:" : u"Sélectionner les filtres du fichier à importer :",
    "Overwrite all data" : u"Ecraser toutes les données",
    "You must select at least one filter!" : u"Vous devez sélectionner au moins 1 filtre !",
    "Error: minValue must be less than maxValue" : u"Erreur : minValue doit être inférieure à maxValue",
    "New File" : u"Nouveau Fichier",
    "Windows Bitmap (*.bmp)" : u"", # New in v1.3.6
    "Animation (*.gif)" : u"", # New in v2.2.1
    "JPEG (*.jpg)" : u"", # New in v1.3.6
    "Zsoft Paintbrush (*.pcx)" : u"", # New in v2.2.1
    "Portable Network Graphics (*.png)" : u"", # New in v1.3.6
    "Netpbm (*.pnm)" : u"", # New in v2.2.1
    "Tagged Image File (*.tif)" : u"", # New in v2.2.1
    "ASCII Text Array (*.xpm)" : u"", # New in v2.2.1
    "Windows Icon (*.ico)" : u"", # New in v2.2.1
    "fps" : u"",
    "Frame" : u"",
    "A crash detected at the last running!" : u"", # New in v2.2.1
    "&Zoom" : u"", # New in v2.2.1
    "%s translation file updated with new messages to translate" : u"", # New in v2.2.1
    "Translation updated" : u"", # New in v2.2.1
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.2.1
    "%s language couldn't be loaded" : u"", # New in v2.2.1
    "Paths" : u"", # New in v2.2.1
    "AvsP help directory:" : u"Répertoire aide d'AvsP",
    "Location of the AvsP help directory" : u"Emplacement du répertoire d'aide d'AvsP",
    "Avisynth directory:" : u"Répertoire d'Avisynth :",
    "Location of the avisynth installation directory" : u"Emplacement du répertoire d'installation d'Avisynth",
    "Avisynth help file/url:" : u"Fichier / URL d'aide d'Avisynth :",
    "Location of the avisynth help file or url" : u"Emplacement du fichier ou URL d'aide d'Avisynth",
    "External player:" : u"Lecteur externe :",
    "Location of external program for script playback" : u"Emplacement du programme extérieur pour lecture de script",
    "Additional arguments when running the external player" : u"Paramètres additionnels pour le lecteur externe",
    "External player extra args:" : u"Paramètres pour le lecteur externe :",
    "Documentation search paths:" : u"Chemins de recherche documentation :",
    "Specify which directories to search for docs when you click on a filter calltip" : u"Indiquer ici les chemins des répertoires dans lesquelles chercher les documents d'aide correspondant aux filtres avisynth et accessible par clic sur les bulles d'aide",
    "Documentation search url:" : u"URL pour la recherche de documentation :",
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"L'adresse web de recherche de documents si non trouvé localement (%filtername% contient le nom du filtre)",
    "Text" : u"", # New in v2.2.1
    "Show filter calltips" : u"Afficher les bulle d'aides des filtres",
    "Turn on/off automatic tips when typing filter names" : u"Active/Désactive les bulles d'aide automatiques en cours de frappe des noms de filtres",
    "Always show calltips any time the cursor is within the filter's arguments" : u"Active/Désactive l'affichage automatique des bulles d'aide quand le curseur se situe dans les paramètres d'un filtre",
    "Frequent calltips" : u"Bulles d'aide automatiques",
    "Syntax highlighting" : u"Mise en évidence / coloration syntaxique",
    "Turn on/off avisynth-specific text colors and fonts" : u"Active/Désactive les couleures et polices spécifiques à Avisynth",
    "Show autocomplete on capital letters" : u"Sur lettres majuscules, afficher la liste automatique ",
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"Active/Désactive la liste des filtres quand un mot est commencé par une lettre en majuscule",
    "Show autocomplete list when typing a certain amount of letters" : u"", # New in v2.2.1
    "Don't allow lines wider than the window" : u"Retour à la ligne automatique si la ligne dépasse la taille de la fenêtre",
    "Wrap text" : u"Retour à la ligne auto",
    "Draw lines at fold points" : u"", # New in v2.2.1
    "For code folding, draw a line underneath if the fold point is not expanded" : u"", # New in v2.2.1
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Cocher pour insérer de vrais caractères tabulation au lieu d'espaces quand la touche tab est utilisée",
    "Use tabs instead of spaces" : u"Utiliser des tab au lieu d'espaces",
    "Set the size of the tabs in spaces" : u"Défini la taille d'un tab en espaces",
    "Tab width" : u"Largeur de tab",
    "Initial space to reserve for the line margin in terms of number of digits" : u"Largeur de marge de gauche affichant les numéros de ligne (en nombre de chiffres)",
    "Line margin width" : u"Largeur de la marge",
    "Autocomplete" : u"Remplissage automatique",
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
    "Autoparentheses level" : u"Niveau de parenthèses automatiques",
    "Close \"()\"" : u"Fermés \"()\"", # New in v1.3.2
    "Determines parentheses to insert upon autocompletion" : u"Détermine les parenthèses à insérer en fin d'autocompletion",
    "None \" \"" : u"Aucune",
    "Open \"(\"" : u"Ouverte \"(\"", # New in v1.3.2
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"Indique quelle touche activele texte automatique quand la liste déroulante d'autocompletion est visible",
    "None" : u"Aucune",
    "Preset activation key" : u"Touche pour activation preset",
    "Return" : u"Retour chariot",
    "Tab" : u"", # New in v2.0.0
    "Video" : u"Vidéo",
    "Constantly update video while dragging" : u"Mettre à jour la vidéo en permanence pendant les déplacements du curseur",
    "Update the video constantly when dragging the frame slider" : u"Met à jour en permanence la fenêtre video lors des déplacement du curseur de frames",
    "Enable line-by-line update" : u"Activer la mise à jour ligne à ligne",
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"Permet d'activer la mise à jour de la fenêtre vidéo chaque fois que le curseur change de ligne",
    "Focus the video preview upon refresh" : u"Activer la fenêtre vidéo lors d'un raffraichissement",
    "Switch focus to the video preview window when using the refresh command" : u"Déplace le focus sur la fenêtre vidéo lorsque la commande Raffraichir est utilisée",
    "Refresh preview automatically" : u"", # New in v2.2.1
    "Refresh preview when switch focus on video window or change a value in slider window" : u"", # New in v2.2.1
    "Seeking to a certain frame will seek to that frame on all tabs" : u"", # New in v2.2.1
    "Shared timeline" : u"", # New in v2.2.1
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"", # New in v2.2.1
    "Allow AvsPmod to resize the window" : u"", # New in v2.2.1
    "Separate video preview window" : u"Séparer la fenêtre vidéo",
    "Use a separate window for the video preview" : u"Utilise une fenêtre séparée pour afficher la vidéo",
    "Min text lines on video preview" : u"Nombre de lignes min dans l'éditeur lors de l'affichage vidéo",
    "Minimum number of lines to show when displaying the video preview" : u"Nombre de lignes minimum a afficher dans la partie éditeur lors de l'affichage de la vidéo",
    "Customize the video information shown in the program status bar" : u"Personnaliser les informations de la barre d'état de la fenêtre vidéo",
    "Customize video status bar..." : u"Personnaliser la barre d'état vidéo...",
    "User Sliders" : u"Curseurs utilisateur",
    "Hide slider window by default" : u"Par défaut, cacher la zone des curseurs",
    "Keep the slider window hidden by default when previewing a video" : u"Par défaut, garde la zone des curseurs cachée dans la fenetre de prévisualisation vidéo",
    "Create user sliders automatically" : u"Créer des curseurs utilisateurs automatiquement",
    "Create user sliders automatically using the filter database" : u"Cré des curseurs utilisateurs automatiquement depuis la base de données des filtres",
    "Create user sliders for int and float arguments" : u"Cré des curseurs utilisateurs pour les paramètres int et float",
    "type int/float (numerical slider)" : u"int/float (curseurs numériques)",
    "Create color pickers for hex color arguments" : u"Cré un bouton pour choix de couleur en hex",
    "type int (hex color)" : u"int (couleur en hex)",
    "Create radio boxes for bool arguments" : u"Cré des boutons pour les paramètres bool",
    "type bool" : u"bool",
    "Create listboxes for string list arguments" : u"Cré une liste de string a sélectionner",
    "type string (list)" : u"string (liste)",
    "Create filename pickers for string filename arguments" : u"Cré un bouton pour choisir des noms de fichier",
    "type string (filename)" : u"string (nom de fichiers)",
    "Create placeholders for arguments which have no database information" : u"Cré des emplacements pour les arguments non documentés dans la dase de donnée",
    "undocumented" : u"non-documentés",
    "Determines which filters will initially have hidden arguments in the slider window" : u"Détermine quels filtres auront leurs arguments cachés dans la zone des curseurs",
    "Fold all" : u"Cacher tout",
    "Fold non-numbers" : u"Cacher non-numérique",
    "Fold none" : u"Montrer tout",
    "Fold startup setting" : u"Paramètres par défaut dans la zone de curseurs",
    "Filter exclusion list:" : u"Liste d'exclusion de filtres :",
    "Specify filters never to build automatic sliders for" : u"Défini les filtres pour lesquels aucun curseurs automatique n'apparait",
    "Save/Load" : u"", # New in v2.2.1
    "Automatically save the session on shutdown and load on next startup" : u"Enregistrer automatiquement la session à la fermeture et la recharger au prochain démarrage",
    "Save session for next launch" : u"Enregistrer la session pour le prochain démarrage",
    "Always load startup session" : u"Toujours recharger la dernière session",
    "Always load the auto-saved session before opening any other file on startup" : u"Au démarrage, permet de toujours charger la dernière session sauvegardée avant d'ouvrir d'autre(s) fichier(s)",
    "Always hide the video preview window when loading a session" : u"", # New in v2.2.1
    "Don't preview when loading a session" : u"", # New in v2.2.1
    "Backup session when previewing" : u"", # New in v2.2.1
    "If checked, the current session is backed up prior to previewing any new script" : u"Si actif, la session courante est sauvegardée avant chaque prévisualisation de script",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"Propose de sauver le script avant d'afficher la vidéo correspondante (inopérant avec l'option Afficher la vidéo du script modifié non enregistré)",
    "Prompt to save when previewing" : u"Proposer de sauvegarder le script avant d'afficher la vidéo correspondante",
    "Create a temporary preview script with unsaved changes when previewing the video" : u"Cré un script temporaire incluant les modifications non sauvegardées et servant à la prévisualisation vidéo",
    "Preview scripts with unsaved changes" : u"", # New in v2.2.1
    "Prompt to save each script with unsaved changes when exiting the program" : u"Demande pour chaque script modifié non sauvegardé si une sauvegarde est nécessaire",
    "Prompt to save scripts on program exit" : u"A la fermeture, demander si les modifications du(es) script(s) sont à enregistrer",
    "Save *.avs scripts with AvsPmod markings" : u"", # New in v2.2.1
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"", # New in v2.2.1
    "Misc" : u"Divers",
    "Choose the language used for the interface" : u"", # New in v2.2.1
    "Language *" : u"", # New in v2.2.1
    "Show keyboard images in the script tabs when video has focus" : u"Quand la fenêtre vidéo a le focus, affiche les images claviers dans les onglets des scripts",
    "Use keyboard images in tabs" : u"Utiliser les images claviers dans les onglets",
    "Show tabs in multiline style" : u"", # New in v2.2.1
    "There can be several rows of tabs" : u"", # New in v2.2.1
    "All tabs will have same width" : u"", # New in v2.2.1
    "Show tabs in fixed width" : u"", # New in v2.2.1
    "Enable scroll wheel through similar tabs" : u"", # New in v2.2.1
    "Mouse scroll wheel cycles through tabs with similar videos" : u"Permettre de se déplacer d'onglet à onglet (videos similaires seulement) avec la roue de la sourie",
    "Only allow a single instance of AvsPmod" : u"", # New in v2.2.1
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"", # New in v2.2.1
    "Show warning for bad plugin naming at startup" : u"", # New in v2.2.1
    "Max number of recent filenames" : u"Nombre max de fichiers récents",
    "This number determines how many filenames to store in the recent files menu" : u"Ce nombre détermine le nombre de fichiers récents max affichés dans le menu Fichier",
    "Custom jump size:" : u"Taille personnalisée du saut:",
    "Jump size used in video menu" : u"Défini la distance parcourue lors d'un saut personnalisé dans la fenêtre vidéo",
    "Custom jump size units" : u"Unité du saut personnalisé",
    "Units of custom jump size" : u"Choix de l'unité de mesure du saut personnalisé",
    "hours" : u"heures",
    "minutes" : u"", # New in v1.3.3
    "seconds" : u"secondes",
    "frames" : u"", # New in v1.3.3
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
    "Indent selection" : u"Incrémenter sélection",
    "Unindent selection" : u"Décrémenter sélection",
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
    "25%" : u"", # New in v1.3.8
    "50%" : u"", # New in v1.3.8
    "100% (normal)" : u"", # New in v1.3.8
    "200%" : u"", # New in v1.3.8
    "300%" : u"", # New in v1.3.8
    "400%" : u"", # New in v1.3.8
    "Fill window" : u"Remplir fenêtre",
    "Fit inside window" : u"Ajuster à la fenêtre",
    "Vertically" : u"", # New in v2.2.1
    "Horizontally" : u"", # New in v2.2.1
    "&File" : u"&Fichier",
    "Create a new tab" : u"Créer un nouvel onglet",
    "New tab" : u"Nouvel onglet",
    "Open an existing script" : u"Ouvrir un script existant",
    "Open..." : u"Ouvrir...",
    "Close tab" : u"Fermer l'onglet",
    "Close the current tab" : u"Fermer l'onglet courant",
    "Close all tabs" : u"Fermer tous les onglets",
    "Close every tab" : u"Ferme tous les onglets",
    "Rename tab" : u"", # New in v2.2.1
    "Rename the current tab. If script file is existing, also rename it" : u"", # New in v2.2.1
    "Save the current script" : u"Enregistre le script courant",
    "Choose where to save the current script" : u"Choisir où sauvegarder le script courant",
    "Save script as..." : u"Enregistrer le script sous...",
    "Load a session into the tabs" : u"Ouvre les onglets d'une session",
    "Load session..." : u"Ouvrir session...",
    "Save all the scripts as a session, including slider info" : u"Enregistrer tous les scripts ouverts dans une session, informations curseurs incluses",
    "Save session..." : u"Enregistrer session...",
    "Backup current session" : u"Sauvegarder la session en cours",
    "Backup the current session for next program run" : u"Sauvegarde la session courante pour le prochain redémarrage du programme",
    "Next tab" : u"Onglet suivant",
    "Switch to next script tab" : u"Passe à l'onglet de script suivant",
    "Previous tab" : u"Onglet précédent",
    "Switch to previous script tab" : u"Passe à l'onglet de script précédent",
    "Show the scrap window" : u"Affiche le bloc-note",
    "&Exit" : u"&Quitter",
    "Exit the program" : u"Quitte le programme",
    "&Edit" : u"&Editer",
    "Undo last text operation" : u"Annuler la dernière opération dans l'éditeur de texte",
    "Redo last text operation" : u"Refaire la dernière opération dans l'éditeur de texte",
    "Cut the selected text" : u"Couper la sélection",
    "Copy the selected text" : u"Copier la sélection",
    "Paste the selected text" : u"Coller la sélection",
    "Find..." : u"Chercher...",
    "Open a find text dialog box" : u"Ouvre une boîte de dialogue de recherche",
    "Find next" : u"Chercher suivant",
    "Find the next instance of given text" : u"Cherche l'instance suivante d'un texte donné",
    "Open a replace text dialog box" : u"Ouvre une boîte de dialogue Remplacer",
    "Replace..." : u"Remplacer...",
    "Select All" : u"Sélectionner tout",
    "Select all the text" : u"Sélectionne tout le texte",
    "&Insert" : u"", # New in v2.2.1
    "Choose a source file to insert into the text" : u"Choisir un fichier source à insérer dans le texte",
    "Insert source..." : u"Insérer source...",
    "Get a filename from a dialog box to insert into the text" : u"Récupère un nom de fichier à insérer dans le texte depuis la boîte de dialogue",
    "Insert filename..." : u"Insérer nom de fichier...",
    "Choose a plugin dll to insert into the text" : u"Récupère le nom d'un fichier dll à insérer dans le texte depuis la boîte de dialogue",
    "Insert plugin..." : u"Insérer plugin...",
    "Insert a user-scripted slider into the text" : u"Insère un curseur utilisateur dans le texte",
    "Insert user slider..." : u"Insérer curseur utilisateur...",
    "Insert a tag which indicates a separator in the user slider window" : u"Insert une balise dans le script indiquant une ligne de séparation dans la zone des curseurs",
    "Insert user slider separator" : u"Insérer séparateur de curseurs",
    "Insert the current frame number into the text" : u"Insèrer le numéro de la frame courante dans le texte",
    "Add tags surrounding the selected text for toggling with the video preview" : u"Ajoute des balises entourant le texte sélectionné pour activer / désactiver ce code dans la fenêtre vidéo",
    "Tag selection for toggling" : u"Ajouter balises de code",
    "Clear all tags" : u"Supprimer toutes les balises",
    "Clear all toggle tags from the text" : u"Supprime toutes les balises dans la fenêtre de l'éditeur de texte",
    "Indent the selected lines" : u"Tabule la sélection vers la droite",
    "Unindent the selected lines" : u"Tabule la sélection vers la gauche",
    "Block comment" : u"Commenter le block",
    "Comment or uncomment selected lines" : u"Commente / décommente les lignes sélectionnées",
    "Comment at start of a text style or uncomment" : u"", # New in v2.2.1
    "Style comment" : u"", # New in v2.2.1
    "Toggle current fold" : u"", # New in v2.2.1
    "Toggle the fold point On/OFF at the current line" : u"", # New in v2.2.1
    "Toggle all fold points On/OFF" : u"", # New in v2.2.1
    "Toggle all folds" : u"Permutter (montrer/cacher) tous les curseurs",
    "&AviSynth function" : u"", # New in v2.2.1
    "Show list of filternames matching the partial text at the cursor" : u"Affiche la liste des filtres correspondant au texte partiel au niveau du curseur",
    "Autocomplete all" : u"", # New in v2.2.1
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"", # New in v2.2.1
    "Show calltip" : u"Afficher bulle d'aide",
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"Affiche la bulle d'aide associée à ce filtre (uniquement si le curseur se situe dans les paramètres)",
    "Show function definition" : u"Afficher/éditer la fonction",
    "Show the AviSynth function definition dialog for the filter" : u"Affiche la définition AvsP de la fonction en cours et permet sa modification",
    "Filter help file" : u"Aide filtre",
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"Charge le fichier d'aide associé à ce filtre (uniquement si le curseur se situe dans les paramètres ou si le nom du filtre est sélectionné",
    "&Miscellaneous" : u"", # New in v2.2.1
    "Move line up" : u"Monter ligne",
    "Move the current line or selection up by one line" : u"Monte la ligne courante ou sélection d'une ligne vers le haut",
    "Move line down" : u"Descendre ligne",
    "Move the current line or selection down by one line" : u"Descend la ligne courante ou sélection d'une ligne vers le bas",
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"Copie dans le presse-papier le script courant sans le code spécifique d'AvsP (curseurs utilisateur, Balises)",
    "Copy unmarked script to clipboard" : u"Copier le script nu dans le presse-papier",
    "Copy avisynth error to clipboard" : u"", # New in v2.2.1
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"", # New in v2.2.1
    "&Video" : u"&Vidéo",
    "Add/Remove bookmark" : u"", # New in v2.2.1
    "Mark the current frame on the frame slider" : u"Marque la frame courante sur le curseur de frames",
    "Clear all bookmarks" : u"Supprimer tout",
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
    "Go to next bookmarked frame" : u"Va au favori suivant",
    "Next bookmark" : u"Favori suivant",
    "Go to previous bookmarked frame" : u"Va au favori précédent",
    "Previous bookmark" : u"Favori précédent",
    "Forward 1 frame" : u"Avancer 1 frame",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"Affiche la frame suivante (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Backward 1 frame" : u"Reculer 1 frame",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"Affiche la frame précédente (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Forward 1 second" : u"Avancer 1 seconde",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"Avance d'une seconde dans la vidéo et affiche la frame correspondante (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Backward 1 second" : u"Reculer 1 seconde",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"Recule d'une seconde dans la vidéo et affiche la frame correspondante (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Forward 1 minute" : u"Avancer 1 minute",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"Avance d'une minute dans la vidéo et affiche la frame correspondante (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Backward 1 minute" : u"Reculer 1 minute",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"Recule d'une minute dans la vidéo et affiche la frame correspondante (raccourci clavier actif si le focus se situe sur la fenêtre vidéo)",
    "Forward x units" : u"Avance personnalisée",
    "Jump forward by x units (you can specify x in the options dialog)" : u"Avance de x unités dans la vidéo (personnalisable dans les Options>Paramètres...>Vidéo)",
    "Backwards x units" : u"Recule personnalisé",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"Recule de x unités dans la vidéo (personnalisable dans les Options>Paramètres...>Vidéo)",
    "Go to first frame" : u"Aller à la première frame",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"Va à la première frame vidéo (raccourcis clavier actifs quand la fenêtre vidéo est active",
    "Go to last frame" : u"Aller à la dernière frame",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"Va à la dernière frame vidéo (raccourcis clavier actifs quand la fenêtre vidéo est active",
    "Go to last scrolled frame" : u"Aller à la frame précédemment sélectionnée",
    "Last scrolled frame" : u"frame précédente",
    "Enter a video frame or time to jump to" : u"Entrer un numero de frame ou temps à atteindre",
    "Go to frame..." : u"Aller à la frame...",
    "Crop editor..." : u"Editeur rognage",
    "Show the crop editor dialog" : u"Affiche la fenêtre de l'éditeur rognage",
    "&Trim selection editor" : u"", # New in v2.2.1
    "Show the trim selection editor dialog" : u"Affiche la noite de dialogue des sélections par fonction trim",
    "Show trim selection editor" : u"Affiche l'éditeur de trim",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"Défini le début d'une sélection (affiche l'éditeur de trim si invisible)",
    "Set selection startpoint" : u"Définir le début de la sélection",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"Défini la fin d'une sélection (affiche l'éditeur de trim si invisible)",
    "Set selection endpoint" : u"Définir la fin de la sélection",
    "Zoom video preview to 25%" : u"Affiche la video avec une taille d'image de 25%",
    "Zoom video preview to 50%" : u"Affiche la video avec une taille d'image de 50%",
    "Zoom video preview to 100% (normal)" : u"Affiche la video avec une taille d'image de 100% (par défaut)",
    "Zoom video preview to 200%" : u"Affiche la video avec une taille d'image de 200%",
    "Zoom video preview to 300%" : u"Affiche la video avec une taille d'image de 300%",
    "Zoom video preview to 400%" : u"Affiche la video avec une taille d'image de 400%",
    "Zoom video preview to fill the entire window" : u"Redimensionne la vidéo pour remplir la fenêtre",
    "Zoom video preview to fit inside the window" : u"Redimensionne la vidéo pour s'ajuster a la taille de la fenêtre",
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
    "Save image as..." : u"Enregistrer l'image sous...",
    "Save the current frame as a bitmap" : u"Enregistre la frame courante en tant que bitmap (.BMP)",
    "Force the script to reload and refresh the video frame" : u"Force le rechargement du script et affiche / raffraîchi la fenêtre vidéo",
    "Refresh preview" : u"Raffraîchir vidéo",
    "Show/Hide the preview" : u"", # New in v2.2.1
    "Toggle the video preview" : u"Active / Désactive la fenêtre vidéo",
    "Release all open videos from memory" : u"Décharge de la mémoire toutes les vidéos en cours",
    "Release all videos from memory" : u"Décharger toutes les vidéos de la mémoire",
    "Switch focus between the video preview and the text editor" : u"Bascule le focus entre l'éditeur de texte et la fenêtre vidéo",
    "Switch video/text focus" : u"Basculer focus vidéo/texte",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"Affiche/cache la zone des curseurs (équivalent à double cliquer sur le diviseur)",
    "Toggle the slider sidebar" : u"Afficher/cacher zone curseurs",
    "External player" : u"Lecteur externe",
    "Play the current script in an external program" : u"Joue le script courant dans un programme externe",
    "Show information about the video in a dialog box" : u"Affiche les informations concernant la vidéo dans une boite de dialogue",
    "Video information" : u"Information sur la vidéo",
    "&Options" : u"O&ptions",
    "Always on top" : u"Toujours au premier plan",
    "Keep this window always on top of others" : u"Conserve cette fenêtre au-dessus des autres",
    "Disable video preview" : u"Désactiver la fenêtre vidéo",
    "If checked, the video preview will not be shown under any circumstances" : u"Quand activé, la fenêtre vidéo n'est plus accessible / mise à jour",
    "Associate .avs files with AvsP" : u"Associer les fichiers .avs avec AvsP",
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"Associe dans le registre windows les .avs avec AvsP",
    "AviSynth function definition..." : u"Catalogue des filtres AviSynth...",
    "Edit the various AviSynth script fonts and colors" : u"Permet de personnaliser la coloration syntaxique de AvsP",
    "Fonts and colors..." : u"Polices et couleurs...",
    "Edit the extension-based templates for inserting sources" : u"Permet d'éditer le remplissage automatique du script lors de l'ajout de noms de fichiers d'extension connu",
    "Extension templates..." : u"Proformat extensions...",
    "Configure the program keyboard shortcuts" : u"Permet de personnaliser les raccourcis clavier",
    "Keyboard shortcuts..." : u"", # New in v2.2.1
    "Configure program settings" : u"Permet de configurer les paramètres internes d'AvsP",
    "Program settings..." : u"Paramètres...",
    "&Help" : u"&Aide",
    "Animated tutorial" : u"Tutoriel animé",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"Affiche un tutoriel d'AvsP animé (depuis le site web d'AvsP)",
    "Learn more about AvsP text features (from the AvsP website)" : u"En apprendre plus sur les fonctions texte d'AvsP (depuis le site web d'AvsP)",
    "Text features" : u"Fonctions texte",
    "Learn more about AvsP video features (from the AvsP website)" : u"En apprendre plus sur les fonctions vidéo d'AvsP (depuis le site web d'AvsP)",
    "Video features" : u"Fonctions vidéo",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"En apprendre plus sur les curseurs utilisateur dans AvsP (depuis le site web d'AvsP)",
    "User sliders" : u"Curseurs utilisateur",
    "Learn more about AvsP macros (from the AvsP website)" : u"En apprendre plus sur les macros dans AvsP (depuis le site web d'AvsP)",
    "Macros" : u"&Macros",
    "Avisynth help" : u"Aide Avisynth",
    "Open the avisynth help html" : u"Ouvre le fichier d'aide html d'avisynth",
    "Open Avisynth plugins folder" : u"", # New in v2.2.1
    "Open the avisynth plugins folder" : u"", # New in v2.2.1
    "About this program" : u"Version / Credits",
    "About AvsPmod" : u"", # New in v2.2.1
    "Previous frame" : u"Frame précédente",
    "Next frame" : u"Frame suivante",
    "Run the script with an external program" : u"Lit le script avec le lecteur externe",
    "Run the selected tool" : u"Démarre l'outils sélectionné",
    "&Tools" : u"", # New in v2.2.1
    "a macro check item" : u"", # New in v2.2.1
    "a macro radio item" : u"", # New in v2.2.1
    "Run selected macro" : u"Exécute la macro sélectionnée",
    "View the readme for making macros" : u"Affiche le fichier lisez-moi de création des macros",
    "Open the macros folder" : u"", # New in v2.2.1
    "&Macros" : u"", # New in v2.2.1
    "Close" : u"Fermer",
    "Rename" : u"", # New in v2.2.1
    "Save" : u"Enregistrer",
    "Save as..." : u"Enregistrer sous...",
    "Copy to new tab" : u"Copier vers un nouvel onglet",
    "Reposition to" : u"", # New in v2.2.1
    "Crop editor" : u"Rognage",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"Quand cette boite de dialogue est visible vous pouvez déplacer la bordure de crop la plus proche du pointeur de la souris lors du clic",
    "At script end" : u"En fin de script",
    "At script cursor" : u"A l'emplacement du curseur",
    "Copy to clipboard" : u"Copier dans le presse-papier",
    "Insert Crop() command:" : u"Insérer une commande Crop() :",
    "Apply" : u"OK",
    "Trim editor" : u"Editeur de Trim",
    "Selection options" : u"Options de sélection",
    "Keep selected regions" : u"Conserver les régions sélectionnées",
    "Keep unselected regions" : u"Conserver les régions non-sélectionnées",
    "Mark video frames inside/outside selection" : u"Marquer les frames vidéos dans / en-dehors de la sélection",
    "Use Dissolve() with overlap frames:" : u"", # New in v2.2.1
    "Insert Trim() commands:" : u"Insérer une commande Trim() :",
    "Insert Dissolve() commands:" : u"", # New in v2.2.1
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"Utiliser les boutons additionnels sur la barre du curseur de frames pour créer les selections de frames via Trim",
    "File does not exist!" : u"Ce fichier n'existe pas !",
    "All files (*.*)|*.*" : u"Tous (*.*)",
    "Select a file" : u"Sélectionner un fichier",
    "Create a separator label" : u"Créer un séparateur nommé",
    "Enter separator label" : u"Entrer un nom pour le séparateur",
    "Enter tag name:" : u"Nom de l'étiquette :",
    "Tag definition" : u"Définition de l'étiquette",
    "Chapter" : u"", # New in v2.2.1
    "Set title for bookmarks" : u"", # New in v2.2.1
    "Title" : u"", # New in v2.2.1
    "Frame No." : u"", # New in v2.2.1
    "Time **" : u"", # New in v2.2.1
    "" : u"", # New in v2.2.1
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"", # New in v2.2.1
    "Frame size:" : u"Taille de l'image :",
    "Length:" : u"Durée :",
    "Frame rate:" : u"Framerate :",
    "Colorspace:" : u"Espace de couleur :",
    "Field or frame based:" : u"Field ou frame :",
    "Parity:" : u"Parité",
    "Audio" : u"", # New in v1.3.8
    "Channels:" : u"Nombre de pistes :",
    "Hz" : u"", # New in v1.3.8
    "Sampling rate:" : u"Taux d'échantillonnage :",
    "Sample type:" : u"Type d'échantillon :",
    "bits" : u"", # New in v1.3.8
    "samples" : u"échantillons",
    "Could not find the macros folder!" : u"", # New in v2.2.1
    "Could not find %(readme)s!" : u"%(readme)s introuvable !",
    "Failed to import the selected tool" : u"L'importation de l'outils sélectionné a échouée",
    "You must restart for changes to take effect!" : u"Vous devez relancer l'application pour que les modifications soient appliquées !",
    "Basic" : u"Simple",
    "Default:" : u"Par défaut :",
    "Comment:" : u"Commentaires :",
    "Block Comment:" : u"", # New in v2.2.1
    "__END__ Comment:" : u"", # New in v2.2.1
    "Number:" : u"Nombres :",
    "Operator:" : u"Opérateurs :",
    "String:" : u"Chaines de caractères :",
    "Triple-quoted string:" : u"", # New in v1.2.1
    "Internal filter:" : u"Filtres internes :",
    "External filter:" : u"Filtres externes :",
    "Internal function:" : u"Fonctions internes :",
    "User defined function:" : u"Fonctions utilisateur :",
    "Clip property:" : u"Définitions / propriétés :",
    "AviSynth keyword:" : u"Mots clefs AviSynth :",
    "AviSynth data type:" : u"Type de donnée AviSynth :",
    "AvsP user slider:" : u"Curseurs utilisateur AvsP :",
    "Monospaced font:" : u"Police à largeur constante :",
    "Advanced" : u"Avancé",
    "Incomplete string:" : u"Chaines de caractères incomplète :",
    "Syntax highlight strings which are not completed in a single line differently" : u"Coloration syntaxique différente pour les chaînes de caractères incomplètes sur une même ligne",
    "Brace highlight:" : u"Parenthèses en cours :",
    "Bad brace:" : u"Parenthèses incorrectes :",
    "Bad number:" : u"Nombres incorrects :",
    "Margin line numbers:" : u"Nombres de la marge :",
    "Miscellaneous word:" : u"Mot divers :",
    "Calltip:" : u"Bulle d'aide :",
    "Calltip highlight:" : u"Coloration syntaxique dans la bulles d'aide :",
    "Cursor:" : u"Curseur :",
    "Selection highlight:" : u"", # New in v2.2.1
    "Current line highlight:" : u"", # New in v2.2.1
    "Highlight the line that the caret is currently in" : u"Surligne la ligne où se situe le curseur",
    "Fold margin:" : u"", # New in v2.2.1
    "Scrap window" : u"", # New in v2.2.1
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"", # New in v2.2.1
    "Use monspaced font" : u"", # New in v2.2.1
    "Insert aborted:" : u"Insertion annulée",
    "No dot required in file extension!" : u"Entrer l'extention sans . !",
    "Edit extension-based templates" : u"Editer le remplissages automatique pour les extentions de fichiers",
    "File extension" : u"Extention",
    "Template" : u"Remplissage automatique",
    "This info is used for inserting sources based on file extensions." : u"Cette info est utilisée pour remplir automatiquement le script en fonction de l'extention du fichier ajouté",
    "Any instances of *** in the template are replaced with the filename." : u"Toute répétition de *** dans la zone de remplissage automatique sera remplacé par NomDeFichier.",
    "(If you want relative paths instead of the full filename, use [***].)" : u"(Pour des chemins relatifs au lieu du nom de fichier complet, utiliser [***].)",
    "Associating .avs files will write to the windows registry." : u"Associer les .avs avec AvsP va modifier le registre de windows.",
    "Do you wish to continue?" : u"Voulez-vous continuer ?",
    "Could not find the Avisynth plugins folder!" : u"", # New in v2.2.1
    "AvsPmod version %(version)s " : u"", # New in v2.2.1
    "An AviSynth script editor" : u"Editeur de scripts Avisynth",
    "AvsP Website" : u"Site internet d'AvsP",
    "Active thread on Doom9's forum" : u"", # New in v2.2.1
    "This program is freeware under the GPL license." : u"Ce programme est gratuit (freeware) sous licence GPL.",
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"", # New in v2.2.1
    "copy as time" : u"", # New in v2.2.1
    "copy" : u"", # New in v2.2.1
    "paste" : u"", # New in v2.2.1
    "clear history" : u"", # New in v2.2.1
    "Cannot switch tabs while crop editor is open!" : u"Ne peut pas changer d'onglet quand l'editeur rognage est actif !",
    "Cannot switch tabs while trim editor is open!" : u"Ne peut pas changer d'onglet quand l'éditeur de trim est activé !",
    "pos" : u"", # New in v1.3.8
    "rgb" : u"", # New in v1.3.7
    "rgba" : u"rvba",
    "yuv" : u"", # New in v1.3.7
    "hex" : u"", # New in v1.3.7
    "Invalid crop values detected.  Continue?" : u"Valeures crop non-valide détectées. Continuer ?",
    "You must create at least one frame selection first!" : u"Vous devez dabord créer au moins 1 sélection de frames",
    "Select autocomplete keywords" : u"", # New in v2.2.1
    "exclude long names" : u"", # New in v2.2.1
    "Customize the video status bar message" : u"Personnaliser la barre d'état de la fenêtre vidéo",
    "Video status bar message:" : u"Message de la barre d'état de la fenêtre vidéo",
    "Legend" : u"Légende",
    "Current frame" : u"Frame courante",
    "Framecount" : u"Nombre de frames",
    "Current time" : u"Temps en court",
    "Total time" : u"Durée totale",
    "Width" : u"Largeur",
    "Height" : u"Hauteur",
    "Aspect ratio" : u"Ratio d'aspect",
    "Framerate" : u"", # New in v1.3.8
    "Framerate numerator" : u"Framerate (numérateur)",
    "Framerate denominator" : u"Framerate (dénominateur)",
    "Colorspace" : u"Espace de couleur",
    "Field or frame based" : u"Field ou frame",
    "Parity" : u"Parité",
    "Parity short (BFF or TFF)" : u"Abbréviation parité (BFF ou TFF)",
    "Audio rate" : u"Taux d'échantillonnage audio",
    "Audio length" : u"Durée audio",
    "Audio channels" : u"Nombre de pistes audio",
    "Audio bits" : u"Bits audio",
    "Audio type (Integer or Float)" : u"Type d'échantillon audio (Integer(Entier) ou Float(Décimal))",
    "Pixel position (cursor based)" : u"Position du pixel (curseur)",
    "Pixel hex color (cursor based)" : u"Couleur du pixel en hex (curseur)",
    "Pixel rgb color (cursor based)" : u"Couleur du pixel en rvb (curseur)",
    "Pixel yuv color (cursor based)" : u"Couleur du pixel en yuv (curseur)",
    "Pixel color (auto-detect colorspace)" : u"Couleur du pixel (auto en fct de l'esp de couleur)",
    "Program zoom" : u"Zoom courant",
    "Save changes before closing?" : u"Sauver les changements avant de fermer ?",
    "Cannot create a new tab while crop editor is open!" : u"Ne peut pas créer d'onglet quand l'éditeur de crop est activé !",
    "Cannot create a new tab while trim editor is open!" : u"Ne peut pas créer d'onglet quand l'éditeur de trim est activé !",
    "AviSynth script (avs, avsi)|*.avs;*.avsi|Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"Scripts AviSynth (avs, avsi)|*.avs;*.avsi|Fichiers sources (%(extlist1)s)|*.%(extlist2)s|Tous fichiers (*.*)|*.*",
    "Open a script or source" : u"Ouvrir un script ou source",
    "Reload the file and lose the current changes?" : u"Recharger le script sans garder les modifications ?",
    "Open this file" : u"Ouvrir ce fichier",
    "Save session before closing all tabs?" : u"Sauver la session avant de fermer tous les tabs ?",
    "AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|All files (*.*)|*.*" : u"Script AviSynth (*.avs, *.avsi)|*.avs;*.avsi|Tous (*.*)|*.*",
    "Save current script" : u"Enregistrer le script courant",
    "Directory %(dirname)s does not exist!" : u"Répertoire %(dirname)s n'existe pas !",
    "Load a session" : u"Charger une session",
    "File has been modified since the session was saved. Reload?" : u"Le script a été modifié depuis la dernière session. Recharger ?",
    "Save the session" : u"Enregistrer la session",
    "Save current frame" : u"Enregistrer la frame courante",
    "No image to save" : u"Pas d'image à enregistrer",
    "Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"Fichiers source (%(extlist1)s)|*.%(extlist2)s|Tous (*.*)|*.*",
    "Insert a source" : u"Insérer une source",
    "AviSynth plugin (*.dll)|*.dll|All files (*.*)|*.*" : u"", # New in v2.2.1
    "Insert a plugin" : u"Insérer un plugin",
    "No bookmarks defined!" : u"Aucune position de frame définie !",
    "There must be more than one unique bookmark to use this feature!" : u"Au moins 2 positions enregistrées sont requises pour utiliser cette fonction !",
    "Jump to specified bookmark" : u"Aller à la position demandée",
    "Line: %(line)i  Col: %(col)i" : u"Ligne: %(line)i  Col: %(col)i",
    "Frame Based" : u"", # New in v1.3.8
    "Field Based" : u"", # New in v1.3.8
    "Bottom Field First" : u"", # New in v1.3.8
    "BFF" : u"", # New in v1.3.8
    "Top Field First" : u"", # New in v1.3.8
    "TFF" : u"", # New in v1.3.8
    "Integer" : u"Integer (Entier)",
    "Float" : u"Float (Décimal)",
    "Edit AviSynth function information" : u"Editer les informations des filtres AviSynth",
    "  Function name" : u"  Nom du filtre",
    "Function arguments" : u"Paramètres du filtre",
    "Open filter customization file" : u"Ouvrir le fichier de filtres utilisateur",
    "Calltip-only text file (*.txt)|*.txt" : u"Fichier texte bulle d'aide seulement (*.txt)|*.txt",
    "Filter customization file (*.tag)|*.tag" : u"Fichier de filtres utilisateurs (*.tag)|*.tag",
    "Invalid filter customization file!" : u"Fichier de filtres utilisateur non valide !",
    "Save filter customization file" : u"Enregistrer le fichier de filtres utilisateur",
    "Invalid argument!" : u"Arguments non valide !",
    "Error loading AviSynth!" : u"Erreur au chargement d'AviSynth !",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"Vérifier qu'Avisynth est installé correctement et qu'aucun filtre / script avsi instable n'est présent dans le répertoire plugins d'Avisynth.",
    "Save changes before previewing?" : u"Enregistrer les modifications avant affichage vidéo ?",
    "Executable files (*.exe)|*.exe|All files (*.*)|*.*" : u"Programmes (*.exe)|*.exe|Tous (*.*)|*.*",
    "Select an external player" : u"Sélectionner un lecteur externe",
    "A program must be specified to use this feature!" : u"Un program doit être définie pour utiliser cette fonction !",
    "General settings..." : u"Paramètres généraux...",
    "Invalid slider text: min > max" : u"Erreur curseur : min > max",
    "Invalid slider text: value not in bounds" : u"Erreur curseur : la valeur introduite est en dehors de l'intervalle",
    "Invalid slider text: bad modulo label" : u"Erreur curseur : mise en forme du modulo incorrecte",
    "Invalid slider text: slider label already exists" : u"Erreur curseur : ce nom de curseur existe déjà",
    "Invalid slider text: invalid number" : u"Erreur curseur : nombre incorrecte",
    "Reset to initial value: %(value_formatted)s" : u"Retourner à la valeur initiale : %(value_formatted)s",
    "Reset to initial value: %(value2_formatted)s" : u"", # New in v2.2.1
    "Reset to default value: %(value_formatted)s" : u"Retourner à la valeur par défaut : %(value_formatted)s",
    "Invalid hexadecimal color!" : u"Couleure hex invalide !",
    "Must specify a max value!" : u"Vous devez spécifier une nombre max !",
    "Must specify a min value!" : u"Vous devez spécifier une nombre min !",
    "Min value must be a number!" : u"Min doit être un nombre !",
    "Max value must be a number!" : u"Max doit être un nombre !",
    "Default value must be a number!" : u"Défaut doit être un nombre !",
    "Step size value must be a number!" : u"La taille de pas doit etre un nombre !",
    "Left-click to select a color, right click to reset to default" : u"Clic gauche pour sélectionner une couleure, clic droit pour retourner à la valeur par défaut",
    "Source files (%(extlist1)s)|*.%(extlist2)s" : u"Fichiers sources (%(extlist1)s)|*.%(extlist2)s",
    "Toggle \"%(label)s\" section" : u"Basculer la section \"%(label)s\"",
    "Don't show me this again" : u"", # New in v2.2.1
    "Save as" : u"Enregistrer sous",
    "Select a directory" : u"Sélectionner un répertoire",
    "Enter information" : u"Entrer l'information",
    "Progress" : u"",
    "Error loading the script" : u"Erreur pendant le chargement du script",
    "Error in the macro:" : u"erreur dans la macro :",
    "Couldn't find %(macrofilename)s" : u"%(macrofilename)s introuvable",
    "Failed to open the AVI file" : u"Echec de l'ouverture du fichier AVI",
    "Failed to open the AVI frame" : u"Echec de l'ouverture de la frame AVI",
    "Failed to retrieve AVI frame" : u"Echec de la récupération de la frame AVI",
    "Ctrl" : u"", # New in v1.2.0
    "Alt" : u"", # New in v1.2.0
    "Shift" : u"", # New in v1.2.0
    "Program Settings" : u"Paramètres",
    "Browse" : u"Parcourir",
    "* Requires program restart for full effect" : u"* Nécessite de relancer l'application pour prendre effet",
    "Invalid directory!" : u"Répertoire incorrecte !",
    "Invalid filename!" : u"Nom de fichier incorrecte !",
    "Edit shortcuts" : u"Editer raccourcis",
    "Menu label" : u"Intitulé du menu",
    "Keyboard shortcut" : u"Raccourci clavier",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"Double-cliquer ou taper Entrer sur un article pour éditer son raccourci",
    "Shortcut" : u"", # New in v2.2.1
    "Action" : u"", # New in v2.2.1
    "Edit the keyboard shortcut" : u"Editer les raccourcis clavier",
    "Key:" : u"Touche :",
    "Clear" : u"Supprimer",
    "%(keyString)s not found in key string list" : u"%(keyString)s non trouvée dans la liste de touches",
    "This shortcut is being used by:" : u"Ce raccourci est utilisé par :",
    "Insert" : u"Insérer",
    "Delete" : u"Supprimer",
    "Error: key %(key)s does not exist!" : u"Erreur : la clef %(key)s n'existe pas !",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"Etes-vous sûr de vouloir renommer %(oldName)s en %(newName)s ?",
    "Question" : u"",
    "Insert a new item" : u"Insérer un nouvel object",
    "Must enter a name!" : u"Un nom doit être attribué !",
    "Item %(newKey)s already exists!" : u"Objet %(newKey)s existe déjà !",
    "Warning: no value entered for item %(newKey)s!" : u"Attention : Aucune valeure entrée pour l'objet %(newKey)s !",
    "Message" : u"",
    "Select an item to delete first" : u"Sélectionner un objet à supprimer en premier",
    "Are you sure you want to delete item %(key)s?" : u"Etes-vous sûr de vouloir supprimer l'objet %(key)s ?",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"Calculateur redimensionnement...",
    "Calculate an appropriate resize for the video" : u"Calcule un redimensionnement approprié pour la vidéo",
    "Resize calculator" : u"Calculateur de redimensionnement",
    "Input" : u"Entrée",
    "Video resolution:" : u"Résolution vidéo :",
    "Pixel aspect ratio:" : u"", # New in v2.0.0
    "Results" : u"Résultats",
    "Aspect ratio error:" : u"Erreur d'aspect ratio :",
    "Settings" : u"Paramètres",
    "Target pixel aspect ratio:" : u"Pixel aspect ratio cible :",
    "Resize block constraints:" : u"Contraintes block de redimensionnement :",
    "Resize percent ranges:" : u"Intervalle de redimensionnement (%) :",
    "Max search aspect ratio error:" : u"Erreur maximum d'aspect ratio recherchée :",
    "Configure" : u"Configurer",
    "compute from .d2v" : u"Automatique depuis .d2v",
    "Configure options" : u"Options de configuration",
    "Avisynth resize:" : u"Filtre redimensionnement :",
    "The current Avisynth script contains errors." : u"Le script Avisynth courant contient des erreurs.",

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"", # New in v2.2.1
    "Encode the current script using x264" : u"", # New in v2.2.1
    "Encode video" : u"Encoder la vidéo",
    "System settings" : u"Paramètres system",
    "Input file:" : u"Fichier en entrée :",
    "Output file:" : u"Fichier en sortie :",
    "Compression settings" : u"Paramètres de compression",
    "Bitrate (kbits/sec):" : u"", # New in v2.0.0
    "calculate" : u"calculer",
    "Quality CRF (0-51):" : u"", # New in v2.2.1
    "Quality CQ (1-31):" : u"", # New in v2.2.1
    "Additional settings" : u"Paramètres complémentaires",
    "Credits start frame:" : u"Frame de début du géneric de fin :",
    "Command line settings" : u"Paramètres lign de commande",
    "Run" : u"Démarrer",
    "First time using this compression preset!" : u"Première utilisation de ce preset de compression !",
    "Please enter the exe paths in the following dialog." : u"Entrer les chemins vers les exe dans la boite de dialogue suivante.",
    "Exe pathnames" : u"Chemins des exe",
    "Open an AviSynth script" : u"Ouvrir un script Avisynth",
    "AviSynth script (*.avs)|*.avs" : u"Script Avisynth (*.avs)|*.avs",
    "Save the video as" : u"Enregistrer la vidéo sous",
    "Select a program" : u"Sélectionner un program",
    "Program (*.exe)|*.exe" : u"", # New in v2.0.0
    "Unreplaced items remain in the command line:" : u"Paramètres non remplacés dans la ligne de commande :",
    "Unknown exe paths!" : u"Chemins exe inconnus !",
    "General" : u"Général",
    "Credits warning minutes:" : u"Avertissement si durée genéric de fin > (minutes) :",
    "Automatically compute bitrate value on startup" : u"Calculer automatiquement le bitrate au démarrage",
    "Automatically compute pixel aspect ratio from d2v on startup" : u"Déterminer automatiquement au démarrage le pixel aspect ratio depuis le d2v",
    "Append batch commands to the avs script as comments" : u"Ajouter en commentaire les commandes batch dans le script avs",
    "Encoder priority:" : u"Priorité encoder :",
    "Path to %(name)s:" : u"Chemin vers %(name)s :",
    "Extra arguments:" : u"Paramètres supplémentaires :",
    "Bitrate Calculator" : u"Calculateur de bitrate",
    "Output info" : u"Info fichier en sortie",
    "Total size:" : u"Taille totale :",
    "Container:" : u"Container :",
    "(None)" : u"(Aucun)",
    "Video info" : u"Info vidéo",
    "Framecount:" : u"Total frames :",
    "FPS:" : u"", # New in v2.0.0
    "Audio info" : u"Info audio",
    "Audio file:" : u"Fichier audio :",
    "Compress audio" : u"Compresser",
    "Audio bitrate:" : u"Bitrate audio:",
    "Format:" : u"Format :",
    "Subtitles info" : u"Info sous-titres",
    "Subtitles file:" : u"Fichier sous-titres :",
    "Total time:" : u"Durée totale :",
    "Video size:" : u"Taille vidéo :",
    "Audio size:" : u"Taille audio :",
    "Subtitles size:" : u"Taille sous-titres :",
    "Overhead size:" : u"Taille perdue dans container :",
    "Bitrate:" : u"", # New in v2.0.0
    "Open the audio file" : u"Ouvrir le fichier audio",
    "Open the subtitles file" : u"Ouvrir le fichier sous-titres",
    "%(h)i hr and %(m)i min" : u"%(h)i hr et %(m)i min",

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"", # New in v2.2.1
    "Use avs2avi to save the current script as an avi" : u"", # New in v2.2.1
    "Please select the path to avs2avi.exe" : u"Indiquer le chemin vers avs2avi.exe",
    "Error: avs2avi is required to save an avi!" : u"Erreur : avs2avi est requis pour enregistrer en avi !",
    "Pass: %(pass)s / %(passes)s" : u"Passe: %(pass)s / %(passes)s",
    "Frame: %(frame)i / %(frames)i" : u"Frame: %(frame)i / %(frames)i",
    "Size: %(size).2f MB" : u"Taille: %(size).2f Mo",
    "FPS: %(fps).1f fps" : u"", # New in v1.2.0
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"Temps restant : %(hr)02i:%(min)02i:%(sec)02i",
    "Input file (.avs):" : u"Fichier source (.avs) :",
    "Output file (.avi):" : u"Fichier destination (.avi) :",
    "# of passes:" : u"# de passes :",
    "Priority:" : u"Priorité :",
    "Error: Unknown button" : u"Erreur : Bouton inconnu",
    "Save the avi as" : u"Enregistrer l'avi sous",
    "Avi file (*.avi)|*.avi" : u"Fichier Avi (*.avi)",
    "Input file does not exist!" : u"Le fichier source n'existe pas !",
    "Input file must be an avisynth script!" : u"Le fichier source doit être un script Avisynth !",
    "Output path does not exist!" : u"Le chemin de destination n'existe pas !",
    "# of passes must be an integer!" : u"# de passes doit être un nombre entier !",
    "Priority must be an integer!" : u"La priorité doit être un nombre entier !",
    "Stop" : u"Arrêter",
    "Done" : u"Terminé",
    "Process stopped." : u"Processus arrêté",
    "Processing..." : u"Exécution en cours...",
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"Terminé en %(hr)i heure(s) et %(min)i minute(s).",
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"Terminé en %(min)i minute(s) et %(sec)i seconde(s).",
    "Finished in %(time).1f seconds." : u"Terminé en %(time).1f secondes.",
    "Filesize: %(size).2f MB" : u"Taille du fichier: %(size).2f Mo",
    "The current script contains errors, exiting." : u"Le script courant contient des erreurs, fermeture.",
    "Save as AVI" : u"Enregistrer en AVI",
}