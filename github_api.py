from github import Github
from datetime import datetime
import json
import os

# ------------------------  USER MANUAL ------------------------
# Unauthorized users are limited to 50 queries per hour. To 
# extend your ability to send requests, set your Personal Github 
# token as an environment variable named 'GIT_TOKEN'. The 
# application works correctly even if you do not enter this 
# variable.
#
# 1. After launching the application we get information about
# whether our authorization was successful.
#
# 2. In the next step, you need to select from which pull 
# requests you want to get data. Enter the answer into the 
# terminal:
#
#   o - only open pull requests
#   c - only closed pull requests
#   a - both open and closed pull requests
#
# 3. The collected data is written to a JSON file. The timestamp 
# is selected as the file name. JSON files are stored in the 
# 'output_json' folder.
# --------------------------------------------------------------

class Github_pulls():
    
    token = os.getenv('GIT_TOKEN')
    auth = False
    pulls = []

    def authorization(self):
        
        print('\nAUTHORIZATION PROCESS')
        if self.token == None:
            print('* Environment Variable "GIT_TOCKEN" was not found\n')
        else:
            print('* Authorization passed successfully.\n')
            self.auth = True 

    def get_repo(self, state):

        print('\nProcessing (...)')

        owner = "contiamo"
        repo = "restful-react"

        if self.auth==True: 
            g = Github(self.token, per_page=100)
        else:
            g = Github(per_page=100)
        
        res = g.get_repo('{}/{}'.format(owner, repo))
        pulls = res.get_pulls(state=state)

        for pull in pulls:
            self.pulls.append(pull.raw_data)


    def pulls_to_json(self):

        now = datetime.now()
        date_label = now.strftime("%Y-%m-%d_%H-%M-%S")

        with open(os.path.abspath('output_json/{}.json'.format(date_label)), 'w', encoding='utf-8') as f:
            json.dump(self.pulls, f, ensure_ascii=False, indent=4)

        pulls_qty = len(self.pulls)

        print('\nYou got a data from {} Pull Requests.'.format(pulls_qty))
        print('File "{}.json" successfully saved.\n'.format(date_label))

    def run(self):

        self.authorization()
        pulls_state = input('Do you want to receive data from open, closed or all pull requests ? [o/c/a]\n> ')
        
        if pulls_state=='o':
            self.get_repo(state='open')
        elif pulls_state=='c':
            self.get_repo(state='closed')
        elif pulls_state=='a':
            self.get_repo(state='all')
        else:
            print('Incorrect input value')
            exit()

        self.pulls_to_json()

if __name__=='__main__':
    pulls = Github_pulls()
    pulls.run()
