'''
Created on Jul 17, 2014

@author: c3h3
'''

class EdxUrls(object):
    edx_site_dict = {"edx":"https://courses.edx.org",
                     "stanford":"https://class.stanford.edu",
                     }
    
    def __init__(self, edx_site="edx"):
        assert edx_site in self.edx_site_dict.keys()
        
        self.base = self.edx_site_dict[edx_site]
        self.login_ajax = self.base + "/login_ajax"
        self.dashboard = self.base + "/dashboard"
        
    
         
