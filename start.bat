C:\Users\fantv\Documents\Python\virtualenv\db\Scripts\activate
cd C:\Users\fantv\Documents\Python\project\db_project
REM py src\db\build_max_request.py DRM_INT public_view .\sql\drm_int_view.sql

REM CHeck this post for a good redirection with START 
REM https://superuser.com/questions/338277/windows-cmd-batch-start-and-output-redirection
REM /B if we don't want to see the window ! ^are escpae character ?!
start "Test db_perform" cmd /c py src\db\db_perform.py .\json\DRM_INT_test.json .\logs\log_perform.conf -n=100 