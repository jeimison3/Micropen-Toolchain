import time,sys,subprocess,os,platform,configparser

__OS = platform.system()
iPROJ_NAME = sys.argv[1].replace("'","").replace("\"","") # Remove aspas
iPROJ_PATH = sys.argv[2].replace("'","").replace("\"","").replace("/","\\") # Remove aspas, muda indicador de diretorios

dNOCOMPILE = False

def isWin():
    return __OS == "Windows"


for directive in sys.argv:
    if directive == "-exec": # Busca diretiva de execução
        dNOCOMPILE = True
        break

iPROJ_CONF_LOAD = iPROJ_PATH+"\\settings.ini" if isWin() else iPROJ_PATH+"/settings.ini"
iPROJ_OUTPUT = iPROJ_PATH+"\\output\\"+iPROJ_NAME if isWin() else iPROJ_PATH+"/output/"+iPROJ_NAME

cfg = configparser.ConfigParser()
cfg.read(iPROJ_CONF_LOAD)
iPROJ_PORT = cfg.get('ARCH','PORT')
iPROJ_PORT_PROCESSOR = cfg.get('ARCH','PORTPROC')
iPROJ_EXTRAS_CMD = ""

if cfg.get('ARCH','ISFREE') == '0':
    iPROJ_EXTRAS_CMD = iPROJ_EXTRAS_CMD+" --use-non-free"
if dNOCOMPILE:
    iPROJ_EXTRAS_CMD = iPROJ_EXTRAS_CMD+" -c"

files4include = os.listdir(iPROJ_PATH)


iFILES_LIST = "" # Busca arquivos C na pasta de projeto
for FNAME in files4include:
    if FNAME.lower().endswith('.c'):
        iFILES_LIST = iFILES_LIST+" "+ (iPROJ_PATH+"\\"+FNAME)

try:
    retcode = subprocess.call("sdcc" + iPROJ_EXTRAS_CMD + " -m"+iPROJ_PORT+" -p"+iPROJ_PORT_PROCESSOR + iFILES_LIST + " -o " + iPROJ_OUTPUT , shell=True)
    if retcode == 0:
        if not dNOCOMPILE:
            print("Compiled. \".hex\" generated at output folder.")
    else:
        print("Returned error code: ", retcode, file=sys.stderr)
except OSError as e:
    print("Running failure:", e, file=sys.stderr)
finally:
    print("Task finished.")
