# -*- coding: utf-8 -*-

from nonebot import *
from . import polymerization
from hoshino import R, Service, priv, util
import hoshino
from hoshino.typing import CQEvent, CQHttpError, Message

bot = get_bot()

sv = Service('圣杯战争', help_='''
我也不知道咋用
'''.strip(), bundle='pcr娱乐')


@sv.on_message("group")
async def entranceFunction(bot, ev: CQEvent):
    msg = str(ev.message)
    userQQ = ev.user_id
    userGroup = ev.group_id
    rawMsg = ev.message
    await polymerization.aggregationCall(bot, userQQ, userGroup, msg, rawMsg)
