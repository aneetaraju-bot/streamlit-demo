import streamlit as st

st.title("🚀 Hello Streamlit!")
st.write("This is my first app online using Streamlit Cloud.")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Exam Score Visualizer", layout="centered")
st.title("📊 Exam Score Visualizer")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        
        st.subheader("📄 Data Preview")
        st.dataframe(df)

        # Ensure correct columns
        required_columns = {"Student Name", "Exam", "Score"}
        if required_columns.issubset(df.columns):
            df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
            df = df.dropna(subset=["Score"])

            # Step 2: Select exam
            exam_list = df["Exam"].unique()
            selected_exam = st.selectbox("📌 Select an Exam", exam_list)

            # Step 3: Filter and visualize
            filtered_df = df[df["Exam"] == selected_exam]

            st.subheader(f"📊 Scores in {selected_exam}")
            st.bar_chart(filtered_df.set_index("Student Name")["Score"])

        else:
            st.error("❌ CSV must contain 'Student Name', 'Exam', and 'Score' columns.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload a CSV file to begin.")
