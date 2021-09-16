import os
import asyncio
from loguru import logger
from dotenv import load_dotenv
from hotjb.server import HotJBServer

async def main(loop):
    '''
    主函数。
    '''

    debug = os.getenv('HOTJB_DEBUG', False)
    host = os.getenv('HOTJB_HOST', '0.0.0.0')
    port = os.getenv('HOTJB_PORT', 30000)
    worker_count = os.getenv('HOTJB_WORKER_COUNT', 5)
    logger.add(
        'runtime/logs/{time}.log',
        level='TRACE' if debug else 'INFO',
        rotation='00:00',
        retention='7 days',
    )
    logger.info(f'server: {host}:{port}')
    server = HotJBServer(worker_count)
    server.ready()
    await server.serve(loop, host, port)
    return server

if __name__ == '__main__':
    try:
        load_dotenv()
        loop = asyncio.get_event_loop()
        server = loop.run_until_complete(main(loop))
        loop.run_forever()
    except KeyboardInterrupt as e:
        logger.info('keyboard interrupt')
    except Exception as e:
        logger.error(e)
    finally:
        if server != None:
            server.close()