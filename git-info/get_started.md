## git file structure
* working directory->staging area->local repo(.git folder)->remote repo


## start a project
* from remote repo
```bash
~/.gitconfig # file that stores configuration parameters
git version
git config --global user.name "***"
git config --global user.email "***"
git config --global --list # verify setup
git config --global core.autocrlf input # don't convert LF or CRLF
git config --global credential.helper 'cache --timeout=3600' # cache token

git clone url
cd repo_directory
git status # check branch and other information

echo "hello" >> start.txt
git status



git add start.txt # add file to staging area, so it's tracked file now
git status

git commit -m "adding start.text file" # commit file to local repo
git status

git fetch # non-destructive command, only update references
git pull origin master # always pull before push, sync remote repo first
git push origin master # push to remote repo
# input credentials maybe needed
```
* from local zero
```bash
git init fresh-project # create a new project
cd fresh-project
ls -al # verify .git folder exists
git status

cd ..
rm -rf fresh-project # delete project
```

* from local existing project, link to remote repo
```bash
cd existing-project
git init # create repo in existing folder
git status
git add . # add all files to staging area
git commit -m "first commit" # commit all files in one go
git status

git remote add origin remote-repo-url # link local repo to remote repo
git remote -v # verify linking
git push origin master # push to remote repo
```
