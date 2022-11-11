#!/usr/bin/python3
import datetime
import os
import threading
import configparser
import json

# Sends multiple repositories to github
# 
# 10.11.2022
#
# Henry Palonen / PalonenLABS Oy

def fullpath(name):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return os.path.join(__location__, name)

def read_config():
    config = configparser.ConfigParser()
    config.read(fullpath('conf.ini'))
    return config

# thread function for each repository
def handle_repo(repo, githubuser, tmpdir, repodir):
    # assume that repo directory is format
    # /a/git/CUSTOMER/PROJECT.GIT and parse them from the path

    # whether to actually run these commands or not
    actuallyruncommands = True

    splitted = repo.split('/')
    name = splitted[len(splitted)-1].replace('.git','')
    customer = splitted[len(splitted)-2]

    stream = os.popen('cd ' + tmpdir + ' && git clone ' + repo)
    output = stream.read()
    print("{}".format(output))
    
    github_reponame = githubuser + "/" + customer + "_" + name
    print("repo would be {}".format(github_reponame))

    cmds = {
        'Repo create': 'gh repo create ' + github_reponame + ' --private',
        'Remote add': 'cd ' + os.path.join(tmpdir, name) + ' && git pull && git remote add github git@github.com:' + github_reponame + '.git',
        'Push': 'cd ' + os.path.join(tmpdir, name) + ' && git push github master',
        'Move': 'cd ' + repodir + ' && mv ' + name + '.git transferred-to-github-' + name + '.git'
    }

    for c in cmds:
        print("{} : {}".format(c, cmds[c]))
        if actuallyruncommands:
            # actually run the commands
            stream = os.popen(cmds[c])
            output = stream.read()
            print("{}".format(output))

    #stream = os.popen('cd ' + name + ' && gh repo create ' + github_reponame)
    #output = stream.read()
    #print("{}".format(output))

# main program
if __name__ == "__main__":

    config = read_config()

    threads = list()
    now = datetime.datetime.now()
    print ("---------------------")
    print ("Start ... {}".format(now.strftime("%Y-%m-%d %H:%M:%S")))

    repodir = config['Settings']['repodir']
    githubuser = config['Settings']['githubuser']
    tmpdir = config['Settings']['tmpdir']
    
    os.system('mkdir -p ' + tmpdir)

    repofile = os.path.join(repodir, githubuser + "_repos.txt")
        
    print("Outputting repos to {}".format(repofile))

    os.system('find ' + repodir + ' -type d -name "*.git"|grep -v "transferred-to-github" > ' + repofile)

    file1 = open(repofile, 'r')

    repos = file1.readlines()

    for repo in repos:
        repo = repo.strip()
        handle_repo(repo, githubuser, tmpdir, repodir, )
