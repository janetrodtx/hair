import streamlit as st
import pandas as pd

# ✅ Load CSVs from GitHub Raw URLs
hair_issues_url = "https://raw.githubusercontent.com/janetrodtx/hair/main/hair_issues_data.csv"
styling_products_url = "https://raw.githubusercontent.com/janetrodtx/hair/main/styling_products_data.csv"

# Load datasets
df_issues = pd.read_csv(hair_issues_url)
df_styling = pd.read_csv(styling_products_url)

df_issues.columns = df_issues.columns.str.strip()
df_styling.columns = df_styling.columns.str.strip()

# ✅ Session state init
if "step" not in st.session_state:
    st.session_state.step = 1
if "journey" not in st.session_state:
    st.session_state.journey = None

# 🔁 Navigation
def next_step():
    st.session_state.step += 1

def go_back():
    st.session_state.step -= 1

# 🎨 Dark Mode Styling
st.markdown("""
<style>
body, .stApp { background-color: black; color: white; }
h1, h2, h3, .stSelectbox label, .stRadio label {
    color: white; text-align: center; font-family: 'Arial', sans-serif;
}
.stButton button {
    background-color: #FFD700; color: black; font-weight: bold;
    border-radius: 8px; padding: 10px;
}
.stRadio div { color: white !important; }
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

    journey_options = ["Hair Concerns & Product Solutions", "Styling Product Recommendations"]
    default_index = journey_options.index(st.session_state.journey) if st.session_state.journey else 0
    choice = st.radio("", journey_options, index=default_index, horizontal=True)
    st.session_state.journey = choice

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            next_step()

# --- Step 3: Select Concern or Style Goal ---
elif st.session_state.step == 3:
    if st.session_state.journey == "Hair Concerns & Product Solutions":
        st.image("3.png", use_container_width=True)
        options = df_issues["Issue"].dropna().unique()
        issue = st.selectbox("Select Your Hair Concern:", ["Select an option"] + list(options))

        if issue != "Select an option":
            st.session_state.hair_issue = issue
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("⬅ Back"):
                    go_back()
            with col2:
                if st.button("Next ➡"):
                    next_step()
        else:
            st.warning("⬆️ Please select your hair concern to continue.")

    else:
        st.image("4.png", use_container_width=True)
        options = df_styling["Styling Goal"].dropna().unique()
        goal = st.selectbox("Select Your Styling Goal:", ["Select an option"] + list(options))

        if goal != "Select an option":
            st.session_state.styling_goal = goal
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("⬅ Back"):
                    go_back()
            with col2:
                if st.button("Next ➡"):
                    next_step()
        else:
            st.warning("⬆️ Please select your styling goal to continue.")

# --- Step 4: Show Hair Concern Info ---
elif st.session_state.step == 4 and st.session_state.journey == "Hair Concerns & Product Solutions":
    data = df_issues[df_issues["Issue"] == st.session_state.hair_issue].iloc[0]
    st.markdown(f"""
    <h2 style='text-align:center;'>Understanding {data['Issue']}</h2>
    <p style='text-align:center;'>📖 <b>Definition:</b> {data['Definition']}</p>
    <p style='text-align:center;'>⚠️ <b>Cause:</b> {data['Cause']}</p>
    <p style='text-align:center;'>🛠 <b>Solution:</b> {data['Solution']}</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            next_step()

# --- Step 5: Budget for Concerns ---
elif st.session_state.step == 5 and st.session_state.journey == "Hair Concerns & Product Solutions":
    st.image("5.png", use_container_width=True)
    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up", "$75 & Up"])
    st.session_state.budget = budget

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("See Recommendations ➡"):
            next_step()

# --- Step 6: Product Recommendations (Concerns) ---
elif st.session_state.step == 6 and st.session_state.journey == "Hair Concerns & Product Solutions":
    filtered = df_issues[
        (df_issues["Issue"] == st.session_state.hair_issue) &
        (df_issues["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    st.markdown(f"<h2 style='text-align:center;'>Recommended for {st.session_state.hair_issue}</h2>", unsafe_allow_html=True)
    if not filtered.empty:
        row = filtered.iloc[0]
        st.write(f"💰 **Budget:** {row['Budget']}")
        st.write("🛍 Click the link to purchase:")
        product_text = row['Recommended Product & Link']
        if "](" in product_text:
            st.markdown("🔹 " + product_text.replace(", ", "\n🔹 "), unsafe_allow_html=True)
        else:
            st.write("🔹 " + product_text)
    else:
        st.warning("❌ No product found for this selection.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            next_step()

# --- Step 4 (Alt): Budget for Styling ---
elif st.session_state.step == 4 and st.session_state.journey == "Styling Product Recommendations":
    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up"])
    st.session_state.styling_budget = budget

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("See Products ➡"):
            next_step()

# --- Step 5 (Alt): Styling Products Display ---
elif st.session_state.step == 5 and st.session_state.journey == "Styling Product Recommendations":
    filtered = df_styling[
        (df_styling["Styling Goal"] == st.session_state.styling_goal) &
        (df_styling["Budget"].str.lower().str.strip() == st.session_state.styling_budget.lower().strip())
    ]

    if not filtered.empty:
        row = filtered.iloc[0]
        st.markdown(f"<h2 style='text-align:center;'>Style: {row['Styling Goal']}</h2>", unsafe_allow_html=True)
        st.write(f"✨ **Product Type:** {row['Product Type']}")
        st.write(f"📖 **Description:** {row['Description']}")
        st.write(f"💡 **How to Use:** {row['How to Use']}")
        product_text = row['Recommended Product & Link']
        if "](" in product_text:
            st.markdown("🔹 " + product_text.replace(", ", "\n🔹 "), unsafe_allow_html=True)
        else:
            st.write("🔹 " + product_text)
    else:
        st.warning("❌ No product found for this style and budget.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            st.session_state.step = 10

# --- Step 10: Final Page ---
elif st.session_state.step == 10:
    st.image("7.png", use_container_width=True)

    st.markdown("""
    <h2 style='text-align:center;'> About Me ⚡</h2>
    <p style='text-align:center;'>Hi, I’m Janet, a former hairstylist with 10 years in the hair industry. I merged my love of hair care with data analytics to create this app. ✨</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='text-align:center;'> What This App Does ⚡</h2>
    <p style='text-align:center;'>Personalized product recommendations based on your hair concerns or styling goals, with budget options and shopping links. Shop smarter, not harder! 🛍</p>
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


