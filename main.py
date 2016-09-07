# -*- coding: utf-8 -*-

from wox import Wox
from lunar import Lunar
from dateutil.parser import parse
import datetime
import os

week_day_dict = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期天',
}


class ChineseCalendar(Wox):
    def query(self, query):
        result = []
        try:
            if not query or query == "now":
                ln = Lunar()
            else:
                # 兼容时间戳，如 1473905472000
                if len(query.split(" ")) == 1 and len(query) == 12 or len(query) == 13:
                    try:
                        timenumber = float(query) / 1e3
                        query = str(datetime.datetime.fromtimestamp(timenumber))
                    except ValueError:
                        pass
                ln = Lunar(parse(query))
        except ValueError:
            result.append({
                "Title": 'Can not parse input string',
                "SubTitle": 'Please input standard date and time format strings',
                "IcoPath": "Images/app.png",
            })
        else:
            jieri = ln.ln_jie()  # 阳历节日
            date = ln.localtime.strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
            notime = False
            if date[11:] == "00:00:00":
                notime = True
            time1 = date[0: 11] if notime else date
            result.append({
                "Title": time1 + (' 【' + jieri + '】' if jieri else ""),
                "SubTitle": ln.localtime.strftime("%A") + " " + week_day_dict[ln.localtime.weekday()],
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "add_to_clipboard",
                    "parameters": [time1],
                    "dontHideAfterAction": False
                }
            })
            if datetime.datetime(1901, 1, 1) < ln.localtime:
                jieqi = ln.ln_jieqi()  # 节气
                jieri_lu = ln.ln_jie(True)  # 农历节日
                lutime1 = '{} {}'.format(ln.ln_date_str(), '【' + jieri_lu + '】' if jieri_lu else "")
                lutime2 = '【{}】 {}年-{}日{} {}'.format(ln.sx_year(), ln.gz_year(),
                                                     ln.gz_day(),
                                                     ("-" + ln.gz_hour() + "时") if not notime else "",
                                                     '  节气: ' + jieqi if jieqi else "")
                result.append({
                    "Title": lutime1,
                    "SubTitle": lutime2,
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": "add_to_clipboard",
                        "parameters": [lutime1],
                        "dontHideAfterAction": False
                    }
                })
        return result

    def add_to_clipboard(self, text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)


if __name__ == "__main__":
    ChineseCalendar()
