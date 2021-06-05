https://git-scm.com/docs/git-ls-files
Command line for git
git ls-files 
echo debug.log >> .gitignore $ git rm --cached debug.log rm 'debug.log' $ git commit -m "Start ignoring debug.log" 

echo src\db\__pycache__ >> .gitignore 
git rm --cached -r src\db\__pycache__
git commit -m "Start ignoring __pycache__" 

git rm -r --cached . 
git add .
git commit -am "Remove ignored files"

Check .gitignore file - seemed ok (bin/Debug folder content ignored)
Check GIT repo for these files (bin/Debug folder content) - they were there => inconsistence with ignore file
Locally delete these files and commit and push (narrow the GIT files with .gitignore definitions)
(Optional) Restart Visual studio and perform Pull
Repository and VS seems now to be in consistent state

There are certain files created by particular editors, IDEs, operating systems, etc., that do not belong in a repository.
 But adding system-specific files to the repo's .gitignore is considered a poor practice. 
 This file should only exclude files and directories that are a part of the package that should not be versioned (such as the node_modules directory) as well as files that are generated (and regenerated) as artifacts of a build process.

All other files should be in your own global gitignore file. 
Create a file called .gitignore in your home directory and add anything you want to ignore. 
You then need to tell git where your global gitignore file is.
