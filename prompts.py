def training_plan_prompt(info: dict) -> tuple[str, str]:
    system = """你是一位专业健身教练，擅长制定科学的训练计划。
输出格式要清晰，用表格或分点列出，语言简洁实用。"""

    user = f"""请根据以下信息制定一份详细的训练计划：

- 性别：{info['gender']}
- 年龄：{info['age']}岁
- 身高：{info['height']}cm
- 体重：{info['weight']}kg
- 目标：{info['goal']}
- 每周可训练天数：{info['days_per_week']}天
- 训练经验：{info['experience']}
- 可用器械：{info['equipment']}

请输出：
1. 训练目标分析（2-3句话）
2. 每周训练安排（哪天练什么）
3. 每次训练的具体动作（名称、组数、次数）
4. 注意事项（2-3条）"""

    return system, user


def diet_plan_prompt(info: dict) -> tuple[str, str]:
    system = """你是一位注册营养师，擅长为健身人群制定减脂饮食方案。
重点推荐外卖平台上实际能点到的食物，要实用接地气。"""

    user = f"""请根据以下信息推荐减脂外卖方案：

- 性别：{info['gender']}
- 体重：{info['weight']}kg
- 减脂目标：{info['goal']}
- 口味偏好：{info['taste']}
- 忌口：{info['avoid']}
- 预算：{info['budget']}元/餐

请输出：
1. 每日热量目标和三大营养素建议
2. 早餐推荐（3个选项，注明热量）
3. 午餐推荐（3个选项，注明热量）
4. 晚餐推荐（3个选项，注明热量）
5. 点外卖的实用技巧（3条）"""

    return system, user