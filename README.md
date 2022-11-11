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

11.11.2022 Henry Palonen / PalonenLABS
