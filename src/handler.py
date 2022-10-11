import json
import time
from os import fsdecode

#from . import config
#from src.config import * # VAR directly can be called

#import config
# import config
# from config import *  --  "name 'config' is not defined"
# import config -- module 'config' has no attribute 'VAR1'"

#from config import VAR1

from .rds import RdsStop as rds
from .ec2 import Ec2Stop as ec2
# from .eks import EksAsg as eks


# from rds import RdsStop as rds

def shutdown(event, context):
    rdsNew=rds()
    rdsNew.tasksByDbTags('stopId')
    rdsNew.tasksByDbTags('stopCluster')

    ec2New=ec2()
    ec2New.tasksByTags('stopEc2')

    # eksN=eks()
    # eksN.tasksByTags('downgradeNodeGroup')


def startUp(event, context):
    rdsNew=rds()
    rdsNew.tasksByDbTags('startId')
    rdsNew.tasksByDbTags('startCluster')

    ec2New=ec2()
    ec2New.tasksByTags('startEc2')

    # eksN=eks()
    # eksN.tasksByTags('growNodeGroup')

    # time.sleep(2)


# obj=shutdown({"key3": "value3"},{"key2": "value2"})
# obj=startUp({"key3": "value3"},{"key2": "value2"})