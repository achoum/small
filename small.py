# 
# Small 
# Short for "Small Reverse Polish Notation Programming Language"
# The small programming language
# By Mathieu Guillame-Bert
#    achoum@gmail.com
# 
# Version
#    1.0
#    First version. The supported operators are:
#    != * + - / < <= == > >= duplicate exec export get head if length load merge print println set stop tail throw trace vars

import sys

class Context:
    def __init__(self):
        self.debug = False
        
def getGlobalContext( s = Context() ):
    return s

class Env:
 
    def __init__(self,parent=None):
        self.vars = {}
        self.parent = parent
        if parent == None:
            self.stack = []
            self.deph = 0;
        else:
            self.stack = parent.stack
            self.deph = parent.deph + 1
            
    def setVar(self,k,v):
        self.vars[k] = v
        
    def getVar(self,k):
        if k in self.vars:
            return self.vars[k]
        else:
            if self.parent == None:
                raise Exception("Unknown variable "+k)
            else:
                return self.parent.getVar(k)
          
    def toString(self,n):
        
        tab = "\t| " * n
        r = ""
        
        if n==1:
            r += tab + "*Stack\n"
            for s in self.stack:
                r += tab + "   " + str(s) + "\n"  
        
        r += tab + "Env lvl " + str(self.deph) + "\n"

        r += tab + "*Variables\n"
        for k,v in self.vars.items():
            r += tab + "   " + str(k) + " : " + str(v) + "\n"
        else:
            r += tab + "*none*" + "\n"
            
        if self.parent != None:
            r += self.parent.toString(n+1)
            
        return r
          
    def __str__(self):
        return self.toString(1);

def parseExpression(ls,i=0):
    r = []
    while i < len(ls):
        if ls[i] == "{" :
            e,i = parseExpression( ls , i + 1 )
            r.append( e )
            if ls[i] != "}" :
                raise Exception("Unexpected }")
            i += 1
        elif ls[i] == "}" :
            break
        else :
            v = ls[i]
            if v.isdigit():
                v = int(v)
            r.append( v )
            i += 1 
    return r,i

def readExpression(l):
    ls = l.split()
    return parseExpression( ls )[0]

def testRequire( ex , env , req ):
    if len(env.stack) < len(req):
        raise Exception(ex+" requiert "+str(len(req))+" argument(s)\n"+str(env))
    for i in range(len(req)):
        if req[i] != None:
            if not isinstance( env.stack[ i - len(req) ] , req[i] ):
                raise Exception("argument " + str(i+1) + " of " + ex + " should be a " + str(req[i]) + " but is \"" + str(env.stack[ i - len(req) ]) + "\" instead\n"+str(env))

def execExprList( lex , env ):
    for ex in lex:
        execExpr( ex , env )

def execExpr( ex , env ):
    if isinstance(ex,str):
        if ex == "+":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 + a2 )
        elif ex == "-":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 - a2 )
        elif ex == "*":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 * a2 )
        elif ex == "/":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 / a2 )
            
        elif ex == "<":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 < a2 )
            
        elif ex == ">":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 > a2 )
            
        elif ex == "<=":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 <= a2 )
            
        elif ex == ">=":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 >= a2 )
            
        elif ex == "==":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 == a2 )
            
        elif ex == "!=":
            testRequire(ex,env,[int,int])
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            env.stack.append( a1 != a2 )
            
        elif ex == "print":
            testRequire(ex,env,[None])
            a1 = env.stack.pop()
            sys.stdout.write(str(a1))
            
        elif ex == "println":
            testRequire(ex,env,[None])
            a1 = env.stack.pop()
            print(a1)
            
        elif ex == "trace":
            print(env)
            
        elif ex == "length":
            testRequire(ex,env,[ list ])
            v = env.stack.pop()
            v = len( v )
            env.stack.append( v )
            
        elif ex == "throw":
            testRequire(ex,env,[ None ])
            env.stack.pop()
            
        elif ex == "merge":
            testRequire(ex,env,[ list , list ])
            l2 = env.stack.pop()
            l1 = env.stack.pop()
            env.stack.append( l1 + l2 )
            
        elif ex == "head":
            testRequire(ex,env,[ list ])
            l = env.stack.pop()
            env.stack.append( l[0] )
            
        elif ex == "tail":
            testRequire(ex,env,[ list ])
            l = env.stack.pop()
            env.stack.append( l[1:] )
            
        elif ex == "duplicate":
            testRequire(ex,env,[None])
            v = env.stack.pop()
            env.stack.append( v )
            env.stack.append( v )
            
        elif ex == "if":
            testRequire(ex,env,[bool,None,None])
            a3 = env.stack.pop()
            a2 = env.stack.pop()
            a1 = env.stack.pop()
            sub_env = Env( env )
            if a1:
                execExprList( a2 , sub_env )
            else:
                execExprList( a3 , sub_env )
            
        elif ex == "exec":
            testRequire(ex,env,[None])
            a1 = env.stack.pop()
            sub_env = Env( env )
            execExprList( a1 , sub_env )
        
        elif ex == "get":
            testRequire(ex,env,[str])
            k = env.stack.pop()
            v = env.getVar(k)
            env.stack.append( v )
        
        elif ex == "set":
            testRequire(ex,env,[None,str])
            k = env.stack.pop()
            v = env.stack.pop()
            env.setVar(k,v)
        
        elif ex == "exit":
            sys.exit()
            
        elif ex == "read":
            v = raw_input()
            env.setVar(k,v)
            
        elif ex == "load":
            testRequire(ex,env,[str])
            path = env.stack.pop()
            with open (path, "r") as myfile:
                v = readExpression( myfile.read() )
            env.stack.append( v )
            
        elif ex == "export":
            testRequire(ex,env,[None])
            if env.parent == None:
                raise Exection("Cannot export from main environement frame")
            l = env.stack.pop()
            for e in l:
                if not isinstance(e,str):
                    raise Exection("export need a list of string")
                env.parent.vars[e] = env.vars[e]
                
        elif ex == "vars":
            v = [ k for k in env.vars.keys() ]
            env.stack.append( v )
			
        else:
            env.stack.append( ex )
			
    else:
        env.stack.append( ex )

def execString(line):
    if getGlobalContext().debug:
        print("@Run expression: \""+line+"\"")
        
    ex = readExpression( line ) # Parse the input
    env = Env() # Create the environment
    execExprList(ex,env) # Execute the input
    
    if getGlobalContext().debug:
        #print("@Final environment:")
        #print(str(env))
        print("@Final stack: " + str(env.stack))

def execStdin():
    env = Env() # Create the environment
    while(True):
        sys.stdout.write('> ')
        line = raw_input() # Get the input
        l = readExpression( line ) # Parse the input
        execExprList( l , env ) # Execute the input
        print( env.stack ) # Print the stack i.e. the result
    print("@shut down")

if __name__ == "__main__":
    execStdin()


