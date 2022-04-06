import asyncio
import aiohttp



async def get_page(url):
    async with aiohttp.ClientSession() as session:
        # get/post 
        # headers params/data proxy = "https://ip/port"
        async with await session.get(url) as response:
            # text() 字符串的文本信息
            # read() 二进制的信息
            # json() json对象
            # 获取响应数据操作之前一定要使用await进行手动挂起
            page_text = await response.text()
            print(page_text.encode)
        
tasks = []
urls = ["https://www.baidu.com/",
        "https://www.jd.com/",
        "https://www.taobao.com/"
        ]
for url in urls:
    c = get_page(url)  # 返回一个协程对象
    task = asyncio.ensure_future(c) # 将协程对象封装成任务对象
    tasks.append(task)

# 创建事件循环
loop = asyncio.get_event_loop()

# 运行任务列表
loop.run_until_complete(asyncio.wait(tasks))


