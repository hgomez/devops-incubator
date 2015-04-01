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

 

