import os.path
import json


filename = 'config.json' # select file by type file name
dict = {'GEMM_P': [ ], 'GEMM_Q': [ ]}

#didn't use
#def write_to_config(configString):
#    if os.path.exists(configPath + filename):
#        for i in range(10000):
#            #incase error
#            if i >= 9999:
#                return " error: i = " + str(i)
#            if os.path.exists(configPath + filename + str(i)):
#                continue
#            else:
#                os.rename(configPath + filename, configPath + filename + str(i))
#                break
#    else:
#        return "no config.log file in configPath: " + configPath
#    file_obj = open(configPath + filename, "w+")
#    file_obj.write(configString)
#    return " done "

def create_config(configPath):
    list1 = [256]
    list2 = []
    for i in range(256, 513, 128):
        list2.append(i)
    for key in dict:
        dict[key] = list2
    dict["GEMM_Q"] = list1
    #for
    #    for i in range(1, 10, 2)

    with open(configPath + filename, 'w') as fp:
        json.dump(dict, fp)
    #for double
    ##for single
    ##dict = {'GEMM_P': 512, 'GEMM_Q': 256}
    #configString = ""
    #for key in dict:
    #    configString += key + '\n' + str(dict[key]) + '\n'
    #write_to_config(configString)
    return "create config done!"
    