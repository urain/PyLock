#
#                __________________
#              /   ______________   \
#             |   |              |   |
#             |   |              |   |
#             |   |              |   |
#             |   |              |   |
#             ########################
#             ########################
#             ########_PyLock_########
#             ########################
#             ########################
#
# USAGE:  python PyLock.py [name_of_python_script]
# OUTPUT: [name_of_python_script]-tmp.py
#
# DESCRIPTION:
# ------------
# This is an evil tool built to read in another Python script and output
# the code in an obfuscated format. It does this by:
#   1. Replacing user created variables with 1,2,or 3 letter variable substitutions.
#   2. Replacing all builtin Python methods/functions/objects by assigning the object to obfuscated variables.
#   3. Pre-pending the ingested script with a decryption function for unencrypting the now obfuscated builtin objects.
#
# ISSUES
# ------
# At this time the script does have problems identifying all variances of variables i.e. variable names inbetween quotes of strings.
# builtin variable assignments for functions that correspond to user created variables, etc.

import re
import ast
import sys

file_name = sys.argv[1]
e = eval(dir()[0])
blah = ""
long_vars=[]
sub_short_vars=[]
sub_list=[]
builtin_commands=[]
builtin_sub_list=[]
builtin_imports=[]
builtin_imports_function=[]
builtin_imports_sub_list=[]

#read in the code
with open((file_name),"r") as f:
  blah=f.read()
  f.close()

#find imports in script
builtin_imports = re.findall(r'^import\s+([a-zA-Z_]{2,40})',blah,re.MULTILINE)

#delete the import lines
blah = re.sub(re.compile(r'^import\s+([a-zA-Z_]{2,40})',blah,re.MULTILINE),'',blah)

#find unique import.function used in code
for i in builtin_imports:
  p = re.compile(r'\b'+i+r'\.[a-zA-Z_]{2,40}')
  m = p.findall(blah)
  for j in m:
    if j not in builtin_imports_function:
      builtin_imports_function.append(j)
      
      #TODO add rest of code
