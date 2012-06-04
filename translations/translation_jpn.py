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

# Japanese translation authors:
#   niiyan v2.0.2

version = "2.3.0"

messages = {
    "Find" : u"検索",
    "Replace" : u"置換",
    "Cannot find \"%(text)s\"" : u"", # New in v2.3.0
    "Replaced %(count)i times" : u"%(count)i回置換しました",
    "AviSynth fonts and colors" : u"フォントと色の設定",
    "Background" : u"背景色",
    "Font" : u"フォント",
    "Text color" : u"文字色",
    "OK" : u"", # New in v1.2.1
    "Cancel" : u"キャンセル",
    "Scrap Window" : u"スクラップウィンドウ",
    "Undo" : u"元に戻す",
    "Redo" : u"やり直し",
    "Cut" : u"切り取り",
    "Copy" : u"コピー",
    "Paste" : u"貼り付け",
    "Select all" : u"すべて選択",
    "Refresh" : u"更新",
    "Insert frame #" : u"フレーム番号を挿入",
    "Save to file..." : u"ファイルに保存",
    "Clear all" : u"すべてをクリア",
    "Toggle scrap window" : u"スクラップウィンドウの切り替え",
    "Save script" : u"上書き保存",
    "Error: no contextMenu variable defined for window" : u"エラー: コンテキストメニュー変数がウィンドウに対して定義されていません",
    "Text document" : u"", # New in v2.3.0
    "All files" : u"", # New in v2.3.0
    "Save scrap text" : u"スクラップテキストを保存",
    "This field must contain a value!" : u"値が入力されていません！！",
    "This slider label already exists!" : u"このラベルはすでに存在しています！",
    "Invalid slider label modulo syntax!" : u"スライダラベルの倍数指定のシンタックスが無効",
    "This field must contain a number!" : u"数値を入力してください！",
    "The min value must be less than the max!" : u"最小値は最大値より小さく設定してください！",
    "The initial value must be between the min and the max!" : u"初期値は最小値と最大値の間に設定してください！",
    "The min value must be a multiple of %(mod)s!" : u"最小値は%(mod)sの倍数でなければなりません！",
    "The max value must be a multiple of %(mod)s!" : u"最大値は%(mod)sの倍数でなければなりません！",
    "The initial value must be a multiple of %(mod)s!" : u"初期値は%(mod)sの倍数でなければなりません！",
    "The difference between the min and max must be greater than %(mod)s!" : u"最小値と最大値の差は%(mod)sより大きくなければなりません！",
    "Error" : u"エラー",
    "Define user slider" : u"ユーザスライダの定義",
    "Slider label:" : u"スライダのラベル",
    "Min value:" : u"最小値",
    "Max value:" : u"最大値",
    "Initial value:" : u"初期値",
    "Add or override AviSynth functions in the database" : u"データベースにAviSynth関数を追加または再定義",
    "Core filters" : u"内蔵フィルタ",
    "Plugins" : u"プラグイン",
    "User functions" : u"ユーザ定義関数",
    "Script functions" : u"スクリプト関数",
    "Clip properties" : u"クリッププロパティ",
    "Include %(title)s in autcompletion lists" : u"オートコンプリートリストに %(title)s を含める",
    "New function" : u"新規追加",
    "Edit selected" : u"編集",
    "Delete selected" : u"削除",
    "Select installed" : u"インストール済みのプラグインを選択",
    "Import from files" : u"", # New in v2.2.0
    "Export customizations" : u"カスタマイズのエクスポート",
    "Clear customizations" : u"カスタマイズのクリア",
    "Clear manual presets" : u"プリセットのクリア",
    "When importing, don't show the choice dialog" : u"", # New in v2.2.0
    "Edit function information" : u"関数情報の編集",
    "Name:" : u"名前:",
    "Type:" : u"タイプ:",
    "clip property" : u"クリッププロパティ",
    "core filter" : u"内蔵フィルタ",
    "plugin" : u"プラグイン",
    "script function" : u"スクリプト関数",
    "user function" : u"ユーザ定義関数",
    "Arguments:" : u"引数:",
    "define sliders" : u"スライダの定義",
    "reset to default" : u"デフォルトにリセット",
    "Slider information" : u"スライダ情報",
    "Preset:" : u"プリセット:",
    "Auto-generate" : u"自動生成",
    "Filter name already exists!" : u"そのフィルタ名はすでに存在します！",
    "Invalid filter name!" : u"無効なフィルタ名です！",
    "Renaming not allowed!" : u"名前を変更することはできません！",
    "You must use dllname_function naming format for plugins!" : u"プラグインについては「dll名_関数」という命名書式を使用しなければなりません！",
    "Open Customization files, Avisynth scripts or Avsp options files" : u"", # New in v2.2.0
    "All supported" : u"", # New in v2.3.0
    "Customization file" : u"", # New in v2.3.0
    "AvsP data" : u"", # New in v2.3.0
    "AviSynth script" : u"", # New in v2.3.0
    "Unrecognized files" : u"", # New in v2.2.0
    "Select import functions" : u"", # New in v2.2.0
    "select all" : u"", # New in v2.2.0
    "select none" : u"", # New in v2.2.0
    "select all (file only)" : u"", # New in v2.2.0
    "select none (file only)" : u"", # New in v2.2.0
    "Red - a customized function already exists." : u"", # New in v2.2.0
    "No customizations to export!" : u"エクスポートするカスタマイズが存在しません！",
    "Save filter customizations" : u"フィルタカスタマイズの保存",
    "This will delete all filter customizations. Continue?" : u"すべてのフィルタカスタマイズを削除します。続行しますか？",
    "Warning" : u"警告",
    "This will delete all manually defined presets. Continue?" : u"すべての手動で定義されたプリセットを削除します。続行しますか？",
    "Do you want to delete this custom filter entirely?" : u"このカスタムフィルタを完全に削除しますか？",
    "Edit filter database" : u"フィルタデータベースを編集",
    "Default" : u"デフォルト",
    "Min value" : u"最小値",
    "Max value" : u"最大値",
    "Step size" : u"ステップサイズ",
    "Value list (comma separated)" : u"値のリスト（カンマ区切り）",
    "Value must be True or False!" : u"値はTrueまたはFalseでなければなりません！",
    "Must enter a value list!" : u"値のリストを入力してください",
    "Export filter customizations" : u"フィルタのカスタマイズのエクスポート",
    "Import filter customizations" : u"フィルタのカスタマイズのインポート",
    "Select filters to export:" : u"エクスポートするフィルタの選択:",
    "Select filters to import from the file:" : u"ファイルからインポートするフィルタの選択:",
    "Overwrite all data" : u"すべてのデータを上書きする",
    "You must select at least one filter!" : u"少なくとも1つのフィルタを選択しなければなりません！",
    "Error: minValue must be less than maxValue" : u"エラー: minValueはmaxValueより小さくなければなりません",
    "New File" : u"新しいファイル",
    "Windows Bitmap" : u"", # New in v2.3.0
    "Animation" : u"", # New in v2.3.0
    "JPEG" : u"", # New in v2.3.0
    "Zsoft Paintbrush" : u"", # New in v2.3.0
    "Portable Network Graphics" : u"", # New in v2.3.0
    "Netpbm" : u"", # New in v2.3.0
    "Tagged Image File" : u"", # New in v2.3.0
    "ASCII Text Array" : u"", # New in v2.3.0
    "Windows Icon" : u"", # New in v2.3.0
    "fps" : u"",
    "Frame" : u"フレーム",
    "A crash detected at the last running!" : u"", # New in v2.2.0
    "&Zoom" : u"", # New in v2.2.0
    "%s translation file updated with new messages to translate" : u"", # New in v2.3.0
    "Translation updated" : u"", # New in v2.3.0
    "%s translation file updated.  No new messages to translate." : u"", # New in v2.3.0
    "%s language couldn't be loaded" : u"", # New in v2.3.0
    "Paths" : u"", # New in v2.2.0
    "AvsP help directory:" : u"AvsPのヘルプのディレクトリ",
    "Location of the AvsP help directory" : u"AvsPのヘルプのディレクトリの場所",
    "Avisynth directory:" : u"AviSynthのディレクトリ",
    "Location of the avisynth installation directory" : u"AviSynthをインストールしたディレクトリの場所",
    "Avisynth help file/url:" : u"AviSynthヘルプファイル/URL:",
    "Location of the avisynth help file or url" : u"AviSynthヘルプファイルの場所またはURL",
    "External player:" : u"外部プレーヤー",
    "Location of external program for script playback" : u"スクリプトの再生用の外部プログラムの場所",
    "Additional arguments when running the external player" : u"外部プレーヤーを使用する時の追加の引数",
    "External player extra args:" : u"外部プレーヤーのオプション",
    "Documentation search paths:" : u"ドキュメント検索パス",
    "Specify which directories to search for docs when you click on a filter calltip" : u"フィルタのコールチップ上でクリックした時にドキュメントを検索するディレクトリを指定",
    "Documentation search url:" : u"マニュアル検索URL:",
    "The web address to search if docs aren't found (the filter's name replaces %filtername%)" : u"マニュアルが見つからない場合に検索するウェブアドレス（%filtername% がフィルタの名前に置換されます）",
    "Text" : u"", # New in v2.2.0
    "Show filter calltips" : u"フィルタのコールチップを表示",
    "Turn on/off automatic tips when typing filter names" : u"フィルタ名の入力時に自動的にヒントを表示する/しない",
    "Always show calltips any time the cursor is within the filter's arguments" : u"カーソルがフィルタのパラメータの中にある時は、常にコールチップを表示する",
    "Frequent calltips" : u"常にコールチップを表示",
    "Syntax highlighting" : u"シンタックスの強調表示",
    "Turn on/off avisynth-specific text colors and fonts" : u"AviSynth特有のテキストの色とフォントを強調する/しない",
    "Show autocomplete on capital letters" : u"大文字で始まる単語にオートコンプリートを表示",
    "Turn on/off automatic autocomplete list when typing words starting with capital letters" : u"大文字で始まる単語の入力時に自動的にオートコンプリートのリストを表示する/しない",
    "Amount of letters typed" : u"", # New in v2.3.0
    "Show autocomplete list when typing a certain amount of letters" : u"", # New in v2.2.0
    "Don't allow lines wider than the window" : u"テキストがウィンドウの幅を超える場合は折り返す",
    "Wrap text" : u"現在のウィンドウの幅で折り返す",
    "Draw lines at fold points" : u"", # New in v2.2.0
    "For code folding, draw a line underneath if the fold point is not expanded" : u"", # New in v2.2.0
    "Check to insert actual tabs instead of spaces when using the Tab key" : u"Tabキー使用時に、半角スペースの代わりに現在のタブ幅を挿入するためのチェック",
    "Use tabs instead of spaces" : u"スペースの代わりにタブを使用",
    "Set the size of the tabs in spaces" : u"半角スペースの何個分かでタブのサイズを設定する",
    "Tab width" : u"タブ幅",
    "Initial space to reserve for the line margin in terms of number of digits" : u"桁数の点で行番号欄のマージンを確保するための初期のスペース",
    "Line margin width" : u"行番号欄のマージン",
    "Autocomplete" : u"オートコンプリート",
    "Add user defined variables into autocomplete list" : u"", # New in v2.2.0
    "Show autocomplete with variables" : u"", # New in v2.2.0
    "Show autocomplete on single matched lowercase variable" : u"", # New in v2.2.0
    "When typing a lowercase variable name, show autocomplete if there is only one item matched in keyword list" : u"", # New in v2.2.0
    "Add icons into autocomplete list. Using different type to indicate how well a filter's presets is defined" : u"", # New in v2.2.0
    "Show autocomplete with icons" : u"", # New in v2.2.0
    "Don't show autocomplete when calltip is active" : u"", # New in v2.2.0
    "When calltip is active, autocomplete will not be activate automatically. You can still show autocomplete manually" : u"", # New in v2.2.0
    "Customize autocomplete keyword list..." : u"", # New in v2.2.0
    "Customize the keyword list shown in the autocomplete choice box" : u"", # New in v2.2.0
    "Autoparentheses level" : u"丸括弧のオートコンプリートのレベル",
    "Close \"()\"" : u"括弧を閉じる \"()\"", # New in v1.3.2
    "Determines parentheses to insert upon autocompletion" : u"オートコンプリートで挿入する丸括弧の数を決定します",
    "None \" \"" : u"括弧なし \" \"", # New in v1.3.2
    "Open \"(\"" : u"開き丸括弧のみ \"(\"", # New in v1.3.2
    "Determines which key activates the filter preset when the autocomplete box is visible" : u"オートコンプリートボックスが表示されている時にどのキーでフィルタプリセットを有効化するかを決定する",
    "None" : u"なし",
    "Preset activation key" : u"プリセット有効化キー",
    "Return" : u"リターン",
    "Tab" : u"", # New in v2.0.0
    "Video" : u"映像",
    "Constantly update video while dragging" : u"スライドバーの移動中、フレームごとにプレビューを更新",
    "Update the video constantly when dragging the frame slider" : u"スライドバーを使ってフレームを移動しているとき、フレームごとに絶えずプレビューを更新する",
    "Enable line-by-line update" : u"行移動ごとにプレビューを更新",
    "Enable the line-by-line video update mode (update every time the cursor changes line position)" : u"チェックすると、カーソルが行の位置を変更するごとにビデオプレビューを更新する",
    "Focus the video preview upon refresh" : u"更新時にビデオプレビューにフォーカス",
    "Switch focus to the video preview window when using the refresh command" : u"更新時にフォーカスをビデオプレビューウィンドウにスイッチする",
    "Refresh preview automatically" : u"", # New in v2.2.0
    "Refresh preview when switch focus on video window or change a value in slider window" : u"", # New in v2.2.0
    "Seeking to a certain frame will seek to that frame on all tabs" : u"", # New in v2.2.0
    "Shared timeline" : u"", # New in v2.2.0
    "Allow AvsPmod to resize and/or move the program window when updating the video preview" : u"", # New in v2.2.0
    "Allow AvsPmod to resize the window" : u"", # New in v2.2.0
    "Separate video preview window" : u"ビデオプレビューウィンドウを分離",
    "Use a separate window for the video preview" : u"ビデオプレビュー用に独立したウィンドウを使用する",
    "Min text lines on video preview" : u"テキストの行数の最小値（ビデオプレビュー時）",
    "Minimum number of lines to show when displaying the video preview" : u"ビデオプレビュー時に表示するスクリプトの行数の最小値",
    "Customize the video information shown in the program status bar" : u"プログラムのステータスバーに表示されるビデオ情報をカスタマイズ",
    "Customize video status bar..." : u"ビデオステータスバーのカスタマイズ...",
    "User Sliders" : u"ユーザスライダ",
    "Hide slider window by default" : u"デフォルトでスライダウィンドウを隠す",
    "Keep the slider window hidden by default when previewing a video" : u"ビデオをプレビューする時にデフォルトでスライダウィンドウを隠れたままにする",
    "Create user sliders automatically" : u"ユーザスライダを自動的に生成する",
    "Create user sliders automatically using the filter database" : u"フィルタデータベースを使ってユーザスライダを自動的に生成します",
    "Create user sliders for int and float arguments" : u"int型とfloat型の引数用のユーザスライダを生成",
    "type int/float (numerical slider)" : u"int/float型（数値のスライダ）",
    "Create color pickers for hex color arguments" : u"16進数の引数用にカラーピッカを生成",
    "type int (hex color)" : u"int型（16進数）",
    "Create radio boxes for bool arguments" : u"bool型の引数用にラジオボックスを生成",
    "type bool" : u"bool型",
    "Create listboxes for string list arguments" : u"string型のリスト引数用にリストボックスを生成",
    "type string (list)" : u"string型（リスト）",
    "Create filename pickers for string filename arguments" : u"string型のファイル名引数用にファイルピッカを生成",
    "type string (filename)" : u"string型（ファイル名）",
    "Create placeholders for arguments which have no database information" : u"データベース情報のない引数用にプレースフォルダを生成",
    "undocumented" : u"データベース未掲載",
    "Determines which filters will initially have hidden arguments in the slider window" : u"初期状態でスライダウィンドウ内のどの引数を隠すかを決定する",
    "Fold all" : u"すべてを折りたたむ",
    "Fold non-numbers" : u"数値以外を折りたたむ",
    "Fold none" : u"すべてを展開",
    "Fold startup setting" : u"折りたたみ初期設定",
    "Filter exclusion list:" : u"除外フィルタリスト:",
    "Specify filters never to build automatic sliders for" : u"オートマチックスライダを構築しないフィルタを指定する",
    "Save/Load" : u"", # New in v2.2.0
    "Automatically save the session on shutdown and load on next startup" : u"終了時に自動的にセッションを保存し、次回起動時にロードする",
    "Save session for next launch" : u"セッションの自動保存（次回起動時にロードされます）",
    "Always load startup session" : u"常にセッションを読み込む",
    "Always load the auto-saved session before opening any other file on startup" : u"起動時に常に他のファイルを開く前に自動保存されたセッションを読み込む",
    "Always hide the video preview window when loading a session" : u"", # New in v2.2.0
    "Don't preview when loading a session" : u"", # New in v2.2.0
    "Backup session periodically (minutes)" : u"", # New in v2.3.0
    "Backup the session every X minutes, if X > 0" : u"", # New in v2.3.0
    "Backup session when previewing" : u"", # New in v2.2.0
    "If checked, the current session is backed up prior to previewing any new script" : u"有効にすると、プレビューの更新ごとに現在のセッションがバックアップされる",
    "Prompt to save a script before previewing (inactive if previewing with unsaved changes)" : u"外部プレビューの前にスクリプトの保存のためのダイアログを表示（未保存の変更を含むプレビューを許可しているなら動作せず）",
    "Prompt to save when previewing" : u"プレビュー時に保存のためのダイアログを表示",
    "Create a temporary preview script with unsaved changes when previewing the video" : u"ビデオプレビュー時に、未保存の変更を含む外部プレビュー用の一時スクリプトを生成する",
    "Preview scripts with unsaved changes" : u"", # New in v2.2.0
    "Don't prompt to save scripts without file" : u"", # New in v2.3.0
    "When closing a tab, don't prompt to save the script if it doesn't already exist on the filesystem" : u"", # New in v2.3.0
    "Prompt to save each script with unsaved changes when exiting the program" : u"プログラムを終了する時に保存されていない変更のあるスクリプトを保存するためのダイアログを表示する",
    "Prompt to save scripts on program exit" : u"プログラム終了時にスクリプトを保存するダイアログを表示",
    "Save *.avs scripts with AvsPmod markings" : u"", # New in v2.2.0
    "Save AvsPmod-specific markings (user sliders, toggle tags, etc) as a commented section in the *.avs file" : u"", # New in v2.2.0
    "Misc" : u"その他",
    "Choose the language used for the interface" : u"", # New in v2.3.0
    "Language *" : u"", # New in v2.3.0
    "Show keyboard images in the script tabs when video has focus" : u"ビデオにフォーカスがある時にスクリプトタブにキーボード画像を表示する",
    "Use keyboard images in tabs" : u"タブ内にキーボード画像を使用",
    "Show tabs in multiline style" : u"", # New in v2.2.0
    "There can be several rows of tabs" : u"", # New in v2.2.0
    "All tabs will have same width" : u"", # New in v2.2.0
    "Show tabs in fixed width" : u"", # New in v2.2.0
    "Enable scroll wheel through similar tabs" : u"", # New in v2.2.0
    "Mouse scroll wheel cycles through tabs with similar videos" : u"マウスのスクロールホイールで類似したビデオのタブを切り替え表示する",
    "Only allow a single instance of AvsPmod" : u"", # New in v2.2.0
    "Show warning at startup if there are dlls with bad naming in default plugin folder" : u"", # New in v2.2.0
    "Show warning for bad plugin naming at startup" : u"", # New in v2.2.0
    "Max number of recent filenames" : u"最近使ったファイルの名前を保存する数",
    "This number determines how many filenames to store in the recent files menu" : u"この数値が最近使ったファイルのメニューに保存されるファイル名の数を決定する",
    "Custom jump size:" : u"カスタムジャンプサイズ:",
    "Jump size used in video menu" : u"ビデオメニューで使われるカスタマイズ可能なフレーム間移動の大きさ",
    "Custom jump size units" : u"カスタムジャンプサイズの単位",
    "Units of custom jump size" : u"カスタムジャンプサイズの単位",
    "hours" : u"時間",
    "minutes" : u"分",
    "seconds" : u"秒",
    "frames" : u"フレーム",
    "Extend selection to line down position" : u"", # New in v2.2.0
    "Scroll down" : u"", # New in v2.2.0
    "Extend rectangular selection to line down position" : u"", # New in v2.2.0
    "Extend selection to line up position" : u"", # New in v2.2.0
    "Scroll up" : u"", # New in v2.2.0
    "Extend rectangular selection to line up position" : u"", # New in v2.2.0
    "Go to previous paragraph" : u"", # New in v2.2.0
    "Extend selection to previous paragraph" : u"", # New in v2.2.0
    "Go to next paragraph" : u"", # New in v2.2.0
    "Extend selection to next paragraph" : u"", # New in v2.2.0
    "Extend selection to previous character" : u"", # New in v2.2.0
    "Go to previous word" : u"", # New in v2.2.0
    "Extend selection to previous word" : u"", # New in v2.2.0
    "Extend rectangular selection to previous character" : u"", # New in v2.2.0
    "Extend selection to next character" : u"", # New in v2.2.0
    "Go to next word" : u"", # New in v2.2.0
    "Extend selection to next word" : u"", # New in v2.2.0
    "Extend rectangular selection to next character" : u"", # New in v2.2.0
    "Go to previous word part" : u"", # New in v2.2.0
    "Extend selection to previous word part" : u"", # New in v2.2.0
    "Go to next word part" : u"", # New in v2.2.0
    "Extend selection to next word part" : u"", # New in v2.2.0
    "Extend selection to start of line" : u"", # New in v2.2.0
    "Go to start of document" : u"", # New in v2.2.0
    "Extend selection to start of document" : u"", # New in v2.2.0
    "Go to start of line" : u"", # New in v2.2.0
    "Extend selection to end of line" : u"", # New in v2.2.0
    "Go to end of document" : u"", # New in v2.2.0
    "Extend selection to end of document" : u"", # New in v2.2.0
    "Go to end of line" : u"", # New in v2.2.0
    "Extend selection to previous page" : u"", # New in v2.2.0
    "Extend rectangular selection to previous page" : u"", # New in v2.2.0
    "Extend selection to next page" : u"", # New in v2.2.0
    "Extend rectangular selection to next page" : u"", # New in v2.2.0
    "Delete to end of word" : u"", # New in v2.2.0
    "Delete to end of line" : u"", # New in v2.2.0
    "Delete back" : u"", # New in v2.2.0
    "Delete to start of word" : u"", # New in v2.2.0
    "Delete to start of line" : u"", # New in v2.2.0
    "Cancel autocomplete or calltip" : u"", # New in v2.2.0
    "Indent selection" : u"選択範囲をインデント",
    "Unindent selection" : u"選択範囲をアンインデント",
    "Newline" : u"", # New in v2.2.0
    "Zoom in" : u"", # New in v2.2.0
    "Zoom out" : u"", # New in v2.2.0
    "Reset zoom level to normal" : u"", # New in v2.2.0
    "Line cut" : u"", # New in v2.2.0
    "Line delete" : u"", # New in v2.2.0
    "Line copy" : u"", # New in v2.2.0
    "Transpose line with the previous" : u"", # New in v2.2.0
    "Line or selection duplicate" : u"", # New in v2.2.0
    "Convert selection to lowercase" : u"", # New in v2.2.0
    "Convert selection to uppercase" : u"", # New in v2.2.0
    "Sort bookmarks ascending" : u"", # New in v2.2.0
    "sort ascending" : u"", # New in v2.2.0
    "Show bookmarks with timecode" : u"", # New in v2.2.0
    "show time" : u"", # New in v2.2.0
    "Show bookmarks with title" : u"", # New in v2.2.0
    "show title" : u"", # New in v2.2.0
    "Resolution-based" : u"", # New in v2.3.0
    "BT.709" : u"", # New in v2.3.0
    "BT.601" : u"", # New in v2.3.0
    "TV levels" : u"", # New in v2.3.0
    "PC levels" : u"", # New in v2.3.0
    "Progressive" : u"", # New in v2.2.0
    "Interlaced" : u"", # New in v2.2.0
    "Swap UV" : u"", # New in v2.2.0
    "25%" : u"", # New in v1.3.8
    "50%" : u"", # New in v1.3.8
    "100% (normal)" : u"100%（標準）",
    "200%" : u"", # New in v1.3.8
    "300%" : u"", # New in v1.3.8
    "400%" : u"", # New in v1.3.8
    "Fill window" : u"ウィンドウに合わせる",
    "Fit inside window" : u"プレビューウィンドウに合わせる",
    "Vertically" : u"", # New in v2.2.0
    "Horizontally" : u"", # New in v2.2.0
    "&File" : u"ファイル",
    "Create a new tab" : u"新しいタブを作成",
    "New tab" : u"新しいタブ",
    "Open an existing script" : u"既存のスクリプトを開く",
    "Open..." : u"開く",
    "Close tab" : u"タブを閉じる",
    "Close the current tab" : u"現在のタブを閉じる",
    "Close all tabs" : u"すべてのタブを閉じる",
    "Close every tab" : u"すべてのタブを閉じる",
    "Rename tab" : u"", # New in v2.2.0
    "Rename the current tab. If script file is existing, also rename it" : u"", # New in v2.2.0
    "Save the current script" : u"現在のスクリプトを保存",
    "Choose where to save the current script" : u"現在のスクリプトを保存する場所を選択",
    "Save script as..." : u"名前を付けて保存",
    "Load a session into the tabs" : u"セッションをタブに読み込む",
    "Load session..." : u"セッションを読み込む",
    "Save all the scripts as a session, including slider info" : u"すべてのスクリプトをセッションとして保存（スライダ情報を含む）",
    "Save session..." : u"セッションを保存",
    "Backup current session" : u"現在のセッションをバックアップ",
    "Backup the current session for next program run" : u"次回起動時用に現在のセッションをバックアップする",
    "Next tab" : u"次のタブ",
    "Switch to next script tab" : u"次のスクリプトのタブに移動",
    "Previous tab" : u"前のタブ",
    "Switch to previous script tab" : u"前のスクリプトのタブに移動",
    "Show the scrap window" : u"スクラップウィンドウを表示",
    "&Exit" : u"終了",
    "Exit the program" : u"プログラムを終了",
    "&Edit" : u"編集",
    "Undo last text operation" : u"最後に行ったテキストの変更を元に戻す",
    "Redo last text operation" : u"最後に行ったテキストの変更をやり直す",
    "Cut the selected text" : u"選択されたテキストを切り取る",
    "Copy the selected text" : u"選択されたテキストをコピー",
    "Paste the selected text" : u"選択されたテキストを貼り付け",
    "Find..." : u"検索...",
    "Open a find text dialog box" : u"検索ダイアログボックスを開く",
    "Find next" : u"次を検索",
    "Find the next instance of given text" : u"次の候補を検索",
    "Open a replace text dialog box" : u"置換ダイアログボックスを開く",
    "Replace..." : u"置換...",
    "Select All" : u"すべて選択",
    "Select all the text" : u"すべてのテキストを選択",
    "&Insert" : u"", # New in v2.2.0
    "Choose a source file to insert into the text" : u"テキストに挿入するソースファイルを選択",
    "Insert source..." : u"ソースを挿入",
    "Get a filename from a dialog box to insert into the text" : u"テキストに挿入するファイル名をダイアログボックスから取得",
    "Insert filename..." : u"ファイル名を挿入",
    "Choose a plugin dll to insert into the text" : u"テキストに挿入するプラグイン（dll）を選択",
    "Insert plugin..." : u"プラグインを挿入",
    "Insert a user-scripted slider into the text" : u"ユーザ定義スライダをテキストに挿入",
    "Insert user slider..." : u"ユーザスライダを挿入",
    "Insert a tag which indicates a separator in the user slider window" : u"ユーザスライダウィンドウにセパレータを示すタグを挿入する",
    "Insert user slider separator" : u"ユーザスライダセパレータを挿入",
    "Insert the current frame number into the text" : u"現在のフレーム番号をテキストに挿入",
    "Add tags surrounding the selected text for toggling with the video preview" : u"ビデオプレビューの切り替えのために選択されたテキストを囲むタグを追加",
    "Tag selection for toggling" : u"切り替え用のタグ選択",
    "Clear all tags" : u"すべてのタグをクリア",
    "Clear all toggle tags from the text" : u"テキストからすべての切り替えタグをクリア",
    "Indent the selected lines" : u"選択された行をインデント",
    "Unindent the selected lines" : u"選択された行をアンインデント",
    "Block comment" : u"ブロックコメント",
    "Comment or uncomment selected lines" : u"選択された行をコメント化/非コメント化",
    "Comment at start of a text style or uncomment" : u"", # New in v2.2.0
    "Style comment" : u"", # New in v2.2.0
    "Toggle current fold" : u"", # New in v2.2.0
    "Toggle the fold point On/OFF at the current line" : u"", # New in v2.2.0
    "Toggle all fold points On/OFF" : u"", # New in v2.2.0
    "Toggle all folds" : u"すべての折りたたみの展開/折りたたみ",
    "&AviSynth function" : u"", # New in v2.2.0
    "Show list of filternames matching the partial text at the cursor" : u"カーソル位置までの部分的なテキストにマッチするフィルタ名のリストを表示",
    "Autocomplete all" : u"", # New in v2.2.0
    "Disregard user's setting, show full list of filternames matching the partial text at the cursor" : u"", # New in v2.2.0
    "Show calltip" : u"コールチップの表示",
    "Show the calltip for the filter (only works if cursor within the arguments)" : u"フィルタのコールチップを表示する（カーソルが引数の中にある場合にのみ動作）",
    "Show function definition" : u"関数定義を表示",
    "Show the AviSynth function definition dialog for the filter" : u"このフィルタのAviSynth関数定義ダイアログを表示する",
    "Filter help file" : u"フィルタのヘルプを表示",
    "Run the help file for the filter (only works if cursor within the arguments or name is highlighted)" : u"フィルタのヘルプを表示する（カーソルが引数の中にあるか、名前が強調されている場合にのみ動作）",
    "&Miscellaneous" : u"", # New in v2.2.0
    "Move line up" : u"1行上へ移動",
    "Move the current line or selection up by one line" : u"現在の行か選択範囲の1行上へ移動する",
    "Move line down" : u"1行下へ移動",
    "Move the current line or selection down by one line" : u"現在の行か選択範囲の1行下へ移動する",
    "Copy the current script without any AvsP markings (user-sliders, toggle tags) to the clipboard" : u"AvsP独自のマーキング（ユーザスライダや切り替え用のタグ）を含まない現在のスクリプトをクリップボードにコピーする",
    "Copy unmarked script to clipboard" : u"マークのないスクリプトをクリップボードにコピー",
    "Copy avisynth error to clipboard" : u"", # New in v2.2.0
    "Copy the avisynth error message shown on the preview window to the clipboard" : u"", # New in v2.2.0
    "&Video" : u"ビデオ",
    "Add/Remove bookmark" : u"", # New in v2.2.0
    "Mark the current frame on the frame slider" : u"現在のフレームをフレームスライダ上にマークする",
    "Clear all bookmarks" : u"すべてのブックマークをクリア",
    "Titled &bookmarks" : u"", # New in v2.2.0
    "Move the nearest titled bookmark to the current position. A historic title will be restored if it matches the condition." : u"", # New in v2.2.0
    "Move titled bookmark" : u"", # New in v2.2.0
    "Restore all historic titles" : u"", # New in v2.2.0
    "Restore historic titles" : u"", # New in v2.2.0
    "Clear all historic titles" : u"", # New in v2.2.0
    "Clear historic titles" : u"", # New in v2.2.0
    "Generate titles for untitled bookmarks by the pattern - 'Chapter %02d'" : u"", # New in v2.2.0
    "Set title (auto)" : u"", # New in v2.2.0
    "Edit title for bookmarks in a list table" : u"", # New in v2.2.0
    "Set title (manual)" : u"", # New in v2.2.0
    "&Navigate" : u"", # New in v2.2.0
    "Go to &bookmark" : u"", # New in v2.2.0
    "Go to next bookmarked frame" : u"次のブックマークへ移動",
    "Next bookmark" : u"次のブックマーク",
    "Go to previous bookmarked frame" : u"前のブックマークへ移動",
    "Previous bookmark" : u"前のブックマーク",
    "Forward 1 frame" : u"1フレーム進む",
    "Show next video frame (keyboard shortcut active when video window focused)" : u"次のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Backward 1 frame" : u"1フレーム戻る",
    "Show previous video frame (keyboard shortcut active when video window focused)" : u"前のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Forward 1 second" : u"1秒進む",
    "Show video 1 second forward (keyboard shortcut active when video window focused)" : u"1秒先のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Backward 1 second" : u"1秒戻る",
    "Show video 1 second back (keyboard shortcut active when video window focused)" : u"1秒前のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Forward 1 minute" : u"1分進む",
    "Show video 1 minute forward (keyboard shortcut active when video window focused)" : u"1分先のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Backward 1 minute" : u"1分戻る",
    "Show video 1 minute back (keyboard shortcut active when video window focused)" : u"1分前のフレームを表示（ビデオウィンドウ フォーカス時、キーボードショートカット有効）",
    "Forward x units" : u"x進む",
    "Jump forward by x units (you can specify x in the options dialog)" : u"x先にジャンプする（xと単位はカスタムジャンプサイズのオプションで指定可能）",
    "Backwards x units" : u"x戻る",
    "Jump backwards by x units (you can specify x in the options dialog)" : u"x前にジャンプする（xと単位はカスタムジャンプサイズのオプションで指定可能）",
    "Go to first frame" : u"先頭フレームへ移動",
    "Go to first video frame (keyboard shortcut active when video window focused)" : u"先頭のビデオフレームへ移動する（ビデオウィンドウフォーカス時、キーボードショートカット有効）",
    "Go to last frame" : u"最終フレームへ移動",
    "Go to last video frame (keyboard shortcut active when video window focused)" : u"最終のビデオフレームへ移動する（ビデオウィンドウフォーカス時、キーボードショートカット有効）",
    "Go to last scrolled frame" : u"最後にスクロールされたフレームへ移動",
    "Last scrolled frame" : u"最後にスクロールされたフレーム",
    "Enter a video frame or time to jump to" : u"ジャンプするビデオフレームの番号または時間を入力する",
    "Go to frame..." : u"フレームジャンプ",
    "Crop editor..." : u"Cropエディタ...",
    "Show the crop editor dialog" : u"Cropエディタのダイアログを表示",
    "&Trim selection editor" : u"", # New in v2.2.0
    "Show the trim selection editor dialog" : u"Trim選択エディタダイアログを表示",
    "Show trim selection editor" : u"Trim選択エディタの表示",
    "Set a selection startpoint (shows the trim editor if not visible)" : u"選択開始位置を設定する（非表示ならTrimエディタを表示）",
    "Set selection startpoint" : u"選択開始位置の設定",
    "Set a selection endpoint (shows the trim editor if not visible)" : u"選択終了位置を設定する（非表示ならTrimエディタを表示）",
    "Set selection endpoint" : u"選択終了位置の設定",
    "Zoom video preview to 25%" : u"ビデオプレビューを25%にズーム",
    "Zoom video preview to 50%" : u"ビデオプレビューを50%にズーム",
    "Zoom video preview to 100% (normal)" : u"ビデオプレビューを100%にズーム（標準）",
    "Zoom video preview to 200%" : u"ビデオプレビューを200%にズーム",
    "Zoom video preview to 300%" : u"ビデオプレビューを300%にズーム",
    "Zoom video preview to 400%" : u"ビデオプレビューを400%にズーム",
    "Zoom video preview to fill the entire window" : u"ウィンドウ全体に合わせてビデオプレビューをズーム",
    "Zoom video preview to fit inside the window" : u"プレビューウィンドウの内側に収めるようにビデオプレビューをズーム",
    "Enlarge preview image to next zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.2.0
    "Shrink preview image to previous zoom level. Not work under 'Fill window' or 'Fit inside window'" : u"", # New in v2.2.0
    "&Flip" : u"", # New in v2.2.0
    "Flip video preview upside down" : u"", # New in v2.2.0
    "Flip video preview from left to right" : u"", # New in v2.2.0
    "&YUV -> RGB" : u"", # New in v2.2.0
    "Swap chroma channels (U and V)" : u"", # New in v2.2.0
    "Use BT.709 coefficients for HD, BT.601 for SD (default)" : u"", # New in v2.3.0
    "Use BT.709 coefficients" : u"", # New in v2.3.0
    "Use BT.601 coefficients" : u"", # New in v2.3.0
    "Use limited range (default)" : u"", # New in v2.3.0
    "Use full range" : u"", # New in v2.3.0
    "For YV12 only, assume it is progressive (default)" : u"", # New in v2.2.0
    "For YV12 only, assume it is interlaced" : u"", # New in v2.2.0
    "Save image as..." : u"名前を付けて画像を保存...",
    "Save the current frame as a bitmap" : u"現在のフレームをビットマップファイルとして保存",
    "Force the script to reload and refresh the video frame" : u"スクリプトをリロードして、ビデオフレームを最新の状態にする",
    "Refresh preview" : u"プレビューの更新",
    "Show/Hide the preview" : u"", # New in v2.2.0
    "Toggle the video preview" : u"ビデオプレビューの切り替え",
    "Release all open videos from memory" : u"開いたすべてのビデオをメモリから解放する",
    "Release all videos from memory" : u"すべてのビデオをメモリから解放",
    "Switch focus between the video preview and the text editor" : u"ビデオプレビューとテキストエディタとの間でフォーカスを切り替える。",
    "Switch video/text focus" : u"フォーカスの切り替え",
    "Show/hide the slider sidebar (double-click the divider for the same effect)" : u"スライダのサイドバーの表示/非表示を切り替える（区切り線をダブルクリックでも同じ効果）",
    "Toggle the slider sidebar" : u"スライダのサイドバーを表示/非表示",
    "Request every video frame once (analysis pass for two-pass filters)" : u"", # New in v2.3.0
    "Run analysis pass" : u"", # New in v2.3.0
    "External player" : u"外部プレーヤー",
    "Play the current script in an external program" : u"現在のスクリプトを外部プログラムで再生",
    "Show information about the video in a dialog box" : u"ダイアログボックスにビデオに関する情報を表示",
    "Video information" : u"ビデオ情報",
    "&Options" : u"オプション",
    "Always on top" : u"常に前面に表示",
    "Keep this window always on top of others" : u"このウィンドウを他のウィンドウの前面に表示する",
    "Disable video preview" : u"ビデオプレビューを無効",
    "If checked, the video preview will not be shown under any circumstances" : u"チェックすると、ビデオプレビューが常に非表示になる",
    "Associate .avs files with AvsP" : u".avsファイルをAvsPと関連付け",
    "Configure this computer to open .avs files with AvsP when double-clicked" : u"ダブルクリックした時に、AvsPで.avsファイルを開くようにこのコンピュータを設定する。",
    "AviSynth function definition..." : u"AviSynth関数の定義...",
    "Edit the various AviSynth script fonts and colors" : u"さまざまなAviSynthスクリプトのフォントと色を編集する",
    "Fonts and colors..." : u"フォントと色...",
    "Edit the extension-based templates for inserting sources" : u"ソースを挿入するための拡張子別のテンプレートを編集",
    "Extension templates..." : u"拡張子別テンプレート...",
    "Configure the program keyboard shortcuts" : u"プログラムのキーボードショートカットを編集する",
    "Keyboard shortcuts..." : u"", # New in v2.2.0
    "Configure program settings" : u"プログラムの設定を行う",
    "Program settings..." : u"プログラム設定",
    "&Help" : u"ヘルプ",
    "Animated tutorial" : u"動画チュートリアル",
    "View an animated tutorial for AvsP (from the AvsP website)" : u"AvsPのための動画チュートリアルをみる（AvsPホームページから）",
    "Learn more about AvsP text features (from the AvsP website)" : u"AvsPのテキスト機能についてもっと学ぶ（AvsPホームページから）",
    "Text features" : u"テキスト機能",
    "Learn more about AvsP video features (from the AvsP website)" : u"AvsPのビデオ機能についてもっと学ぶ（AvsPホームページから）",
    "Video features" : u"ビデオ機能",
    "Learn more about AvsP user sliders (from the AvsP website)" : u"AvsPのユーザスライダについてもっと学ぶ（AvsPホームページから）",
    "User sliders" : u"ユーザスライダ",
    "Learn more about AvsP macros (from the AvsP website)" : u"AvsPのマクロについてもっと学ぶ（AvsPホームページから）",
    "Macros" : u"マクロ",
    "Avisynth help" : u"AviSynthヘルプ",
    "Open the avisynth help html" : u"AviSynthのヘルプを開く",
    "Open Avisynth plugins folder" : u"", # New in v2.2.0
    "Open the avisynth plugins folder" : u"", # New in v2.2.0
    "About this program" : u"このプログラムについて",
    "About AvsPmod" : u"", # New in v2.2.0
    "Previous frame" : u"前のフレーム",
    "Next frame" : u"次のフレーム",
    "Run the script with an external program" : u"外部プログラムを使ってスクリプトを実行する",
    "Run the selected tool" : u"選択されたツールを実行",
    "&Tools" : u"", # New in v2.2.0
    "A macro check item" : u"", # New in v2.3.0
    "A macro radio item" : u"", # New in v2.3.0
    "Run selected macro" : u"選択されたマクロを実行",
    "View the readme for making macros" : u"マクロ作成のためのreadmeを読む",
    "Open macros folder" : u"", # New in v2.3.0
    "Open the macros folder" : u"", # New in v2.2.0
    "&Macros" : u"", # New in v2.2.0
    "Close" : u"閉じる",
    "Rename" : u"", # New in v2.2.0
    "Save" : u"保存",
    "Save as..." : u"名前を付けて保存",
    "Copy to new tab" : u"新しいタブにコピー",
    "Reposition to" : u"", # New in v2.2.0
    "Crop editor" : u"Cropエディタ",
    "You can drag the crop regions with the left mouse button when this dialog is visible, cropping the edge closest to the initial mouse click." : u"このダイアログの表示中、プレビュー画面の上をマウスの左ボタンでドラッグすると、\n最初にクリックした位置に最も近い画像の縁をCropできる",
    "At script end" : u"スクリプトの最後",
    "At script cursor" : u"カーソルの位置",
    "Copy to clipboard" : u"クリップボードにコピー",
    "Insert Crop() command:" : u"Crop()コマンドの挿入位置:",
    "Apply" : u"適用",
    "Trim editor" : u"Trimエディタ",
    "Selection options" : u"範囲選択オプション",
    "Keep selected regions" : u"選択された範囲を残す",
    "Keep unselected regions" : u"選択されていない範囲を残す",
    "Mark video frames inside/outside selection" : u"選択範囲の内側/外側のビデオフレームをマーキング",
    "Use Dissolve() with overlap frames:" : u"", # New in v2.2.0
    "Insert Trim() commands:" : u"Trim()コマンドの挿入位置:",
    "Insert Dissolve() commands:" : u"", # New in v2.2.0
    "Use the buttons which appear on the video slider handle to create the frame selections to trim." : u"トリミングするフレームの選択を行うには、ビデオスライダのつまみの上に現れるボタンを使用してください。",
    "File does not exist!" : u"ファイルが存在しません！",
    "Select a file" : u"ファイルを選択",
    "Create a separator label" : u"セパレータのラベルを作成",
    "Enter separator label" : u"セパレータのラベルを入力",
    "Enter tag name:" : u"タグ名の入力:",
    "Tag definition" : u"タグの定義",
    "Chapter" : u"", # New in v2.2.0
    "Set title for bookmarks" : u"", # New in v2.2.0
    "Title" : u"", # New in v2.2.0
    "Frame No." : u"", # New in v2.2.0
    "Time **" : u"", # New in v2.2.0
    "Left-click on a selected item or double-click to edit.\n\n*  RED - a historic title, not a real bookmark.\n** Time may be unavailable or incorrect before preview refreshed." : u"", # New in v2.3.0
    "Cannot use crop editor unless zoom set to 100% and non-flipped!" : u"", # New in v2.2.0
    "Error loading the script" : u"スクリプトの読み込みエラー",
    "Starting analysis pass..." : u"", # New in v2.3.0
    "Frame size:" : u"フレームサイズ:",
    "Length:" : u"長さ:",
    "Frame rate:" : u"フレームレート:",
    "Colorspace:" : u"色空間:",
    "Field or frame based:" : u"フィールドベース/フレームベース:",
    "Parity:" : u"パリティ:",
    "Audio" : u"音声",
    "Channels:" : u"チャンネル:",
    "Hz" : u"", # New in v1.3.8
    "Sampling rate:" : u"サンプリング周波数:",
    "Sample type:" : u"サンプルタイプ:",
    "bits" : u"ビット",
    "samples" : u"サンプル",
    "Could not find the macros folder!" : u"", # New in v2.2.0
    "Could not find %(readme)s!" : u"%(readme)sを見つけることができませんでした！",
    "Failed to import the selected tool" : u"選択されたツールのインポートに失敗しました！",
    "You must restart for changes to take effect!" : u"変更を有効にするには再起動する必要があります！",
    "Basic" : u"基本設定",
    "Default:" : u"デフォルト:",
    "Comment:" : u"コメント:",
    "Block Comment:" : u"", # New in v2.2.0
    "__END__ Comment:" : u"", # New in v2.2.0
    "Number:" : u"数値:",
    "Operator:" : u"演算子:",
    "String:" : u"文字列:",
    "Triple-quoted string:" : u"3連2重引用符:",
    "Internal filter:" : u"内蔵フィルタ:",
    "External filter:" : u"外部フィルタ:",
    "Internal function:" : u"内部関数:",
    "User defined function:" : u"ユーザー定義関数:",
    "Clip property:" : u"クリッププロパティ:",
    "AviSynth keyword:" : u"AviSynthキーワード:",
    "AviSynth data type:" : u"AviSynthデータ型:",
    "AvsP user slider:" : u"AvsPユーザスライダ:",
    "Monospaced font:" : u"等幅フォント",
    "Advanced" : u"高度な設定",
    "Incomplete string:" : u"不完全な文字列:",
    "Syntax highlight strings which are not completed in a single line differently" : u"入力が完了していない文字列のある行を強調表示する",
    "Brace highlight:" : u"大括弧 {} の強調表示:",
    "Bad brace:" : u"無効な大括弧 {}:",
    "Bad number:" : u"無効な数値",
    "Margin line numbers:" : u"行番号:",
    "Miscellaneous word:" : u"その他:",
    "Calltip:" : u"コールチップ:",
    "Calltip highlight:" : u"コールチップの強調表示:",
    "Cursor:" : u"カーソル:",
    "Selection highlight:" : u"", # New in v2.2.0
    "Current line highlight:" : u"", # New in v2.2.0
    "Highlight the line that the caret is currently in" : u"現在キャレットがある行を強調表示する",
    "Fold margin:" : u"", # New in v2.2.0
    "Scrap window" : u"", # New in v2.2.0
    "Override all fonts to use a specified monospace font(no effect on scrap window)" : u"", # New in v2.2.0
    "Use monspaced font" : u"", # New in v2.2.0
    "Insert aborted:" : u"中止された挿入:",
    "No dot required in file extension!" : u"ファイルの拡張子にドット（.）を付ける必要はありません！",
    "Edit extension-based templates" : u"拡張子別のテンプレートを編集",
    "File extension" : u"拡張子",
    "Template" : u"テンプレート",
    "This info is used for inserting sources based on file extensions." : u"この情報はファイルの拡張子に基づいてソースを挿入するために使用されます。",
    "Any instances of *** in the template are replaced with the filename." : u"テンプレート内の *** はファイル名に置き換えられます。",
    "(If you want relative paths instead of the full filename, use [***].)" : u"（フルパスの代わりに相対パスを使いたいなら、[***]を使用してください。）",
    "Associating .avs files will write to the windows registry." : u".avsファイルとの関連付けをWindowsのレジストリに書き込む。",
    "Do you wish to continue?" : u"続行しますか？",
    "Above keys are built-in editing shortcuts. If item is checked,\nit will not be overrided by a menu shortcut in script window." : u"", # New in v2.3.0
    "* This shortcut is active only when video window has focus.\n~ This shortcut is active only when script window has focus." : u"", # New in v2.3.0
    "Could not find the Avisynth plugins folder!" : u"", # New in v2.2.0
    "AvsPmod version %(version)s " : u"", # New in v2.2.0
    "An AviSynth script editor" : u"AviSynthスクリプトエディタ",
    "AvsP Website" : u"AvsPウェブサイト",
    "Active thread on Doom9's forum" : u"", # New in v2.2.0
    "This program is freeware under the GPL license." : u"このプログラムはGPLライセンスに基づくフリーウェアです。",
    "Input a frame number or time (hr:min:sec) and hit Enter. Right-click to retrieve from history." : u"", # New in v2.2.0
    "copy as time" : u"", # New in v2.2.0
    "copy" : u"", # New in v2.2.0
    "paste" : u"", # New in v2.2.0
    "clear history" : u"", # New in v2.2.0
    "Cannot switch tabs while crop editor is open!" : u"Cropエディタが開いている時はタブを切り替えることができません！",
    "Cannot switch tabs while trim editor is open!" : u"Trimエディタを開いている間はタブを切り替えることができません！",
    "Invalid crop values detected.  Continue?" : u"無効なCrop値が検出されました。続行しますか？",
    "You must create at least one frame selection first!" : u"少なくとも1つ以上の選択範囲を作成しなければなりません！",
    "Select autocomplete keywords" : u"", # New in v2.2.0
    "exclude long names" : u"", # New in v2.2.0
    "Customize the video status bar message" : u"ビデオステータスバーのメッセージをカスタマイズ",
    "Video status bar message:" : u"ビデオステータスバーのメッセージ:",
    "Legend" : u"凡例",
    "Current frame" : u"現在のフレーム",
    "Framecount" : u"フレーム総数",
    "Current time" : u"現在の時間",
    "Total time" : u"総時間",
    "Width" : u"幅",
    "Height" : u"高さ",
    "Aspect ratio" : u"アスペクト比",
    "Framerate" : u"フレームレート",
    "Framerate numerator" : u"フレームレートの分子",
    "Framerate denominator" : u"フレームレートの分母",
    "Colorspace" : u"色空間",
    "Field or frame based" : u"フィールドベース/フレームベース",
    "Parity" : u"パリティ",
    "Parity short (BFF or TFF)" : u"パリティの簡略表記（BFF/TFF）",
    "Audio rate" : u"音声レート",
    "Audio length" : u"音声の長さ",
    "Audio channels" : u"音声のチャンネル",
    "Audio bits" : u"音声のビット数",
    "Audio type (Integer or Float)" : u"音声のタイプ（整数/浮動小数点数）",
    "Pixel position (cursor based)" : u"ピクセルの座標（カーソルベース）",
    "Pixel hex color (cursor based)" : u"ピクセルの16進数値（カーソルベース）",
    "Pixel rgb color (cursor based)" : u"ピクセルのRGB色（カーソルベース）",
    "Pixel yuv color (cursor based)" : u"ピクセルのYUV色（カーソルベース）",
    "Pixel color (auto-detect colorspace)" : u"ピクセルの色（色空間自動判別）",
    "Program zoom" : u"表示倍率",
    "Note: The \"\\t\\t\" or \"\\T\\T\" is used to separate the left and right portions of the status bar\n         message." : u"", # New in v2.3.0
    "A macro is still running. Close anyway?" : u"", # New in v2.3.0
    "Save changes before closing?" : u"閉じる前に変更を保存しますか？",
    "Cannot create a new tab while crop editor is open!" : u"Cropエディタを開いている間は新しいタブを作成できません！",
    "Cannot create a new tab while trim editor is open!" : u"Trimエディタを開いている間は新しいタブを作成できません！",
    "Source files" : u"", # New in v2.3.0
    "Open a script or source" : u"スクリプトまたはソースを開く",
    "Reload the file and lose the current changes?" : u"ファイルをリロードしますか？現在までの変更は失われます。",
    "Open this file" : u"このファイルを開く",
    "Save session before closing all tabs?" : u"すべてのタブを閉じる前にセッションを保存しますか？",
    "Save current script" : u"現在のスクリプトを保存",
    "Directory %(dirname)s does not exist!" : u"ディレクトリ%(dirname)sは存在しません！",
    "Load a session" : u"セッションの読み込み",
    "File has been modified since the session was saved. Reload?" : u"前にセッションが保存されてからファイルが修正されています。リロードしますか？",
    "Save the session" : u"セッションの保存",
    "No image to save" : u"保存する画像がありません",
    "Save current frame" : u"現在のフレームを保存",
    "Insert a source" : u"ソースの挿入",
    "All supported plugins" : u"", # New in v2.3.0
    "AviSynth plugins" : u"", # New in v2.3.0
    "VirtualDub plugins" : u"", # New in v2.3.0
    "VFAPI plugins" : u"", # New in v2.3.0
    "Insert a plugin" : u"プラグインの挿入",
    "No bookmarks defined!" : u"ブックマークが定義されていません！",
    "There must be more than one unique bookmark to use this feature!" : u"この機能を使用するには2つ以上のブックマークがなければなりません！",
    "Jump to specified bookmark" : u"指定されたブックマークへジャンプ",
    "Line: %(line)i  Col: %(col)i" : u"行: %(line)i  列: %(col)i",
    "Frame Based" : u"フレームベース",
    "Field Based" : u"フィールドベース",
    "Bottom Field First" : u"ボトムフィールドファースト",
    "BFF" : u"", # New in v1.3.8
    "Top Field First" : u"トップフィールドファースト",
    "TFF" : u"", # New in v1.3.8
    "Integer" : u"整数",
    "Float" : u"浮動小数点数",
    "pos" : u"座標",
    "hex" : u"16進数",
    "rgb" : u"RGB",
    "rgba" : u"RGBA",
    "yuv" : u"YUV",
    "Edit AviSynth function information" : u"AviSynth関数情報の編集",
    "  Function name" : u"  関数名",
    "Function arguments" : u"パラメータ",
    "Open filter customization file" : u"フィルタのカスタマイズファイルを開く",
    "Filter customization file" : u"", # New in v2.3.0
    "Calltip-only text file" : u"", # New in v2.3.0
    "Invalid filter customization file!" : u"無効なフィルタカスタマイスファイル！",
    "Save filter customization file" : u"フィルタのカスタマイスファイルを保存",
    "Invalid argument!" : u"無効なパラメータ！",
    "Error loading AviSynth!" : u"AviSynthの読み込みに関するエラー！",
    "Make sure you have AviSynth installed and that there are no unstable plugins or avsi files in the AviSynth plugins directory." : u"AviSynthがインストール済みで、不安定なプラグインやavsiファイルがAviSynthのpluginsディレクトリに存在しないことを確認してください。",
    "Save changes before previewing?" : u"プレビュー前に変更を保存しますか？",
    "Executable files" : u"", # New in v2.3.0
    "Select an external player" : u"外部プレーヤーの選択",
    "A program must be specified to use this feature!" : u"この機能を使用するにはプログラムを指定しなければなりません！",
    "General settings..." : u"一般的な設定...",
    "Invalid slider text: min > max" : u"無効なスライダテキスト: 最小値が最大値より大きい",
    "Invalid slider text: value not in bounds" : u"無効なスライダテキスト: 範囲外の値",
    "Invalid slider text: bad modulo label" : u"無効なスライダテキスト: ラベルの倍数指定が不正",
    "Invalid slider text: slider label already exists" : u"無効なスライダテキスト: スライダのラベルがすでに存在する",
    "Invalid slider text: invalid number" : u"無効なスライダテキスト: 無効な数値",
    "Invalid slider tag for rescaling!\nAccept only +, -, or an integer." : u"", # New in v2.3.0
    "Reset to initial value: %(value_formatted)s" : u"初期値%(value_formatted)sにリセット",
    "Reset to initial value: %(value2_formatted)s" : u"", # New in v2.2.0
    "Reset to default value: %(value_formatted)s" : u"デフォルト設定にリセット: %(value_formatted)s",
    "Invalid hexadecimal color!" : u"無効な16進数色！",
    "Must specify a max value!" : u"最大値を指定する必要があります！",
    "Must specify a min value!" : u"最小値を指定する必要があります！",
    "Min value must be a number!" : u"最小値は数値でなければなりません！",
    "Max value must be a number!" : u"最大値は数値でなければなりません！",
    "Default value must be a number!" : u"デフォルト値は数値でなければなりません！",
    "Step size value must be a number!" : u"ステップサイズの値は数でなければなりません！",
    "Left-click to select a color, right click to reset to default" : u"色を選択するには左クリック、デフォルト値にリセットするには右クリックしてください",
    "Toggle \"%(label)s\" section" : u"\"%(label)s\"の範囲をオン/オフ",
    "Above plugin names contain undesirable symbols.\nRename them to only use alphanumeric or underscores,\nor make sure to use them in short name style only." : u"", # New in v2.3.0
    "Don't show me this again" : u"", # New in v2.2.0
    "Save as" : u"名前を付けて保存",
    "Select a directory" : u"ディレクトリの選択",
    "Enter information" : u"情報の入力",
    "Progress" : u"進捗状況",
    "A get pixel info operation has already started" : u"", # New in v2.3.0
    "Error in the macro:" : u"マクロのエラー",
    "Couldn't find %(macrofilename)s" : u"%(macrofilename)sが見つかりませんでした",
    "Failed to open the AVI file" : u"AVIファイルのオープンに失敗しました",
    "Failed to open the AVI frame" : u"AVIフレームのオープンに失敗しました",
    "Failed to retrieve AVI frame" : u"AVIフレームの検索に失敗しました",
    "Ctrl" : u"",
    "Alt" : u"",
    "Shift" : u"",
    "Program Settings" : u"プログラム設定",
    "Browse" : u"参照",
    "* Requires program restart for full effect" : u"* 有効にするにはプログラムを再起動する必要があります",
    "Invalid directory!" : u"無効なディレクトリ！",
    "Invalid filename!" : u"無効なファイル名！",
    "Edit shortcuts" : u"ショートカットの編集",
    "Menu label" : u"メニューのラベル",
    "Keyboard shortcut" : u"キーボードショートカット",
    "Double-click or hit enter on an item in the list to edit the shortcut." : u"ショートカットを編集するには、リストのアイテムをダブルクリックするか、\nアイテムを選択した状態でEnterキーを入力してください",
    "Shortcut" : u"", # New in v2.2.0
    "Action" : u"", # New in v2.2.0
    "Edit the keyboard shortcut" : u"キーボードショートカットの編集",
    "Key:" : u"キー",
    "Clear" : u"クリア",
    "%(keyString)s not found in key string list" : u"%(keyString)sはキー文字列の一覧から見つかりませんでした",
    "This shortcut is being used by:" : u"このショートカットは次のメニューですでに使われています:",
    "Insert" : u"追加",
    "Delete" : u"削除",
    "Error: key %(key)s does not exist!" : u"エラー: %(key)sは存在しません！",
    "Are you sure you want to rename from %(oldName)s to %(newName)s?" : u"本当に%(oldName)sを%(newName)sに変更してもよろしいですか？",
    "Question" : u"質問",
    "Insert a new item" : u"新しいアイテムの追加",
    "Must enter a name!" : u"名前を入力してください！",
    "Item %(newKey)s already exists!" : u"%(newKey)sはすでに登録されています！",
    "Warning: no value entered for item %(newKey)s!" : u"警告: %(newKey)sの値が入力されていません！",
    "Message" : u"メッセージ",
    "Select an item to delete first" : u"先に削除するフィルタを選択してください",
    "Are you sure you want to delete item %(key)s?" : u"本当に%(key)sを削除してもよろしいですか？",

    #--- Tool: resize_calc.py ---#
    "Resize calculator..." : u"リサイズ計算機...",
    "Calculate an appropriate resize for the video" : u"ビデオの適切なリサイズを計算する",
    "Resize calculator" : u"リサイズ計算機",
    "Input" : u"入力",
    "Video resolution:" : u"ビデオ解像度:",
    "Pixel aspect ratio:" : u"ピクセルアスペクト比:",
    "Results" : u"結果",
    "Aspect ratio error:" : u"アスペクト比エラー:",
    "Settings" : u"設定",
    "Target pixel aspect ratio:" : u"目標ピクセルアスペクト比",
    "Resize block constraints:" : u"リサイズブロック制限",
    "Resize percent ranges:" : u"リサイズパーセント幅",
    "Max search aspect ratio error:" : u"", # New in v2.0.0
    "Configure" : u"設定",
    "compute from .d2v" : u".d2vから計算",
    "Configure options" : u"設定オプション",
    "Avisynth resize:" : u"Avisynthリサイズ:",
    "The current Avisynth script contains errors." : u"現在のAvisynthスクリプトはエラーを含んでいます。",

    #--- Tool: encoder_gui.py ---#
    "Save to MP4..." : u"", # New in v2.2.0
    "Encode the current script using x264" : u"", # New in v2.2.0
    "Encode video" : u"ビデオのエンコード",
    "System settings" : u"システム設定",
    "Input file:" : u"入力ファイル:",
    "Output file:" : u"出力ファイル:",
    "Compression settings" : u"圧縮設定",
    "Bitrate (kbits/sec):" : u"ビットレート（キロビット/秒）",
    "calculate" : u"計算",
    "Quality CRF (0-51):" : u"", # New in v2.2.0
    "Quality CQ (1-31):" : u"", # New in v2.2.0
    "Additional settings" : u"追加設定",
    "Credits start frame:" : u"クレジット開始フレーム:",
    "Command line settings" : u"コマンドライン設定",
    "Run" : u"実行",
    "First time using this compression preset!" : u"この圧縮プリセットを使用するのはこれが初めてです！",
    "Please enter the exe paths in the following dialog." : u"次のダイアログにexeファイルのパスを入力してください。",
    "Exe pathnames" : u"exeファイルのパス名",
    "Open an AviSynth script" : u"AviSynthスクリプトを開く",
    "AviSynth script (*.avs)|*.avs" : u"AviSynthスクリプト (*.avs)|*.avs",
    "Save the video as" : u"ビデオに名前を付けて保存",
    "Select a program" : u"プログラムの選択",
    "Program (*.exe)|*.exe" : u"プログラム (*.exe)|*.exe",
    "Unreplaced items remain in the command line:" : u"置換されないアイテムはコマンドラインにとどまる:",
    "Unknown exe paths!" : u"exeファイルのパスが不明です！",
    "General" : u"一般",
    "Credits warning minutes:" : u"クレジット警告分数:",
    "Automatically compute bitrate value on startup" : u"開始時にビットレート値を自動的に計算",
    "Automatically compute pixel aspect ratio from d2v on startup" : u"開始時にd2vからピクセルアスペクト比を自動的に計算",
    "Append batch commands to the avs script as comments" : u"バッチコマンドをコメントとしてAVSスクリプトに追加",
    "Encoder priority:" : u"エンコーダの優先度:",
    "Path to %(name)s:" : u"%(name)s までのパス:",
    "Extra arguments:" : u"追加の引数:",
    "Bitrate Calculator" : u"ビットレート計算機",
    "Output info" : u"出力情報",
    "Total size:" : u"総サイズ",
    "Container:" : u"コンテナ:",
    "(None)" : u"(なし)",
    "Video info" : u"ビデオ情報",
    "Framecount:" : u"フレーム数:",
    "FPS:" : u"フレームレート:",
    "Audio info" : u"音声情報",
    "Audio file:" : u"音声ファイル:",
    "Compress audio" : u"音声の圧縮",
    "Audio bitrate:" : u"音声ビットレート:",
    "Format:" : u"フォーマット:",
    "Subtitles info" : u"字幕情報",
    "Subtitles file:" : u"字幕ファイル:",
    "Total time:" : u"総時間:",
    "Video size:" : u"ビデオサイズ:",
    "Audio size:" : u"音声サイズ:",
    "Subtitles size:" : u"字幕サイズ:",
    "Overhead size:" : u"オーバーヘッドサイズ:",
    "Bitrate:" : u"ビットレート:",
    "Open the audio file" : u"音声ファイルを開く",
    "Open the subtitles file" : u"字幕ファイルを開く",
    "%(h)i hr and %(m)i min" : u"%(h)i 時間 and %(m)i 分",

    #--- Tool: avs2avi_gui.py ---#
    "Save to AVI..." : u"", # New in v2.2.0
    "Use avs2avi to save the current script as an avi" : u"", # New in v2.2.0
    "Please select the path to avs2avi.exe" : u"avs2avi.exeのパスを選択してください",
    "Error: avs2avi is required to save an avi!" : u"エラー: AVIを保存するにはavs2aviが必要です！",
    "Pass: %(pass)s / %(passes)s" : u"パス: %(pass)s / %(passes)s",
    "Frame: %(frame)i / %(frames)i" : u"フレーム: %(frame)i / %(frames)i",
    "Size: %(size).2f MB" : u"サイズ: %(size).2f MB",
    "FPS: %(fps).1f fps" : u"フレームレート: %(fps).1f fps",
    "Time left: %(hr)02i:%(min)02i:%(sec)02i" : u"残り時間: %(hr)02i:%(min)02i:%(sec)02i",
    "Input file (.avs):" : u"入力ファイル (.avs):",
    "Output file (.avi):" : u"出力ファイル (.avi):",
    "# of passes:" : u"パスの回数",
    "Priority:" : u"優先度",
    "Error: Unknown button" : u"エラー: 不明なボタン",
    "Save the avi as" : u"名前を付けてAVIを保存",
    "Avi file (*.avi)|*.avi" : u"AVIファイル (*.avi)|*.avi",
    "Input file does not exist!" : u"入力されたファイルが存在しません！",
    "Input file must be an avisynth script!" : u"入力ファイルはAviSynthスクリプトでなければなりません！",
    "Output path does not exist!" : u"出力先のパスが存在しません！",
    "# of passes must be an integer!" : u"パスの回数は整数でなければなりません！",
    "Priority must be an integer!" : u"優先度は整数でなければなりません！",
    "Stop" : u"中止",
    "Done" : u"終了",
    "Process stopped." : u"処理は中止されました。",
    "Processing..." : u"実行中...",
    "Finished in %(hr)i hour(s) and %(min)i minute(s)." : u"終了しました（所要時間: %(hr)i 時間 %(min)i 分）",
    "Finished in %(min)i minute(s) and %(sec)i second(s)." : u"終了しました（所要時間: %(min)i 分 and %(sec)i 秒）",
    "Finished in %(time).1f seconds." : u"終了しました（所要時間: %(time).1f 秒）",
    "Filesize: %(size).2f MB" : u"ファイルサイズ: %(size).2f MB",
    "The current script contains errors, exiting." : u"現在のスクリプトはエラーを含んでいます。終了します。",
    "Save as AVI" : u"AVIとして保存",

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
    "Type" : u"タイプ",
    "Value" : u"", # New in v2.3.0
    "Bookmarks represent..." : u"", # New in v2.3.0
    "Override 'Value' with the bookmark's title" : u"", # New in v2.3.0
    "ConditionalReader file" : u"", # New in v2.3.0
    "Insert the ConditionalReader file path at the current cursor position" : u"", # New in v2.3.0
    "Bool" : u"", # New in v2.3.0
    "String" : u"文字列",
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
    "Information" : u"情報",
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