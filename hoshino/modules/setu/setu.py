import os
import random
import asyncio
import requests

from urllib.parse import urlparse

from nonebot.exceptions import CQHttpError

from hoshino import R, Service, priv
from hoshino.util import FreqLimiter, DailyNumberLimiter, fig2b64
from matplotlib import pyplot as plt

_max = 5
SETU_DISABLE_NOTICE = '本群涩图功能已禁用\n如欲开启，请与维护组联系'
EXCEED_NOTICE = f'您今天已经冲过{_max}次了，请明早5点后再来！'
_ncnt = DailyNumberLimiter(0)  # 记录调用次数
_nlmt = DailyNumberLimiter(_max)
_flmt = FreqLimiter(5)

sv = Service('setu', manage_priv=priv.SUPERUSER, enable_on_default=True, visible=False)
setu_folder = R.img('setu/').path
r18_setu_folder = R.img('setu_r18/').path

setu_aliases = ('涩图', '瑟图', '色图', '不够涩', '不够瑟', '不够色', '再来点', '再来份', '再来张', '看过了', '炼铜', '铜',
                '来点涩图', '来点瑟图', '来点色图', '来份涩图', '来份瑟图', '来份色图', '来张涩图', '来张瑟图', '来张色图',
                '来一点涩图', '来一点瑟图', '来一点色图', '来一份涩图', '来一份瑟图', '来一份色图', '来一张涩图', '来一张瑟图', '来一张色图',
                '来亿点涩图', '来亿点瑟图', '来亿点色图', '来亿份涩图', '来亿份瑟图', '来亿份色图', '来亿张涩图', '来亿张瑟图', '来亿张色图')

# 使用本地涩图库
def setu_gener():
    while True:
        filelist = os.listdir(setu_folder)
        random.shuffle(filelist)
        for filename in filelist:
            if os.path.isfile(os.path.join(setu_folder, filename)):
                yield R.img('setu/', filename)

setu_gener = setu_gener()

# 使用lolicon api
def setu_gener_online(R18=False, keyword=''):
    URL = 'https://api.lolicon.app/setu/'  
    PARAMS = {'apikey': '391107215ed359c98f4829', 'keyword':keyword, 'r18': int(R18)}  # size1200 is unavailable due to mysterious reasons
    res = requests.get(url = URL, params = PARAMS).json()
    if not res['code']:  # 获取图片成功
        img_meta = [res['data'][0][field] for field in ['pid', 'author', 'tags']]
        img_url = res['data'][0]['url']
        img1200_url = re.sub('(.+)/img-original/(.+)(\.\w+$)', r'\1/img-master/\2_master1200.jpg', img_url)
        img_name = os.path.basename(urlparse(img_url).path)
        if not R18:
            folder = setu_folder
            path = 'setu/'
        else:
            folder = r18_setu_folder
            path = 'setu_r18/'
        if os.path.isfile(os.path.join(folder, img_name)):  # 涩图已缓存
            return R.img(path, img_name), img_meta
        else:  # 涩图未缓存，开始下载
            for url in [img1200_url, img_url]:  # 尝试下载1200px版，如失败则下载原版
                resp = requests.get(url)
                if resp.status_code == 200:
                    img_data = resp.content
                    with open(os.path.join(folder, img_name), 'wb') as handler:
                        handler.write(img_data)
                    return R.img(path, img_name), img_meta
            raise CQHttpError()  # 获取图片失败
    else:
        raise CQHttpError()  # 获取图片失败

def get_setu(R18=False, keyword=''):
    # return setu_gener.__next__(), []
    return setu_gener_online(R18, keyword)

# 正则解析所有文本并响应

# @sv.on_rex(r'不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜')
# async def setu(bot, ev):
    # """随机叫一份涩图，对每个用户有冷却时间"""
    # uid = ev['user_id']
    # if not _nlmt.check(uid):
        # await bot.send(ev, EXCEED_NOTICE, at_sender=True)
        # return
    # if not _flmt.check(uid):
        # await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
        # return
    # _flmt.start_cd(uid)
    # _nlmt.increase(uid)

    # # conditions all ok, send a setu.
        
    # try:
        # await bot.send(ev, pic.cqcode)
    # except CQHttpError:
        # sv.logger.error(f"发送图片{pic.path}失败")
        # try:
            # await bot.send(ev, '涩图太涩，发不出去勒...')


# 以命令形式响应

@sv.on_command('setu', deny_tip=SETU_DISABLE_NOTICE, aliases=setu_aliases, only_to_me=True)
async def setu(bot, ev):
    """随机叫一份涩图，对每个用户有冷却时间"""
    uid = ev['user_id']
    _ncnt.check(uid)  # 刷新次数
    if uid not in bot.config.SUPERUSERS:
        if not _nlmt.check(uid):
            await bot.send(ev, EXCEED_NOTICE, at_sender=True)
            return
        if not _flmt.check(uid):
            await bot.send(ev, '您冲得太快了，请稍候再冲', at_sender=True)
            return
        pic, meta = get_setu(r18, kw)
        msg_id = (await bot.send(ev, f'{pic.cqcode}\nPid: {meta[0]}\tAuthor: {meta[1]}\nTags: {"; ".join(meta[2][1::2])}'))['message_id']
        self_id = ev['self_id']
        _flmt.start_cd(uid)
        _nlmt.increase(uid)
        _ncnt.increase(uid)
    except CQHttpError:
        sv.logger.error(f"发送图片失败")
        try:
            await bot.send(ev, '涩图太涩，发不出去啦……')
        except:
            pass

    if r18:
        await asyncio.sleep(10)
        await bot.delete_msg(self_id=self_id, message_id=msg_id)
        chieri = R.img('chieri2.jpg').cqcode
        await bot.send(ev, f'这张涩图太涩，不给你们看啦！\n{chieri}')


# setu.args_parser 装饰器将函数声明为 setu 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@setu.args_parser
async def _(session:CommandSession):
    stripped_arg = session.current_arg_text.strip()
    session.state['keyword'] = stripped_arg


@sv.on_command('涩图头子排行榜', aliases='色图头子排行榜', only_to_me=True)
async def setu_ranking(bot, ev):
    mstat = []
    mlist = (await bot.get_group_member_list(self_id=ev['self_id'], group_id=ev['group_id']))
    for m in mlist:
        if _ncnt.get_num(m['user_id']) and m['user_id'] not in bot.config.SUPERUSERS:
            mstat.append((m['nickname'], _ncnt.get_num(m['user_id'])))
    mstat.sort(key=lambda x: x[1], reverse=True)
    
    yn = len(mstat)
    if not yn:
        await bot.send(ev, f'今天的涩图头子还没有出现呢！大家继续加油哦～♪')
        return
    else:
        fig, ax = plt.subplots()
        name = list(map(lambda i: i[0], mstat))
        score = list(map(lambda i: i[1], mstat))
        y_pos = list(range(yn))

        y_size = 0.3 * yn + 1.0
        fig.set_size_inches(10, y_size)
        bars = ax.barh(y_pos, score, align='center')
        ax.set_title(f"本群涩图头子排行榜")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(name)
        ax.set_ylim((-0.6, yn - 0.4))
        ax.invert_yaxis()
        ax.set_xlabel('分数')
        ax.ticklabel_format(axis='x', style='plain')
        for rect in bars:
            w = rect.get_width()
            ax.text(w, rect.get_y() + rect.get_height() / 2, f'{w:d}', ha='left', va='center')
        plt.subplots_adjust(left=0.12, right=0.96, top=1 - 0.35 / y_size, bottom=0.55 / y_size)
        pic = fig2b64(plt)
        plt.close()

        await bot.send(ev, MessageSegment.image(pic), at_sender=True)


@sv.on_rex(r'^来瓶营养快线$', normalize=False)
async def energize(bot, ev):
    if ev['user_id'] not in bot.config.SUPERUSERS:
        await bot.send(ev, R.img('都可以但是要先给钱.jpg').cqcode)
        return
    count = 0
    for m in ev['message']:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = int(m.data['qq'])
            _nlmt.reset(uid)
            count += 1
    if count:
        await bot.send(ev, f"已为{count}位用户送出营养快线一瓶！记得不要冲得太快哦～")

