import streamlit as st
import pandas as pd

# ✅ Load dataset
df = pd.read_csv("New Hair Data - Updated_Hair_Issues_Dataset.csv.csv")
df.columns = df.columns.str.strip()

# ✅ Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "journey" not in st.session_state:
    st.session_state.journey = None

# 🔁 Navigation
def next_step():
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

# 🎨 Styling
st.markdown("""
<style>
body, .stApp {
    background-color: black;
    color: white;
}
h1, h2, h3, .stSelectbox label, .stRadio label {
    color: white;
    text-align: center;
    font-family: 'Arial', sans-serif;
}
.stButton button {
    background-color: #FFD700;
    color: black;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
}
.stRadio div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- Step 1: Welcome ---
if st.session_state.step == 1:
    st.image("1.png", use_container_width=True)
    if st.button("Start"):
        next_step()

# --- Step 2: Choose Journey ---
elif st.session_state.step == 2:
    st.image("2.png", use_container_width=True)
    st.markdown("<h3 style='text-align:center;'>What are you looking for?</h3>", unsafe_allow_html=True)
    choice = st.radio("", ["Hair Concerns & Product Solutions", "Styling Product Recommendations"], horizontal=True)
    st.session_state.journey = choice

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("Next ➡️"):
            next_step()

# --- Step 3: Journey Logic ---
elif st.session_state.step == 3:
    if st.session_state.journey == "Hair Concerns & Product Solutions":
        st.image("3.png", use_container_width=True)
        hair_issue = st.selectbox("Select Your Hair Concern:", df["Issue"].dropna().unique())
        st.session_state.hair_issue = hair_issue

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Back"):
                go_back()
        with col2:
            if st.button("Next ➡️"):
                next_step()
    else:
        st.image("4.png", use_container_width=True)
        styling_goal = st.selectbox("Select Your Styling Goal:", df["Styling Goal"].dropna().unique())
        st.session_state.styling_goal = styling_goal

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Back"):
                go_back()
        with col2:
            if st.button("Next ➡️"):
                next_step()

# --- Step 4: Hair Concern Details ---
elif st.session_state.step == 4 and st.session_state.journey == "Hair Concerns & Product Solutions":
    issue_data = df[df["Issue"] == st.session_state.hair_issue].iloc[0]

    st.markdown(f"""
    <h2 style='text-align:center;'>Understanding {issue_data['Issue']}</h2>
    <p style='text-align:center;'>📖 <b>Definition:</b> {issue_data['Definition']}</p>
    <p style='text-align:center;'>⚠️ <b>Cause:</b> {issue_data['Cause']}</p>
    <p style='text-align:center;'>🛠 <b>Solution:</b> {issue_data['Solution']}</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("Next ➡️"):
            next_step()

# --- Step 5: Budget Selection (NO PNGs) ---
elif st.session_state.step == 5 and st.session_state.journey == "Hair Concerns & Product Solutions":
    st.image("5.png", use_container_width=True)

    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up", "$75 & Up"])
    st.session_state.budget = budget

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("See Recommendations ➡️"):
            next_step()

# --- Step 6: Show Hair Concern Product Recommendations ---
elif st.session_state.step == 6 and st.session_state.journey == "Hair Concerns & Product Solutions":
    result = df[
        (df["Issue"] == st.session_state.hair_issue) &
        (df["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    st.image("back2.png", use_container_width=True)

    if not result.empty:
        st.markdown(f"<h2 style='text-align:center;'>Recommended for {st.session_state.hair_issue}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **Budget:** {result.iloc[0]['Budget']}")
        st.write("🛍 Click the link to purchase:")

        product_text = result.iloc[0]['Recommended Product & Link']
        if "](" in product_text:
            formatted_products = product_text.replace(", ", "\n🔹 ")
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {product_text}")
    else:
        st.warning("❌ No product found for this selection.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("Next ➡️"):
            st.session_state.step = 10  # Go to Final Page

# --- Step 4 (Alt): Styling Product Budget ---
elif st.session_state.step == 4 and st.session_state.journey == "Styling Product Recommendations":
    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up"])
    st.session_state.styling_budget = budget

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("See Products ➡️"):
            next_step()

# --- Step 5 (Alt): Show Styling Product Details ---
elif st.session_state.step == 5 and st.session_state.journey == "Styling Product Recommendations":
    result = df[
        (df["Styling Goal"] == st.session_state.styling_goal) &
        (df["Budget"].str.lower().str.strip() == st.session_state.styling_budget.lower().strip())
    ]

    if not result.empty:
        result = result.iloc[0]
        st.markdown(f"<h2 style='text-align:center;'>Style: {result['Styling Goal']}</h2>", unsafe_allow_html=True)
        st.write(f"✨ **Product Type:** {result['Product Type']}")
        st.write(f"📖 **Description:** {result['Description']}")
        st.write(f"💡 **How to Use:** {result['How to Use']}")

        if "](" in result["Recommended Product & Link"]:
            formatted_products = result["Recommended Product & Link"].replace(", ", "\n🔹 ")
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {result['Recommended Product & Link']}")
    else:
        st.warning("❌ No product found for this style + budget.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back"):
            go_back()
    with col2:
        if st.button("Next ➡️"):
            st.session_state.step = 10  # Final Page

# --- Step 10: Final Page ---
elif st.session_state.step == 10:
    st.image("6.png", use_container_width=True)

    st.markdown("""
    <h2 style='text-align:center;'>Thanks for Visiting Hi Voltage Visuals ⚡</h2>
    <p style='text-align:center;'>With over a decade as a licensed hairstylist, I'm blending hands-on expertise with creative data tools. Stay tuned for more magic! ✨</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;'>
    <a href="https://www.amazon.com/shop/yourstore" target="_blank">🛍 Amazon Store</a> |
    <a href="https://www.instagram.com/yourhandle" target="_blank">📸 Instagram</a> |
    <a href="https://www.tiktok.com/@yourhandle" target="_blank">🎵 TikTok</a>
    </p>
    """, unsafe_allow_html=True)

    if st.button("Start Over"):
        st.session_state.step = 1
