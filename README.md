# AI 健身助手

基于大语言模型的智能健身与饮食规划应用，支持个性化训练计划生成、减脂外卖推荐以及多轮对话追问，已部署上线可在线体验。

## 在线体验

🔗 **[fitness-ai.streamlit.app](https://c6yuhevxb6wpy5v2c24gq6.streamlit.app)**

## 功能介绍

- **个性化训练计划** — 根据性别、年龄、身高体重、训练目标、训练经验及可用器械，由 AI 生成详尽的周训练计划，包含每日动作、组数次数及注意事项
- **减脂外卖推荐** — 结合口味偏好、忌口和预算，AI 推荐实际外卖平台可点到的减脂餐食，标注热量和营养素
- **多轮追问对话** — 生成计划后可持续追问（如"第一天动作怎么做标准"），AI 基于完整上下文给出针对性解答，体验类似健身私教
- **双标签页设计** — 训练与饮食分栏切换，交互清晰，一页搞定

## 技术栈

- **前端** — Streamlit（Python Web 框架，声明式 UI）
- **AI 引擎** — DeepSeek Chat API（OpenAI 兼容接口）
- **对话管理** — 基于 Session State 的多轮对话历史，保持上下文连贯
- **提示工程** — 预设专业健身教练 / 注册营养师角色 System Prompt，结构化输出
- **部署** — Streamlit Cloud，环境变量管理 API Key

## 本地运行

```bash
git clone https://github.com/touqiangguang21-debug/kunkun-.git
cd kunkun-
pip install -r requirements.txt
```

创建 `.env` 文件，填入你的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=your_api_key_here
```

启动应用：

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501` 即可使用。
