from asyncio import sleep
from aiohttp import web, ClientSession
from loguru import logger
from .worker import HotJBWorker

class HotJBServer:
    '''
    分发服务端服务
    '''

    def __init__(self, worker_count=6):
        '''
        初始化，设置和生成 worker 池。
        '''

        self.app = web.Application()
        self.app.add_routes([
            web.post('/tokenize', self.tokenize)
        ])

        self.workers = []
        for i in range(worker_count):
            worker = HotJBWorker(30001 + i)
            self.workers.append(worker)
            logger.debug(f'new worker {i}')

    def ready(self):
        '''
        预备，初始化 worker 。
        '''

        for i, worker in enumerate(self.workers):
            worker.attach()
            logger.debug(f'worker {i} attach')
        return self
        

    def close(self):
        '''
        关闭，回收 worker 。
        '''

        for worker in self.workers:
            worker.detach()
            logger.debug(f'worker {worker.port} detach')

    async def transfer(self, port, data):
        '''
        转发请求到 worker 并返回结果。
        '''
        
        url = f'http://127.0.0.1:{port}'
        async with ClientSession() as session:
            async with session.post(url, json=data) as response:
                result = {
                    'status': response.status,
                    'headers': response.headers,
                    'content': await response.text()
                }
                return result

    def dispatch(self):
        '''
        调度获取 worker
        '''

    async def tokenize(self, request):
        '''
        请求处理，分配 worker 并转发。
        '''

        for i in range(100):
            for worker in self.workers:
                if worker.idle:
                    worker.idle = False
                    data = await request.json()
                    logger.debug(f'transfer: {worker.port}')
                    r = await self.transfer(worker.port, data)
                    worker.idle = True
                    return web.Response(
                        status=r['status'],
                        headers=r['headers'],
                        body = r['content'],
                    )
            await sleep(0.1)
            logger.warning(f'busy: {i}')
        logger.warning(f'busy timeout')
        return web.Response(
            status=500,
            text="server busy"
        )
        

    async def serve(self, loop, host, port):
        '''
        创建异步 HTTP 服务。
        '''
        
        return await loop.create_server(
            self.app.make_handler(),
            host=host,
            port=port
        )
    
