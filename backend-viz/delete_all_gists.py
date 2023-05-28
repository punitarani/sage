from github import Github as git
import os

g=git(os.getenv('API_TOKEN'))

i=0
for gist in g.get_user().get_gists():
    i = i+1
    gist.delete()
    print("Delted")
