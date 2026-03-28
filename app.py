import streamlit as st
import json
from datetime import date, datetime
from uuid import uuid4

# ------------------ CONFIG ------------------
st.set_page_config(page_title="World Monitor Level up", layout="wide")

# ------------------ STORAGE ------------------
DATA_FILE = "progress_pro.json"

DEFAULT_DATA = {
    "xp": 0,
    "level": 1,
    "streak": 0,
    "last_date": str(date.today()),
    "tasks": [],  # {id, title, xp, done, created_at}
    "achievements": []  # strings
}


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ------------------ INIT SESSION ------------------
if "data" not in st.session_state:
    st.session_state.data = load_data()


# ------------------ CORE LOGIC ------------------

def recalc_level():
    st.session_state.data["level"] = st.session_state.data["xp"] // 100 + 1


def add_xp(points, reason=""):
    st.session_state.data["xp"] += points
    prev_level = st.session_state.data["level"]
    recalc_level()
    if st.session_state.data["level"] > prev_level:
        st.balloons()
        st.success(f"🎉 LEVEL UP! You reached Level {st.session_state.data['level']}")


def update_streak():
    today = str(date.today())
    if st.session_state.data["last_date"] != today:
        st.session_state.data["streak"] += 1
        st.session_state.data["last_date"] = today
        if st.session_state.data["streak"] % 5 == 0:
            add_xp(50, "5-day streak bonus")
            st.success("🔥 5-Day Streak Bonus +50 XP")


def add_task(title, xp):
    st.session_state.data["tasks"].append({
        "id": str(uuid4()),
        "title": title,
        "xp": xp,
        "done": False,
        "created_at": str(datetime.now())
    })


def complete_task(task_id):
    for t in st.session_state.data["tasks"]:
        if t["id"] == task_id and not t["done"]:
            t["done"] = True
            add_xp(t["xp"], t["title"])
            st.success(f"✅ {t['title']} completed! +{t['xp']} XP")
            check_achievements()
            break


def check_achievements():
    xp = st.session_state.data["xp"]
    ach = st.session_state.data["achievements"]

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
        return [("Learn API basics", 20), ("Fetch sample data", 25)]
    elif level <= 4:
        return [("Clean dataset", 30), ("Create visualizations", 40)]
    elif level <= 6:
        return [("Build ML model", 50), ("Evaluate model", 40)]
    else:
        return [("Deploy Streamlit app", 60), ("Optimize performance", 50)]


# ------------------ UI ------------------
st.title("🎮 World Monitor Quest PRO")
st.caption("Gamified AI Project System")

# Stats
col1, col2, col3 = st.columns(3)
col1.metric("🏆 Level", st.session_state.data["level"])
col2.metric("⭐ XP", st.session_state.data["xp"])
col3.metric("🔥 Streak", st.session_state.data["streak"])

# Progress
progress = st.session_state.data["xp"] % 100
st.progress(progress)

# ------------------ TASK MANAGER ------------------
st.subheader("🧩 Your Missions")

with st.form("add_task_form"):
    title = st.text_input("Task Name")
    xp = st.number_input("XP Reward", 10, 100, 25)
    submitted = st.form_submit_button("Add Task")
    if submitted and title:
        add_task(title, xp)
        st.success("Task Added!")

# Display tasks
for t in st.session_state.data["tasks"]:
    col1, col2 = st.columns([4, 1])
    col1.write(f"{'✅' if t['done'] else '⬜'} {t['title']} (+{t['xp']} XP)")
    if not t["done"]:
        if col2.button("Complete", key=t["id"]):
            complete_task(t["id"])

# ------------------ AI SUGGESTIONS ------------------
st.subheader("🤖 Suggested Tasks")
for task, xp in suggest_tasks(st.session_state.data["level"]):
    if st.button(f"Add: {task} (+{xp} XP)"):
        add_task(task, xp)

# ------------------ STREAK ------------------
st.subheader("🔥 Daily Check-in")
if st.button("Mark Today Complete"):
    update_streak()

# ------------------ ACHIEVEMENTS ------------------
st.subheader("🏅 Achievements")
for a in st.session_state.data["achievements"]:
    st.write(f"🏆 {a}")

# ------------------ REWARDS ------------------
st.subheader("🎁 Rewards")
level = st.session_state.data["level"]

if level == 3:
    st.success("🎬 Reward: Watch a Movie")
if level == 5:
    st.success("🎧 Reward: Buy Something")
if level == 10:
    st.balloons()
    st.success("🚀 BIG REWARD: Celebrate & Share Project")

# ------------------ SAVE ------------------
save_data(st.session_state.data)

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Controls")

if st.sidebar.button("Reset Progress"):
    st.session_state.data = DEFAULT_DATA.copy()
    st.sidebar.success("Reset Done")

st.sidebar.markdown("---")
st.sidebar.write("PRO Version 🚀")
