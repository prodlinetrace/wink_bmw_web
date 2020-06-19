# wink_bmw_web
Traceability for Winkelmann BMW fuel injector rail - web application

## how to deploy to prod:

### Install Fast CGI Feature for IIS:
https://docs.microsoft.com/en-us/iis/application-frameworks/install-and-configure-php-on-iis/enable-fastcgi-support-in-iis-7-on-windows-server-2008-windows-server-2008-r2-windows-vista-or-windows-7

### Install pyton wfastcgi module
-  install pip module
```
pip install wfastcgi
```
- enable module:
cmd (run as administrator) -> `wfastcgi-enable`

# start IIS console and enable application:
E:\trace_web\web.config