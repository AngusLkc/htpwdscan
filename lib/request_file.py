#!/usr/bin/env python
# encoding=utf-8

import urlparse
import re
import os

def parse_command_line_url(self):
    if not self.args.u.lower().startswith('http'):
        self.args.u = 'http://%s' % self.args.u
    (self.args.scm, self.args.netloc, self.args.path, _params, self.args.query, _fragment) = urlparse.urlparse(self.args.u, 'http')
    parse_host_port(self)

def parse_host_port(self):
    if self.args.netloc.find(':') < 0:
        self.args.host = self.args.netloc.strip()
        self.args.host_port = 443 if self.args.scm == 'https' else 80
    else:
        self.args.host, self.args.host_port = self.args.netloc.split(':')
        self.args.host = self.args.host.strip()
        self.args.host_port =int(self.args.host_port)

def parse_request(self):
    self.http_headers = {
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html; htpwdScan 0.03)'
    }
    if self.args.u:
        parse_command_line_url(self)
        return
    if not os.path.exists(self.args.f):
        raise Exception('HTTP request file not found.')
    self.args.scm = 'https' if self.args.https else 'http'
    with open(self.args.f) as f:
        post_text = f.read()
    lines = post_text.split('\n')
    first_line = lines[0].strip()
    self.args.get = True if first_line.upper().startswith('GET') else False
    self.args.netloc = re.search('Host: (.*)', post_text).group(1).strip()
    self.args.path = first_line.split(' ')[1]
    if self.args.path.find('://') > 0:
        self.args.path = self.args.path.replace('://', '')
        self.args.path = self.args.path[self.args.path.find('/'):].strip()
    if self.args.get:
        (_, _, self.args.path, _, self.args.query, _) = urlparse.urlparse(self.args.path)
    else:
        for i in range(len(lines)-1 , 0, -1):
            if lines[i].strip():
                self.args.query = lines[i].strip()
                break
    keys = ['User-Agent', 'Cookie', 'Origin', 'Referer', 'Client-IP', 'X-Forwarded-For', 'X-Forwarded-Host', 'Via', 'Content-Type', 'Accept-Language', 'Authorization']
    for k in keys:
        m = re.search('%s: (.*)' % k, post_text)
        if m: self.http_headers[k] = m.group(1).strip()
    parse_host_port(self)
