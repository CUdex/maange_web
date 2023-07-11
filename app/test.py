import asyncio
import awsTools

async def run_functions():
    # 비동기 함수들을 await하여 실행
    results = []
    results = await asyncio.gather(awsTools.getInstance(), awsTools.getVpc())

    return results

async def main():
    task = asyncio.create_task(run_functions())
    print('1111')
    await task
    print('end')
    

asyncio.run(main())