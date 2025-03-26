import streamlit as st
from openai import OpenAI
import os

# Get API key
api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

# Debugging (REMOVE in production)
st.write("API Key:", "Found" if api_key else "Missing")

if not api_key:
    st.error("API key is missing. Please set it in Streamlit secrets or environment variables.")
    st.stop()

# Set environment variable (if needed)
os.environ["OPENROUTER_API_KEY"] = api_key

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
)
client.api_key = api_key  # Ensure API key is assigned

def call_deepseek_api(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return completion.choices[0].message.content if completion.choices else "Empty response."
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return "API call failed."

# --- Streamlit App UI ---
st.title("Startup Fundraising Prompt Generator using Prompt God from Raj")
st.write("Choose one of the two modes below to generate a custom fundraising prompt:")

# Mode selection
mode = st.radio("Select Prompt Mode:", options=["Preset Mode", "Custom Mode"], horizontal=True)

if mode == "Preset Mode":
    st.subheader("Preset Prompt Generator")
    with st.form("preset_form"):
        # Required fields
        stage = st.selectbox("Startup Stage", options=["Pre-seed", "Seed", "Series A", "Series B+"])
        industry = st.text_input("Industry (e.g., SaaS, Fintech, HealthTech)", placeholder="Enter your industry")
        investor_type = st.selectbox("Target Investors", options=["Angel Investors", "Venture Capitalists", "Crowdfunding"])
        
        # Optional field
        challenge = st.text_area("Specific Challenges (optional)", 
                               help="Describe any specific issues you are facing, e.g., pitch deck, valuation concerns.",
                               placeholder="No specific challenges mentioned")
        
        preset_submitted = st.form_submit_button("Generate Preset Prompt")

    if preset_submitted:
        # Validate required fields
        if not industry.strip():
            st.warning("Please fill in the Industry field")
            st.stop()
            
        # Build the prompt
        challenge_text = challenge if challenge.strip() else "No specific challenges mentioned"
        preset_prompt = (
            f"As an expert startup fundraising advisor, how should a {industry.strip()} startup "
            f"at the {stage} stage approach {investor_type}? "
            f"Address these specific challenges: {challenge_text}. "
            "Provide actionable strategies and common pitfalls to avoid."
        )

        # Display and process
        st.subheader("Crafted Preset Prompt")
        st.code(preset_prompt, language="text")

        with st.spinner("Contacting Prompt God The Almighty..."):
            preset_reply = call_deepseek_api(preset_prompt)
            
        st.subheader("Behold Our Lord's Reply 🙏")
        st.markdown(preset_reply)
        st.success("Preset prompt generation complete!")

elif mode == "Custom Mode":
    st.subheader("Custom Prompt Generator")
    with st.form("custom_form"):
        custom_prompt = st.text_area("Enter your custom prompt below:", 
                                   height=150,
                                   placeholder="e.g., 'How to negotiate valuation with Series A investors in AI space?'",
                                   help="Type any fundraising-related prompt you need help with.")
        custom_submitted = st.form_submit_button("Generate Custom Prompt")

    if custom_submitted:
        if not custom_prompt.strip():
            st.warning("Please enter a custom prompt")
            st.stop()

        st.subheader("Your Custom Prompt")
        st.code(custom_prompt, language="text")

        with st.spinner("Contacting Prompt God The Almighty..."):
            custom_reply = call_deepseek_api(custom_prompt.strip())  # Fixed variable name
            
        st.subheader("Behold Our Lord's Reply 🙏")
        st.markdown(custom_reply)
        st.success("Custom prompt generation complete!")  # Fixed success message