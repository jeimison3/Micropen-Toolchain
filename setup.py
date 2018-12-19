import configparser,os
from pathlib import Path

SETUPPATH = str(Path().absolute())

WORKSPACE = "E:\\Programação\\GITProjs\\PROJECT1BASE"
#PROJ_NAME = "TEST01"

print("Assistente de configuração de toolchain SDCC.")
PROJ_NAME = input('Nome do projeto: ')


WORK_PROJ = WORKSPACE+"\\"+PROJ_NAME


iPROJ_NON_FREE_LIBS_CMD = " --use-non-free"
iPROJ_PORT = "pic14"
iPROJ_PORT_PROCESSOR = "12f629"
iPROJ_PORT_PROCESSOR_LIB = "pic12f629.h"

PORT_LIB_INCL = "C:/Program Files/SDCC/non-free/include/pic14" # Maneira que a IDE le locais


# Cria pasta do projeto
if not os.path.exists(WORK_PROJ):
    os.makedirs(WORK_PROJ)
    os.makedirs(WORK_PROJ+'\\.kdev4')
    os.makedirs(WORK_PROJ+'\\output')


kdevprjPre = open(WORK_PROJ+'\\'+PROJ_NAME+'.kdev4',mode="w",encoding='utf-8')
kdevprjPre.write("[Project]\nCreatedFrom=\nManager=KDevCustomBuildSystem\nName="+PROJ_NAME+"\n")
kdevprjPre.close()

# Trecho que configura projeto do KDevelop:
kdevprj = open(WORK_PROJ+'\\.kdev4\\'+PROJ_NAME+'.kdev4',mode="w",encoding='utf-8')

kdevprj.write("[Buildset]\nBuildItems=@Variant(\\x00\\x00\\x00\\t\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0b\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x10\\x00P\\x00i\\x00c\\x00B\\x00a\\x00s\\x00e\\x003)\n\n")
kdevprj.write("[Cppcheck]\ncheckPerformance=true\n\n") # Otimização para Low-Processing

kdevprj.write("[CustomBuildSystem][BuildConfig0][ToolBuild]\nArguments=\nEnabled=false\nEnvironment=\nExecutable=\nType=0\n\n")
kdevprj.write("[CustomBuildSystem][BuildConfig0][ToolClean]\nArguments=\nEnabled=false\nEnvironment=\nExecutable=\nType=3\n\n")
kdevprj.write("[CustomBuildSystem][BuildConfig0][ToolConfigure]\nArguments=\nEnabled=false\nEnvironment=\nExecutable=\nType=1\n\n")
kdevprj.write("[CustomBuildSystem][BuildConfig0][ToolInstall]\nArguments=\nEnabled=false\nEnvironment=\nExecutable=\nType=2\n\n")
kdevprj.write("[CustomBuildSystem][BuildConfig0][ToolPrune]\nArguments=\nEnabled=false\nEnvironment=\nExecutable=\nType=4\n\n")

kdevprj.write("[CustomDefinesAndIncludes][ProjectPath0][Compiler]\nName=None\n\n")
kdevprj.write("[CustomDefinesAndIncludes][ProjectPath0][Includes]\n1="+PORT_LIB_INCL.replace("\\","/")+"\n\n")
kdevprj.write("[Launch]\nLaunch Configurations=Launch Configuration 0\n\n")
kdevprj.write("[Launch][Launch Configuration 0]\nConfigured Launch Modes=execute\nConfigured Launchers=scriptAppLauncher\nName=SDCC Run\nType=Script Application\n\n")

kdevprj.write("[Launch][Launch Configuration 0][Data]\n")
kdevprj.write("Arguments='"+PROJ_NAME+"' '"+WORK_PROJ.replace("\\","/")+"'\n")
kdevprj.write("EnvironmentGroup=\n")
kdevprj.write("Executable=file:///" + SETUPPATH.replace("\\","/") + "/compila.py\n")
kdevprj.write("Execute on Remote Host=false\n")
kdevprj.write("Interpreter=python\n")
kdevprj.write("Output Filtering Mode=2\n")
kdevprj.write("Remote Host=\n")
kdevprj.write("Run current file=false\n")
kdevprj.write("Working Directory=")

kdevprj.close()

#==============================================================================================
# Configuração do reconstrutor de parâmetros

cfg = configparser.ConfigParser({
    'PROJECT':{
        'NAME':PROJ_NAME,
        'PATH':WORK_PROJ
    },
    'ARCH':{
        'PORT':iPROJ_PORT,
        'PORTPROC':iPROJ_PORT_PROCESSOR,
        'ISFREE':'0'
    },
    'INCLUDES':{
        'PORTPATH':PORT_LIB_INCL,
        'PORTPROCLIB':iPROJ_PORT_PROCESSOR_LIB,
    }
})

#==============================================================================================

# Salva configuração
with open(WORK_PROJ+'\\settings.ini', 'w') as ponteiroEscrita:
    cfg.write(ponteiroEscrita)

#==============================================================================================
# Cria arquivos iniciais do desenvolvimento:

# main.c
mainfile = open(WORK_PROJ+'\\main.c',mode="w",encoding='utf-8')
mainfile.write("#include <"+iPROJ_PORT_PROCESSOR_LIB+">\n") # Inclui biblioteca do PORT
mainfile.write("#include \"BUILDSET.h\"\n\n") # Inclui arquivo de configuração do toolchain
mainfile.write("int main(){\n")
mainfile.write("\t\n\twhile(1){\n")
mainfile.write("\t\t\n\t}\n}")
mainfile.close()

toolfile = open(WORK_PROJ+'\\BUILDSET.h',mode="w",encoding='utf-8')
toolfile.write("/*ARQUIVO GERADO AUTOMATICAMENTE, NÃO FAÇA ALTERAÇÕES */")
toolfile.close()
