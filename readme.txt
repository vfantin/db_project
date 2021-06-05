https://git-scm.com/docs/git-ls-files
Command line for git
git ls-files 
echo debug.log >> .gitignore $ git rm --cached debug.log rm 'debug.log' $ git commit -m "Start ignoring debug.log" 




echo src\db\__pycache__ >> .gitignore 
git rm --cached -r src\db\__pycache__
git commit -m "Start ignoring __pycache__" 

Check .gitignore file - seemed ok (bin/Debug folder content ignored)
Check GIT repo for these files (bin/Debug folder content) - they were there => inconsistence with ignore file
Locally delete these files and commit and push (narrow the GIT files with .gitignore definitions)
(Optional) Restart Visual studio and perform Pull
Repository and VS seems now to be in consistent state