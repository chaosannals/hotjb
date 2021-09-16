from time import time_ns
from asyncio import sleep
from aiohttp import web, ClientSession
from loguru import logger
from .worker import HotJBWorker
from .transfer import HotJBTransfer

class HotJBServer:
    '''
    分发服务端服务
    '''

    def __init__(self, worker_count=6, out_time=10.0):
        '''
        初始化，设置和生成 worker 池。
        '''

        self.app = web.Application()
        self.app.add_routes([
            web.post('/tokenize', self.tokenize)
        ])

        self.workers : list[HotJBWorker] = []
        for i in range(worker_count):
            worker = HotJBWorker(30001 + i)
            self.workers.append(worker)
            logger.info(f'{i} new worker {worker.port}')

        self.out_time = out_time

    def ready(self):
        '''
        预备，初始化 worker 。
        '''

        for i, worker in enumerate(self.workers):
            worker.attach()
            logger.info(f'{i} worker {worker.port} attach')
        return self
        

    def close(self):
        '''
        关闭，回收 worker 。
        '''

        for i, worker in enumerate(self.workers):
            worker.detach()
            logger.info(f'{i} worker {worker.port} detach')

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

    async def dispatch(self) -> HotJBTransfer:
        '''
        '''

        start_time = time_ns()
        while True:
            for worker in self.workers:
                if worker.idle:
                    end_time = time_ns()
                    duration = (end_time - start_time) / 1000000000.0
                    logger.info(f'transfer {duration:.5f}s: {worker.port}')
                    return HotJBTransfer(worker)
            end_time = time_ns()
            duration = (end_time - start_time) / 1000000000.0
            if duration > self.out_time:
                break
            await sleep(0.01)
        return None

    async def tokenize(self, request):
        '''
        请求处理，分配 worker 并转发。
        '''

        with await self.dispatch() as t:
            if t != None:
                data = await request.json()
                r = await t.transfer(data)
                return web.Response(
                    status=r['status'],
                    headers=r['headers'],
                    body = r['content'],
                )

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
    
