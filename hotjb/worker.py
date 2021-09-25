import os
import json
import jieba
from loguru import logger
from multiprocessing import Process
from wsgiref.simple_server import make_server
from .entity import HotJBEntity

class HotJBWorker:
    '''
    处理类
    '''

    def __init__(self, port, keyword_save=True):
        '''
        初始化。
        '''

        self.idle = True
        self.port = port
        self.keyword_save = keyword_save
        self.process = Process(target=self._work_process)
        self.entity = HotJBEntity

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
        result = list(jieba.cut_for_search(data['text']))

        # 记录关键词
        if self.keyword_save:
            logger.info(f'keyword: {result}')    

        start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
        return [ bytes(json.dumps(result), encoding='utf8') ]

    def _work_process(self):
        '''
        '''
        # 初始化
        debug = os.getenv('HOTJB_DEBUG', False)
        log_level = os.getenv('HOTJB_LOG_LEVEL', 'TRACE' if debug else 'INFO')
        logger.remove()
        logger.add(
            f'runtime/logs/{{time:YYYY-MM-DD}}-{self.port}.log',
            level=log_level,
            rotation='00:00',
            retention='7 days',
            encoding='utf8'
        )
        try:
            # 加载扩展字典
            edp = 'config/extdict.txt'
            if os.path.isfile(edp):
                jieba.load_userdict(edp)
                logger.info(f'load userdict: {edp}')
            
            # 开启服务
            with make_server('127.0.0.1', self.port, self._work_respond) as httpd:
                logger.info(f'worker {self.port} start server:')
                httpd.serve_forever()
        except Exception as e:
            logger.error(e)
        finally:
            logger.info(f'worker {self.port} end.')
