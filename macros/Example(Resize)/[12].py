# NTSC DV 16:9 - 40:33
# above 'NTSC DV 16:9 - 40:33' will be displayed on menu, because filename contains no label, 

# if several macros are doing very similar things, 
# you can just write a main one to handle all cases.
# use callafter=True to ensure the main marco runs after return of the current macro.
# In general, you should return a value, and then,
# the main macro can retrive it from variable 'last'
avsp.ExecuteMenuCommand('Customized', callafter=True)
return 40, 33