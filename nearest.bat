@echo off
call Scripts\activate.bat
python nearest.py -a "sound board" "churchview" "worship leader" "bass" "shut down"
call Scripts\deactivate.bat