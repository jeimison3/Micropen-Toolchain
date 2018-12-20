import configparser,os,platform
from pathlib import Path



portList = ["mcs51","z80","z180","r2k","r3ka","gbz80","tlcs90","ds390","pic16","pic14","TININative","ds400","hc08","s08","stm8"]
WORKSPACE = "" # Definido a cada inicialização

portArchs = {
    "pic14":{
        "Windows":{
            "includes":["C:\\Program Files\\SDCC\\include\\pic14","C:\\Program Files\\SDCC\\non-free\\include\\pic14"],
            "subports":["C:\\Program Files\\SDCC\\non-free\\include\\pic14"],
            "sdccatribs":["--use-non-free"],
            "filterportname":["pic"]
        }
    }
}


SETUPPATH = str(Path().absolute())
__OS = platform.system()

def isWin():
    return __OS == "Windows"

def MicroToolInit():
    PySettsMicrotool = "micropen.conf"
    cfg = configparser.ConfigParser()
    if not os.path.isfile(PySettsMicrotool): # Não foi configurado
        WSPACE_REF = os.environ['USERPROFILE']+"\\Micronpen" if isWin() else os.environ['HOME']+"/Micronpen"
        cfg.add_section('Projects')
        cfg.set('Projects', 'Workspace', WORKSPACE)
        if not os.path.exists(WORKSPACE):
            os.makedirs(WORKSPACE)
        with open(PySettsMicrotool, 'w') as ponteiroEscrita:
            cfg.write(ponteiroEscrita)
    else: # Foi configurado
        cfg.read(PySettsMicrotool)
        WSPACE_REF = cfg.get('Projects', 'Workspace')
    return [WSPACE_REF]


def listFilesPath(pathname,extens):
    retn = []
    for arquivo in os.listdir(pathname):
        if arquivo.lower().endswith(extens.lower()):
            retn.append(arquivo)
    return retn

def StringFilterList(Input, Lista):
    for Filtro in Lista:
        Input = Input.replace(Filtro,"")
    return Input

def chooseAPort():
    LIB_NAME_INCLUDE = "" # Arquivo de inclusão
    LIB_PATH_LOAD = "" # Pasta de inclusão
    LIB_PORT_NAME = "" # Acompanha -m
    LIB_SUB_PORT_NAME = "" # Acompanha -p

    defColunasLista = 2
    defColunasSpacing = "\t| "

    print("Digite o numero correspondente ao port escolhido:")
    i = 0
    STRprint = ""
    for PORT in portList:
        i=i+1
        STRprint=STRprint+ ("["+str(i)+"] "+PORT+"\t\t")
        if i % defColunasLista == 0:
            STRprint=STRprint+"\n"
    print(STRprint)
    elmtId = int(input("=> "))-1
    if not (elmtId >= 0 and elmtId < len(portList)):
        return
    LIB_PORT_NAME = portList[elmtId]

    #=================================================

    ContaEscolha = 0
    VetorDistribuicao = []
    for PASTA in portArchs[LIB_PORT_NAME][__OS]['includes']:
        ConteudoPasta = listFilesPath(PASTA,".h")
        print(" ---> "+PASTA+"\n")
        printTexto = ""
        for LIB in ConteudoPasta:
            printTexto = printTexto+("["+str(ContaEscolha)+"] "+LIB)+defColunasSpacing
            if ContaEscolha % 5 == 1:
                printTexto = printTexto+"\n"
            ContaEscolha=ContaEscolha+1
        VetorDistribuicao.append(ContaEscolha)
        print(printTexto)

    subportId = int(input("=> "))
    if not (subportId >= 0 and subportId < ContaEscolha):
        return
    mainPort = 0
    indexPort = 0
    for PASTA_LIM in VetorDistribuicao:
        if subportId < PASTA_LIM: # Encontrado
            absoluteId = subportId-mainPort
            LIB_PATH_LOAD = portArchs[LIB_PORT_NAME][__OS]['includes'][indexPort]
            listaArquivos = listFilesPath(LIB_PATH_LOAD,".h")
            LIB_NAME_INCLUDE = listaArquivos[absoluteId]
            LIB_SUB_PORT_NAME = StringFilterList(LIB_NAME_INCLUDE, portArchs[LIB_PORT_NAME][__OS]['filterportname']).replace(".h","")
            break
        indexPort = indexPort+1
        mainPort = mainPort+PASTA_LIM

    return [LIB_PATH_LOAD,LIB_NAME_INCLUDE,LIB_PORT_NAME,LIB_SUB_PORT_NAME]


def setupProject():
    PROJ_NAME = input('Nome do projeto: ')
    WORK_PROJ = WORKSPACE+"\\"+PROJ_NAME if isWin() else WORKSPACE+"/"+PROJ_NAME
    print("Pasta: "+WORKSPACE)

    vectPort = chooseAPort()
    PORT_LIB_INCL = vectPort[0].replace("\\","/") # Converte para endereçamento da IDE
    iPROJ_PORT_PROCESSOR_LIB = vectPort[1] # Nome da biblioteca
    iPROJ_PORT = vectPort[2] # Nome do port
    iPROJ_PORT_PROCESSOR = vectPort[3] # Portproc

    iPROJ_NON_FREE_LIBS_CMD = "" # Inicializa atributos extras do port

    for ATRIBS in portArchs[iPROJ_PORT][__OS]["sdccatribs"]:
        iPROJ_NON_FREE_LIBS_CMD = iPROJ_NON_FREE_LIBS_CMD+" "+ATRIBS

    # Inicia criação da estrutura:
    # Cria pasta do projeto:
    if not os.path.exists(WORK_PROJ):
        os.makedirs(WORK_PROJ)
        os.makedirs(WORK_PROJ+'\\.kdev4')
        os.makedirs(WORK_PROJ+'\\output')

    # Estrutura reconhecimento do projeto na IDE:
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
    #BUILDSET.h
    toolfile = open(WORK_PROJ+'\\BUILDSET.h',mode="w",encoding='utf-8')
    toolfile.write("/*ARQUIVO GERADO AUTOMATICAMENTE, NÃO FAÇA ALTERAÇÕES */")
    toolfile.close()

    # Concluído
    print("\n| Projeto construido em \""+WORK_PROJ+"\".\n| Para alterar as propriedades atualmente suportadas no seu projeto, veja outras opções na ferramenta.\n")





INIT_VARS = MicroToolInit() # Configurações iniciais
WORKSPACE = INIT_VARS[0] # Atualiza Workspace
while(True):
    print("=================================================\nAssistente de configuração de toolchain SDCC.\n=================================================\n\n")
    print("1. Novo projeto.\n2. Abrir projeto.\nx. Sair.")
    OPT_IN = input("=> ")
    if OPT_IN.lower() == "x":
        break
    OPCAO = int(OPT_IN)
    if(OPCAO == 1):
        setupProject()
    else:
        print("Opção desconhecida ou não implementada. Desculpe :/")
