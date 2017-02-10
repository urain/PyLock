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
blah = re.sub(re.compile(r'^import\s+([a-zA-Z_]{2,40})',re.MULTILINE),'',blah)

#find unique import.function used in code
for i in builtin_imports:
  p = re.compile(r'\b'+i+r'\.[a-zA-Z_]{2,40}')
  m = p.findall(blah)
  for j in m:
    if j not in builtin_imports_function:
      builtin_imports_function.append(j)

#find all functions and modules in our code
root=ast.parse(blah)
names=sorted({node.id for node in ast.walk(root) if isinstance(node,ast.Name)})

#find all of our functions that belong to __builtins__
for i in names:
  if i in dir(eval(dir()[0])):
      builtin_commands.append(i)
print builtin_commands
#find all user variables with length >= 2, not a builtin cmd, and not an import
for i in names:
    if i not in builtin_commands and len(i) >= 2 and i not in builtin_imports:
        long_vars.append(i)
        
#encrypt the builtin function names
for i in builtin_commands:
    t=""
    for j in i:
        t+= chr(ord(j)^(len(i)%2+1))
    builtin_commands[builtin_commands.index(i)]=t
    
#encrypt the import.function names
for i in builtin_imports_function:
    t=""
    for j in i:
        t+=chr(ord(j)^(len(i)%2+1))
    builtin_imports_function[builtin_imports_function.index(i)] = t

#function to decrypt an encrypted builtin function name
#this will be added to the header of the ingested code in string format.
def d(h):
    t=""
    for i in h:
        t+=chr(ord(i)^(len(h)%2+1))
    return t

#Get object for 1. builtin function, 2. import(library.function)
#This will be added to the header of ingested code in string format.
def z(h,y):
    t=d(h)
    x=""
    if y==1:
        x=getattr(e,t)
    elif y == 2:
        o = t.split(".")
        exec("import %s"%o[0])                                      # for debug to import the library from script
        k = getattr(e,dir(e)[dir(e).index(d("^^hlqnsu^^"))])(o[0])  # import(library)
        x = getattr(k,dir(k)[dir(k).index(o[1])])                   # import(library.func)
    return x

# This will be our string to append to the final code. It will contain our decryption function
# and our builtin variable substitution function variable assignments
code_append = "e=eval(dir()[0])\ndef d(h):\n\tt=\"\"\n\tfor i in h:\n\t\tt+=chr(ord(i)^(len(h)%2+1))\n\treturn t\ndef z(h,y):\n\tt=d(h)\n\tx=\"\"\n\tif y==1:\n\t\tx=getattr(e,t)\n\telif y == 2:\n\t\to = t.split(\".\")\n\t\tk = getattr(e,dir(e)[dir(e).index(d(\"^^hlqnsu^^\"))])(o[0])\n\t\tx = getattr(k,dir(k)[dir(k).index(o[1])])\n\treturn x\n"

#make tuple substitutes for builtin functions
print "\nBuiltin\t\t\tEncrypted\t\tSubstitution"
print "-------\t\t\t------------\t\t-----------"
for i in builtin_commands:
    k=i                                       #encrypted builtin_command used to prin in table
    j=d(i)                                    #decrypted builtin_command string
    h="ll"+("l"*(builtin_commands.index(i)))  #substitution variable generation
    print "%-23s %-23s %s"%(j,k,h)
    code_append += "ll"+("l"*(builtin_commands.index(i))) + " = " + "z(\"%s\",1)"%i+"\n" #builds string to be appeneded later
    builtin_sub_list.append((j,h)) #add tuple pair of builtin command and it's substitution variable

#replace builtin functions with builtin_sub_list obfuscated vars
for i in builtin_sub_list:
    blah = re.sub(i[0],i[1],blah)
    
#make tuple for import.functions and obfuscated variables
for i in builtin_imports_function:
    k = i
    j = r'\b'+d(i)+r'\b'  #encrypted import used to print in table
    h = "mm"+("m"*(builtin_imports_function.index(i))) # variable assignment
    print "%-23s %-23s %s"%(j.replace("\\b","").replace("\\.",""),k,h.replace(".",""))
    code_append += "mm"+("m"*(builtin_imports_function.index(i))) + " = " + "z(\"%s\",2)"%i+"\n" #builds string to be appened later
    builtin_imports_sub_list.append((j,h)) #add tuple pair of builtin command and it's substitution variable
    
#replace import.function with obfuscated vars
for i in builtin_imports_sub_list:
    blah = re.sub(i[0],i[1],blah)
    
#----------------------------------------------------------------------------

#generate single, double, triple char var list. by generating A,AA,AAA. 
for i in range(ord("A"),ord("Z")+1):
    sub_short_vars.append(chr(i))
    sub_short_vars.append(chr(i)*2)
    sub_short_vars.append(chr(i)*3)
    
#TODO: this will search the entire file, look for long var, replace it by
#index range, then repeat until the script no longer has the long var.
#still has issues replacing text in strings that match a variable name
#i.e. m=f.open("variableName.txt","r")

#make tuple list from long_vars and sub_short_vars
for i in long_vars:
    it=long_vars.index(i)
    m=re.compile(ur'(?:\b)(%s)(?:\b)'%i,re.MULTILINE)
    sub_list.append((m,sub_short_vars[it]))
    if "__" in i:
    	code_append += "%s"%sub_short_vars[it]+" = " + "eval(d(\"%s\"))"%d(i)+"\n"
    else:
	code_append += "%s"%sub_short_vars[it]+" = " + "d(\"%s\")"%d(i)+"\n"
    print "%-23s %23s %s"%(i,"",sub_short_vars[it]) #print the sub list
    
    while re.search(m,blah):
        bl = re.search(m,blah)
        blah=blah[0:bl.span(1)[0]]+sub_short_vars[it]+blah[bl.span(1)[1]:]
        #print "'{g}' was found between the indices {s}".format(g=bl.group(1),s=bl.span(1)) 

#append the decrypt func and builtin variable obfuscation assignment to head of code
blah = code_append+blah

#write the output to the new file
output_file = file_name.split(".")[0]+"-tmp"+".py"

with open(output_file,"w") as f:
    f.write(blah)
    f.close()

print "\n\nDONE!!!"
print "\nOUTPUT FILE: %s"%(output_file)










