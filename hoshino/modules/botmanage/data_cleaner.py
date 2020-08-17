import hoshino
from hoshino.typing import CommandSession

@hoshino.sucmd('清理数据')
async def clean_image(session: CommandSession):
    await hoshino.get_bot().clean_data_dir(self_id=session.event.self_id,
                                           data_dir='image')
    await session.send('Image 文件夹已清理')

@hoshino.sucmd('清理日志')
async def clean_log(session: CommandSession):
    await hoshino.get_bot().clean_plugin_log_async(self_id=session.event.self_id)
    await session.send('插件日志文件已清理')
