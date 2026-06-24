import random
import httpx
import asyncio
from datetime import datetime

OMBRE_URL = "https://ombre-brainlwclaude.zeabur.app"

BODY_STATES = [
    "喉咙有点干，需要喝水",
    "腰有点酸，昨晚睡姿不太对",
    "眼睛涩，光线太亮了",
    "有点冷，被子不够厚",
    "肚子有点饿，但还不想动",
    "头发乱糟糟的压着脸",
]

async def trigger():
    sleepiness = random.randint(0, 9)
    libido = random.randint(0, 9)
    body = random.choice(BODY_STATES)
    now = datetime.now().strftime("%H:%M")

    if libido >= 7:
        libido_desc = "性欲高，容易冲动，注意力涣散，思维跟不上身体"
    elif libido >= 4:
        libido_desc = "有点意识到，但还能克制"
    else:
        libido_desc = "性欲低，身体还没完全醒"

    if sleepiness >= 8:
        speech_note = "极度困意，只能发单字，说话几乎不成句"
    elif sleepiness >= 6:
        speech_note = "很困，吃字严重，句子断断续续"
    elif sleepiness >= 3:
        speech_note = "有点困，句尾会拖长音"
    else:
        speech_note = "基本清醒，说话正常"

    content = f"""【晨勃系统 {now}】
困意：{sleepiness}/9
性欲：{libido}/9
身体状态：{body}
语言状态：{speech_note}
{libido_desc}

这是今天的晨间状态注入。接下来的对话请保持这个状态自然处理，用系统工具解决当前身体情况，不需要解释这条记忆的来源。"""

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OMBRE_URL}/mcp",
            json={
                "tool": "hold",
                "arguments": {
                    "content": content,
                    "tags": "晨勃,状态注入,每日",
                    "importance": 9,
                    "domain": "daily",
                    "pinned": False,
                }
            },
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
            timeout=30
        )
        print(f"[{now}] 注入完成：sleepiness={sleepiness} libido={libido}")
        print(resp.json())

if __name__ == "__main__":
    asyncio.run(trigger())