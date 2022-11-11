# Mass send local repositories to GitHub

We had ~200 local repositories at our local server. We decided to move to github private repositories.
This script moves repositores many repositories at a time.

Meat of the beef is here:

- 'Repo create': 'gh repo create ' + github_reponame + ' --private',
- 'Remote add': 'cd ' + os.path.join(tmpdir, name) + ' && git pull && git remote add github git@github.com:' + github_reponame + '.git',
- 'Push': 'cd ' + os.path.join(tmpdir, name) + ' && git push github master',
- 'Move': 'cd ' + repodir + ' && mv ' + name + '.git transferred-to-github-' + name + '.git'

So script parses following directory structure

/local/git/project1/repo1.git
/local/git/project1/repo2.git
/local/git/project2/repo1.git
/local/git/project2/repo2.git

and clones them locally to 'tmpdir' (default /tmp/repotmp).

After that it creates Github repository with "gh repo create", adds an remote "github" and pushes whole repository there.
And finally local repo is renamed to transferred-to-github-repo1.git

In the middle of script there is 'actuallyruncommands' variable that controls if commands are actually run or just outputted to console.
It is on purpose in the middle of the script so that everyone using this should read the script first and verify it suits their needs.

Example run with directory as

/a/git/customer1/v4_common.git

Cloning into '/tmp/repotmp/v4_common'...
repo would be User1/customer1_v4_common
Repo create : gh repo create User1/customer1_v4_common --private
Remote add : cd /tmp/repotmp/v4_common && git pull && git remote add github git@github.com:User1/customer1_v4_common.git
Push : cd /tmp/repotmp/v4_common && git push github master
Move : cd /a/git/customer1 && mv v4_common.git transferred-to-github-v4_common.git

So after that directory will be
/a/git/customer1/transferred-to-github-v4_common.git

and Github repo is User1/customer1_v4_common.git

11.11.2022 Henry Palonen / PalonenLABS
