import createConfig
import tuneByConfigs
import exportPerf

configPath = '/home/lichendi/config/'
if __name__ == '__main__':
    #createConfig.create_config(configPath)
    #print("create config done!")
    tuneByConfigs.tuneByConfig(configPath)
    print("tune by config done!")
    print()
    print()
    print()