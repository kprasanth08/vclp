import pymongo


class MongoDB(object):
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(MongoDB, cls).__new__(cls)
            return cls.__instance
        else:
            raise SyntaxError('This class shall not be instantiated this way. Use get_instance() method.')

    def __init__(self):
        self.dbclient = pymongo.MongoClient(
            "mongodb://vclp_mongodb_so:yD5SaAjVoSyE950@d1fm1mon122.amr.corp.intel.com:7889,d2fm1mon122.amr.corp.intel.com:7889,d3fm1mon122.amr.corp.intel.com:7889/vclp_mongodb?replicaSet=mongo7889")

        self.mgdb = self.dbclient["vclp_mongodb"]

    def get_mongodb(self):
        return self.mgdb
