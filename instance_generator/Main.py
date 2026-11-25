


configPath = "./config.dat"

import sys
import datParser
import ValidateConfig as v
import InstanceGenerator as ig
from AMMMGlobals import AMMMException


def run():
    try:
        print("AMMM Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configPath)
        
        config = datParser.DATParser.parse(configPath)
        v.ValidateConfig.validate(config)

        print("Creating Instances...")
        instGen = ig.InstanceGenerator(config)
        instGen.generate()
        print("Done")

        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())