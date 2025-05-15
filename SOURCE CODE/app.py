import streamlit as st
from app.login import login_page
from app.super_admin import super_admin_page
from app.dashboard import dashboard_page
from app.data_collection import data_collection_page
from app.report_control import report_control_page
from app.smart_appointment import smart_appointment_page
from app.doctor_dashboard import doctor_dashboard_page
from app.patient_portal import patient_portal_page
from app.pdf_extraction import extract_text_from_pdf
from app.model_integration import get_medicine_recommendation, parse_model_output
from app.data_analysis import load_data, filter_data, plot_donut_chart, plot_age_donut_chart

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.sidebar.title("Navigation")
        selection = st.sidebar.selectbox("Go to", [
            "Dashboard",
            "Data Collection",
            "Report Control",
            "Smart Appointment",
            "Doctor Dashboard",
            "Patient Portal",
            "Diabetic Medicine Suggestion",
            "Data Analysis"
        ])
        if selection == "Dashboard":
            dashboard_page()
        elif selection == "Data Collection":
            data_collection_page()
        elif selection == "Report Control":
            report_control_page()
        elif selection == "Smart Appointment":
            smart_appointment_page()
        elif selection == "Doctor Dashboard":
            doctor_dashboard_page()
        elif selection == "Patient Portal":
            patient_portal_page()
        elif selection == "Diabetic Medicine Suggestion":
            diabetic_medicine_suggestion_page()
        elif selection == "Data Analysis":
            data_analysis_page()
    else:
        st.sidebar.title("Navigation")
        selection = st.sidebar.selectbox("Go to", ["Admin Page", "Super Admin Login"])
        if selection == "Admin Page":
            login_page()
        elif selection == "Super Admin Login":
            super_admin_page()

def diabetic_medicine_suggestion_page():
    st.title('Diabetic Medicine Suggestion Application')
    page = st.sidebar.selectbox("Choose a page", ["Home", "Data Analysis"])
    if page == "Home":
        st.markdown(
            "<h1 style='color: red;'>This is an experimental application. Please consult a real doctor for suggestions.</h1>",
            unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file is not None:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            extracted_text = extract_text_from_pdf("temp.pdf")
            st.write("Extracted Text from PDF:")
            st.write(extracted_text)
            model_output = get_medicine_recommendation(extracted_text)
            current_condition, medicine_suggestion, treatment_suggestion = parse_model_output(model_output)
            st.write('### Current Condition of the Patient')
            st.write(current_condition)
            st.write('### Medicine Suggestion')
            st.write(medicine_suggestion)
            st.write('### Treatment Suggestion')
            st.write(treatment_suggestion)
    elif page == "Data Analysis":
        st.header("Data Analysis")
        excel_file = st.file_uploader("Upload Excel File", type=["xls", "xlsx"])
        if excel_file is not None:
            try:
                df = load_data(excel_file)
                st.write("Data preview:")
                st.write(df.head())
                filter_option = st.selectbox("Select Filter Option for Donut Chart", ["Gender", "Age", "Diabetic-Type"])
                if filter_option == "Age":
                    plot_age_donut_chart(df)
                    st.image('src/donut_chart_age.png', caption='Age Distribution')
                else:
                    plot_donut_chart(df, filter_option)
                    st.image('src/donut_chart.png', caption=f'Distribution of {filter_option}')
                st.write("Filtered data preview:")
                st.write(df)
            except ValueError as e:
                st.error(str(e))

def data_analysis_page():
    st.header("Data Analysis")
    excel_file = st.file_uploader("Upload Excel File", type=["xls", "xlsx"])
    if excel_file is not None:
        try:
            df = load_data(excel_file)
            st.write("Data preview:")
            st.write(df.head())
            filter_option = st.selectbox("Select Filter Option for Donut Chart", ["Gender", "Age", "Diabetic-Type"])
            if filter_option == "Age":
                plot_age_donut_chart(df)
                st.image('src/donut_chart_age.png', caption='Age Distribution')
            else:
                plot_donut_chart(df, filter_option)
                st.image('src/donut_chart.png', caption=f'Distribution of {filter_option}')
            st.write("Filtered data preview:")
            st.write(df)
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
