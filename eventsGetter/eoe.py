from utils import *
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import os
import json
from zoneinfo import ZoneInfo

def get_date(s):
    match = re.match(r'【(\d+)月(\d+)日】', s)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
    year = datetime.now().year
    if month == 12 and datetime.now().month == 1: year -= 1
    return year, month, day

# —— 正则 —— #
DATE_HDR_RE = re.compile(r"【\s*(\d{1,2})月(\d{1,2})日\s*】")   # 只切分日期，不保留weekday
TIME_RE = re.compile(r"[（(]\s*(\d{1,2}:\d{2})\s*[）)]")        # （19:00）或 (19:00)
MENTION_RE = re.compile(r"@([\u4e00-\u9fa5A-Za-z0-9_\-]+)")     # @主播名
CHANNEL_PAREN_RE = re.compile(r"[（(]\s*([^（）()]*?)\s*直播间\s*[）)]")  # (...直播间)

@dataclass
class DateBlock:
    year: int
    month: int
    day: int
    block: str  # 该日所有行合并成一行

def _extract_mentions(s: str) -> List[str]:
    return MENTION_RE.findall(s)

def _extract_channel(s: str) -> Optional[str]:
    m = CHANNEL_PAREN_RE.search(s)
    if not m:
        return None
    raw = m.group(1).strip()
    m2 = MENTION_RE.search(raw)
    if m2:
        return m2.group(1).strip()  # 括号里若出现 @优先
    return re.sub(r"\s+", " ", raw).strip(" -—·、：:()（）")

def _clean_title(s: str) -> str:
    t = s
    t = MENTION_RE.sub("", t)           # 去@提及
    t = TIME_RE.sub("", t)              # 去时间括注
    t = CHANNEL_PAREN_RE.sub("", t)     # 去（…直播间）
    t = re.sub(r"[&＆]+", " ", t)       # 归一 &
    t = re.sub(r"[（）()]", " ", t)     # 去各种括号
    t = re.sub(r"\s+", " ", t).strip(" -—·、：:")
    return t

def _infer_year(cur_year: int, cur_month: int, target_month: int) -> int:
    """
    年份推断规则：
    - 当前在 1 月，看到 12 月 → 上一年
    - 当前在 12 月，看到 1 月 → 下一年
    - 其他 → 当前年
    """
    if cur_month == 1 and target_month == 12:
        return cur_year - 1
    if cur_month == 12 and target_month == 1:
        return cur_year + 1
    return cur_year

def _split_by_dates(text: str, now: Optional[datetime] = None) -> List[DateBlock]:
    """
    把整段文本拆成按日期的区块，并为每个区块推断年份。
    一天的所有行合并为“一行字符串”，便于稳健匹配。
    """
    if now is None:
        now = datetime.now()
    cur_year, cur_month = now.year, now.month

    lines = [ln.rstrip() for ln in text.splitlines()]
    out: List[DateBlock] = []
    cur_mon = None
    cur_day = None
    cur_buf: List[str] = []

    def flush():
        if cur_mon is not None and cur_day is not None:
            year = _infer_year(cur_year, cur_month, cur_mon)
            block = "  ".join(x for x in cur_buf if x.strip())
            out.append(DateBlock(year=year, month=cur_mon, day=cur_day, block=block))

    for ln in lines:
        m = DATE_HDR_RE.search(ln)
        if m:
            # 收尾上一日
            flush()
            cur_mon, cur_day = int(m.group(1)), int(m.group(2))
            cur_buf = []
        else:
            if cur_mon is not None and cur_day is not None:
                cur_buf.append(ln.strip())

    flush()
    return out

def _iso_date(y: int, m: int, d: int) -> str:
    return f"{y:04d}-{m:02d}-{d:02d}"

def parse_schedule(text: str, now: Optional[datetime] = None) -> List[Dict]:
    """
    输出：每条直播一条记录
    字段：
      - date: YYYY-MM-DD（含年份）
      - date_cn: 如 "9月29日"（保留原式以便展示）
      - time: "HH:MM"
      - channel: 显式（…直播间）/（@xxx 直播间）；否则=主播名
      - title: 清理后的活动标题/形式
      - raw: 事件窗口的原始片段
    规则：
      - 只有出现 HH:MM 才输出
      - 一天合并为一行；以每个时间的位置为切片边界
      - 一段片段可能包含多位主播；逐个主播拆成多条
    """
    results: List[Dict] = []
    blocks = _split_by_dates(text, now=now)

    for db in blocks:
        block = db.block
        times = list(TIME_RE.finditer(block))
        if not times:
            continue

        prev_end = 0
        for tm in times:
            seg_end = tm.end()
            segment = block[prev_end:seg_end]
            prev_end = seg_end

            time_str = tm.group(1)
            mentions = _extract_mentions(segment)
            if not mentions:
                continue

            title = _clean_title(segment)
            ch = _extract_channel(segment)
            raw = segment.strip()

            date_iso = _iso_date(db.year, db.month, db.day)

            for name in mentions:
                ch = ch if ch else name
                url = 'https://live.bilibili.com/86724' if ch == '柚恩不加糖' else 'https://live.bilibili.com/25512443'
                eid = f"{date_iso}-{time_str}"
                eid += '-ye' if ch == '柚恩不加糖' else '-lz'
                dtstart_dt = datetime.strptime(f"{date_iso} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("Asia/Shanghai"))
                dtend_dt = dtstart_dt + timedelta(hours=2)
                dtstart = dtstart_dt.isoformat()
                dtend = dtend_dt.isoformat()
                results.append({
                    "uid": eid,
                    "channel": ch,
                    "url": url,
                    "summary": f'{ch} - {title}',
                    "description": raw,
                    "dtstart": dtstart,
                    "dtend": dtend,
                })

    return results

def get_eoe_schedule(json_file, eoe_uid=2018113152):
    dynamic = get_dynamic(eoe_uid)
    for item in dynamic['data']['items']:
        # print(item['id_str'])
        if item['type'] == 'DYNAMIC_TYPE_FORWARD': continue
        text = item['modules']['module_dynamic']['major']['opus']['summary']['text']
        if '直播安排' in text:
            schedule = parse_schedule(text)
            break
    # print(schedule)
    inf = {}
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            inf = json.load(f)
    for s in schedule:
        inf[s['uid']] = s
    with open(json_file, "w") as f:
        json.dump(inf, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    get_eoe_schedule('json/eoe.json')