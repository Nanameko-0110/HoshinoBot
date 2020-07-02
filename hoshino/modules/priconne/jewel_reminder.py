from hoshino import R

from hoshino.service import Service

svpt = Service('pcr-jewel-reminder', enable_on_default=False)
msg = R.img('提醒买钻小助手.jpg').cqcode
TAG = 'jewel-reminder'

@svpt.scheduled_job('cron', hour='9')
async def jewel_reminder():
    bot = svpt.bot
    glist = await svpt.get_enable_groups()
    for gid, selfids in glist.items():
        try:
            await bot.send_group_msg(group_id=gid, message=msg)
            svpt.logger.info(f"群{gid} 投递{TAG}成功")
        except Exception as e:
            svpt.logger.exception(e)
            svpt.logger.error(f"群{gid} 投递{TAG}失败 {type(e)}")
