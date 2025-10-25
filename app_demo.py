import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Mental Math Trainer",
    page_icon="🧮",
    layout="centered"
)

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
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'problem_history' not in st.session_state:
    st.session_state.problem_history = []

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
time_limit = st.sidebar.slider(
    "Time Limit (seconds)",
    min_value=5, max_value=60, value=30
)

# Display statistics
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("✅ Score", st.session_state.score)
with col2:
    st.metric("📝 Attempts", st.session_state.total_attempts)
with col3:
    if st.session_state.total_attempts > 0:
        accuracy = (st.session_state.score / 
                   st.session_state.total_attempts) * 100
        st.metric("🎯 Accuracy", f"{accuracy:.1f}%")

st.markdown("---")

# Generate new problem button
if st.button("🎲 New Problem", type="primary"):
    problem, answer = generate_problem(operation, difficulty)
    st.session_state.current_problem = problem
    st.session_state.current_answer = answer
    st.session_state.start_time = time.time()

# Display current problem
if st.session_state.current_problem:
    st.markdown(f"### Problem: {st.session_state.current_problem}")
    
    # Check timer
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, time_limit - elapsed)
        
        if remaining > 0:
            st.progress(remaining / time_limit)
            st.markdown(f"⏱️ Time remaining: **{remaining:.1f}s**")
        else:
            st.error("⏰ Time's up!")
            st.session_state.current_problem = None
            st.session_state.current_answer = None
    
    # Answer input
    user_answer = st.number_input(
        "Your answer:",
        value=0,
        step=1,
        key="answer_input"
    )
    
    # Submit button
    if st.button("✓ Submit Answer"):
        st.session_state.total_attempts += 1
        
        if user_answer == st.session_state.current_answer:
            st.session_state.score += 1
            st.success("🎉 Correct! Well done!")
        else:
            st.error(f"❌ Incorrect. The answer was "
                    f"{st.session_state.current_answer}")
        
        # Add to history
        st.session_state.problem_history.append({
            'problem': st.session_state.current_problem,
            'correct_answer': st.session_state.current_answer,
            'user_answer': user_answer,
            'correct': user_answer == st.session_state.current_answer
        })
        
        st.session_state.current_problem = None
        st.session_state.current_answer = None
        st.session_state.start_time = None

else:
    st.info("👆 Click 'New Problem' to start practicing!")

# Reset button
if st.sidebar.button("🔄 Reset Statistics"):
    st.session_state.score = 0
    st.session_state.total_attempts = 0
    st.session_state.problem_history = []
    st.success("Statistics reset!")

# Show problem history
if st.sidebar.checkbox("📊 Show History") and st.session_state.problem_history:
    st.sidebar.markdown("### Recent Problems")
    for i, item in enumerate(reversed(st.session_state.problem_history[-5:])):
        status = "✅" if item['correct'] else "❌"
        st.sidebar.text(f"{status} {item['problem']} = {item['user_answer']}")