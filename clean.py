import os
import re

cdir = "/home/jinhao/Desktop/testing/"
regex_lib = '\<(.*?)\>'
regex_local = '"(.*?")\>'

def enumfile(cdir):
    '''gets all c files from a directory
    ignores h files
    '''
    set_cfile_c = [f for f in os.listdir(cdir) \
                   if (os.path.isfile(os.path.join(cdir, f)) and ".c" in f)]
    set_cfile_h = [f for f in os.listdir(cdir) \
                   if (os.path.isfile(os.path.join(cdir, f)) and ".h" in f)]
    return set_cfile_c, set_cfile_h

def find_bad_includes(cfile_c, cfile_h):
    '''moves the includes from the c file to the h file
    deletes the includes from the c file
    '''
    print "Processing " + cfile_c

    bad_lib_includes = []
    bad_local_includes = []

    # gets all the include statements in the file
    # that are NOT the same name as the file itself    
    with open(cdir+cfile_c, "r") as f:
        lines = f.readlines()
        for line in lines:
            if "#include" in line:
                lib_include = re.search(regex_lib, line)
                local_include = re.search(regex_local, line)

                if lib_include:
                    c_import = lib_include.group(1).replace(".h",".c")
                    if c_import != cfile_c:
                        print "This import must be taken out! " + c_import
                        bad_lib_includes.append(line)

                if local_include:
                    c_import = lib_include.group(1).replace(".h",".c")
                    if c_import != cfile_c:
                        print "This import must be taken out! " + c_import
                        bad_local_includes.append(line)

                

    # checks if the bad includes are already in the h file
    with open(cdir + cfile_h, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line in bad_lib_includes:
                bad_lib_includes.pop(line)
            if line in bad_local_includes:
                bad_local_includes.pop(line)

    return bad_lib_includes, bad_local_includes

def get_h(cfile_c, set_cfile_h):
    '''checks if c file has h file
    returns the h file if it has
    returns None if it does not
    '''
    h_file = None 

    cfile_h = cfile_c.replace(".c", ".h")
    if cfile_h in set_cfile_h:
        h_file = cfile_h

    return h_file

def remove_bad_includes(cfile_c, bad_lib_includes, bad_local_includes):
    with open(cdir + cfile_c, "r") as f:
        lines = f.readlines()
    with open(cdir + cfile_c, "w") as f:
        for line in lines:

            if line not in bad_lib_includes and line not in bad_local_includes:
                f.write(line)
    print "removed!"

def proper_place(cfile_h, bad_lib_includes, bad_local_includes):
    with open(cdir + cfile_h, "r") as f:
        content_cfile_h = f.read()
    with open(cdir + cfile_h, "w") as f:
        f.seek(0,0)
        for include in bad_lib_includes:
           f.write(include+ "\n")
        
        for include in bad_local_includes:
           f.write(include+ "\n")

        f.write(content_cfile_h)
     

def main():
    set_cfile_c, set_cfile_h = enumfile(cdir)
    
    print set_cfile_c
    print set_cfile_h
    
    for cfile_c in set_cfile_c:
        cfile_h = get_h(cfile_c, set_cfile_h)
        
        if (cfile_h != None):        

            bad_lib_includes, bad_local_includes = \
                    find_bad_includes(cfile_c, cfile_h)

            remove_bad_includes(cfile_c, bad_lib_includes, bad_local_includes)            
            proper_place(cfile_h, bad_lib_includes, bad_local_includes)            

main()
