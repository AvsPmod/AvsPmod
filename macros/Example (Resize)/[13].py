# NTSC DVD 4:3 - 8:9
# above 'NTSC DVD 4:3 - 8:9 will be displayed on menu, because filename contains no label, 

# if several macros are doing very similar things, 
# you can just write a main one to handle all cases.
# use callafter=True to ensure the main marco runs after return of the current macro.
# In general, you should return a value, and then,
# the main macro can retrive it from variable 'last'
avsp.ExecuteMenuCommand(_('Customized'), callafter=True)
return 8, 9