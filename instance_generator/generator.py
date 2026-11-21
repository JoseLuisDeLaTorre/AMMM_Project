


configPath = "./config.dat"

import sys
import datParser
import ValidateConfig as v
import InstanceGenerator as ig


config = datParser.DATParser.parse(configPath)
v.ValidateConfig.validate(config)
instGen = ig.InstanceGenerator(config)
instGen.generate()