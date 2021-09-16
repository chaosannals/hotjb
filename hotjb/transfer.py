from aiohttp import ClientSession
from .worker import HotJBWorker

class HotJBTransfer:
    '''
    '''

    def __init__(self, worker: HotJBWorker):
        '''
        '''

        self.worker = worker

    def __enter__(self):
        '''
        '''

        self.worker.idle = False
        return self

    def __exit__(self, exc_type, exc, tb):
        '''
        '''

        self.worker.idle = True

    async def transfer(self, data):
        '''
        转发请求到 worker 并返回结果。
        '''
        
        url = f'http://127.0.0.1:{self.worker.port}'
        async with ClientSession() as session:
            async with session.post(url, json=data) as response:
                result = {
                    'status': response.status,
                    'headers': response.headers,
                    'content': await response.text()
                }
                return result