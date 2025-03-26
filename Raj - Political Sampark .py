import os
import subprocess
try:
    import openai
except ImportError:
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "openai"])
    import openai

import streamlit as st
from openai import OpenAI

openrouter_api_key = "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" 

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

def call_deepseek_api(prompt: str) -> str:
    """
    Call the DeepSeek model via OpenRouter API and return the generated text.
    """
    try:
        completion = client.chat.completions.create(
            extra_headers={"Authorization": f"Bearer {openrouter_api_key}"},
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling DeepSeek API: {e}")
        return "API call failed."

# --- Streamlit App UI ---
st.title("Startup Fundraising Prompt Generator using Prompt God from Raj")
st.write("Choose one of the two modes below to generate a custom fundraising prompt:")

# Mode selection: Preset or Custom
mode = st.radio("Select Prompt Mode:", options=["Preset Mode", "Custom Mode"])

if mode == "Preset Mode":
    st.subheader("Preset Prompt Generator")
    with st.form("preset_form"):
        stage = st.selectbox("Startup Stage", options=["Pre-seed", "Seed", "Series A", "Series B+"])
        industry = st.text_input("Industry (e.g., SaaS, Fintech, HealthTech)")
        investor_type = st.selectbox("Target Investors", options=["Angel Investors", "Venture Capitalists", "Crowdfunding"])
        challenge = st.text_area("Specific Challenges (optional)",
                                    help="Describe any specific issues you are facing, e.g., pitch deck, valuation concerns.")
        preset_submitted = st.form_submit_button("Generate Preset Prompt")

    if preset_submitted:
        # Craft a prompt from the selected parameters.
        preset_prompt = (
            f"How can a {industry} startup at the {stage} stage attract {investor_type}? "
            f"Consider that the founder faces the following challenge: {challenge if challenge else 'No specific challenge provided.'}"
        )
        st.subheader("Crafted Preset Prompt")
        st.code(preset_prompt, language="text")

        st.write("Contacting Prompt God The Almighty")
        with st.spinner("Wait hold on He will take few Second to reply..."):
            preset_reply = call_deepseek_api(preset_prompt)
        st.subheader("Behold Our Lord's Reply")
        st.write(preset_reply)
        st.success("Preset prompt generation complete!")

elif mode == "Custom Mode":
    st.subheader("Custom Prompt Generator")
    with st.form("custom_form"):
        custom_prompt = st.text_area("Enter your custom prompt below:", height=150,
                                        help="Type any prompt you wish. You can include as much detail as needed.")
        custom_submitted = st.form_submit_button("Generate Custom Prompt")

    if custom_submitted:
        st.subheader("Your Custom Prompt")
        st.code(custom_prompt, language="text")

        st.write("Contacting Prompt God The Almighty")
        with st.spinner("Wait hold on He will take few Second to reply..."):
            preset_reply = call_deepseek_api(custom_prompt)
        st.subheader("Behold Our Lord's Reply")
        st.write(preset_reply)
        st.success("Preset prompt generation complete!")