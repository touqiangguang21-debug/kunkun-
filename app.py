import streamlit as st
from llm import chat
from prompts import training_plan_prompt, diet_plan_prompt

st.set_page_config(page_title="健身AI助手", page_icon="💪", layout="centered")

st.title("💪 健身AI助手")
st.caption("训练计划 + 减脂外卖，一站搞定")

# ── 初始化 session state ──────────────────────────
if "training_messages" not in st.session_state:
    st.session_state.training_messages = None
    st.session_state.training_system = None
if "diet_messages" not in st.session_state:
    st.session_state.diet_messages = None
    st.session_state.diet_system = None

tab1, tab2 = st.tabs(["🏋️ 训练计划", "🥗 减脂外卖"])


def render_followup(system_key, messages_key, prefix):
    """统一的追问区域"""
    messages = st.session_state[messages_key]
    if messages is None:
        return

    system = st.session_state[system_key]

    # 显示历史对话
    for msg in messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    # 追问输入
    followup = st.chat_input("继续追问…", key=f"{prefix}_chat")
    if followup:
        with st.spinner("AI 正在回复…"):
            reply = chat(system, followup, history=messages)
        messages.append({"role": "user", "content": followup})
        messages.append({"role": "assistant", "content": reply})
        st.session_state[messages_key] = messages
        st.rerun()


# ── 训练计划 ──────────────────────────────────────
with tab1:
    st.subheader("告诉我你的情况")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("性别", ["男", "女"])
        age = st.number_input("年龄", 15, 60, 22)
        height = st.number_input("身高(cm)", 140, 220, 175)
        weight = st.number_input("体重(kg)", 40, 150, 70)
    with col2:
        goal = st.selectbox("训练目标", ["减脂", "增肌", "增肌减脂", "提升体能"])
        days = st.selectbox("每周训练天数", [2, 3, 4, 5, 6])
        experience = st.selectbox("训练经验", ["零基础", "初级(练过几个月)", "中级(练过1年以上)"])
        equipment = st.selectbox("可用器械", ["健身房（全器械）", "家里（无器械）", "家里（哑铃/弹力带）"])

    if st.button("生成训练计划", type="primary", use_container_width=True):
        info = {
            "gender": gender, "age": age, "height": height,
            "weight": weight, "goal": goal, "days_per_week": days,
            "experience": experience, "equipment": equipment
        }
        with st.spinner("AI正在为你定制训练计划..."):
            system, user = training_plan_prompt(info)
            result = chat(system, user)

        st.session_state.training_system = system
        st.session_state.training_messages = [
            {"role": "user", "content": user},
            {"role": "assistant", "content": result}
        ]
        st.rerun()

    render_followup("training_system", "training_messages", "training")

# ── 减脂外卖 ──────────────────────────────────────
with tab2:
    st.subheader("告诉我你的饮食需求")

    col1, col2 = st.columns(2)
    with col1:
        gender2 = st.selectbox("性别 ", ["男", "女"])
        weight2 = st.number_input("体重(kg) ", 40, 150, 70)
        goal2 = st.selectbox("减脂目标", ["快速减脂", "缓慢稳定减脂", "维持体重"])
    with col2:
        taste = st.multiselect("口味偏好", ["川湘辣味", "清淡", "日料", "快餐", "沙拉", "东南亚"], default=["清淡"])
        avoid = st.text_input("忌口（没有可不填）", placeholder="如：海鲜、香菜")
        budget = st.selectbox("单餐预算", [15, 20, 30, 40, 50])

    if st.button("生成外卖方案", type="primary", use_container_width=True):
        info = {
            "gender": gender2, "weight": weight2, "goal": goal2,
            "taste": "、".join(taste) if taste else "无特别偏好",
            "avoid": avoid if avoid else "无",
            "budget": budget
        }
        with st.spinner("AI正在为你推荐减脂外卖..."):
            system, user = diet_plan_prompt(info)
            result = chat(system, user)

        st.session_state.diet_system = system
        st.session_state.diet_messages = [
            {"role": "user", "content": user},
            {"role": "assistant", "content": result}
        ]
        st.rerun()

    render_followup("diet_system", "diet_messages", "diet")
