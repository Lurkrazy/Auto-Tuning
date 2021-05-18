#read keys and values from config.json, and search every key in files, and replace then by all values
import autoRun
import os
import os.path

resultPath = '/home/lichendi/results/'
filename = 'config.json' # select file by type file name
resultFile = 'result.log'

def writeResult(result, config):
    if os.path.exists(resultPath + resultFile):
        for i in range(10000):
            #incase error
            if i >= 9999:
                return " error: i = " + str(i)
            if os.path.exists(resultPath + resultFile + str(i)):
                continue
            else:
                os.rename(resultPath + resultFile, resultPath + resultFile + str(i))
                break
    else:
        return "no result.log file in resultPath: " + resultPath
    file_obj = open(resultPath + resultFile, "w+")
    print("config:")
    print(config)
    print("res:")
    print(result)
    file_obj.write(str(result))
    return " done "

#read from config.json
def read_from_config(configPath):
    with open(configPath + 'config.json','r') as f:
        for line in f.readlines():
            line_as_dict = json.loads(line)
            # process here the dict
        print(line_as_dict)

def read_config_exist(configPath):
    allConfig = []
    with open(configPath + filename) as file_obj: # open file with open() function and make alias name from filename (file_obj)
        for line in file_obj: # using for looping to read entire content line-by-line
            allConfig.append(line.rstrip()) # we used rstrip() funtion to remove trailing spaces. it makes contents readable
    return allConfig

def tuneByConfig(configPath):
    allConfig = read_config_exist(configPath)
    print("all config:")
    print(allConfig)

    p = 504
    q = 1024
    #tuning
    #for config in allConfig:
    for i in range(0, 1):
        #print(config)
        result = autoRun.autoTune(p, q, i)
        print(result)
        #write config and result to files
        #writeResult(result, config)
    #print("tune by config done!")
    return allConfig