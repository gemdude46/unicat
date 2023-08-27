import sys, random
if len(sys.argv) != 2:
    sys.exit(-1)

with open(sys.argv[1],'r') as cf:
    uc=cf.read()

mem={}

ins = []

c=""

while len(uc) > 0:
    if repr(uc)[1:].startswith("\\xf0\\x9f\\x98\\xb"):
        c+=str(int(repr(uc)[16],16)-8)
        uc=uc[4:]
        continue
    if repr(uc)[1:].startswith("\\xf0\\x9f\\x99\\x80"):
        c+='8'
        uc=uc[4:]
        continue
    #print repr(uc)
    uc=uc[1:]

def parseNbr():
    global c
    n=""
    if len(c) == 0:
        return 1337
    while c[0]!='8':
        n+=c[0]
        c=c[1:]
        if len(c) == 0:
            return 1337
    c=c[1:]
    if c[0] == '7':
        n='-'+n
    c=c[1:]
    if n in ('','-'): return 0
    return int(n,8)
        

def parseStmt():
    global c
    if len(c) < 2:
        c=""
        return ("asgnlit",-1,-1)
    if c[0] == '3' and c[1] == '1':
        c=c[2:]
        return ("asgnlit",parseNbr(),parseNbr())
    if c[0] == '5' and c[1] == '7':
        c=c[2:]
        return ("jumpif>",parseNbr(),parseNbr())
    if c[0] == '5' and c[1] == '4':
        c=c[2:]
        return ("echovar",parseNbr())
    if c[0] == '4' and c[1] == '4':
        c=c[2:]
        return ("echoval",parseNbr())
    if c[0] == '4' and c[1] == '6':
        c=c[2:]
        return ("pointer",parseNbr())
    if c[0] == '8' and c[1] == '3':
        c=c[2:]
        return ("randomb",parseNbr())
    if c[0] == '2' and c[1] == '4':
        c=c[2:]
        return ("inputst",parseNbr())
    if c[0] == '7' and c[1] == '8':
        c=c[2:]
        if len(c) == 0:
            return ("asgnlit",-1,-1)
        xc=c[0]
        c=c[1:]
        return ("applop"+{2:'-',8:'*',7:'/'}.get(int(xc),'+'),parseNbr(),parseNbr())
    if c[0] == '8' and c[1] == '8':
        c=c[2:]
        return ("diepgrm",)
    c=c[1:]
    return ("asgnlit",-1,-1)

while len(c) > 0:
    ins.append(parseStmt())

#print ins

while True:
    mem[-1]=mem.get(-1,-1)+1
    try: it = ins[mem[-1]]
    except IndexError: it = ("asgnlit",-1,-1)
    if it[0] == "diepgrm":
        sys.exit()
    if it[0] == "pointer":
        mem[it[1]]=mem.get(mem.get(it[1],0),0)
    if it[0] == "randomb":
        mem[it[1]]=random.choice([0,1])
    if it[0] == "asgnlit":
        mem[it[1]]=it[2]
    if it[0] == "jumpif>" and mem.get(it[1],0) > 0:
        mem[-1]=it[2]
    if it[0] == "applop+":
        mem[it[1]]=mem.get(it[1],0)+mem.get(it[2],0)
    if it[0] == "applop-":
        mem[it[1]]=mem.get(it[1],0)-mem.get(it[2],0)
    if it[0] == "applop/":
        mem[it[1]]=mem.get(it[1],0)/mem.get(it[2],0)
    if it[0] == "applop*":
        mem[it[1]]=mem.get(it[1],0)*mem.get(it[2],0)
    if it[0] == "echovar":
        sys.stdout.write(unichr(mem.get(it[1],0)))
    if it[0] == "echoval":
        sys.stdout.write(str(mem.get(it[1],0)))
    if it[0] == "inputst":
        inp = sys.stdin.readline()
        for k in range(it[1],it[1]+len(inp)):
            mem[k]=ord(inp[k-it[1]])
        mem[k+1]=0
