import streamlit as st
import pandas as pd

# ✅ Load CSVs from GitHub (no local files)
hair_issues_url = "https://raw.githubusercontent.com/janetrodtx/hair/main/hair_issues_data.csv"
styling_products_url = "https://raw.githubusercontent.com/janetrodtx/hair/main/styling_products_data.csv"

df_issues = pd.read_csv(hair_issues_url)
df_styling = pd.read_csv(styling_products_url)

df_issues.columns = df_issues.columns.str.strip()
df_styling.columns = df_styling.columns.str.strip()

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

    journey_options = ["Hair Concerns & Product Solutions", "Styling Product Recommendations"]
    default_index = journey_options.index(st.session_state.journey) if st.session_state.journey else 0
    choice = st.radio("", journey_options, index=default_index, horizontal=True)
    st.session_state.journey = choice

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            next_step()

# --- Step 3: Hair Concerns or Styling Goals ---
elif st.session_state.step == 3:
    if st.session_state.journey == "Hair Concerns & Product Solutions":
        st.image("3.png", use_container_width=True)
        hair_issues = df_issues["Issue"].dropna().unique()
        hair_issue = st.selectbox("Select Your Hair Concern:", ["Select an option"] + list(hair_issues))

        if hair_issue != "Select an option":
            st.session_state.hair_issue = hair_issue
            col1, col2 = st.columns(2)
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
        styling_goals = df_styling["Styling Goal"].dropna().unique()
        styling_goal = st.selectbox("Select Your Styling Goal:", ["Select an option"] + list(styling_goals))

        if styling_goal != "Select an option":
            st.session_state.styling_goal = styling_goal
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅ Back"):
                    go_back()
            with col2:
                if st.button("Next ➡"):
                    next_step()
        else:
            st.warning("⬆️ Please select your styling goal to continue.")

# --- Step 4: Show Hair Concern Details ---
elif st.session_state.step == 4 and st.session_state.journey == "Hair Concerns & Product Solutions":
    issue_data = df_issues[df_issues["Issue"].str.lower().str.strip() == st.session_state.hair_issue.lower().strip()].iloc[0]

    st.markdown(f"""
    <h2 style='text-align:center;'>Understanding {issue_data['Issue']}</h2>
    <p style='text-align:center;'>📖 <b>Definition:</b> {issue_data['Definition']}</p>
    <p style='text-align:center;'>⚠️ <b>Cause:</b> {issue_data['Cause']}</p>
    <p style='text-align:center;'>🛠 <b>Solution:</b> {issue_data['Solution']}</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            next_step()

# --- Step 5: Budget for Hair Concerns ---
elif st.session_state.step == 5 and st.session_state.journey == "Hair Concerns & Product Solutions":
    st.image("5.png", use_container_width=True)

    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up", "$75 & Up"])
    st.session_state.budget = budget

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("See Recommendations ➡"):
            next_step()

# --- Step 6: Show Hair Concern Product Recommendations ---
elif st.session_state.step == 6 and st.session_state.journey == "Hair Concerns & Product Solutions":
    result = df_issues[
        (df_issues["Issue"].str.lower().str.strip() == st.session_state.hair_issue.lower().strip()) &
        (df_issues["Budget"].str.lower().str.strip() == st.session_state.budget.lower().strip())
    ]

    st.markdown(f"<h2 style='text-align:center;'>Recommended for {st.session_state.hair_issue}</h2>", unsafe_allow_html=True)

    if not result.empty:
        row = result.iloc[0]
        st.write(f"💰 **Budget:** {row['Budget']}")
        st.write("🛍 Click the link to purchase:")

        product_text = row['Recommended Product & Link']
        if "](" in product_text:
            formatted_products = product_text.replace(", ", "\n🔹 ")
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {product_text}")
    else:
        st.warning("❌ No product found for this selection.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("Next ➡"):
            st.session_state.step = 10

# --- Step 4 (Alt): Styling Product Budget ---
elif st.session_state.step == 4 and st.session_state.journey == "Styling Product Recommendations":
    budget = st.radio("Select Your Budget:", ["Under $25", "$25 & Up"])
    st.session_state.styling_budget = budget

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_back()
    with col2:
        if st.button("See Products ➡"):
            next_step()

# --- Step 5 (Alt): Show Styling Product Details ---
elif st.session_state.step == 5 and st.session_state.journey == "Styling Product Recommendations":
    result = df_styling[
        (df_styling["Styling Goal"].str.lower().str.strip() == st.session_state.styling_goal.lower().strip()) &
        (df_styling["Budget"].str.lower().str.strip() == st.session_state.styling_budget.lower().strip())
    ]

    if not result.empty:
        row = result.iloc[0]
        st.markdown(f"<h2 style='text-align:center;'>Style: {row['Styling Goal']}</h2>", unsafe_allow_html=True)
        st.write(f"✨ **Product Type:** {row['Product Type']}")
        st.write(f"📖 **Description:** {row['Description']}")
        st.write(f"💡 **How to Use:** {row['How to Use']}")

        product_text = row['Recommended Product & Link']
        if "](" in product_text:
            formatted_products = product_text.replace(", ", "\n🔹 ")
            st.markdown(f"🔹 {formatted_products}", unsafe_allow_html=True)
        else:
            st.write(f"🔹 {product_text}")
    else:
        st.warning("❌ No product found for this style + budget.")

    col1, col2 = st.columns(2)
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
    <p style='text-align:center;'>Hi, I’m Janet, a former hairstylist with 10 years of experience in the hair industry and a passion for hair education. After years of helping clients find the right products, I combined my expertise with data analytics & visualization to create an easier way to shop for hair care. ✨</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style='text-align:center;'> What This App Does ⚡</h2>
    <p style='text-align:center;'>This app takes the guesswork out of hair care by giving you personalized product recommendations based on your hair type, concerns, and budget. No more wasting money on the wrong products—just the best choices, tailored for YOU, with links to shop directly.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;'>
    <a href="https://www.amazon.com/shop/yourstore" target="_blank">Amazon Store</a> |
    <a href="https://www.instagram.com/yourhandle" target="_blank">Instagram</a> |
    <a href="https://www.tiktok.com/@yourhandle" target="_blank">TikTok</a>
    </p>
    """, unsafe_allow_html=True)

    if st.button("Start Over"):
        st.session_state.step = 1


