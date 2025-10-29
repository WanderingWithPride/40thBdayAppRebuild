import streamlit as st

st.title("What Token Does Streamlit See?")

# What's in the file?
st.header("1. What's in secrets.toml file:")
try:
    with open('.streamlit/secrets.toml', 'r') as f:
        lines = [line for line in f if 'GITHUB_TOKEN' in line and not line.strip().startswith('#')]
        if lines:
            token_line = lines[0]
            token = token_line.split('"')[1]
            st.code(f"File has: {token[:30]}...{token[-20:]}")
            st.text(f"Length: {len(token)}")
except Exception as e:
    st.error(f"Error reading file: {e}")

# What does st.secrets have?
st.header("2. What does st.secrets have:")
try:
    if hasattr(st, 'secrets') and 'GITHUB_TOKEN' in st.secrets:
        token = st.secrets['GITHUB_TOKEN']
        st.code(f"st.secrets has: {token[:30]}...{token[-20:]}")
        st.text(f"Length: {len(token)}")
    else:
        st.error("st.secrets doesn't have GITHUB_TOKEN!")
except Exception as e:
    st.error(f"Error: {e}")

# Are they the same?
st.header("3. Do they match?")
try:
    with open('.streamlit/secrets.toml', 'r') as f:
        lines = [line for line in f if 'GITHUB_TOKEN' in line and not line.strip().startswith('#')]
        file_token = lines[0].split('"')[1]

    streamlit_token = st.secrets['GITHUB_TOKEN']

    if file_token == streamlit_token:
        st.success("✅ YES - They match!")
    else:
        st.error("❌ NO - They are different!")
        st.text(f"File:      {file_token[:30]}...{file_token[-20:]}")
        st.text(f"Streamlit: {streamlit_token[:30]}...{streamlit_token[-20:]}")
except Exception as e:
    st.error(f"Error comparing: {e}")

st.markdown("---")
st.markdown("**If they don't match, Streamlit has cached the old token!**")
