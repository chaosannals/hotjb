import json
import jieba
from multiprocessing import Process
from wsgiref.simple_server import make_server

class HotJBWorker:
    '''
    处理类
    '''

    def __init__(self, port):
        '''
        初始化。
        '''

        self.idle = True
        self.port = port
        self.process = Process(target=self._work_process)

    def attach(self):
        '''
        起效。
        '''

        self.process.start()

    def detach(self):
        '''
        退出。
        '''

        self.process.terminate()

    def _work_respond(self, environ, start_response):
        '''
        处理响应
        '''

        content_length = int(environ.get('CONTENT_LENGTH', 0))
        content = environ.get('wsgi.input').read(content_length)
        data = json.loads(content)
        # result = list(jieba.cut(data['text'], use_paddle=True))
        result = list(jieba.cut_for_search(data['text']))
        start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
        return [ bytes(json.dumps(result), encoding='utf8') ]

    def _work_process(self):
        '''
        '''

        # jieba.enable_paddle()

        with make_server('127.0.0.1', self.port, self._work_respond) as httpd:
            httpd.serve_forever()
