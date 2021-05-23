Ctrl F5 doesn't work to execute test because VC tries to execute it like a script and not like a module
In this case, import doesn't work.
So for now to execute and debug tests. 
py -m test.Testbulk_insert

Look this 
https://gaopinghuang0.github.io/2018/08/03/python3-import-and-project-layout

Command to laucnh test from root directory
py -m unittest discover -s .\src\db\tests -t .\src\db -p 'Test*' -v