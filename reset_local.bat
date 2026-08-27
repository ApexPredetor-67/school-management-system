@echo off
if exist school.db del /q school.db
if exist static\uploads\profiles rmdir /s /q static\uploads\profiles
mkdir static\uploads\profiles
echo Local database and uploaded profiles reset.
