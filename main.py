# -*- coding: utf-8 -*-

from wox import Wox
from lunar import Lunar
from dateutil.parser import parse
import datetime


class ChineseCalendar(Wox):
    def query(self, query):
        result = []
        try:
            if not query:
                ln = Lunar()
            else:
                # 兼容纯long时间，如 1473905472000
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
                "SubTitle": 'Please read the docs',
                "IcoPath": "Images/app.png",
            })
        else:
            jieqi = ln.ln_jieqi()
            jieri_lu = ln.ln_jie(True)
            jieri = ln.ln_jie()
            date = ln.localtime.strftime('%Y-%m-%d %H:%M:%S')
            notime = False
            if date[11:] == "00:00:00":
                notime = True
            result.append({
                "Title": '时间 {} {}'.format(date[0: 11] if notime else date,
                                           '【' + jieri + '】' if jieri else ""),
                "SubTitle": '【{}年】 {} 【{}年-{}日{}】{} {}'.format(ln.sx_year(), ln.ln_date_str(), ln.gz_year(),
                                                               ln.gz_day(),
                                                               ("-" + ln.gz_hour() + "时") if not notime else "",
                                                               '【' + jieqi + '】' if jieqi else "",
                                                               '【' + jieri_lu + '】' if jieri_lu else ""),
                "IcoPath": "Images/app.png",
            })
            return result


if __name__ == "__main__":
    ChineseCalendar()
