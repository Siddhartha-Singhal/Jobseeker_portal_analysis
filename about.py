import streamlit as st
import pandas as pd

st.title("Sewayojan Portal - Jobseeker Data Overview")

st.markdown("""
This dataset provides detailed information from the **Jobseeker's side** of the **Sewayojan portal**, 
an online employment platform launched by the Government of India.

The portal allows jobseekers to:
- Register and manage their profiles
- Search and apply for employment opportunities
- Track verification and submission statuses
- Monitor login attempts and account activity

This analysis focuses on understanding user registration behavior, login patterns, and other relevant indicators from the jobseeker perspective.
""")

# Define the data as a list of dictionaries
columns_data = [
    {"Column Name": "js_unique_id", "Description": "Unique identifier for each job seeker (JS)."},
    {"Column Name": "request_date", "Description": "Date when the JS made the registration or request."},
    {"Column Name": "daily_serial_no", "Description": "Serial number assigned per day for tracking new entries."},
    {"Column Name": "eng_name_of_js", "Description": "Full name of the job seeker (in English)."},
    {"Column Name": "phone_no_js", "Description": "Phone number of the job seeker."},
    {"Column Name": "js_email", "Description": "Email ID of the job seeker."},
    {"Column Name": "js_request_ip_address", "Description": "IP address from which the registration/request was made."},
    {"Column Name": "generated_1st_pwd", "Description": "System-generated initial password."},
    {"Column Name": "pwd_sent_mode", "Description": "Mode through which password was sent (SMS, email, etc.)."},
    {"Column Name": "pwd_sent_date", "Description": "Date when the password was sent to the JS."},
    {"Column Name": "js_first_log_date", "Description": "Date when the JS logged in for the first time."},
    {"Column Name": "current_pwd", "Description": "Current active password for the JS (likely hashed/encrypted)."},
    {"Column Name": "js_browser", "Description": "Browser name used by the JS (e.g., Chrome, Firefox)."},
    {"Column Name": "js_browser_ver", "Description": "Version of the browser used."},
    {"Column Name": "csc_request_key", "Description": "Unique key associated with Common Service Center (if used)."},
    {"Column Name": "csc_user_typ", "Description": "User type from CSC – operator, kiosk, etc."},
    {"Column Name": "question_id", "Description": "Security question ID selected during registration."},
    {"Column Name": "security_answer", "Description": "Answer provided for the security question."},
    {"Column Name": "prf_submitted", "Description": "Whether the profile has been submitted (Yes/No or flag)."},
    {"Column Name": "aft_satyapan_login_dt", "Description": "Login date after identity verification (satyapan)."},
    {"Column Name": "satyapan_done", "Description": "Flag indicating if verification (satyapan) is complete."},
    {"Column Name": "final_submittion_date", "Description": "Date when the final profile/form was submitted."},
    {"Column Name": "sw_unique_id", "Description": "Unique ID for the social worker (if any)."},
    {"Column Name": "sw_unique_id_create_date", "Description": "Date when the SW ID was created."},
    {"Column Name": "LastloginDate", "Description": "Most recent login date of the JS."},
    {"Column Name": "LoginAttempts", "Description": "Number of login attempts made."},
    {"Column Name": "lock", "Description": "Whether the account is locked (due to failed attempts, etc.)."},
    {"Column Name": "username", "Description": "Username used by the JS to log in."},
    {"Column Name": "old_reg_YN", "Description": "Indicates if this is an old (previously registered) user."},
    {"Column Name": "ArogyaSetu", "Description": "Indicates if Arogya Setu app status was checked (COVID-era)."},
    {"Column Name": "userActiveDeactive", "Description": "Whether the user account is currently active or deactivated."},
    {"Column Name": "userActiveDeactiveToken", "Description": "Token or reason related to account activation/deactivation."},
    {"Column Name": "Is_Archival", "Description": "Whether the record has been archived."},
    {"Column Name": "usernameEdistrict", "Description": "Alternate username or identifier from an eDistrict platform."},
    {"Column Name": "AadharFlag", "Description": "Flag showing whether Aadhaar was provided."},
    {"Column Name": "Dob", "Description": "Date of birth of the job seeker."},
    {"Column Name": "gender", "Description": "Gender of the JS."},
    {"Column Name": "Aadhar_verify_dt", "Description": "Date on which Aadhaar was verified."},
    {"Column Name": "CheckFlag", "Description": "Likely used for internal validation or admin check purposes."},
    {"Column Name": "userreg", "Description": "Flag indicating successful user registration."},
    {"Column Name": "insertdate", "Description": "Date when the user’s data was inserted into the system."},
    {"Column Name": "NewPassword", "Description": "Recently created or updated password (likely hashed)."},
    {"Column Name": "NewPassFlag", "Description": "Flag indicating if a new password was set."}
]

# Convert to DataFrame
df_columns = pd.DataFrame(columns_data)

# Streamlit output
st.header("📊 Dataset Column Descriptions")
st.dataframe(df_columns, use_container_width=True)
