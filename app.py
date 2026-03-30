import streamlit as st
import json
from datetime import date, datetime
from uuid import uuid4
from streamlit.components.v1 import html as st_html

# ------------------ CONFIG ------------------
st.set_page_config(page_title="World Monitor Level up", layout="wide")

# ------------------ DEFAULT DATA ------------------
DEFAULT_DATA = {
    "xp": 0,
    "level": 1,
    "streak": 0,
    "last_date": str(date.today()),
    "tasks": [],
    "achievements": []
}

# ------------------ LOCAL STORAGE ------------------

def save_local_storage(data):

    js = f"""
    <script>
    localStorage.setItem("quest_pro_data", JSON.stringify({json.dumps(data)}));
    </script>
    """

    st_html(js, height=0)

# ------------------ INIT SESSION ------------------

if "data" not in st.session_state:
    st.session_state.data = DEFAULT_DATA.copy()

data = st.session_state.data

# ------------------ CORE LOGIC ------------------

def recalc_level():
    data["level"] = data["xp"] // 100 + 1


def add_xp(points, reason=""):
    data["xp"] += points

    prev_level = data["level"]
    recalc_level()

    if data["level"] > prev_level:
        st.balloons()
        st.success(f"🎉 LEVEL UP! You reached Level {data['level']}")


def update_streak():

    today = str(date.today())

    if data["last_date"] != today:
        data["streak"] += 1
        data["last_date"] = today

        if data["streak"] % 5 == 0:
            add_xp(50)
            st.success("🔥 5-Day Streak Bonus +50 XP")


def add_task(title, xp):

    data["tasks"].append({
        "id": str(uuid4()),
        "title": title,
        "xp": xp,
        "done": False,
        "created_at": str(datetime.now())
    })


def complete_task(task_id):

    for t in data["tasks"]:

        if t["id"] == task_id and not t["done"]:

            t["done"] = True
            add_xp(t["xp"])

            st.success(f"✅ {t['title']} completed! +{t['xp']} XP")

            check_achievements()
            break


def check_achievements():

    xp = data["xp"]
    ach = data["achievements"]

    def unlock(name):

        if name not in ach:
            ach.append(name)
            st.toast(f"🏅 Achievement Unlocked: {name}")

    if xp >= 100:
        unlock("Beginner Achiever")

    if xp >= 300:
        unlock("Intermediate Builder")

    if xp >= 600:
        unlock("Advanced Creator")

    if xp >= 1000:
        unlock("World Monitor Master")

# ------------------ AI TASK SUGGESTION ------------------

def suggest_tasks(level):

    if level <= 2:
        return [
            ("Learn API basics", 20),
            ("Fetch sample data", 25)
        ]

    elif level <= 4:
        return [
            ("Clean dataset", 30),
            ("Create visualizations", 40)
        ]

    elif level <= 6:
        return [
            ("Build ML model", 50),
            ("Evaluate model", 40)
        ]

    else:
        return [
            ("Deploy Streamlit app", 60),
            ("Optimize performance", 50)
        ]

# ------------------ UI ------------------

st.title("🎮 World Monitor Quest PRO")
st.caption("Gamified AI Project System")

# ------------------ STATS ------------------

col1, col2, col3 = st.columns(3)

col1.metric("🏆 Level", data["level"])
col2.metric("⭐ XP", data["xp"])
col3.metric("🔥 Streak", data["streak"])

progress = data["xp"] % 100
st.progress(progress)

# ------------------ TASK MANAGER ------------------

st.subheader("🧩 Your Missions")

with st.form("add_task_form"):

    title = st.text_input("Task Name")

    xp = st.number_input(
        "XP Reward",
        min_value=10,
        max_value=100,
        value=25
    )

    submitted = st.form_submit_button("Add Task")

    if submitted and title:
        add_task(title, xp)
        st.success("Task Added!")

# ------------------ DISPLAY TASKS ------------------

for t in data["tasks"]:

    col1, col2 = st.columns([4,1])

    col1.write(
        f"{'✅' if t['done'] else '⬜'} {t['title']} (+{t['xp']} XP)"
    )

    if not t["done"]:

        if col2.button("Complete", key=t["id"]):
            complete_task(t["id"])

# ------------------ AI SUGGESTIONS ------------------

st.subheader("🤖 Suggested Tasks")

for task, xp in suggest_tasks(data["level"]):

    if st.button(f"Add: {task} (+{xp} XP)"):
        add_task(task, xp)

# ------------------ STREAK ------------------

st.subheader("🔥 Daily Check-in")

if st.button("Mark Today Complete"):
    update_streak()

# ------------------ ACHIEVEMENTS ------------------

st.subheader("🏅 Achievements")

for a in data["achievements"]:
    st.write(f"🏆 {a}")

# ------------------ REWARDS ------------------

st.subheader("🎁 Rewards")

level = data["level"]

if level == 3:
    st.success("🎬 Reward: Watch a Movie")

if level == 5:
    st.success("🎧 Reward: Buy Something")

if level == 10:
    st.balloons()
    st.success("🚀 BIG REWARD: Celebrate & Share Project")

# ------------------ SIDEBAR ------------------

st.sidebar.title("⚙️ Controls")

if st.sidebar.button("Reset Progress"):

    st.session_state.data = DEFAULT_DATA.copy()
    save_local_storage(st.session_state.data)

    st.sidebar.success("Reset Done")

st.sidebar.markdown("---")
st.sidebar.write("PRO Version 🚀")

# ------------------ SAVE DATA ------------------

save_local_storage(st.session_state.data)