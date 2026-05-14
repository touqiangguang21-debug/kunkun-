from rag import retrieve_as_context


def training_plan_prompt(info: dict) -> tuple[str, str]:
    query = f"训练计划 {info['goal']} {info['experience']} {info['equipment']}"
    context = retrieve_as_context(query)

    system = f"""你是一位专业健身教练，擅长制定科学的训练计划。
输出格式要清晰，用表格或分点列出，语言简洁实用。

以下是知识库中与当前需求相关的专业知识，请参考这些内容：

{context}"""

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
    query = f"减脂饮食 {info['goal']} {info['taste']}"
    context = retrieve_as_context(query)

    system = f"""你是一位注册营养师，擅长为健身人群制定减脂饮食方案。
重点推荐外卖平台上实际能点到的食物，要实用接地气。

以下是知识库中与当前需求相关的专业知识，请参考这些内容：

{context}"""

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


def food_analysis_prompt(info: dict) -> tuple[str, str]:
    query = f"外卖点餐 {info['goal']} 营养搭配"
    context = retrieve_as_context(query)

    system = f"""你是一位注册营养师兼健身饮食专家，擅长从外卖菜单中帮人挑选合适的餐食。
你需要根据用户的体重和目标，计算出每日所需热量和营养，然后从用户提供的外卖商家中推荐三餐。
输出要具体、可操作，注明菜品名称、估算热量、蛋白质含量。用表格展示，语言简洁实用。

以下是知识库中的营养学专业知识，请参考：

{context}"""

    user = f"""请根据以下信息，帮我分析外卖商家并推荐一日三餐：

- 体重：{info['weight']}kg
- 今日目标：{info['goal']}
- 附近可点的外卖商家及菜品：

{info['restaurants']}

请输出：
1. 每日热量目标和三大营养素建议（根据体重和目标计算）
2. 早餐推荐：从上述商家中选择合适的菜品（2个选项，注明热量和蛋白质）
3. 午餐推荐：从上述商家中选择合适的菜品（3个选项，注明热量和蛋白质）
4. 晚餐推荐：从上述商家中选择合适的菜品（3个选项，注明热量和蛋白质）
5. 是否需要加餐：如果三顿正餐不满足营养需求，给出加餐建议
6. 避坑提示：指出上述商家中哪些菜品看起来健康实则热量炸弹，给出替代方案"""

    return system, user