@echo off
start jre8\bin\javaw.exe  -splash:splash.png -cp .;commons-logging-1.1.1.jar;httpclient-4.2.6.jar;httpcore-4.2.5.jar;httpmime-4.2.6.jar;jnlp.jar;bldrm_launcher.jar;commons-dbutils-1.7.jar;sqlite-jdbc-3.23.1.jar com.blinklearning.drm.launcher.Main 
