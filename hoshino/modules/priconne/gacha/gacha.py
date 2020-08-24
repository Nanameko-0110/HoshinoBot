import random

from hoshino import util
from .. import chara


class Gacha(object):

    def __init__(self, pool_name:str = "MIX"):
        super().__init__()
        self.load_pool(pool_name)


    def load_pool(self, pool_name:str):
        config = util.load_config(__file__)
        pool = config[pool_name]
<<<<<<< HEAD
        self.up3_prob = pool["up3_prob"]
        self.up2_prob = pool["up2_prob"]
        self.up2_prob_l = pool["up2_prob_l"]  # 保底第10抽二星概率
        self.up1_prob = pool["up1_prob"]
        self.s3_prob = pool["s3_prob"]
        self.s2_prob = pool["s2_prob"]
        self.s1_prob = 1000 - self.s2_prob - self.s3_prob
        self.up3 = pool["up3"]
        self.up2 = pool["up2"]
        self.up1 = pool["up1"]
=======
        self.up_prob = pool["up_prob"]
        self.s3_prob = pool["s3_prob"]
        self.s2_prob = pool["s2_prob"]
        self.s1_prob = 1000 - self.s2_prob - self.s3_prob
        self.up = pool["up"]
>>>>>>> upstream/master
        self.star3 = pool["star3"]
        self.star2 = pool["star2"]
        self.star1 = pool["star1"]


<<<<<<< HEAD
    def gacha_one(self, up3_prob:int, up2_prob:int, up1_prob:int, s3_prob:int, s2_prob:int, s1_prob:int=None):
        '''
        sx_prob: x星概率，要求和为1000
        upx_prob: x星UP角色概率（从x星划出）
        up_chara: UP角色名列表

        return: (单抽结果:chara, 秘石数:int)
=======
    def gacha_one(self, up_prob:int, s3_prob:int, s2_prob:int, s1_prob:int = None):
        '''
        sx_prob: x星概率，要求和为1000
        up_prob: UP角色概率（从3星划出）
        up_chara: UP角色名列表

        return: (单抽结果:Chara, 秘石数:int)
>>>>>>> upstream/master
        ---------------------------
        |up|      |  20  |   78   |
        |   ***   |  **  |    *   |
        ---------------------------
        '''
        if s1_prob is None:
            s1_prob = 1000 - s3_prob - s2_prob
        total_ = s3_prob + s2_prob + s1_prob
        pick = random.randint(1, total_)
<<<<<<< HEAD
        if pick <= up3_prob:
            return chara.fromname(random.choice(self.up3), 3), 100
        elif pick <= s3_prob:
            return chara.fromname(random.choice(self.star3), 3), 50
        elif pick <= up2_prob + s3_prob:
            return chara.fromname(random.choice(self.up2), 2), 10
        elif pick <= s2_prob + s3_prob:
            return chara.fromname(random.choice(self.star2), 2), 10
        elif pick <= up1_prob + s2_prob + s3_prob:
            return chara.fromname(random.choice(self.up1), 1), 1
=======
        if pick <= up_prob:
            return chara.fromname(random.choice(self.up), 3), 100
        elif pick <= s3_prob:
            return chara.fromname(random.choice(self.star3), 3), 50
        elif pick <= s2_prob + s3_prob:
            return chara.fromname(random.choice(self.star2), 2), 10
>>>>>>> upstream/master
        else:
            return chara.fromname(random.choice(self.star1), 1), 1


    def gacha_ten(self):
        result = []
        hiishi = 0
<<<<<<< HEAD
        up3 = self.up3_prob
        up2 = self.up2_prob
        up2_l = self.up2_prob_l
        up1 = self.up1_prob
=======
        up = self.up_prob
>>>>>>> upstream/master
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for _ in range(9):    # 前9连
<<<<<<< HEAD
            c, y = self.gacha_one(up3, up2, up1, s3, s2, s1)
            result.append(c)
            hiishi += y
        c, y = self.gacha_one(up3, up2_l, 0, s3, s2 + s1, 0)    # 保底第10抽
=======
            c, y = self.gacha_one(up, s3, s2, s1)
            result.append(c)
            hiishi += y
        c, y = self.gacha_one(up, s3, s2 + s1, 0)    # 保底第10抽
>>>>>>> upstream/master
        result.append(c)
        hiishi += y

        return result, hiishi


    def gacha_tenjou(self):
<<<<<<< HEAD
        result = {'up3': [], 's3': [], 's2':[], 's1':[]}
        first_up_pos = 999999
        up3 = self.up3_prob
        up2 = self.up2_prob
        up2_l = self.up2_prob_l
        up1 = self.up1_prob
=======
        result = {'up': [], 's3': [], 's2':[], 's1':[]}
        first_up_pos = 999999
        up = self.up_prob
>>>>>>> upstream/master
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for i in range(9 * 30):
<<<<<<< HEAD
            c, y = self.gacha_one(up3, up2, up1, s3, s2, s1)
            if 100 == y:
                result['up3'].append(c)
=======
            c, y = self.gacha_one(up, s3, s2, s1)
            if 100 == y:
                result['up'].append(c)
>>>>>>> upstream/master
                first_up_pos = min(first_up_pos, 10 * ((i+1) // 9) + ((i+1) % 9))
            elif 50 == y:
                result['s3'].append(c)
            elif 10 == y:
                result['s2'].append(c)
            elif 1 == y:
                result['s1'].append(c)
            else:
                pass    # should never reach here
        for i in range(30):
<<<<<<< HEAD
            c, y = self.gacha_one(up3, up2_l, 0, s3, s2 + s1, 0)
            if 100 == y:
                result['up3'].append(c)
=======
            c, y = self.gacha_one(up, s3, s2 + s1, 0)
            if 100 == y:
                result['up'].append(c)
>>>>>>> upstream/master
                first_up_pos = min(first_up_pos, 10 * (i+1))
            elif 50 == y:
                result['s3'].append(c)
            elif 10 == y:
                result['s2'].append(c)
            else:
                pass    # should never reach here
        result['first_up_pos'] = first_up_pos
        return result
