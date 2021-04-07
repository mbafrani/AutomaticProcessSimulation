class Trace(object):
    def __init__(self,env):
        self.env = env       
    def registerrequest(self):
        	yield self.env.timeout(83040)       
    def examinecasually(self):
        	yield self.env.timeout(507960)       
    def checkticket(self):
        	yield self.env.timeout(7440)       
    def decide(self):
        	yield self.env.timeout(521400)       
    def reinitiaterequest(self):
        	yield self.env.timeout(2880)       
    def examinethoroughly(self):
        	yield self.env.timeout(450360)       
    def paycompensation(self):
        	yield self.env.timeout(266100)       
    def rejectrequest(self):
        	yield self.env.timeout(241485)       
    