import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Mental Math Trainer",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for better button layout on mobile (especially Safari iOS)
st.markdown("""
<style>
    /* Compact spacing throughout the app */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }

    /* Prevent horizontal overflow */
    .main .block-container {
        overflow-x: hidden !important;
    }

    /* Make buttons compact but touch-friendly */
    .stButton > button {
        height: 55px;
        font-size: 22px;
        font-weight: bold;
        margin: 0px;
        padding: 0.2rem;
        width: 100%;
        box-sizing: border-box;
    }

    /* Reduce spacing in markdown elements */
    h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        font-size: 1.8rem !important;
    }

    h3 {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
        font-size: 1.3rem !important;
    }

    /* Compact progress bar */
    .stProgress {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Compact horizontal rules */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Make buttons display in a 3-column grid */
    .stButton {
        display: inline-block !important;
        width: 31% !important;
        margin: 0.5% !important;
        margin-bottom: 0.3rem !important;
        vertical-align: top !important;
        box-sizing: border-box !important;
    }

    .stButton > button {
        width: 100% !important;
    }

    /* Force columns to stay horizontal - use multiple selectors for Safari compatibility */
    div[data-testid="column"] {
        min-width: 0 !important;
        flex: 0 0 48% !important;
        max-width: 48% !important;
        width: 48% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Remove Streamlit's default column padding */
    div[data-testid="column"] > div {
        padding: 0 !important;
    }

    /* Override Streamlit's mobile responsive behavior */
    div[data-testid="stHorizontalBlock"] {
        display: -webkit-box !important;
        display: -webkit-flex !important;
        display: -ms-flexbox !important;
        display: flex !important;
        -webkit-flex-direction: row !important;
        -ms-flex-direction: row !important;
        flex-direction: row !important;
        -webkit-flex-wrap: nowrap !important;
        -ms-flex-wrap: nowrap !important;
        flex-wrap: nowrap !important;
        gap: 2% !important;
        margin-bottom: 0.2rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        padding: 0 !important;
    }

    /* Prevent column stacking on mobile - Safari specific */
    @media (max-width: 768px) {
        /* Tighter container on mobile */
        .block-container {
            padding-left: 0.25rem !important;
            padding-right: 0.25rem !important;
        }

        div[data-testid="column"] {
            flex: 0 0 31% !important;
            -webkit-flex: 0 0 31% !important;
            max-width: 31% !important;
            min-width: 0 !important;
            width: 31% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        div[data-testid="column"] > div {
            padding: 0 !important;
        }

        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            -webkit-flex-direction: row !important;
            flex-wrap: nowrap !important;
            -webkit-flex-wrap: nowrap !important;
            gap: 1.5% !important;
            padding: 0 !important;
        }

        /* Button grid on mobile */
        .stButton {
            width: 30.5% !important;
            margin: 0.75% !important;
            margin-bottom: 0.3rem !important;
        }

        /* Smaller buttons and fonts on mobile */
        .stButton > button {
            height: 42px;
            font-size: 17px;
            padding: 0.1rem;
            margin: 0;
            width: 100% !important;
        }

        h1 {
            font-size: 1.3rem !important;
        }

        h3 {
            font-size: 0.95rem !important;
        }

        /* Compact metrics on mobile */
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }

        /* Smaller progress text */
        p, .stMarkdown {
            font-size: 0.9rem !important;
        }
    }

    /* Make metric cards more compact */
    [data-testid="stMetricValue"] {
        font-size: 1.4rem;
    }

    /* Reduce padding in metrics */
    [data-testid="metric-container"] {
        padding: 0.5rem 0.5rem !important;
    }

    /* Compact error/success messages */
    .stAlert {
        padding: 0.5rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
</style>
""", unsafe_allow_html=True)

def generate_problem(operation, difficulty):
    """Generate a math problem based on operation and difficulty."""
    if difficulty == "Easy":
        min_num, max_num = 1, 10
    elif difficulty == "Medium":
        min_num, max_num = 10, 50
    else:  # Hard
        min_num, max_num = 50, 100

    num1 = random.randint(min_num, max_num)
    num2 = random.randint(min_num, max_num)

    if operation == "Mixed":
        operation = random.choice(["Addition", "Subtraction",
                                   "Multiplication", "Division"])

    if operation == "Addition":
        problem = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == "Subtraction":
        if num1 < num2:
            num1, num2 = num2, num1
        problem = f"{num1} - {num2}"
        answer = num1 - num2
    elif operation == "Multiplication":
        problem = f"{num1} × {num2}"
        answer = num1 * num2
    else:  # Division
        num1 = num2 * random.randint(2, 10)
        problem = f"{num1} ÷ {num2}"
        answer = num1 // num2

    return problem, answer

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_attempts' not in st.session_state:
    st.session_state.total_attempts = 0
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = None
if 'problem_history' not in st.session_state:
    st.session_state.problem_history = []
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'total_problems' not in st.session_state:
    st.session_state.total_problems = 10
if 'quiz_complete' not in st.session_state:
    st.session_state.quiz_complete = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = ""
if 'last_check' not in st.session_state:
    st.session_state.last_check = ""

# Title and description
st.title("🧮 Mental Math Practice")
st.markdown("Sharpen your mental calculation skills!")

# Sidebar settings
st.sidebar.header("⚙️ Settings")
operation = st.sidebar.selectbox(
    "Select Operation",
    ["Addition", "Subtraction", "Multiplication", "Division", "Mixed"]
)
difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)
problem_count = st.sidebar.selectbox(
    "Number of Problems",
    [10, 20, 30, 50]
)

st.markdown("---")

# Start new quiz button
if not st.session_state.quiz_active:
    if st.button("🚀 Start Quiz", type="primary"):
        st.session_state.quiz_active = True
        st.session_state.quiz_complete = False
        st.session_state.score = 0
        st.session_state.total_attempts = 0
        st.session_state.problem_history = []
        st.session_state.total_problems = problem_count
        st.session_state.user_input = ""
        st.session_state.show_feedback = False
        st.session_state.feedback_message = ""
        st.session_state.last_check = ""
        # Generate first problem
        problem, answer = generate_problem(operation, difficulty)
        st.session_state.current_problem = problem
        st.session_state.current_answer = answer
        st.rerun()

# Quiz in progress
if st.session_state.quiz_active and not st.session_state.quiz_complete:
    # Progress indicator
    progress = st.session_state.total_attempts / st.session_state.total_problems
    st.progress(progress)
    st.markdown(f"**Question {st.session_state.total_attempts + 1} of {st.session_state.total_problems}**")

    # Display statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Score", st.session_state.score)
    with col2:
        st.metric("📝 Answered", st.session_state.total_attempts)
    with col3:
        if st.session_state.total_attempts > 0:
            accuracy = (st.session_state.score /
                       st.session_state.total_attempts) * 100
            st.metric("🎯 Accuracy", f"{accuracy:.1f}%")

    st.markdown("---")

    # Display current problem
    if st.session_state.current_problem:
        st.markdown(f"### Problem: {st.session_state.current_problem}")

        # Display current input
        st.markdown(f"### Your answer: **{st.session_state.user_input if st.session_state.user_input else '___'}**")

        # Show feedback message if exists
        if st.session_state.show_feedback:
            if "Correct" in st.session_state.feedback_message:
                st.success(st.session_state.feedback_message)
            else:
                st.error(st.session_state.feedback_message)

        # Auto-check answer when input changes
        def check_and_advance():
            """Check if current input is correct and auto-advance if it is."""
            if st.session_state.user_input and st.session_state.user_input != st.session_state.last_check:
                try:
                    user_answer = int(st.session_state.user_input)
                    st.session_state.last_check = st.session_state.user_input

                    if user_answer == st.session_state.current_answer:
                        # Correct answer - auto advance
                        st.session_state.total_attempts += 1
                        st.session_state.score += 1

                        # Add to history
                        st.session_state.problem_history.append({
                            'problem': st.session_state.current_problem,
                            'correct_answer': st.session_state.current_answer,
                            'user_answer': user_answer,
                            'correct': True
                        })

                        # Check if quiz is complete
                        if st.session_state.total_attempts >= st.session_state.total_problems:
                            st.session_state.quiz_complete = True
                            st.session_state.current_problem = None
                            st.session_state.current_answer = None
                            st.session_state.user_input = ""
                            st.session_state.show_feedback = False
                            st.session_state.last_check = ""
                        else:
                            # Generate next problem
                            problem, answer = generate_problem(operation, difficulty)
                            st.session_state.current_problem = problem
                            st.session_state.current_answer = answer
                            st.session_state.user_input = ""
                            st.session_state.show_feedback = False
                            st.session_state.last_check = ""

                        st.rerun()
                    else:
                        # Wrong answer - show error
                        st.session_state.show_feedback = True
                        st.session_state.feedback_message = f"❌ Wrong! Try again or clear to skip."
                except ValueError:
                    pass  # Not a valid number yet

        # Check answer before rendering keypad
        check_and_advance()

        # Helper functions for button callbacks
        def toggle_negative():
            if st.session_state.user_input:
                if st.session_state.user_input.startswith("-"):
                    st.session_state.user_input = st.session_state.user_input[1:]
                else:
                    st.session_state.user_input = "-" + st.session_state.user_input

        def delete_last():
            st.session_state.user_input = st.session_state.user_input[:-1]
            st.session_state.last_check = ""

        # Numeric keypad - Row 1: 7, 8, 9
        st.button("7", key="btn7", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "7"))
        st.button("8", key="btn8", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "8"))
        st.button("9", key="btn9", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "9"))

        # Row 2: 4, 5, 6
        st.button("4", key="btn4", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "4"))
        st.button("5", key="btn5", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "5"))
        st.button("6", key="btn6", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "6"))

        # Row 3: 1, 2, 3
        st.button("1", key="btn1", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "1"))
        st.button("2", key="btn2", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "2"))
        st.button("3", key="btn3", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "3"))

        # Row 4: ±, 0, ⌫
        st.button("±", key="btn_neg", on_click=toggle_negative)
        st.button("0", key="btn0", on_click=lambda: setattr(st.session_state, 'user_input', st.session_state.user_input + "0"))
        st.button("⌫", key="btn_del", on_click=delete_last)

        # Clear and Skip buttons
        col_clear, col_skip = st.columns(2)

        with col_clear:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.user_input = ""
                st.session_state.last_check = ""
                st.session_state.show_feedback = False
                st.session_state.feedback_message = ""
                st.rerun()

        with col_skip:
            if st.button("⏭️ Skip", use_container_width=True):
                # Mark as incorrect and skip to next
                st.session_state.total_attempts += 1

                # Add to history with current user input (or 0 if empty)
                try:
                    user_answer = int(st.session_state.user_input) if st.session_state.user_input else 0
                except:
                    user_answer = 0

                st.session_state.problem_history.append({
                    'problem': st.session_state.current_problem,
                    'correct_answer': st.session_state.current_answer,
                    'user_answer': user_answer,
                    'correct': False
                })

                # Check if quiz is complete
                if st.session_state.total_attempts >= st.session_state.total_problems:
                    st.session_state.quiz_complete = True
                    st.session_state.current_problem = None
                    st.session_state.current_answer = None
                    st.session_state.user_input = ""
                    st.session_state.show_feedback = False
                    st.session_state.last_check = ""
                else:
                    # Generate next problem
                    problem, answer = generate_problem(operation, difficulty)
                    st.session_state.current_problem = problem
                    st.session_state.current_answer = answer
                    st.session_state.user_input = ""
                    st.session_state.show_feedback = False
                    st.session_state.last_check = ""

                st.rerun()

# Quiz complete - show results
if st.session_state.quiz_complete:
    st.balloons()
    st.success("🎉 Quiz Complete!")

    accuracy = (st.session_state.score / st.session_state.total_problems) * 100

    # Final statistics
    st.markdown("### 📊 Final Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Correct", st.session_state.score)
    with col2:
        st.metric("❌ Incorrect",
                 st.session_state.total_problems - st.session_state.score)
    with col3:
        st.metric("🎯 Accuracy", f"{accuracy:.1f}%")

    # Performance message
    st.markdown("---")
    if accuracy >= 90:
        st.success("🌟 Outstanding! You're a mental math champion!")
    elif accuracy >= 75:
        st.info("👍 Great job! Keep up the good work!")
    elif accuracy >= 60:
        st.warning("💪 Good effort! Practice makes perfect!")
    else:
        st.error("📚 Keep practicing! You'll improve with time!")

    # Show detailed history
    st.markdown("### 📋 Problem Review")
    for i, item in enumerate(st.session_state.problem_history, 1):
        status = "✅" if item['correct'] else "❌"
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(f"{status} Problem {i}: {item['problem']} = {item['correct_answer']}")
        with col2:
            if not item['correct']:
                st.text(f"Your answer: {item['user_answer']}")

    # Restart button
    st.markdown("---")
    if st.button("🔄 Start New Quiz", type="primary"):
        st.session_state.quiz_active = False
        st.session_state.quiz_complete = False
        st.session_state.current_problem = None
        st.session_state.current_answer = None
        st.session_state.user_input = ""
        st.session_state.show_feedback = False
        st.session_state.feedback_message = ""
        st.session_state.last_check = ""
        st.rerun()

# If not started yet
if not st.session_state.quiz_active and not st.session_state.quiz_complete:
    st.info("👆 Click 'Start Quiz' to begin practicing!")
    st.markdown("""
    ### How it works:
    1. Choose your settings in the sidebar
    2. Click 'Start Quiz' to begin
    3. Answer each problem and submit
    4. Get instant feedback after completing all problems
    """)
