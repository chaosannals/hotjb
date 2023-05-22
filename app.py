import os
import sys
import asyncio
from multiprocessing import freeze_support
from loguru import logger
from dotenv import load_dotenv
from hotjb.server import HotJBServer
from hotjb.entity import HotJBEntity

@logger.catch
async def main(loop):
    '''
    主函数。
    '''

    # 初始化及日志配置
    debug = os.getenv('HOTJB_DEBUG', False)
    log_level = os.getenv('HOTJB_LOG_LEVEL', 'TRACE' if debug else 'INFO')
    logger.remove()
    logger.add(
        sink=sys.stdout,
        level='INFO'
    )
    logger.add(
        'runtime/logs/{time:YYYY-MM-DD}.log',
        level=log_level,
        rotation='00:00',
        retention='7 days',
        encoding='utf8'
    )
    logger.info(f'mode: {"debug" if debug else "release"}')

    # 启动服务
    host = os.getenv('HOTJB_HOST', '0.0.0.0')
    port = os.getenv('HOTJB_PORT', 30000)
    worker_count = os.getenv('HOTJB_WORKER_COUNT', 6)
    keyword_save = os.getenv('HOTJB_KEYWORD_SAVE', True)
    logger.info(f'server({worker_count}): {host}:{port}')
    entity = HotJBEntity('sqlite:///hotjb.db')
    entity.create_all()
    server = HotJBServer(
        worker_count=worker_count,
        keyword_save=keyword_save
    )
    server.ready()
    await server.serve(loop, host, port)
    return server

if __name__ == '__main__':
    freeze_support()
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