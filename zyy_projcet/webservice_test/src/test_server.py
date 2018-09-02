#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class Hello_world_service(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def hello_world(self, name, times):
        print name
        print times
        for i in range(times):
            yield u'Hello, %s' % name
            
soap_app = Application( [Hello_world_service], 'zyy_xxk', in_protocol = Soap11(validator='lxml'), out_protocol=Soap11() )

wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('192.168.209.136', 8000, wsgi_app)
    server.serve_forever()