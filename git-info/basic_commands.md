## working on project

* tracked file: files that are already committed or in stage area and git aware of it
```bash
git ls-files # list all tracked files
git status # check current file status


git add . # recursively add all files and folders
git reset # unstage all files

git reset HEAD filename # unstage the file
git checkout -- filename # undo changes on file in working directory
````

* move and rename files
```bash

git mv old_filename new_filename # change file name and stage it
git mv new_filename old_filename # go back as if no changes has been made at all

mv old_filename new_filename # change file name only
git add -A # stage changes including renamed/moved/deleted to stage area
```
* delete files
```bash
rm filename # delete untracked file
git rm filename # delete tracked file and stage it

rm filename # delete tracked file
git add -A # add changes including renamed/moved/deleted to stage area
```

* git log and alias
```bash
git log
git help log # review commit history
git log --abbrev-commit
git log -- filename # review commit history on this file
git show commit_id # review particular commit

git log --oneline --decorate --all --graph # review graph logs
git config --global alias.hist "log --all --graph --decorate --oneline"
# create a command alias named hist
```

* .gitignore
```bash
touch .gitignore # in this file define untracked files
git commit -am "add .gitignore file" # stage and commit in one go
```
* comparison
```bash
git config --global merge.tool p4merge
git config --global mergetool.p4merge.path "C:/Program Files/Perforce/p4merge.exe"
git config --global mergetool.prompt false

git config --global diff.tool p4merge
git config --global difftool.p4merge.path "C:/Program Files/Perforce/p4merge.exe"
git config --global difftool.prompt false

git config --global -l # verify diff and merge tools setting

git diff # compare working directory and staging area
git diff HEAD # compare working directory and local repo (last known commit)
git diff --staged HEAD # compare staging area and local repo (last known commit)
git difftool # compare working directory and staging area using difftool

git diff -- filename # compare on individual file
git diff ae6f876 jifr34f # compare random commits
git diff ae6f876 HEAD # compare random commit with last known commit
git diff HEAD HEAD^ # compare HEAD and HEAD-1


git diff master origin/master # compare local repo and remote repo

```
## working with branches
* work on branches instead of master is best practice
```bash
git branch # list local branches
git branch -a # list all remote and local branches
git branch mynewbranch # create new branch
git branch -m mynewbranch newbranch # rename new branch
git branch -d newbranch # delete branch
git checkout mynewbranch # switch to new branch
```
* fast-forward or non-fast-forward merge (new branch to master)
```bash
git checkout -b new # create and checkout new branch
git commit -am "some changes" # commit a new change on new branch

git checkout master # back to master branch
git diff master new # review changes between two branches
git merge new # merge new to master, fast-forward
# fast-forward merge is only possible when master did not have any further commit
git merge new --no-ff # merge new to master, no-fast-forward
```
* merge conflict
```bash
git mergetool # launch mergetool to resolve conflict, decide which side wins
git commit -m "done resolving merge conflict" # manual commit in the end
```
* rebase so fast-forward merge later is possible (master to new branch)
```bash
git checkout new
git rebase master
git checkout master
git merge new # fast-forward merge

git rebase master
git rebase --abort # in case of conflict, abort rebase

git mergetool # resolve conflict
git rebase --continue
```
* pull rebase
```bash
git pull --rebase origin master # keep local commit ahead of remote origin master
```
## stashing and tagging
* stashing
```bash

```
* tagging
```bash

```
