import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("New Hair Data - Updated_Hair_Issues_Dataset.csv.csv")
df.columns = df.columns.str.strip()

# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 1

# Navigation functions
def next_step():
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

# --- Custom Styling ---
st.markdown("""
    <style>
        body, .stApp { background-color: black; color: white; }
        h1, h2, h3, .stSelectbox label, .stRadio label {
            color: white; font-family: 'Arial', sans-serif; text-align: center;
        }
        .stButton button {
            background-color: #FFD700; color: black; font-weight: bold;
            border-radius: 8px; padding: 10px; font-size: 16px;
        }
        .nav-button {
            font-size: 20px; font-weight: bold; background-color: transparent;
            color: #FFD700; border: 2px solid #FFD700; border-radius: 8px;
            padding: 5px 20px; margin: 10px; cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# --- Step 1: Welcome Page ---
if st.session_state.step == 1:
    st.image("1.png", use_container_width=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start ▶️"):
            next_step()

# --- Step 2: Choose Hair Journey ---
elif st.session_state.step == 2:
    st.markdown("<h2>Select Your Hair Journey</h2>", unsafe_allow_html=True)
    choice = st.radio("Choose an option:", ["Hair Concerns & Recommendations", "Styling Products & Tools"])
    if st.button("Next ▶️"):
        st.session_state.journey = choice
        next_step()
    if st.button("◀️ Back"):
        go_back()

# --- Step 3A: Hair Concerns Flow ---
if st.session_state.get("journey") == "Hair Concerns & Recommendations":
    if st.session_state.step == 3:
        st.markdown("<h2>✨ Let's Pinpoint Your Hair Concern ✨</h2>", unsafe_allow_html=True)
        hair_issue = st.selectbox("Choose your hair concern:", df["Issue"].dropna().unique())
        st.session_state.hair_issue = hair_issue
        if st.button("Next ▶️"):
            next_step()
        if st.button("◀️ Back"):
            go_back()

    elif st.session_state.step == 4:
        issue_data = df[df["Issue"] == st.session_state.hair_issue].iloc[0]
        st.markdown(f"""
            <div style='text-align:center; max-width:700px; margin:auto;'>
                <h2>💡 Understanding {issue_data['Issue']}</h2>
                <p>📖 <b>Definition:</b> {issue_data['Definition']}</p>
                <p>⚠️ <b>Cause:</b> {issue_data['Cause']}</p>
                <p>🛠 <b>Solution:</b> {issue_data['Solution']}</p>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Back"):
                go_back()
        with col2:
            if st.button("Next ▶️"):
                next_step()

    elif st.session_state.step == 5:
        st.markdown("<h2>💰 Choose Your Budget</h2>", unsafe_allow_html=True)
        budget = st.radio("", ["Under $25", "$25 & Up", "$75 & Up"])
        st.session_state.budget = budget
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Back"):
                go_back()
        with col2:
            if st.button("See Recommendations ▶️"):
                next_step()

    elif st.session_state.step == 6:
        result = df[
            (df["Issue"] == st.session_state.hair_issue) &
            (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
        ]
        st.markdown(f"<h2 style='text-align:center;'>Recommended for {st.session_state.hair_issue}</h2>", unsafe_allow_html=True)
        if not result.empty:
            product_text = result.iloc[0]['Recommended Product & Link']
            st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")
            st.write("🛍 Click the Link to Purchase:")
            if "](" in product_text:
                formatted_products = product_text.replace(", ", "\n🔹 ")
                st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
            else:
                st.write(f"🔹 {product_text}")
        else:
            st.warning("❌ No product found for your budget.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Back"):
                go_back()
        with col2:
            if st.button("Finish ✨"):
                st.session_state.step = 7

# --- Step 3B: Styling Products & Tools Flow ---
if st.session_state.get("journey") == "Styling Products & Tools":
    if st.session_state.step == 3:
        st.markdown("<h2>From Curls to Sleek — What's Your Style Mood?</h2>", unsafe_allow_html=True)
        styling_goal = st.selectbox("Choose your style goal:", df["Styling Goal"].dropna().unique())
        st.session_state.styling_goal = styling_goal
        if st.button("Next ▶️"):
            next_step()
        if st.button("◀️ Back"):
            go_back()

    elif st.session_state.step == 4:
        st.markdown("<h2>💰 Choose Your Budget</h2>", unsafe_allow_html=True)
        budget = st.radio("", ["Under $25", "$25 & Up"])
        st.session_state.budget = budget
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Back"):
                go_back()
        with col2:
            if st.button("See Products ▶️"):
                next_step()

    elif st.session_state.step == 5:
        result = df[
            (df["Styling Goal"] == st.session_state.styling_goal) &
            (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
        ]
        st.markdown(f"<h2 style='text-align:center;'>Styling Picks for {st.session_state.styling_goal}</h2>", unsafe_allow_html=True)
        if not result.empty:
            st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")
            st.write(f"🛍 Click the Link to Purchase:")
            st.write(f"{result.iloc[0]['Recommended Product & Link']}")
            st.write(f"🧴 **How to Use:** {result.iloc[0]['How to Use']}")
        else:
            st.warning("❌ No styling product found for your budget.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Back"):
                go_back()
        with col2:
            if st.button("Finish ✨"):
                st.session_state.step = 7

# --- Final Step: Outro Page ---
if st.session_state.step == 7:
    st.markdown("""
        <div style='text-align:center;'>
            <h2>⚡ Hi Voltage Visuals ⚡</h2>
            <p>✨ Created by Janet, a licensed hairstylist of 10+ years turned data artist.</p>
            <p>🧴 Shop my favorites: <a href='https://www.amazon.com/shop/hi.voltage.visuals' target='_blank'>Amazon Storefront</a></p>
            <p>📱 Follow for updates: <a href='https://www.instagram.com/hi.voltage.visuals/' target='_blank'>Instagram</a> | <a href='https://www.tiktok.com/@hi.voltage.visuals' target='_blank'>TikTok</a></p>
            <p>Thanks for exploring your hair journey with me! 💛</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Start Over 🔄"):
        st.session_state.step = 1
