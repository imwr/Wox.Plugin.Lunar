# -*- coding: utf-8 -*-

from wox import Wox
from lunar import Lunar
from dateutil.parser import parse


class ChineseCalendar(Wox):
    def query(self, query):
        result = []
        try:
            if not query:
                ln = Lunar()
            else:
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
                "SubTitle": '{} 【{}年-{}-{}日{}】{} {}'.format(ln.ln_date_str(), ln.sx_year(), ln.gz_year(), 
                                                                ln.gz_day(),
                                                                ("-" + ln.gz_hour() + "时") if not notime else "",
                                                                '【' + jieqi + '】' if jieqi else "",
                                                                '【' + jieri_lu + '】' if jieri_lu else ""),
                "IcoPath": "Images/app.png",
            })

            return result


if __name__ == "__main__":
    ChineseCalendar()