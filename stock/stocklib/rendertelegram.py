import telegram

from .calstockasset import CalStockAsset
from .render import Render


# for Telegram 
BOT_TOKEN = '1406855830:AAHxMrhLzNtKK8veSbxkAF2c9E3WH6clXkY'
TELE_ME = '1404750626'


class RenderTelegram(Render):
    """ send text result to telegram (to predefined destination)
    """

    def __init__(self, calstockasset, opt=None):
        self.calstockasset = calstockasset
        self.mybot = telegram.Bot(token = BOT_TOKEN)

    def draw(self):
        """
            {'total': {'cur_val': 6302.3115, 'gap_from_init': 567.6899,
            'gap_prev': 19.71149999999993, 'init_val': 5734.6215999999995}, 
            'a': {'cur_val': 3662.72, 'gap_from_init': 80.1094, 
            'gap_prev': 2.2099999999999227, 'init_val': 3582.6106},
            'b': {'cur_val': 2639.5915, 'gap_from_init': 487.5805000000001,
            'gap_prev': 17.501500000000007, 'init_val': 2152.011}}
            ----------------
            dict_keys(['total', 'a', 'b'])
        """
        summary = self.calstockasset.get_summary()

        msg = ''
        for grp in ['total', 'a', 'b']:
            grp_val = summary[grp]
            msg_sub = '{}({}) : {}({}%)   <- {}({}%)'.format(
                grp.upper()[0],
                int(grp_val['cur_val']),
                int(grp_val['gap_from_init']),
                round(grp_val['gap_from_init']*100/grp_val['init_val'], 1),
                int(grp_val['gap_prev']),
                round(grp_val['gap_prev']*100 / (grp_val['cur_val']-grp_val['gap_prev']), 1)
            )
            msg += (msg_sub + '\n')
            if grp == 'total':
                msg += '---------------------------------------------------------\n'

        print(msg)
        self.mybot.sendMessage(TELE_ME, msg)



