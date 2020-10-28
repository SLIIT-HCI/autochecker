import autocheckUI as autocheck

DETAIL_JSON =''
SUMMARY_JSON = ''
DETAIL_LIST = []    
JSON_LIST = ''
SUMMARY = []
subDir = ''
testDir = ''

def setSubDir(path):
    global subDir
    subDir = path

def setTestDir(path):
    global testDir
    testDir = path

def jasonify(name, tests):
    n = '"name": "'+name+'"'
    t = '"tests":['
    for i,item in enumerate(tests):
        if i==0:
            t = t+'"'+item.strip()+'"'
        else:
            t = t + ', "'+item.strip()+'"'
    t = t+']'

    return '{' + n + ',' + t +'}'

def init():
    global DETAIL_JSON,SUMMARY_JSON,DETAIL_LIST,SUMMARY,JSON_LIST,subDir,testDir
    DETAIL_JSON =''
    SUMMARY_JSON = ''
    DETAIL_LIST = []    
    JSON_LIST = ''
    SUMMARY = []

    
    #print("---init")
    autocheck.init()
    #print("---print_loading_tests")
    autocheck.print_loading_tests()
    #print("---prep_tests")
    autocheck.prep_tests(testDir)
    #print("---print_start_message")
    autocheck.print_start_message()
    #print("---process")
    autocheck.process(subDir)
    #print("---print_results")
    autocheck.print_results()
    #print("---print_endof_results")
    autocheck.print_endof_results()
    #print("---removeAll")
    autocheck.removeAll(subDir)
    autoOutput = autocheck.returnAll()
    autocheck.emptyLists()


    FILE_POSITIONS = [i for i, r in enumerate(autoOutput) if r == "FileName"]
    #print(FILE_POSITIONS)

    SUMMARY_POSITION = autoOutput.index('SummaryStarted')
    #print(SUMMARY_POSITION)

    #print(autoOutput[0:18])
    
    

    for i in range(len(FILE_POSITIONS)):
        if i==0:
            DETAIL_LIST.append(autoOutput[0:FILE_POSITIONS[i+1]])
        elif i==len(FILE_POSITIONS)-1:
            DETAIL_LIST.append(autoOutput[FILE_POSITIONS[i]:SUMMARY_POSITION])
        else:
            DETAIL_LIST.append(autoOutput[FILE_POSITIONS[i]:FILE_POSITIONS[i+1]])

    for i,item in enumerate(DETAIL_LIST):
        filename = item[1].split('\\')[-1]
        PASSED_TESTS = item[item.index('Compilation')+1:]

        if i == 0:     
            DETAIL_JSON += jasonify(filename,PASSED_TESTS)
        else:
            DETAIL_JSON += ',' + jasonify(filename,PASSED_TESTS)

    DETAIL_JSON = '"data":['+DETAIL_JSON+']'


    SUMMARY = autoOutput[SUMMARY_POSITION:]

    for i, item in enumerate(SUMMARY):
        if i==0:
            SUMMARY_JSON += '"'+item.strip()+'"'
        else:
            SUMMARY_JSON += ','+'"'+item.strip()+'"'

    SUMMARY_JSON = '"summary":['+SUMMARY_JSON+']'


def returnData():
    global DETAIL_JSON,SUMMARY_JSON,DETAIL_LIST,SUMMARY,JSON_LIST
    return '{'+DETAIL_JSON+','+SUMMARY_JSON+'}'










