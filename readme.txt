https://git-scm.com/docs/git-ls-files
Command line for git
git ls-files 
echo debug.log >> .gitignore $ git rm --cached debug.log rm 'debug.log' $ git commit -m "Start ignoring debug.log" 


echo src\db\__pycache__ >> .gitignore 
git rm --cached -r src\db\__pycache__
git commit -m "Start ignoring __pycache__" 