
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

import api_client as api
import components as ui
from config import API_URL


st.set_page_config(
    page_title=" Your Wellness Space",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.inject_css()


if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


def save_checkin(payload, score):
    st.session_state.history.append(
        {
            "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "score": score,
            "sleep": payload["sleep_hours_per_night"],
            "study": payload["study_hours"],
            "activity": payload["physical_activity_hours"],
            "screen": payload["avg_daily_usage_hours"],
            "stress": payload["stress_level"],
        }
    )


def show_home():
    ui.page_header(
        "How are you feeling today?"
    )

    ui.render(
        """
        <div style="
            background:#172C38;
            color:white;
            padding:34px;
            border-radius:24px;
            margin-bottom:22px;
        ">
            <div style="
                color:#B7D8C8;
                font-size:11px;
                letter-spacing:2px;
                font-weight:700;
            ">A MOMENT FOR YOURSELF</div>
            <div style="
                font-family:Fraunces,serif;
                font-size:32px;
                margin:14px 0;
            ">You deserve a moment to pause.</div>
            <div style="
                color:#E0E8E4;
                max-width:580px;
                line-height:1.8;
            ">
                Notice your everyday habits, make time for rest,
                and remember that your wellbeing is more than a number
            </div>
        </div>
        """
    )

    st.subheader("Your wellness space")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            ui.render(
                """
                <div style="font-size:27px">☾</div>
                <h3>Daily check-in</h3>
                <p style="color:#718080">
                Reflect on sleep, study, activity and screen time.
                </p>
                """
            )

            if st.button(
                "Start check-in",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.page = "Check-in"
                st.rerun()

    with col2:
        with st.container(border=True):
            ui.render(
                """
                <div style="font-size:27px">✧</div>
                <h3>Your progress</h3>
                <p style="color:#718080">
                Revisit your previous check-ins and notice patterns.
                </p>
                """
            )

            if st.button(
                "View insights",
                use_container_width=True,
            ):
                st.session_state.page = "Insights"
                st.rerun()

    st.write("")

    ui.notice(
        "gentle",
        "A small reminder",
        "You do not have to make every day perfect. Small, supportive habits matter.",
    )

    ui.page_header(
        "Your daily rhythm",
        "A quick look at the habits you can reflect on.",
    )

    habits = st.columns(4)

    habit_data = [
        ("☾", "Sleep", "Rest and recharge"),
        ("✎", "Study", "Make room for breaks"),
        ("✿", "Movement", "Move in a way you enjoy"),
        ("◷", "Screen time", "Find your own balance"),
    ]

    for column, (symbol, title, description) in zip(
        habits, habit_data
    ):
        with column:
            with st.container(border=True):
                st.markdown(f"### {symbol} {title}")
                st.caption(description)


def show_checkin():
    ui.page_header(
        "Your daily check-in",
        "Share a little about your routine. Enter what feels accurate for you.",
    )

    with st.form("wellness_checkin"):


        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input(
                "Age",
                min_value=10,
                max_value=100,
                value=20,
                step=1,
            )

            gender = st.selectbox(
                "Gender",
                ["Female", "Male"],
            )

            country = st.selectbox(
                "Country",
                [
                    "India",
                    "USA",
                    "Canada",
                    "Australia",
                    "UK",
                    "Germany",
                    "Mexico",
                    "Turkey",
                    "France",
                    "Other",
                ],
            )

        with c2:
            academic_level = st.selectbox(
                "Education level",
                [
                    "Undergraduate",
                    "Graduate",
                    "High School",
                ],
            )

            platform = st.selectbox(
                "Most-used social platform",
                [
                    "Instagram",
                    "YouTube",
                    "WhatsApp",
                    "Facebook",
                    "LinkedIn",
                    "Snapchat",
                    "Twitter",
                    "TikTok",
                    "LINE",
                    "KakaoTalk",
                    "VKontakte",
                    "WeChat",
                ],
            )

            purpose = st.selectbox(
                "Main reason for using social media",
                [
                    "Education",
                    "Networking",
                    "Entertainment",
                    "News",
                ],
            )

        st.divider()
        st.subheader("Your everyday routine")
        st.caption(
            "Use your best estimate. There are no perfect answers."
        )

        c1, c2 = st.columns(2)

        with c1:
            screen = st.slider(
                "Daily social media use (hours)",
                0.0,
                24.0,
                3.0,
                0.5,
            )

            unlocks = st.number_input(
                "Daily phone unlocks",
                min_value=0,
                max_value=1000,
                value=50,
                step=5,
            )

            study = st.slider(
                "Study hours per day",
                0.0,
                24.0,
                5.0,
                0.5,
            )

        with c2:
            activity = st.slider(
                "Physical activity per day (hours)",
                0.0,
                24.0,
                0.5,
                0.5,
            )

            sleep = st.slider(
                "Sleep per night (hours)",
                0.0,
                24.0,
                8.0,
                0.5,
            )

            stress = st.selectbox(
                "How would you describe your stress level?",
                ["Low", "Medium", "High", "Very High"],
            )

        submitted = st.form_submit_button(
            "Complete my check-in",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        payload = {
            "age": int(age),
            "gender": gender,
            "country": country,
            "academic_level": academic_level,
            "most_used_platform": platform,
            "purpose_of_use": purpose,
            "avg_daily_usage_hours": float(screen),
            "daily_unlocks": int(unlocks),
            "study_hours": float(study),
            "physical_activity_hours": float(activity),
            "sleep_hours_per_night": float(sleep),
            "stress_level": stress,
        }

        with st.spinner("Preparing your check-in..."):
            try:
                score = api.predict(
                    payload=payload,
                    base_url=API_URL,
                )

                st.session_state.last_result = {
                    "score": score,
                    "payload": payload,
                }

                save_checkin(payload, score)

            except api.ApiError as error:
                ui.notice(
                    "warning",
                    error.title,
                    error.message,
                    error.details,
                )
                st.stop()

        st.success("Your check-in is complete.")
        st.rerun()

    result = st.session_state.last_result

    if result:
        st.divider()
        ui.page_header(
            "Your check-in summary",
            "Use this as a reflection prompt, not a medical assessment.",
        )

        score = result["score"]
        payload = result["payload"]

        ui.score_dial(score)

        st.write("")

        left, right = st.columns(2)

        with left:
            ui.day_ring(
                payload["sleep_hours_per_night"],
                payload["study_hours"],
                payload["physical_activity_hours"],
                payload["avg_daily_usage_hours"],
            )

        with right:
            ui.card_title("A few gentle reminders")

            reminders = []

            if payload["sleep_hours_per_night"] < 7:
                reminders.append(
                    "Consider whether you can make a little more room for rest."
                )

            if payload["avg_daily_usage_hours"] >= 6:
                reminders.append(
                    "Notice how screen time fits alongside your other activities."
                )

            if payload["physical_activity_hours"] < 0.5:
                reminders.append(
                    "If it feels comfortable, a short walk or stretch may be a useful break."
                )

            if payload["stress_level"] in ["High", "Very High"]:
                reminders.append(
                    "Consider talking with someone you trust about what's been stressful."
                )

            if not reminders:
                reminders.append(
                    "Keep noticing what helps you feel supported and balanced."
                )

            for reminder in reminders:
                ui.notice("gentle", "A thought for you", reminder)

        ui.notice(
            "info",
            "Remember",
            "The score is a model estimate based on the information entered. It cannot diagnose mental health or determine how you truly feel.",
        )


def show_insights():
    ui.page_header(
        "Your insights",
        "Look back at your check-ins and reflect on your routine.",
    )

    history = st.session_state.history

    if not history:
        ui.notice(
            "info",
            "Your story starts here",
            "Complete your first check-in to see your progress here.",
        )

        if st.button("Start your first check-in", type="primary"):
            st.session_state.page = "Check-in"
            st.rerun()

        return

    df = pd.DataFrame(history)

    col1, col2 = st.columns(2)

    with col1:
        ui.stat_tile(
            "Completed check-ins",
            len(df),
            "Saved in this session",
        )

    with col2:
        ui.stat_tile(
            "Most recent score",
            f"{df.iloc[-1]['score']:.1f}",
            "Model estimate, not a diagnosis",
        )

    st.write("")

    fig = px.line(
        df,
        x=df.index + 1,
        y="score",
        markers=True,
        labels={
            "x": "Check-in",
            "score": "Estimated score",
        },
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#253C42",
        margin=dict(l=15, r=15, t=25, b=15),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Your daily rhythm")

    routine_df = df[
        ["sleep", "study", "activity", "screen"]
    ].rename(
        columns={
            "sleep": "Sleep",
            "study": "Study",
            "activity": "Movement",
            "screen": "Screen time",
        }
    )

    routine_fig = px.bar(
        routine_df,
        barmode="group",
        labels={
            "index": "Check-in",
            "value": "Hours",
            "variable": "Routine",
        },
    )

    routine_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#253C42",
    )

    st.plotly_chart(
        routine_fig,
        use_container_width=True,
    )

    ui.notice(
        "gentle",
        "Progress is personal",
        "A score changing does not necessarily mean your wellbeing has improved or worsened. Reflect on your own experience too.",
    )


def show_history():
    ui.page_header(
        "Your check-in history",
        "Your recent check-ins from this session.",
    )

    history = st.session_state.history

    if not history:
        ui.notice(
            "info",
            "Nothing here yet",
            "Your completed check-ins will appear here.",
        )
        return

    df = pd.DataFrame(history)

    display_df = df[
        ["date", "score", "sleep", "study", "activity", "screen", "stress"]
    ].rename(
        columns={
            "date": "Date",
            "score": "Estimated score",
            "sleep": "Sleep (h)",
            "study": "Study (h)",
            "activity": "Movement (h)",
            "screen": "Screen time (h)",
            "stress": "Stress",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    if st.button("Clear session history"):
        st.session_state.history = []
        st.session_state.last_result = None
        st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "Home"


with st.sidebar:
    ui.brand()

    st.caption("YOUR PERSONAL WELLNESS SPACE")
    st.write("")

    pages = [
        "Home",
        "Check-in",
        "Insights",
        "History",
    ]

    selected_page = st.radio(
        "NAVIGATION",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )

    st.session_state.page = selected_page

    st.divider()

    ui.render(
        """
        <div style="font-size:12px;line-height:1.8;color:#D0DDD9">
            Take your time.<br>
            There is no perfect way to feel.
        </div>
        """
    )

    st.write("")
    st.caption("Dusk · Student wellbeing")


if st.session_state.page == "Home":
    show_home()
elif st.session_state.page == "Check-in":
    show_checkin()
elif st.session_state.page == "Insights":
    show_insights()
elif st.session_state.page == "History":
    show_history()
