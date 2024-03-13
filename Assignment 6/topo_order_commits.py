#!/usr/local/cs/bin/python3

import os
import sys
import zlib

def topo_order_commits():
    return finalize()


class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# Step 1: first, we discover the git directory, returning as described in the spec

def find_top_git():

    #we invoke os to assign the current directory to a variable
    current = os.getcwd()

    #construct a while loop to loop as long as we are not at the root, moving up the repository as we will see later in loop
    while(current != os.path.dirname(current)):
        #search for .git
        if (os.path.isdir(current+'/.git')):
            return os.path.join(current, '.git')
        
        #if no .git found, move to parent
        current = os.path.dirname(current)

    #use sys.exit to display error and exit status 1
    sys.exit("Not inside a Git repository")

#Step 2: we find the branch names and also include the branch IDs to make future functions easier

def list_local():
    #We use our first function to get the top git and give it to a variable
    git_var = find_top_git()

    #make a br_dir variable for branch directory
    br_dir = os.path.join(git_var, 'refs', 'heads')
    br_arr = []

    #go through eahc file and append to branch array
    for root, dirs, files in os.walk(br_dir):
        for file in files:
            path = os.path.join(root, file)
            br_arr.append(path[len(br_dir) + 1:])

    #hash_node variable to store hash/node connections
    pairings = {}

    #now move on to branches, go through each and get the ID
    for br in br_arr:
        path = os.path.join(br_dir, br) 
        final = open(path, 'r').read()
        final = final.replace('\n', '')
        pairings[br] = final
    #returns the hash and id pairings
    return pairings

#we make a function to get the parents of any given commit
def find_parts(c_id):

    git_var = find_top_git()
    finder = os.path.join(git_var, 'objects')
    finding = os.path.join(finder, c_id[:2], c_id[2:])
    rest_bart = zlib.decompress(open(finding, 'rb').read())
    found = []

    #Nice, we found a commit
    if rest_bart[:6] == b'commit':

        #now we have tp decode to look for parent
        rest_barts = rest_bart.decode()
        rest_barts = rest_barts.split('\n')

        for decoded in sorted(rest_barts):
            if decoded[:6] == 'parent':
                found.append(decoded[7:])

    return found


#name of function is self explanitory- Step 3
def make_graph():

    #start with empty graph
    graph = {}

    #get the branches using function
    branch_list = list_local()

    #go through the commits and get the commit ID,... same as before
    for c_id in sorted(branch_list.values()):
        
        #same code as last function
        git_var = find_top_git()
        finder = os.path.join(git_var, 'objects')
        finding = os.path.join(finder, c_id[:2], c_id[2:])
        rest_bart = zlib.decompress(open(finding, 'rb').read())

        #Nice, its a commit
        if rest_bart[:6] == b'commit':
            pseudostack = [c_id]
            while pseudostack != []:
                current = pseudostack.pop()

                #check for the commit in graph, if not there, make it- n is for node
                if current in graph:
                    n = graph[current]
                else:
                    n = CommitNode(current)

                #get the parents
                parts_cur = find_parts(current)

                #run through the parents
                for parnt in sorted(parts_cur):
                    n.parents.add(parnt)
                    
                    #check if in graph, new_n is new node
                    if parnt in graph:
                        new_n = graph[parnt]
                    else:
                        new_n = CommitNode(parnt)
                        pseudostack.append(parnt)
                    
                    #we finish the parent-child relationship
                    new_n.children.add(current)
                    graph[parnt] = new_n

                graph[current] = n
    
    return graph

#Step 4- use dfs to get topo sort
def dfs_topo():

    #call function to make the graph
    graph = make_graph()
    topo_sort = []
    visited = set()
    roots = []

    #first, we work on finding the roots
    for c_id in sorted(graph):
        if len(graph[c_id].parents) == 0:
            roots.append(c_id)

    
    #go through roots and add to stack
    for root in roots:
        if root not in visited:
            #things that arent visited
            not_visit = [root]
        
        while not_visit != []:
            current = not_visit.pop()

            #check for commit
            if current not in visited:
                #check case for more than 1 parent
                if len(graph[current].parents) > 1:
                    total = []
                    p_visited = []

                    for part in sorted(graph[current].parents):
                        #handle cases for having seen/not seen parent
                        if part not in visited:
                            total = [part]
                            
                            #originally had this as append, changed to add
                            visited.add(part)
                            
                            while total != []:
                                p_current = total.pop()


                                for part in sorted(graph[p_current].parents):
                                    if part not in visited:
                                        total.append(part)
                                    p_visited.append(p_current)
                                    visited.add(p_current)

                    #start the topo sort
                    for n in reversed(p_visited):
                        topo_sort.append(n)
                    
                for child in sorted(graph[current].children):
                    if child not in visited:
                        not_visit.append(child)
                
                topo_sort.append(current)
                visited.add(current)
            
    return topo_sort


#function that puts everythng together to be called in original function
def finalize():

    fin_graph = make_graph()
    topolog = dfs_topo()[::-1]
    stick = False
    length = len(topolog)
    bras = list_local()

    for var in range(length):
        c_id = topolog[var]
        n = fin_graph[c_id]

        #check if sticky
        if stick:
            
            printer = "="
            stick = False

            #if sticky, print children
            for child in sorted(n.children):
                printer = printer + f'{child} '
            print(printer.rstrip())
        
        print(c_id, end = '')

        for x in sorted(bras.keys()):
            if bras[x] == c_id:
                prints = ' ' + x
                print(prints, end = '')
        print()

        #check if we have arrived at the last element
        if var != length - 1:
             #iterate
             next_id = topolog[var+1]
             next_node = fin_graph[next_id]

             #check if child of next node
             if c_id not in next_node.children:
                    #if it is not in the children return
                    #we make the output this
                    prints = ""

                    for parents in sorted(n.parents):
                        prints = prints + f'{parents} '

                    prints = prints.strip()


                    print(prints + '=')
                    print()
                    stick = True



if __name__ == '__main__':
    topo_order_commits()

                








    




#I used a combination of strace -f and grep in order 
#to test my code for functions that are not allowed.
#I searched for things like "git" to check if i was using some
#functions that are not allowed