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
    pulls_list = []

    # This function checks if our env variable is set. 
    def authorization(self):
        
        print('\nAUTHORIZATION PROCESS')
        if self.token == None:
            print('* Environment Variable "GIT_TOCKEN" was not found\n')
        else:
            print('* Authorization passed successfully.\n')
            self.auth = True 

    # The fuction below get pull requests data from given repo and for given state. 
    def get_repo(self, state):

        print('\nProcessing (...)')

        github_user = "contiamo"
        repository_name = "restful-react"

        if self.auth==True: 
            github_instance = Github(self.token, per_page=100)
        else:
            github_instance = Github(per_page=100)
        
        git_repository = github_instance.get_repo('{}/{}'.format(github_user, repository_name))
        pulls = git_repository.get_pulls(state=state)

        for pull in pulls:
            self.pulls_list.append(pull.raw_data)

    # In this function our result is saved as JSON file. File name is set as a timestamp. 
    def pulls_to_json(self):

        now = datetime.now()
        date_label = now.strftime("%Y-%m-%d_%H-%M-%S")

        with open(os.path.abspath('output_json/{}.json'.format(date_label)), 'w', encoding='utf-8') as f:
            json.dump(self.pulls_list, f, ensure_ascii=False, indent=4)

        pulls_quantity = len(self.pulls_list)

        print('\nYou got a data from {} Pull Requests.'.format(pulls_quantity))
        print('File "{}.json" successfully saved.\n'.format(date_label))

    # This fuction runs all previous fuctions in correct order. 
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