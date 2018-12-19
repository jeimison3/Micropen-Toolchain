import time,sys,subprocess,os

iPROJ_NAME = sys.argv[1].replace("'","").replace("\"","") # Remove aspas
iPROJ_PATH = sys.argv[2].replace("'","").replace("\"","").replace("/","\\") # Remove aspas, muda indicador de diretorios

iPROJ_OUTPUT = iPROJ_PATH + "\\output\\" + iPROJ_NAME

iPROJ_NON_FREE_LIBS_CMD = " --use-non-free"
iPROJ_PORT = "pic14"
iPROJ_PORT_PROCESSOR = "12f629"



files4include = os.listdir(iPROJ_PATH)

iFILES_LIST = ""

for FNAME in files4include:
    if FNAME.lower().endswith('.c'):
        iFILES_LIST = iFILES_LIST+" "+ (iPROJ_PATH+"\\"+FNAME)

try:
    retcode = subprocess.call("sdcc" + iPROJ_NON_FREE_LIBS_CMD + " -m"+iPROJ_PORT+" -p"+iPROJ_PORT_PROCESSOR + iFILES_LIST + " -o " + iPROJ_OUTPUT , shell=True)
    if retcode == 0:
        print("Compilado. HEX gerado.")
    else:
        print("Codigo de erro retornado: ", retcode, file=sys.stderr)
except OSError as e:
    print("Falha na execução:", e, file=sys.stderr)

##print(sys.argv)

##time.sleep(5)
