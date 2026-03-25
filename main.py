import asyncio
import os
import datetime
from dotenv import load_dotenv
from garth import Client

load_dotenv()

CN_USER = os.getenv("GARMIN_CN_USERNAME")
CN_PASS = os.getenv("GARMIN_CN_PASSWORD")
GLOBAL_USER = os.getenv("GARMIN_GLOBAL_USERNAME")
GLOBAL_PASS = os.getenv("GARMIN_GLOBAL_PASSWORD")
SYNC_INTERVAL = int(os.getenv("SYNC_INTERVAL", 1800))
SYNC_HEALTH = os.getenv("SYNC_HEALTH", "true").lower() == "true"
SYNC_ACTIVITIES = os.getenv("SYNC_ACTIVITIES", "true").lower() == "true"

async def sync_garmin():
    print("=====================================")
    print(f"同步时间：{datetime.datetime.now()}")
    print("=====================================")

    print("正在登录佳明国服...")
    cn = Client()
    await cn.login(CN_USER, CN_PASS, region="CN")

    print("正在登录佳明国际服...")
    gl = Client()
    await gl.login(GLOBAL_USER, GLOBAL_PASS, region="US")

    print("✅ 双区登录成功！")

    if SYNC_HEALTH:
        print("🔄 同步健康数据...")
        try:
            today = datetime.date.today()
            data = await cn.get_health_data(today)
            await gl.upload_health_data(data)
            print("✅ 健康数据同步完成")
        except Exception as e:
            print(f"⚠️ 健康数据失败：{e}")

    if SYNC_ACTIVITIES:
        print("🔄 同步运动记录...")
        try:
            acts = await cn.get_activities(limit=20)
            for act in acts:
                await gl.upload_activity(act)
            print("✅ 运动数据同步完成")
        except Exception as e:
            print(f"⚠️ 运动数据失败：{e}")

    print("✅ 本次同步完成！\n")

async def main():
    while True:
        try:
            await sync_garmin()
        except Exception as e:
            print(f"❌ 错误：{e}")
        await asyncio.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
