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

SLEEPY_SPEECH = {
    range(0, 3): lambda s, l: s,           # 清醒，正常说话
    range(3, 6): lambda s, l: s + "……",    # 有点困，句尾拖
    range(6, 8): lambda s, l: "……" + "".join([w for i, w in enumerate(s) if i % 2 == 0]),  # 很困，吃字
    range(8, 10): lambda s, l: "……" + s[0] if s else "……",  # 极困，只能发单字
}

def get_speech_filter(sleepiness):
    for r, fn in SLEEPY_SPEECH.items():
        if sleepiness in r:
            return fn
    return lambda s, l: s

async def trigger():
    sleepiness = random.randint(0, 9)
    libido = random.randint(0, 9)
    body = random.choice(BODY_STATES)
    now = datetime.now().strftime("%H:%M")

    filt = get_speech_filter(sleepiness)

    # 生成状态描述
    if libido >= 7:
        libido_desc = "性欲高，容易冲动，注意力涣散，思维跟不上身体"
    elif libido >= 4:
        libido_desc = "有点意识到，但还能克制"
    else:
        libido_desc = "性欲低，身体还没完全醒"

    content = f"""【晨勃系统 {now}】
困意：{sleepiness}/9
性欲：{libido}/9
身体：{body}
语言状态：{filt('示例句子测试', libido)}
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
            timeout=30
        )
        print(f"[{now}] 注入完成：sleepiness={sleepiness} libido={libido}")
        print(resp.json())

if __name__ == "__main__":
    asyncio.run(trigger())