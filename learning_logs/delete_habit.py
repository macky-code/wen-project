# delete_habit.py
# delete_habit.py
import os
import django

# 设置 Django 环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")
django.setup()

from learning_logs.models import Habit, HabitLog, HabitCheckin


def delete_habit_and_related(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        print(f"❌ 未找到 ID 为 {habit_id} 的 Habit")
        return

    print(f"⚠️ 即将删除 Habit：{habit.name}")
    confirm = input("是否确认删除？(y/n): ")
    if confirm.lower() != 'y':
        print("❌ 已取消删除")
        return

    # 删除相关日志和打卡记录
    logs_deleted = HabitLog.objects.filter(habit=habit).delete()
    checkins_deleted = HabitCheckin.objects.filter(habit=habit).delete()

    # 删除 Habit 本身
    habit.delete()

    print(f"✅ 已删除 Habit：{habit.name}")
    print(f"   - 删除了 {logs_deleted[0]} 条 HabitLog")
    print(f"   - 删除了 {checkins_deleted[0]} 条 HabitCheckin")


# 示例调用：根据实际 Habit 的 ID 替换下面的数字
if __name__ == "__main__":
    try:
        habit_id = int(input("请输入要删除的 Habit ID: "))
        delete_habit_and_related(habit_id)
    except ValueError:
        print("❌ 请输入有效的数字 ID")

