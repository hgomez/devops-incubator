# Investigating nasty issue with docker-registry

When using docker-registry on openSUSE 13.2, rebuilt using easy_install --user, Authorization scheme move from basic to token :
 
    +6987:551ab20a:5|GET /v2/ HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -6987:551ab20a:5
    +6981:551ab20a:6|GET /v1/_ping HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -6981:551ab20a:6
    +6980:551ab20a:6|GET /v1/_ping HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -6980:551ab20a:6
    +6987:551ab20a:6|PUT /v1/repositories/ecd-busybox/ HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Content-Length:312|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Content-type:application/json|X-Docker-Token:true|Accept-Encoding:gzip
    -6987:551ab20a:6
    +6981:551ab20a:7|GET /v1/images/4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Token Token signature=ANPHP92ZNRPBN8JN,repository="library/ecd-busybox",access=write|Accept-Encoding:gzip
    +6980:551ab20a:7|GET /v1/images/ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Token Token signature=ANPHP92ZNRPBN8JN,repository="library/ecd-busybox",access=write|Accept-Encoding:gzip
    -6981:551ab20a:7
    -6980:551ab20a:7
    +6987:551ab20a:7|GET /v1/images/df7546f9f060a2268024c8a230d8639878585defcc1bc6f79d2728a13957871b/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Token Token signature=ANPHP92ZNRPBN8JN,repository="library/ecd-busybox",access=write|Accept-Encoding:gzip
    +6981:551ab20a:8|GET /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Token Token signature=ANPHP92ZNRPBN8JN,repository="library/ecd-busybox",access=write|Accept-Encoding:gzip
    -6987:551ab20a:7
    -6981:551ab20a:8
    +6980:551ab20a:8|PUT /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Content-Length:602|Authorization:Token Token signature=ANPHP92ZNRPBN8JN,repository="library/ecd-busybox",access=write|Content-Type:application/json|Accept-Encoding:gzip
    -6980:551ab20a:8

* https://github.com/docker/docker-registry/issues/541

> If docker-registry runs over HTTPS, docker just sends Basic Authorization headers with every request.
> If docker-registry run over HTTP, docker sends Basic Authorization headers with the first request and after that switches to Token Authorization. It is questionable, whethe that makes sense. 
> If docker sends basic authentication data in plain text over HTTP once, it may as well continue doing so (it is insecure anyways). That way, one would at least have consistent behavior.

No such behaviour when using docker-registry image

    +19403:551bd53a:20|GET /v2/ HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -19403:551bd53a:20
    +19410:551bd53a:1f|GET /v1/_ping HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -19410:551bd53a:1f
    +19404:551bd53a:20|GET /v1/_ping HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:Go 1.1 package http|Accept-Encoding:gzip
    -19404:551bd53a:20
    +19403:551bd53a:21|PUT /v1/repositories/ecd-busybox/ HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Content-Length:312|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Content-type:application/json|X-Docker-Token:true|Accept-Encoding:gzip
    -19403:551bd53a:21
    +19403:551bd53b:22|GET /v1/images/df7546f9f060a2268024c8a230d8639878585defcc1bc6f79d2728a13957871b/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Accept-Encoding:gzip
    +19410:551bd53b:20|GET /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Accept-Encoding:gzip
    +19404:551bd53b:21|GET /v1/images/ea13149945cb6b1e746bf28032f02e9b5a793523481a0a18645fc77ad53c4ea2/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Accept-Encoding:gzip
    +19410:551bd53b:21|GET /v1/images/4986bf8c15363d1c5d15512d5266f8777bfba4974ac56e3270e7760f6f0a8125/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Accept-Encoding:gzip
    -19410:551bd53b:20
    -19403:551bd53b:22
    -19410:551bd53b:21
    -19404:551bd53b:21
    +19404:551bd53b:22|PUT /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Content-Length:602|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Content-Type:application/json|Accept-Encoding:gzip
    -19404:551bd53b:22
    +19403:551bd53b:23|PUT /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/layer HTTP/1.1|Host:registry-ancy.ecd.mycorp.com|User-Agent:docker/1.5.0 go/go1.4.1 git-commit/a8a31ef kernel/3.13.0-37-generic os/linux arch/amd64|Transfer-Encoding:chunked|Authorization:Basic ZWNkLWRlcGxveWVyOjEyMw==|Content-Type:application/octet-stream|Accept-Encoding:gzip
    -19403:551bd53b:23
    +19410:551bd53b:22|PUT /v1/images/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/checksum HTTP/1.1|Host:registry-ancy.ecd.mycorp.com

Let's investigate if problem appears also when using :

* easy_install on various Ubuntu distros
* easy_install on CentOS distros
* easy_install on openSUSE distros

## Ubuntu and easy_install

### 14.04.2

Works
 
    {"host": ["Linux", "a17610144663", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/local/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.6", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyexpat": "2.7.6", "python": "2.7.6 (default, Mar 22 2014, 22:59:56) \n[GCC 4.8.2]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.packages.chardet": "2.2.1", "requests.packages.urllib3": "dev", "requests.packages.urllib3.packages.six": "1.2.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}


### 14.10

Works

    {"host": ["Linux", "9b8a2094604a", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/local/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "chardet": "2.2.1", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.8", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyexpat": "2.7.8", "python": "2.7.8 (default, Oct 20 2014, 15:05:19) \n[GCC 4.9.1]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "six": "1.7.3", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "urllib3": "1.8.3", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}


### 15.04 

Works

    {"host": ["Linux", "d09a42662acd", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/local/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "OpenSSL": "0.13.1", "OpenSSL.version": "0.13.1", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.9", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyasn1": "0.1.7", "pyasn1.debug": "0.1.7", "pyexpat": "2.7.9", "python": "2.7.9 (default, Mar 26 2015, 21:53:54) \n[GCC 4.9.2]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.packages.chardet": "2.2.1", "requests.packages.urllib3": "dev", "requests.packages.urllib3.packages.six": "1.2.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}
 
## CentOS 

### CentOS 7

Works

    {"host": ["Linux", "2d973a43cc3a", "3.13.0-37-generic", "#64-Ubuntu SMP Mon Sep 22 21:28:38 UTC 2014", "x86_64", "x86_64"], "launch": ["/usr/bin/gunicorn", "--access-logfile", "-", "--error-logfile", "-", "--max-requests", "100", "-k", "gevent", "--graceful-timeout", "3600", "-t", "3600", "-w", "4", "-b", "0.0.0.0:5000", "--reload", "docker_registry.wsgi:application"], "versions": {"M2Crypto.m2xmlrpclib": "0.22", "SocketServer": "0.4", "argparse": "1.1", "backports.lzma": "0.0.3", "backports.ssl_match_hostname": "3.4.0.2", "blinker": "1.3", "cPickle": "1.71", "cgi": "2.6", "ctypes": "1.1.0", "decimal": "1.70", "distutils": "2.7.5", "docker_registry.app": "0.9.1", "docker_registry.core": "2.0.3", "docker_registry.server": "0.9.1", "email": "4.0.3", "flask": "0.10.1", "gevent": "1.0.1", "greenlet": "0.4.5", "gunicorn": "19.1.1", "gunicorn.arbiter": "19.1.1", "gunicorn.config": "19.1.1", "gunicorn.six": "1.2.0", "jinja2": "2.7.3", "json": "2.0.9", "logging": "0.5.1.2", "parser": "0.5", "pickle": "$Revision: 72223 $", "platform": "1.0.7", "pyexpat": "2.7.5", "python": "2.7.5 (default, Jun 17 2014, 18:11:42) \n[GCC 4.8.2 20140120 (Red Hat 4.8.2-16)]", "re": "2.2.1", "redis": "2.10.3", "requests": "2.3.0", "requests.packages.chardet": "2.2.1", "requests.packages.urllib3": "dev", "requests.packages.urllib3.packages.six": "1.2.0", "requests.utils": "2.3.0", "simplejson": "3.6.2", "sqlalchemy": "0.9.4", "tarfile": "$Revision: 85213 $", "urllib": "1.17", "urllib2": "2.7", "werkzeug": "0.10.4", "xml.parsers.expat": "$Revision: 17640 $", "xmlrpclib": "1.0.1", "yaml": "3.11", "zlib": "1.0"}}


