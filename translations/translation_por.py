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

# Português(Br) translation authors:
#   Veiga v1.2.0 - v2.0.1

version = "2.2.1"

messages = {
    "Find" : u"Localizar",
    "Replace" : u"Substiuir por",
    "Cannot find \"%(text)s\"." : u"Impossivel encontrar \"%(text)s\".",
    "Information" : u"Informação",
    "Replace Information" : u"Substituir por",
    "Replaced %(count)i times" : u"Substituições",
    "AviSynth fonts and colors" : u"Avisynth (Fontes & Cores)",
    "Background" : u"Fundo",
    "Font" : u"Fonte",
    "Text color" : u"Côr do Texto",
    "OK" : u"OK",
    "Cancel" : u"Cancelar",
    "Scrap Window" : u"Janela Auxiliar - p/ anotações (utilize botão direito do mouse)",
    "Undo" : u"Desfazer",
    "Redo" : u"Refazer",
    "Cut" : u"Cortar",
    "Copy" : u"Copiar",
    "Paste" : u"Colar",
    "Select all" : u"Selecionar tudo",
    "Refresh" : u"Atualizar",
    "Insert frame #" : u"Inserir nº Quadro atual",
    "Save to file..." : u"Salvar p/ Arquivo...",
    "Clear all" : u"Limpar tudo",
    "Toggle scrap window" : u"Ativar Janela auxiliar",
    "Save script" : u"Salvar script",
    "Error: no contextMenu variable defined for window" : u"Erro: no contextMenu variable defined for window",
    "Text document (*.txt)|*.txt|All files (*.*)|*.*" : u"Documento de Texto (*.txt)|*.txt|Todos os Arquivos (*.*)|*.*",
    "Save scrap text" : u"Salvar texto",
    "This field must contain a value!" : u"Este campo precisa ter um valor",
    "This slider label already exists!" : u"Título do Slider já existe",
    "Invalid slider label modulo syntax!" : u"Sintaxe errada no Título do Slider",
    "This field must contain a number!" : u"Este campo precisa conter um nº",
    "The min value must be less than the max!" : u"O valor mínimo precisa ser menor que o máximo",
    "The initial value must be between the min and the max!" : u"O valor inicial precisa ser entre o mín. e o máx.!",
    "The min value must be a multiple of %(mod)s!" : u"O valor mín. precisa ser um multiplo de %(mod)s!",
    "The max value must be a multiple of %(mod)s!" : u"O valor máx. precisa ser um multiplo de %(mod)s!",
    "The initial value must be a multiple of %(mod)s!" : u"O valor inicial precisa ser um multiplo de %(mod)s!",
    "The difference between the min and max must be greater than %(mod)s!" : u"A diferença entre mín. e máx. precisa ser maior que %(mod)s!",
    "Error" : u"Erro",
    "Define user slider" : u"Defina o slider de função",
    "Slider label:" : u"Título do Slider",
    "Min value:" : u"Valor mín.",
    "Max value:" : u"Valor máx.",
    "Initial value:" : u"Valor inicial",
    "Add or override AviSynth functions in the database" : u"Adicionar ou substituir funções AviSynth no banco de dados",
    "Core filters" : u"Filtros internos",
    "Plugins" : u"Plugins",
    "User functions" : u"Funções do usuario",
    "Script functions" : u"Funções escritas",
    "Clip properties" : u"Propriedades do clip",
    "Include %(title)s in autcompletion lists" : u"Incluir %(title)s nas listas de auto-complemento",
    "New function" : u"Nova função",
    "Edit selected" : u"Editar seleção",
    "Delete selected" : u"Deletar seleção",
    "Select installed" : u"Instalar seleção",
    "Import from files" : u"", # New in v2.2.1
    "Export customizations" : u"Exportar as customizações",
    "Clear customizations" : u"Limpar as customizações",
    "Clear manual presets" : u"Limpar definições manuais",
    "When importing, don't show the choice dialog" : u"", # New in v2.2.1
    "Edit function information" : u"Editar infº de função",
    "Name:" : u"Nome",
    "Type:" : u"Tipo",
    "clip property" : u"Propriedade do video",
    "core filter" : u"Filtro interno",
    "plugin" : u"plugin",
    "script function" : u"Função escrita",
    "user function" : u"Funções do usuario",
    "Arguments:" : u"Argumentos",
    "define sliders" : u"define sliders",
    "reset to default" : u"retornar a configuração padrão",
    "Slider information" : u"Infº de slider",
    "Preset:" : u"Pré-definição:",
    "Auto-generate" : u"Auto-geração",
    "Filter name already exists!" : u"Nome de filtro já existente",
    "Invalid filter name!" : u"Nome de filtro inválido!",
    "Renaming not allowed!" : u"Não permitido renomear",
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
    "No customizations to export!" : u"Não há customização p/ exportação!",
    "Save filter customizations" : u"Salvar customização de filtro",
    "Customization file (*.txt)|*.txt|All files (*.*)|*.*" : u"Arquivo de customização (*.txt)|*.txt|Todos os arquivos (*.*)|*.*",
    "This will delete all filter customizations. Continue?" : u"Isto irá apagar todas as customizações de filtros. Continua?",
    "Warning" : u"Cuidado",
    "This will delete all manually defined presets. Continue?" : u"Isto irá apagar todas as pre-difinições manuais. Continua?",
    "Do you want to delete this custom filter entirely?" : u"Deseja deletar este filtro totalmente",
    "Edit filter database" : u"Edita banco de dados de filtros",
    "Default" : u"Padrão",
    "Min value" : u"Valor mínimo",
    "Max value" : u"Valor máximo",
    "Step size" : u"Tamanho do intervalo",
    "Value list (comma separated)" : u"Lista de valores(separado por virgula)",
    "Value must be True or False!" : u"Valor precisa ser True ou False",
    "Must enter a value list!" : u"Precisa indicar lista de valores",
    "Export filter customizations" : u"Exportar configurações de filtro",
    "Import filter customizations" : u"Importar configurações de filtro",
    "Select filters to export:" : u"Selecionar filtros para exportar",
    "Select filters to import from the file:" : u"Selecionar filtros do arquivo para importar",
    "Overwrite all data" : u"Reescrever todos os dados",
    "You must select at least one filter!" : u"Você precisa selecionar pelo menos um filtro!",
    "Error: minValue must be less than maxValue" : u"Erro: valor min. precisa ser menor que valor max.",
    "New File" : u"Novo Arquivo",
    "Windows Bitmap (*.bmp)" : u"Windows Bitmap (*.bmp)",
    "Animation (*.gif)" : u"", # New in v2.2.1
    "JPEG (*.jpg)" : u"JPEG (*.jpg)",
    "Zsoft Paintbrush (*.pcx)" : u"", # New in v2.2.1
    "Portable Network Graphics (*.png)" : u"Portable Network Graphics (*.png)",
    "Netpbm (*.pnm)" : u"", # New in v2.2.1
    "Tagged Image File (*.tif)" : u"", # New in v2.2.1
    "ASCII Text Array (*.xpm)" : u"", # New in v2.2.1
    "Windows Icon (*.ico)" : u"", # New in v2.2.1
    "fps" : u"fps",
    "Frame" : u"Quadro",
    "A crash detected at the last running!" : u"", # New in v2.2.1
    "&Zoom" : u"", # New in v2.2.1
    "%s translation file updated with new messages to translate" : u"", # New in v2.2.1
    "Translation updated" : u"", # New in v2.2.1
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.2.1
    "%s language couldn't be loaded" : u"", # New in v2.2.1
    "Paths" : u"", # New in v2.2.1
    "AvsP help directory:" : u"Diretório do Help (AvsP)",
    "Location of the AvsP help directory" : u"Local do help (caminho, pasta) do AvsP",
    "Avisynth directory:" : u"Diretório Avisynth",
    "Location of the avisynth installation directory" : u"Local do diretório de instalação do Avisynth",
    "Avisynth help file/url:" : u"Avisynth, Arquivo Ajuda / URL",
    "Location of the avisynth help file or url" : u"Local do Arquivo Ajuda Avisynth / URL",
    "External player:" : u"Player externo",
    "Location of external program for script playback" : u"Local do programa (Player externo de script)",
    "Additional arguments when running the external player" : u"Argumentos adicionais p/ qdo usar o player externo",
    "External player extra args:" : u"Arqumentos extras p/ player externo",
    "Documentation search paths:" : u"Local da documenção para pesquisa",
    "Specify which directories to search for docs when you click on a filter calltip" : u"Indique os diretorios a serem pesquisados qdo clicar em ajuda(calltip) de um filtro",
    "Documentation search url:" : u"URL para pesquisa de documentação:",
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"Endereço web p/ pesquisa se docs ñ foram encontrados (the filter's name replaces %filtername%)",
    "Text" : u"", # New in v2.2.1
    "Show filter calltips" : u"Mostrar ajuda de filtro",
    "Turn on/off automatic tips when typing filter names" : u"Ativar/Desativar ajuda automática qdo digitar o nome do filtro",
    "Always show calltips any time the cursor is within the filter's arguments" : u"Mostrar ajuda(calltips), sempre que o cursor estiver entre os argumentos de um filtro",
    "Frequent calltips" : u"Ajuda (calltips) frequentes",
    "Syntax highlighting" : u"Realçar sintaxe",
    "Turn on/off avisynth-specific text colors and fonts" : u"Ativando/Desativando  determinadas cores de texto/fontes do Avisynth",
    "Show autocomplete on capital letters" : u"Mostrar auto-complemento p/ letras Maiúsculas",
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"Ativar/Desativar a lista de complemento automático qdo iniciar digitação com letras maiúsculas",
    "Show autocomplete list when typing a certain amount of letters" : u"", # New in v2.2.1
    "Don't allow lines wider than the window" : u"Não permitir linhas maiores que a janela",
    "Wrap text" : u"Quebra automática de linha",
    "Draw lines at fold points" : u"", # New in v2.2.1
    "For code folding, draw a line underneath if the fold point is not expanded" : u"", # New in v2.2.1
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Marque p/ inserir a tabulação atual ao invés de espaços qdo usar a tecla Tab",
    "Use tabs instead of spaces" : u"Use Tabs ao invés de espaços",
    "Set the size of the tabs in spaces" : u"Defina o tamanho dos Tabs em espaços",
    "Tab width" : u"Largura do Tab",
    "Initial space to reserve for the line margin in terms of number of digits" : u"Margem (nº de digitos)",
    "Line margin width" : u"Largura da margem",
    "Autocomplete" : u"Autocompletar",
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
    "Autoparentheses level" : u"Nivel de Autoparenteses",
    "Close \"()\"" : u"Fechado \"()\"", # New in v1.3.2
    "Determines parentheses to insert upon autocompletion" : u"Determina parenteses na insersão de complemento automático",
    "None \" \"" : u"Nada \" \"", # New in v1.3.2
    "Open \"(\"" : u"Aberto \"(\"", # New in v1.3.2
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"Determine qual chave ativa a pré-definição do filtro, qdo a caixa auto-completar está visivel",
    "None" : u"Nada",
    "Preset activation key" : u"Chaves de ativação de pré-definições",
    "Return" : u"Retornar",
    "Tab" : u"Tab",
    "Video" : u"Video",
    "Constantly update video while dragging" : u"Atualizar constantemente o video qdo arrastar o slider de função",
    "Update the video constantly when dragging the frame slider" : u"Atualiza constantemente o video qdo arrastado o slider de quadro",
    "Enable line-by-line update" : u"Ativar o atualizador linha/linha",
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"Ativar o atualisador de video linha/linha(atualiza janela de video toda vez que o cursor muda de linha)",
    "Focus the video preview upon refresh" : u"Focar a janela de video na atualização",
    "Switch focus to the video preview window when using the refresh command" : u"Alterar o foco p/ janela de video qdo usar o comando de atualização",
    "Refresh preview automatically" : u"", # New in v2.2.1
    "Refresh preview when switch focus on video window or change a value in slider window" : u"", # New in v2.2.1
    "Seeking to a certain frame will seek to that frame on all tabs" : u"", # New in v2.2.1
    "Shared timeline" : u"", # New in v2.2.1
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"", # New in v2.2.1
    "Allow AvsPmod to resize the window" : u"", # New in v2.2.1
    "Separate video preview window" : u"Janela de video separada",
    "Use a separate window for the video preview" : u"Usa a janela de video separada",
    "Min text lines on video preview" : u"Tamanho mínimo da janela de texto(linhas)",
    "Minimum number of lines to show when displaying the video preview" : u"Número mínimo de linhas da janela de texto, com a janela de video ativa ",
    "Customize the video information shown in the program status bar" : u"Configuração das informações de video mostradas na barra de status",
    "Customize video status bar..." : u"Configurar infos p/ barrra de status",
    "User Sliders" : u"Slider de Função",
    "Hide slider window by default" : u"Ocultar a janela de slider(defaut)",
    "Keep the slider window hidden by default when previewing a video" : u"Manter a janela de slider oculta qdo mostrar o video(defaut)",
    "Create user sliders automatically" : u"Criar slider de função automaticamente",
    "Create user sliders automatically using the filter database" : u"Criar o slider de função automaticamente usando o banco de dados de filtro",
    "Create user sliders for int and float arguments" : u"Criar sliders de função para argumentos inteiros e decimais",
    "type int/float (numerical slider)" : u"Tipo inteiro/decimal (slider numérico)",
    "Create color pickers for hex color arguments" : u"Criar amostra de cor p/ argumentos de cor hex",
    "type int (hex color)" : u"Tipo int (cor hex)",
    "Create radio boxes for bool arguments" : u"Criar botão de radio p/ argumentos boleanos(true/false)",
    "type bool" : u"Tipo boleano(true/false)",
    "Create listboxes for string list arguments" : u"Criar caixa de texto p/ relação de argumentos em string",
    "type string (list)" : u"Tipo string (relação,lista)",
    "Create filename pickers for string filename arguments" : u"Criar caixa de texto p/ relação de nome de arquivos, de argumentos em string (nome de arquivo)",
    "type string (filename)" : u"Tipo string (nome de arquivo)",
    "Create placeholders for arguments which have no database information" : u"Criar espaço (mostra o nome) p/ arqumentos que não tem informação no banco de dados",
    "undocumented" : u"Nome dos argumentos do texto mesmo sem valores no banco de dados",
    "Determines which filters will initially have hidden arguments in the slider window" : u"Determina como os sliders serão inicialmente carregados",
    "Fold all" : u"Não",
    "Fold non-numbers" : u"Só os numéricos",
    "Fold none" : u"Todos",
    "Fold startup setting" : u"Modo de inicialização (mostrar argumentos ?)",
    "Filter exclusion list:" : u"Filtrar (lista de exclusão)",
    "Specify filters never to build automatic sliders for" : u"Especificar p/ quais filtros não construir sliders automatimente",
    "Save/Load" : u"", # New in v2.2.1
    "Automatically save the session on shutdown and load on next startup" : u"Salvar automaticamente a sessão no shutdown e carrega-la na próxima abertura",
    "Save session for next launch" : u"Salvar sessão para próxima vez",
    "Always load startup session" : u"Sempre carregar no inicio da sessão",
    "Always load the auto-saved session before opening any other file on startup" : u"Carregar inicialm/ a sessão salva automaticamente, antes de abrir qquer outro arquivo",
    "Always hide the video preview window when loading a session" : u"", # New in v2.2.1
    "Don't preview when loading a session" : u"", # New in v2.2.1
    "Backup session when previewing" : u"", # New in v2.2.1
    "If checked, the current session is backed up prior to previewing any new script" : u"Se ativado, a sessão atual será salva antes de mostrar qquer novo video",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"Alerta p/ salvar o script antes da visualização(inativo se visualizando com alterações não salvas)",
    "Prompt to save when previewing" : u"Alerta para salvar durante a visualização",
    "Create a temporary preview script with unsaved changes when previewing the video" : u"Cria um script temporario com as alteraçoes não salvas  quando vendo o video",
    "Preview scripts with unsaved changes" : u"", # New in v2.2.1
    "Prompt to save each script with unsaved changes when exiting the program" : u"Alertar p/ salvar cada script com alterações ainda ñ salvas, qdo sair do programa",
    "Prompt to save scripts on program exit" : u"Alertar p/ salvar scripts qdo sair do programa",
    "Save *.avs scripts with AvsPmod markings" : u"", # New in v2.2.1
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"", # New in v2.2.1
    "Misc" : u"Miscelânias",
    "Choose the language used for the interface" : u"", # New in v2.2.1
    "Language *" : u"", # New in v2.2.1
    "Show keyboard images in the script tabs when video has focus" : u"Mostra nas fichas, o numero correspondente do teclado qdo o video estiver focado",
    "Use keyboard images in tabs" : u"Mostra o número correspondente do teclado nas fichas",
    "Show tabs in multiline style" : u"", # New in v2.2.1
    "There can be several rows of tabs" : u"", # New in v2.2.1
    "All tabs will have same width" : u"", # New in v2.2.1
    "Show tabs in fixed width" : u"", # New in v2.2.1
    "Enable scroll wheel through similar tabs" : u"", # New in v2.2.1
    "Mouse scroll wheel cycles through tabs with similar videos" : u"A roda do mouse irá navegar pelas fichas com videos similares",
    "Only allow a single instance of AvsPmod" : u"", # New in v2.2.1
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"", # New in v2.2.1
    "Show warning for bad plugin naming at startup" : u"", # New in v2.2.1
    "Max number of recent filenames" : u"Últimos arquivos(nº máximo)",
    "This number determines how many filenames to store in the recent files menu" : u"Determina o número máximo de nome de arquivos abertos recentemente que serão mostrados como últimos arquivos",
    "Custom jump size:" : u"Definir tamanho do avanço/retrocesso",
    "Jump size used in video menu" : u"Tamanho do avanço/retrocesso no menu de video",
    "Custom jump size units" : u"Unidade de avanço/retrocesso",
    "Units of custom jump size" : u"Unidade de avanço/retocesso",
    "hours" : u"horas",
    "minutes" : u"minutos",
    "seconds" : u"segundos",
    "frames" : u"quadros",
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
    "Indent selection" : u"Tabula seleção",
    "Unindent selection" : u"ReverteTab. da seleção",
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
    "100% (normal)" : u"100% (normal)",
    "200%" : u"200%",
    "300%" : u"300%",
    "400%" : u"400%",
    "Fill window" : u"Toda a Janela",
    "Fit inside window" : u"Até a Janela",
    "Vertically" : u"", # New in v2.2.1
    "Horizontally" : u"", # New in v2.2.1
    "&File" : u"&Arquivo",
    "Create a new tab" : u"Cria uma nova ficha",
    "New tab" : u"Nova ficha",
    "Open an existing script" : u"Abir um script existente",
    "Open..." : u"Abrir...",
    "Close tab" : u"Fechar ficha",
    "Close the current tab" : u"Fecha a ficha em uso",
    "Close all tabs" : u"Fechar todas as fichas",
    "Close every tab" : u"Fecha todas as fichas",
    "Rename tab" : u"", # New in v2.2.1
    "Rename the current tab. If script file is existing, also rename it" : u"", # New in v2.2.1
    "Save the current script" : u"Salva o script em uso",
    "Choose where to save the current script" : u"Escolha onde salvar o script em uso",
    "Save script as..." : u"Salvar script como",
    "Load a session into the tabs" : u"Carregar uma sessão nas fichas",
    "Load session..." : u"Carregar sessão...",
    "Save all the scripts as a session, including slider info" : u"Salvar todos os scripts como uma sessão, inclusive informação de slider",
    "Save session..." : u"Salvar sessão...",
    "Backup current session" : u"Backup da sessão atual",
    "Backup the current session for next program run" : u"Backup da sessão atual p/ próxima vez",
    "Next tab" : u"Próxima ficha",
    "Switch to next script tab" : u"Muda p/ a próxima ficha(script)",
    "Previous tab" : u"Ficha anterior",
    "Switch to previous script tab" : u"Muda p/ a ficha anterior(script)",
    "Show the scrap window" : u"Mostrar Janeça auxiliar",
    "&Exit" : u"&Sair",
    "Exit the program" : u"Sair do programa",
    "&Edit" : u"&Editar",
    "Undo last text operation" : u"Desfazer último texto",
    "Redo last text operation" : u"Refazeer último texto",
    "Cut the selected text" : u"Cortar texto selecionado",
    "Copy the selected text" : u"Copiar texto selecionado",
    "Paste the selected text" : u"Colar o texto selecionado",
    "Find..." : u"Localizar...",
    "Open a find text dialog box" : u"Abre uma caixa de pesquisa de texto",
    "Find next" : u"Localizar a próxima",
    "Find the next instance of given text" : u"Pesquisa a próxima ocorrência do texto informado",
    "Open a replace text dialog box" : u"Abre uma caixa de texto a ser substituido",
    "Replace..." : u"Substituir...",
    "Select All" : u"Selecionar tudo",
    "Select all the text" : u"Seleciona todo o texto",
    "&Insert" : u"", # New in v2.2.1
    "Choose a source file to insert into the text" : u"Escolha um arquivo fonte p/ inserir no texto",
    "Insert source..." : u"Inserir Arq. fonte...",
    "Get a filename from a dialog box to insert into the text" : u"Pega um nome de arquivo de uma caixa de dialogo p/ inserir no texto",
    "Insert filename..." : u"Inserir nome de arquivo",
    "Choose a plugin dll to insert into the text" : u"Escolha um nome de plugin dll p/ inserir no texto",
    "Insert plugin..." : u"Inserir plugin... ",
    "Insert a user-scripted slider into the text" : u"Insere no texto, o script do slider da função...",
    "Insert user slider..." : u"Inserir slider de função ...",
    "Insert a tag which indicates a separator in the user slider window" : u"Insere separador do slider de função",
    "Insert user slider separator" : u"Inserir separador do slider de função",
    "Insert the current frame number into the text" : u"Insere no texto o nº do quadro atual",
    "Add tags surrounding the selected text for toggling with the video preview" : u"Adiciona identificação ao texto selecionado para possibilitar ativar / desativar um ou mais plugins previamente selecionados",
    "Tag selection for toggling" : u"Identif. seleç. p/ alternar",
    "Clear all tags" : u"Limpar todas identificações",
    "Clear all toggle tags from the text" : u"Limpa todas as identificações de texto",
    "Indent the selected lines" : u"Tabula as linhas selecionadas",
    "Unindent the selected lines" : u"Reverte Tab. nas linhas selecionadas",
    "Block comment" : u"Transf. Seleção em comentario",
    "Comment or uncomment selected lines" : u"Comenta ou reverte comentario das linhas selecionadas",
    "Comment at start of a text style or uncomment" : u"", # New in v2.2.1
    "Style comment" : u"", # New in v2.2.1
    "Toggle current fold" : u"", # New in v2.2.1
    "Toggle the fold point On/OFF at the current line" : u"", # New in v2.2.1
    "Toggle all fold points On/OFF" : u"", # New in v2.2.1
    "Toggle all folds" : u"Mostrar/ocultar todos os argumentos",
    "&AviSynth function" : u"", # New in v2.2.1
    "Show list of filternames matching the partial text at the cursor" : u"Mostra lista parcial de filtros com base no texto em digitação",
    "Autocomplete all" : u"", # New in v2.2.1
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"", # New in v2.2.1
    "Show calltip" : u"Mostrar ajuda de cursor(calltip)",
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"Mostra a ajuda de cursor(calltip) p/ um filtro (sòmente se o cursor estiver entre os argumentos)",
    "Show function definition" : u"Mostrar definição de função",
    "Show the AviSynth function definition dialog for the filter" : u"Mostra a definição da função Avisynth p/ o filtro",
    "Filter help file" : u"Arquivo HELP de filtro",
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"Ativar arquivo HELP p/ o filtro(sòmente se cursor estiver entre os argumentos ou  o nome realçado)",
    "&Miscellaneous" : u"", # New in v2.2.1
    "Move line up" : u"Mover linha p/ cima",
    "Move the current line or selection up by one line" : u"Move  a linha atual  ou selecionada, uma linha p/ cima.",
    "Move line down" : u"Mover linha p/ baixo",
    "Move the current line or selection down by one line" : u"Move  a linha atual  ou selecionada, uma linha p/ baixo.",
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"Copia o script atual sem qquer sinal Avsp (slider de função, idendificadores de alternacia on/off (ctrl+T)) p/ a area de transferência",
    "Copy unmarked script to clipboard" : u"Copia script(s/ sinais) p/ area de transf.",
    "Copy avisynth error to clipboard" : u"", # New in v2.2.1
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"", # New in v2.2.1
    "&Video" : u"&Video",
    "Add/Remove bookmark" : u"", # New in v2.2.1
    "Mark the current frame on the frame slider" : u"Marcar quadro atual no slider de quadro",
    "Clear all bookmarks" : u"Desmarcar todos os quadros",
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
    "Go to next bookmarked frame" : u"Avança para o próximo quadro marcado",
    "Next bookmark" : u"Próximo quadro marcado",
    "Go to previous bookmarked frame" : u"Retorna para o último quadro marcado",
    "Previous bookmark" : u"Último quadro marcado",
    "Forward 1 frame" : u"Próximo quadro",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"Mostra o próximo quadro(atalho de teclado ativado quando janela de video está focada)",
    "Backward 1 frame" : u"Quadro anterior",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"Mostra o quadro anterior (atalho de teclado ativado quando janela de video está focada)",
    "Forward 1 second" : u"Avançar 1 segundo",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"Mostra o quadro 1 segundo p/ frente (atalho de teclado ativado quando janela de video está focada)",
    "Backward 1 second" : u"Voltar 1 segundo",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"Mostra o quadro 1 segundo atrás (atalho de teclado ativado quando janela de video está focada)",
    "Forward 1 minute" : u"Avançar 1 minuto",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"Mostra o quadro 1 minuto p/ frente (atalho de teclado ativado quando janela de video está focada)",
    "Backward 1 minute" : u"Voltar 1 minuto",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"Mostra o quadro 1 minuto atrás (atalho de teclado ativado quando janela de video está focada)",
    "Forward x units" : u"Avançar x unidades",
    "Jump forward by x units (you can specify x in the options dialog)" : u"Avançar x unidades(defina x em configurações)",
    "Backwards x units" : u"Retroceder x unidades",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"Retroceder x unidades(defina x em configurações)",
    "Go to first frame" : u"Mover p/ o 1º quadro",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"Mover p/ 1º quadro de video (atalho de teclado ativo qdo janela de video está focada)",
    "Go to last frame" : u"Mover p/ último quadro",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"Mover p/ último quadro de video (atalho de teclado ativo qdo janela de video está focada)",
    "Go to last scrolled frame" : u"Ir para o último quadro mostrado",
    "Last scrolled frame" : u"Ultimo quadro mostrado",
    "Enter a video frame or time to jump to" : u"Entre com o nº do quadro ou o tempo p/ ir para:",
    "Go to frame..." : u"Ir para o quadro...",
    "Crop editor..." : u"Editor de apara(crop)",
    "Show the crop editor dialog" : u"Mostra o editor de apara (crop)",
    "&Trim selection editor" : u"", # New in v2.2.1
    "Show the trim selection editor dialog" : u"Mostrar editor de seleção de corte",
    "Show trim selection editor" : u"Mostrar editor de seleção de corte",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"Define um ponto de início de seleção(Mostra o editor de corte se não visivel)",
    "Set selection startpoint" : u"Define um ponto de inicio de seleção",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"Define um ponto de término de seleção(Mostra o editor de corte se não visivel)",
    "Set selection endpoint" : u"Define um ponto de término de seleção",
    "Zoom video preview to 25%" : u"Altera zoom p/ 25%",
    "Zoom video preview to 50%" : u"Altera zoom p/ 50%",
    "Zoom video preview to 100% (normal)" : u"Altera zoom p/ 100% (normal)",
    "Zoom video preview to 200%" : u"Altera zoom p/ 200%",
    "Zoom video preview to 300%" : u"Altera zoom p/ 300%",
    "Zoom video preview to 400%" : u"Altera zoom p/ 400%",
    "Zoom video preview to fill the entire window" : u"Zoom video para preencher toda a janela",
    "Zoom video preview to fit inside the window" : u"Zoom video até o limite da janela",
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
    "Save image as..." : u"Salvar imagem como...",
    "Save the current frame as a bitmap" : u"Salvar quadro atual como bitmap",
    "Force the script to reload and refresh the video frame" : u"Força recarregar o script e atualizar o quadro de video",
    "Refresh preview" : u"Mostrar/Atualizar o video",
    "Show/Hide the preview" : u"", # New in v2.2.1
    "Toggle the video preview" : u"Alternar janela de video",
    "Release all open videos from memory" : u"Liberar todos os videos abertos da memória",
    "Release all videos from memory" : u"Liberar memória",
    "Switch focus between the video preview and the text editor" : u"Alterna o foco entre janelas video/texto",
    "Switch video/text focus" : u"Alternar foco (video/texto)",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"Mostra/Oculta o slide / sidebar(Clique duplo faz o mesmo eveito",
    "Toggle the slider sidebar" : u"Ativar/Desat. slide/sidebar",
    "External player" : u"Player externo",
    "Play the current script in an external program" : u"Mostra video do script atual em um programa externo",
    "Show information about the video in a dialog box" : u"Mostra informaçao do video em uma caixa de dialogo",
    "Video information" : u"Informação do video",
    "&Options" : u"&Opções",
    "Always on top" : u"Sempre a frente",
    "Keep this window always on top of others" : u"Mantem esta janela sempre a frente das outras",
    "Disable video preview" : u"Desabilitar janela de video",
    "If checked, the video preview will not be shown under any circumstances" : u"Nunca mostrar janela de video",
    "Associate .avs files with AvsP" : u"Associar arquivos .avs com AvsP",
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"Configura (clique-duplo)p/ abrir arquivos .avs no AvsP ",
    "AviSynth function definition..." : u"Configurar ajuda de  função...",
    "Edit the various AviSynth script fonts and colors" : u"Escolha fonte e côr p/ os vários scripts Avisynth",
    "Fonts and colors..." : u"Fontes e Cores",
    "Edit the extension-based templates for inserting sources" : u"Edita a associacão (extensão - modelo) para inserir Arq. fontes",
    "Extension templates..." : u"Extensão de modelos",
    "Configure the program keyboard shortcuts" : u"Permite configurar os atalhos de teclado",
    "Keyboard shortcuts..." : u"", # New in v2.2.1
    "Configure program settings" : u"Configurar programa",
    "Program settings..." : u"Configurações",
    "&Help" : u"&Ajuda",
    "Animated tutorial" : u"Tutorial animado",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"Ver um tutorial animado p/ AvsP (AvsP website)",
    "Learn more about AvsP text features (from the AvsP website)" : u"Aprenda mais sobre edição de texto no AvsP (AvsP website)",
    "Text features" : u"Texto",
    "Learn more about AvsP video features (from the AvsP website)" : u"Aprenda mais sobre edição de video no AvsP (AvsP website)",
    "Video features" : u"Video",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"Aprenda mais sobre edição de sliders de função no AvsP (AvsP website)",
    "User sliders" : u"Sliders de função",
    "Learn more about AvsP macros (from the AvsP website)" : u"Aprenda mais sobre edição de macros p/ AvsP (AvsP website)",
    "Macros" : u"Macros",
    "Avisynth help" : u"Ajuda Avisynth",
    "Open the avisynth help html" : u"Abre ajuda html do avisynth",
    "Open Avisynth plugins folder" : u"", # New in v2.2.1
    "Open the avisynth plugins folder" : u"", # New in v2.2.1
    "About this program" : u"Sôbre este programa",
    "About AvsPmod" : u"", # New in v2.2.1
    "Previous frame" : u"Quadro anterior",
    "Next frame" : u"Próximo quadro",
    "Run the script with an external program" : u"Executa o script com um programa externo",
    "Run the selected tool" : u"Aplicar a ferramenta selecionada",
    "&Tools" : u"", # New in v2.2.1
    "a macro check item" : u"", # New in v2.2.1
    "a macro radio item" : u"", # New in v2.2.1
    "Run selected macro" : u"Executa a macro selecionada",
    "View the readme for making macros" : u"Ver o leiame para fazer macros",
    "Open the macros folder" : u"", # New in v2.2.1
    "&Macros" : u"", # New in v2.2.1
    "Close" : u"Fechar",
    "Rename" : u"", # New in v2.2.1
    "Save" : u"Salvar",
    "Save as..." : u"Salvar como...",
    "Copy to new tab" : u"Copiar p/ nova tabulação",
    "Reposition to" : u"", # New in v2.2.1
    "Crop editor" : u"Editor crop",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"Aqui, você pode definir valores de apara (crop) observando o resultado na imagem, ou enquanto este editor estiver aberto, (clicando direto na imagem se preferir)",
    "At script end" : u"No fim do script",
    "At script cursor" : u"Na posição do cursor",
    "Copy to clipboard" : u"Copiar para area de transferência",
    "Insert Crop() command:" : u"Inserir comando Crop()",
    "Apply" : u"Aplicar",
    "Trim editor" : u"Editor de corte",
    "Selection options" : u"Opções selecionadas",
    "Keep selected regions" : u"Manter as regiões selecionadas",
    "Keep unselected regions" : u"Manter as regiões não selecionadas",
    "Mark video frames inside/outside selection" : u"Marcar os quadros dentro/fora da seleção",
    "Use Dissolve() with overlap frames:" : u"", # New in v2.2.1
    "Insert Trim() commands:" : u"Inserir comandos de corte -Trim()",
    "Insert Dissolve() commands:" : u"", # New in v2.2.1
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"Use os botões que aparecem no slider de video para criar seleções de corte",
    "File does not exist!" : u"Arquivo inexistente!",
    "All files (*.*)|*.*" : u"Todos os arquivos(*.*)|*.*",
    "Select a file" : u"Seleciona um arquivo",
    "Create a separator label" : u"Criar um separador de título",
    "Enter separator label" : u"Criar separador de título",
    "Enter tag name:" : u"Coloque o nome",
    "Tag definition" : u"Definir identificação",
    "Chapter" : u"", # New in v2.2.1
    "Set title for bookmarks" : u"", # New in v2.2.1
    "Title" : u"", # New in v2.2.1
    "Frame No." : u"", # New in v2.2.1
    "Time **" : u"", # New in v2.2.1
    "" : u"", # New in v2.2.1
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"", # New in v2.2.1
    "Frame size:" : u"Tamanho do quadro",
    "Length:" : u"Comprimento",
    "Frame rate:" : u"Quadros / segundo",
    "Colorspace:" : u"Sistema de cor",
    "Field or frame based:" : u"Formato (campo ou quadro:)",
    "Parity:" : u"Paridade",
    "Audio" : u"Audio",
    "Channels:" : u"Canais",
    "Hz" : u"Hz",
    "Sampling rate:" : u"Tx amostragem",
    "Sample type:" : u"Tipo de amostra",
    "bits" : u"bits",
    "samples" : u"amostras",
    "Could not find the macros folder!" : u"", # New in v2.2.1
    "Could not find %(readme)s!" : u"Impossivel encontrar %(readme)s!",
    "Failed to import the selected tool" : u"Falha ao importar a ferramenta selecionada",
    "You must restart for changes to take effect!" : u"Você precisa reiniciar para que as alterções tenham efeito",
    "Basic" : u"Básico",
    "Default:" : u"Padrão:",
    "Comment:" : u"Comentario:",
    "Block Comment:" : u"", # New in v2.2.1
    "__END__ Comment:" : u"", # New in v2.2.1
    "Number:" : u"Número:",
    "Operator:" : u"Operação:",
    "String:" : u"String:",
    "Triple-quoted string:" : u"String com 3 aspas:",
    "Internal filter:" : u"Filtro interno:",
    "External filter:" : u"Filtro externo:",
    "Internal function:" : u"Função interna:",
    "User defined function:" : u"Função definida pelo usuario:",
    "Clip property:" : u"Propriedades do Clip:",
    "AviSynth keyword:" : u"Palavra chave do AviSynth:",
    "AviSynth data type:" : u"Tipo de dados do AviSynth:",
    "AvsP user slider:" : u"Função de slider:",
    "Monospaced font:" : u"Fonte fixa:",
    "Advanced" : u"Avançado",
    "Incomplete string:" : u"String incompleta:",
    "Syntax highlight strings which are not completed in a single line differently" : u"Realça o texto de strings que não cabem em uma linha",
    "Brace highlight:" : u"{ Chave realçada }:",
    "Bad brace:" : u"{ Chave inválida }:",
    "Bad number:" : u"Número inválido:",
    "Margin line numbers:" : u"Número da linha:",
    "Miscellaneous word:" : u"Palavra miscelânia:",
    "Calltip:" : u"Ajuda de cursor:",
    "Calltip highlight:" : u"Destaca ajuda de cursor:",
    "Cursor:" : u"Cursor",
    "Selection highlight:" : u"", # New in v2.2.1
    "Current line highlight:" : u"", # New in v2.2.1
    "Highlight the line that the caret is currently in" : u"Realça a linha em que o cursor se encontra",
    "Fold margin:" : u"", # New in v2.2.1
    "Scrap window" : u"", # New in v2.2.1
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"", # New in v2.2.1
    "Use monspaced font" : u"", # New in v2.2.1
    "Insert aborted:" : u"Inserção abortada",
    "No dot required in file extension!" : u"Ponto não requerido na extensão do arquivo!",
    "Edit extension-based templates" : u"Editar extensão associada a modelo",
    "File extension" : u"Extensão de arquivo",
    "Template" : u"Modelo",
    "This info is used for inserting sources based on file extensions." : u"Esta informacão é usada p/ inserir arq. fontes com base na extensão do arquivo",
    "Any instances of *** in the template are replaced with the filename." : u"Qquer ocorrência de *** no modelo(template) são substituidos pelo nome do arquivo",
    "(If you want relative paths instead of the full filename, use [***].)" : u"", # New in v2.2.1
    "Associating .avs files will write to the windows registry." : u"Arquivos .avs associados serão incluidos no registro do Windows.",
    "Do you wish to continue?" : u"Deseja continuar?",
    "Could not find the Avisynth plugins folder!" : u"", # New in v2.2.1
    "AvsPmod version %(version)s " : u"", # New in v2.2.1
    "An AviSynth script editor" : u"Um editor de script para AviSynth",
    "AvsP Website" : u"AvsP Website",
    "Active thread on Doom9's forum" : u"", # New in v2.2.1
    "This program is freeware under the GPL license." : u"Este programa sob licença GPL é livre",
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"", # New in v2.2.1
    "copy as time" : u"", # New in v2.2.1
    "copy" : u"", # New in v2.2.1
    "paste" : u"", # New in v2.2.1
    "clear history" : u"", # New in v2.2.1
    "Cannot switch tabs while crop editor is open!" : u"Impossível mudar de ficha com o editor crop aberto",
    "Cannot switch tabs while trim editor is open!" : u"Impossivel mudar enquanto o editor de corte está aberto",
    "pos" : u"pos",
    "rgb" : u"rgb",
    "rgba" : u"rgba",
    "yuv" : u"yuv",
    "hex" : u"hex",
    "Invalid crop values detected.  Continue?" : u"Detectados valores inválidos para crop. Continua? ",
    "You must create at least one frame selection first!" : u"Você precisa criar no mínimo uma selação primeiro",
    "Select autocomplete keywords" : u"", # New in v2.2.1
    "exclude long names" : u"", # New in v2.2.1
    "Customize the video status bar message" : u"Configuração das informações p/ barra de status",
    "Video status bar message:" : u"Informações p/ barra de status",
    "Legend" : u"Legenda",
    "Current frame" : u"Quadro atual",
    "Framecount" : u"Contador de quadro",
    "Current time" : u"Tempo decorrido",
    "Total time" : u"Tempo total",
    "Width" : u"Largura",
    "Height" : u"Altura",
    "Aspect ratio" : u"Proporção (W / H)",
    "Framerate" : u"Quadros / segundo ",
    "Framerate numerator" : u"Numerador de quadros/segundo",
    "Framerate denominator" : u"Denominador de quadros/segundo",
    "Colorspace" : u"Sistema de cor",
    "Field or frame based" : u"Formato (campo ou quadro)",
    "Parity" : u"Paridade",
    "Parity short (BFF or TFF)" : u"Ordem dos campos (BFF or TFF)",
    "Audio rate" : u"Taxa de audio",
    "Audio length" : u"Comprimento de audio",
    "Audio channels" : u"Canais de audio",
    "Audio bits" : u"Audio bits",
    "Audio type (Integer or Float)" : u"Tipo de audio(fixo ou variavel",
    "Pixel position (cursor based)" : u"Posição do pixel (pos. do cursor)",
    "Pixel hex color (cursor based)" : u"Cor hex do pixel (pos. do cursor)",
    "Pixel rgb color (cursor based)" : u"Cor rgb do pixel (pos. do cursor)",
    "Pixel yuv color (cursor based)" : u"Cor yuv do pixel (pos. do cursor)",
    "Pixel color (auto-detect colorspace)" : u"Cor do pixel (detecção automática do sistema de cor)",
    "Program zoom" : u"Zoom atual",
    "Save changes before closing?" : u"Salvar alterações antes de fechar?",
    "Cannot create a new tab while crop editor is open!" : u"Impossivel criar uma nova ficha enquanto o editor de Apara (Crop) está aberto",
    "Cannot create a new tab while trim editor is open!" : u"Impossivel criar uma nova ficha enquanto o editor de Corte está aberto",
    "AviSynth script (avs, avsi)|*.avs;*.avsi|Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"AviSynth script (avs, avsi)|*.avs;*.avsi|Arquivos fonte (%(extlist1)s)|*.%(extlist2)s|Todos os arquivos (*.*)|*.*",
    "Open a script or source" : u"Abrir um script ou fonte",
    "Reload the file and lose the current changes?" : u"Recarregar o arquivo e perder as alterações atuais",
    "Open this file" : u"Abir este arquivo",
    "Save session before closing all tabs?" : u"Salvar seção antes de fechar todas as fichas?",
    "AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|All files (*.*)|*.*" : u"AviSynth script (*.avs, *.avsi)|*.avs;*.avsi|Todos os arquivos (*.*)|*.*",
    "Save current script" : u"Salvar script atual",
    "Directory %(dirname)s does not exist!" : u"Diretório %(dirname)s não existe!",
    "Load a session" : u"Carregar a sessão",
    "File has been modified since the session was saved. Reload?" : u"Arquivo foi modificado desde a última sessão salva. Recarregar?",
    "Save the session" : u"Salvar a sessão",
    "Save current frame" : u"Salvar quadro atual",
    "No image to save" : u"Nenhuma imagem p/ salvar",
    "Source files (%(extlist1)s)|*.%(extlist2)s|All files (*.*)|*.*" : u"Arquivos fontes (%(extlist1)s)|*.%(extlist2)s|Todos os arquivos (*.*)|*.*",
    "Insert a source" : u"Inserir Arq. fonte",
    "AviSynth plugin (*.dll)|*.dll|All files (*.*)|*.*" : u"AviSynth plugin (*.dll)|*.dll|Todos os arquivos (*.*)|*.*",
    "Insert a plugin" : u"Inserir um plugin",
    "No bookmarks defined!" : u"Não existe ponto marcado definido",
    "There must be more than one unique bookmark to use this feature!" : u"É preciso ter mais de um unico ponto marcado para usar esta possibilidade",
    "Jump to specified bookmark" : u"Ir para um determinado ponto marcado",
    "Line: %(line)i  Col: %(col)i" : u"Linha: %(line)i  Coluna: %(col)i",
    "Frame Based" : u"Base quadro",
    "Field Based" : u"Base campo",
    "Bottom Field First" : u"Campo inferior primeiro",
    "BFF" : u"BFF",
    "Top Field First" : u"Campo superior primeiro",
    "TFF" : u"TFF",
    "Integer" : u"Fixo",
    "Float" : u"Variavel",
    "Edit AviSynth function information" : u"Editor de informção da função Avisynth",
    "  Function name" : u" Nome da função",
    "Function arguments" : u"Argumentos da função",
    "Open filter customization file" : u"Abrir arquivo de configuração de filtro",
    "Calltip-only text file (*.txt)|*.txt" : u"Somente ajuda p/ arquivo texto (*.txt)|*.txt",
    "Filter customization file (*.tag)|*.tag" : u"Arquivo de configuração de filtro (*.tag)|*.tag",
    "Invalid filter customization file!" : u"Arquivo de configuração de filtro inválido",
    "Save filter customization file" : u"Salvar arquivo de configuração de filtro",
    "Invalid argument!" : u"Agumento inválido!",
    "Error loading AviSynth!" : u"Erro carregando AviSynth!",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"Certifique-se de que você tem o AviSynth instalado, e não tem nenhum arquivo (plugin ou avsi) instável no diretório de plugins do AviSynth ",
    "Save changes before previewing?" : u"Salvar as alterações antes da pré-visulização",
    "Executable files (*.exe)|*.exe|All files (*.*)|*.*" : u"Arquivos executáveis (*.exe)|*.exe|Todos os Arquivos (*.*)|*.*",
    "Select an external player" : u"Selecione um Player externo",
    "A program must be specified to use this feature!" : u"Para usar esta caracteristica, é preciso indicar um programa",
    "General settings..." : u"Configurações gerais...",
    "Invalid slider text: min > max" : u"Texto de slider inválido: mínimo > máximo",
    "Invalid slider text: value not in bounds" : u"Texto de slider inválido: valor não aceitavel",
    "Invalid slider text: bad modulo label" : u"Texto de slider inválido: nome inválido p/ o módulo",
    "Invalid slider text: slider label already exists" : u"Texto de slider inválido: nome já existe",
    "Invalid slider text: invalid number" : u"Texto de slider inválido: número inválido",
    "Reset to initial value: %(value_formatted)s" : u"Retornar para os valores iniciais: %(value_formatted)s",
    "Reset to initial value: %(value2_formatted)s" : u"", # New in v2.2.1
    "Reset to default value: %(value_formatted)s" : u"Retornar aos valores padrões: %(value_formatted)s",
    "Invalid hexadecimal color!" : u"Cor hexadecimal invalida!",
    "Must specify a max value!" : u"Preciso especificar um valor máximo!",
    "Must specify a min value!" : u"Preciso especificar um valor mínimo!",
    "Min value must be a number!" : u"Valor mínimo precisa ser um número!",
    "Max value must be a number!" : u"Valor máximo precisa ser um número!",
    "Default value must be a number!" : u"Valor padrão precisa ser um número!",
    "Step size value must be a number!" : u"Valor precisa ser um número!",
    "Left-click to select a color, right click to reset to default" : u"Clique esquerdo p/ selecionar a cor, clique direito p/ retornar ao padrão",
    "Source files (%(extlist1)s)|*.%(extlist2)s" : u"Arquivos fonte (%(extlist1)s)|*.%(extlist2)s",
    "Toggle \"%(label)s\" section" : u"Ativar/Desat. secção: \"%(label)s\" ",
    "Don't show me this again" : u"", # New in v2.2.1
    "Save as" : u"Salvar como",
    "Select a directory" : u"Selecionar um diretório",
    "Enter information" : u"Entrar informação",
    "Progress" : u"Progresso",
    "Error loading the script" : u"Erro durante carregamento do script",
    "Error in the macro:" : u"Erro na macro:",
    "Couldn't find %(macrofilename)s" : u"Não foi possivel encontrar %(macrofilename)s",
    "Failed to open the AVI file" : u"Falha ao abrir o arquivo AVI",
    "Failed to open the AVI frame" : u"Falha ao abrir o quadro AVI",
    "Failed to retrieve AVI frame" : u"Falha ao reabrir o quadro AVI",
    "Ctrl" : u"Ctrl",
    "Alt" : u"Alt",
    "Shift" : u"Shift",
    "Program Settings" : u"Configurações do programa",
    "Browse" : u"Mostre",
    "* Requires program restart for full effect" : u"* Necessario reiniciar o programa p/ ter efeito",
    "Invalid directory!" : u"Diretório inválido",
    "Invalid filename!" : u"Nome de arquivo inválido",
    "Edit shortcuts" : u"Editor de atalho",
    "Menu label" : u"Título do Menu",
    "Keyboard shortcut" : u"Atalho de teclado",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"Duplo clique ou pressione enter em um item da lista, para editar o atalho",
    "Shortcut" : u"", # New in v2.2.1
    "Action" : u"", # New in v2.2.1
    "Edit the keyboard shortcut" : u"Editor de atalhos",
    "Key:" : u"Key",
    "Clear" : u"Limpar",
    "%(keyString)s not found in key string list" : u"%(keyString)s não encontrado na lista de chave de string",
    "This shortcut is being used by:" : u"Este atalho está sendo usado por",
    "Insert" : u"Inserir",
    "Delete" : u"Deletar",
    "Error: key %(key)s does not exist!" : u"Erro: chave %(key)s não existe",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"Tem certesa que quer renomear de:%(oldName)s para:%(newName)s? ",
    "Question" : u"Pergunta",
    "Insert a new item" : u"Insira um novo item",
    "Must enter a name!" : u"Necessario entrar um nome!",
    "Item %(newKey)s already exists!" : u"Item %(newKey)s já existe!",
    "Warning: no value entered for item %(newKey)s!" : u"Cuidado: não incluido valor p/ item %(newKey)s!",
    "Message" : u"Mensage",
    "Select an item to delete first" : u"Selecione um item para apagar primeiro",
    "Are you sure you want to delete item %(key)s?" : u"Tem certeza que deseja apagar o item %(key)s?",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"(Re)Calcular Tamanho",
    "Calculate an appropriate resize for the video" : u"Calcula novo tamanho apropriado p/ o video",
    "Resize calculator" : u"Calculadora p/ redimensionar tamanho",
    "Input" : u"Entrada",
    "Video resolution:" : u"Resolução de video",
    "Pixel aspect ratio:" : u"proporção de video(aspect ratio) pixel",
    "Results" : u"Resultados",
    "Aspect ratio error:" : u"Erro de aspect ratio",
    "Settings" : u"Configurações",
    "Target pixel aspect ratio:" : u"Pixel aspect ratio desejado",
    "Resize block constraints:" : u"Redimensionar blocos",
    "Resize percent ranges:" : u"Redimensionar intervalos %",
    "Max search aspect ratio error:" : u"máximo erro (desejado) de aspect ratio",
    "Configure" : u"Configuração",
    "compute from .d2v" : u"processar de .d2v",
    "Configure options" : u"Opções de configuração",
    "Avisynth resize:" : u"Tamanho AviSynth",
    "The current Avisynth script contains errors." : u"O script AviSynth atual contém erros",

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"", # New in v2.2.1
    "Encode the current script using x264" : u"", # New in v2.2.1
    "Encode video" : u"Codificar video",
    "System settings" : u"Configurações do sistema",
    "Input file:" : u"Arquivo de entrada:",
    "Output file:" : u"Arquivo de saída:",
    "Compression settings" : u"Configurações p/ comprimir",
    "Bitrate (kbits/sec):" : u"Bitrate (kbits/sec):",
    "calculate" : u"calcular",
    "Quality CRF (0-51):" : u"", # New in v2.2.1
    "Quality CQ (1-31):" : u"", # New in v2.2.1
    "Additional settings" : u"Configurações adicionais",
    "Credits start frame:" : u"Quadro inicial dos créditos",
    "Command line settings" : u"Configuração da linha de comando",
    "Run" : u"Executar",
    "First time using this compression preset!" : u"Usando estes dados de compressão pela 1ª vez ?",
    "Please enter the exe paths in the following dialog." : u"Favor incluir o caminho do seu (encoder) exe no diálogo seguite",
    "Exe pathnames" : u"Caminho exe",
    "Open an AviSynth script" : u"Abrir um script Avisynth",
    "AviSynth script (*.avs)|*.avs" : u"Script AviSynth (*.avs)|*.avs",
    "Save the video as" : u"Salvar o arquivo como",
    "Select a program" : u"Selecionar um programa",
    "Program (*.exe)|*.exe" : u"Programa (*.exe)|*.exe",
    "Unreplaced items remain in the command line:" : u"Itens não substituidos na linha de comando",
    "Unknown exe paths!" : u"Caminho exe desconhecido",
    "General" : u"Geral",
    "Credits warning minutes:" : u"Alerta de tempo(minutos) p/ créditos",
    "Automatically compute bitrate value on startup" : u"Computar automaticamente o bitrate no inicio",
    "Automatically compute pixel aspect ratio from d2v on startup" : u"Computar automaticamente no inicio, o aspect ratio de d2v",
    "Append batch commands to the avs script as comments" : u"Adicionar lote de comandos aos scripts avs como comentários",
    "Encoder priority:" : u"Prioridade de codificação",
    "Path to %(name)s:" : u"Caminho para %(name)s:",
    "Extra arguments:" : u"Argumentos extras",
    "Bitrate Calculator" : u"Calculadora p/ bitrate",
    "Output info" : u"Informações (Tamanho x Tipo)",
    "Total size:" : u"Tamanho total:",
    "Container:" : u"Tipo",
    "(None)" : u"(Nada)",
    "Video info" : u"Infº de video",
    "Framecount:" : u"Numero de quadros",
    "FPS:" : u"FPS",
    "Audio info" : u"Infº de audio",
    "Audio file:" : u"Arquivo de audio",
    "Compress audio" : u"Compressão de audio",
    "Audio bitrate:" : u"Bitrate de audio",
    "Format:" : u"Formato",
    "Subtitles info" : u"Infº de legenda",
    "Subtitles file:" : u"Arquivo de legenda",
    "Total time:" : u"Tempo total",
    "Video size:" : u"Tamanho de video",
    "Audio size:" : u"Tamanho de audio",
    "Subtitles size:" : u"Tamanho da legenda",
    "Overhead size:" : u"Tamanho a mais",
    "Bitrate:" : u"Bitrate:",
    "Open the audio file" : u"Abrir o arquivo de audio",
    "Open the subtitles file" : u"Abrir o arquivo de legenda",
    "%(h)i hr and %(m)i min" : u"%(h)i hr and %(m)i min",

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"", # New in v2.2.1
    "Use avs2avi to save the current script as an avi" : u"", # New in v2.2.1
    "Please select the path to avs2avi.exe" : u"Favor indicar o caminho p/ avs2avi.exe",
    "Error: avs2avi is required to save an avi!" : u"Erro: é necessário avs2avi para salvar um avi!",
    "Pass: %(pass)s / %(passes)s" : u"Passos: %(pass)s / %(passes)s",
    "Frame: %(frame)i / %(frames)i" : u"Quadro: %(frame)i / %(frames)i",
    "Size: %(size).2f MB" : u"Tamanho: %(size).2f MB",
    "FPS: %(fps).1f fps" : u"FPS: %(fps).1f fps",
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"Tempo restante: %(hr)02i:%(min)02i:%(sec)02i",
    "Input file (.avs):" : u"Arquivo fonte (.avs):",
    "Output file (.avi):" : u"Salvar em (.avi):",
    "# of passes:" : u"nº de passes",
    "Priority:" : u"Prioridade",
    "Error: Unknown button" : u"Erro: comando desconhecido",
    "Save the avi as" : u"Salvar avi como",
    "Avi file (*.avi)|*.avi" : u"Arquivo Avi (*.avi)|*.avi",
    "Input file does not exist!" : u"Arquivo fonte não encontrado!",
    "Input file must be an avisynth script!" : u"Arquivo fonte precisa ser um script Avisynth",
    "Output path does not exist!" : u"Diretório de saida inexistente",
    "# of passes must be an integer!" : u"nº de passos precisa ser um nº inteiro",
    "Priority must be an integer!" : u"Prioridade precisa ser um nº inteiro",
    "Stop" : u"pare",
    "Done" : u"Feito",
    "Process stopped." : u"Processo interrompido",
    "Processing..." : u"Processando",
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"Terminado em  %(hr)i hour(s) and %(min)i minute(s).",
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"Terminado em %(min)i minute(s) and %(sec)i second(s).",
    "Finished in %(time).1f seconds." : u"Terminado em %(time).1f seconds.",
    "Filesize: %(size).2f MB" : u"Tamanho do arquivo: %(size).2f MB",
    "The current script contains errors, exiting." : u"O script atual contem erros, saindo...",
    "Save as AVI" : u"Salvar como AVI",
}