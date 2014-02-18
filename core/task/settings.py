
import os

DJANGO_PATH = os.path.split( os.path.split( os.path.realpath(__file__) )[0] )[0]

APP_SETTINGS = {
'mcprod.files'  : { 'status_json': #'http://atlas-project-mc-production.web.cern.ch/atlas-project-mc-production/requests/status.json' , # 
                                                 DJANGO_PATH+os.sep+'mcprod'+os.sep+'status.json',
                    'panda_links': 'D:/DEV/deft-ui/branches/sgayazov/bigpandamon/mcprod/panda_links.csv'},
'mcprod.auth'   : { 'user': 'bigpandamontestuser',
                    'password': 'Y8NLCmjHROqMIRWk'},
'mcprod.default.email.list' : ['mborodin@cern.ch'],
'mcprod.email.from' : 'mborodin@cern.ch'
}
