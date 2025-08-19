import pandas as pd
import plotly.express as px
import streamlit as st

# Load dataset
df = pd.read_csv("Preprocessed_DataJobSeeker.csv")



# Title and description
st.subheader("Final Summary of Removed Columns – Data Preprocessing")
st.write("""
This table highlights the final set of columns removed from the dataset after thorough preprocessing. 
These columns were excluded due to reasons like high null values, sensitive content, incorrect formatting, or lack of analytical relevance.
""")

# Data for final removed columns
data = {
    "Column": [
        "`usernameEdistrict`",
        "`Is_Archival`, `ArogyaSetu`, `satyapan_done`, `CheckFlag`, `AadharFlag`, `old_reg_YN`, `lock`",
        "`NewPassword`, `NewPassFlag`, `userActiveDeactiveToken`, `generated_1st_pwd`, `current_pwd`",
        "`aft_satyapan_login_dt`, `sw_unique_id_create_date`",
        "`Dob`, `gender`, `Aadhar_verify_dt`, `csc_request_key`, `csc_user_type`",
        "`daily_serial_no`",
        "`username`, `sw_unique_id`",
        "`question_id`, `security_answer`, `userActiveDeactive`"
    ],
    "Reason to Leave As It Is & Not Use in Analysis": [
        "100% null",
        "Single value only",
        "Sensitive or hashed passwords",
        "Data in wrong format; expected date but is time",
        "More than 93,000 rows are missing",
        "Likely sequential and not useful",
        "Not sure what it shows",
        "Not relevant unless you're analyzing security patterns"
    ]
}

# Create DataFrame
df_removed_final = pd.DataFrame(data)

# Display in Streamlit
st.dataframe(df_removed_final, use_container_width=True)



# --- Visualization: Login Behavior Donut Chart ---
st.subheader("Login Behavior: Users Who Logged In vs Never Logged In")

# Convert date columns to datetime
df['clean_insertdate'] = pd.to_datetime(df['clean_insertdate'], errors='coerce')
df['clean_js_first_log_date'] = pd.to_datetime(df['clean_js_first_log_date'], errors='coerce')

# Categorize users
df['login_status'] = df['clean_js_first_log_date'].isna().map({True: 'Never Logged In', False: 'Logged In'})

# Count users in each category
login_counts = df['login_status'].value_counts().reset_index()
login_counts.columns = ['Login Status', 'Count']

# Plot using Plotly (Donut Chart)
fig = px.pie(login_counts, 
             names='Login Status', 
             values='Count',
             hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Pastel,
             width=550,
             height=400)

fig.update_traces(textposition='inside', textinfo='percent+label')

# Display in Streamlit
st.plotly_chart(fig)

st.markdown("**Summary:**<br>Out of all the users who signed up on the platform, 93.8% have logged in at least once, while 6.2% have never logged in.", unsafe_allow_html=True)



# --- Visualization: Time to Login Distribution ---
st.subheader("Distribution of Time Taken by Users to Log In After Signup")

# Drop rows where either date is missing
df_filtered = df.dropna(subset=['clean_insertdate', 'clean_js_first_log_date'])

# Convert to datetime if not already
df_filtered['clean_insertdate'] = pd.to_datetime(df_filtered['clean_insertdate'], errors='coerce')
df_filtered['clean_js_first_log_date'] = pd.to_datetime(df_filtered['clean_js_first_log_date'], errors='coerce')

# Calculate time difference in days
df_filtered['days_to_login'] = (df_filtered['clean_js_first_log_date'] - df_filtered['clean_insertdate']).dt.days

# Filter out negative values
df_filtered = df_filtered[df_filtered['days_to_login'] >= 0]

# Calculate average
average_days = df_filtered['days_to_login'].mean()
st.write(f"📊 **Average time to login:** `{average_days:.2f}` days")

# Plot histogram
fig = px.histogram(
    df_filtered,
    x='days_to_login',
    nbins=180,
    labels={'days_to_login': 'Days from Signup to First Login'},
    color_discrete_sequence=['#00bcd4']
)

fig.update_layout(
    xaxis_title='Days to Login',
    yaxis_title='Number of Users',
    width=700,
    height=450
)

st.plotly_chart(fig)

st.markdown("**Summary:**<br>Most of the people LogIn within 1-2 days after SignUp", unsafe_allow_html=True)



# --- Visualization: Distribution of Login Attempts ---
st.subheader("Distribution of Login Attempts per User")

# Drop missing values from LoginAttempts column
login_freq = df['LoginAttempts'].dropna()

# Plot histogram
fig = px.histogram(
    login_freq,
    x="LoginAttempts",
    nbins=30,
    labels={"LoginAttempts": "Number of Logins"},
    color_discrete_sequence=["#96b6c5"]
)

fig.update_layout(
    xaxis_title="Number of Logins",
    yaxis_title="Number of Users",
    bargap=0.1,
    xaxis_range=[0, 10]
)

# Display chart in Streamlit
st.plotly_chart(fig)

st.markdown("**Summary:**<br>Only 1-2 Login attempts are made per user", unsafe_allow_html=True)



# --- Visualization: Verification Status ---
st.subheader("Jobseeker Verification Status")

# Map and count verified vs. not verified users
verification_counts = df['is_verified'].map({0: 'Verified', 1: 'Not Verified'}).value_counts().reset_index()
verification_counts.columns = ['Verification Status', 'Count']

# Plot Pie Chart
fig = px.pie(
    verification_counts,
    names='Verification Status',
    values='Count',
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(width=400, height=400)

# Display in Streamlit
st.plotly_chart(fig)

st.markdown("**Summary:**<br>More than 93% of users have verified email_id and phone_no", unsafe_allow_html=True)



# Title
st.subheader("Login Behavior vs Verification Status")

# Convert login date column to datetime
df['clean_js_first_log_date'] = pd.to_datetime(df['clean_js_first_log_date'], errors='coerce')

# Create login behavior column
df['login_status'] = df['clean_js_first_log_date'].isna().map({True: 'Never Logged In', False: 'Logged In'})

# Map is_verified to meaningful labels
df['verification_status'] = df['is_verified'].map({0: 'Verified', 1: 'Not Verified'})

# Group data
grouped = df.groupby(['verification_status', 'login_status']).size().reset_index(name='Count')

# Plot using Plotly
fig = px.bar(
    grouped,
    x='verification_status',
    y='Count',
    color='login_status',
    barmode='group',
    labels={
        'verification_status': 'Verification Status',
        'Count': 'Number of Users',
        'login_status': 'Login Behavior'
    },
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_layout(width=700, height=450)

# Display plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("**Summary:**<br>Verified people are more logged_in than not_verified ones", unsafe_allow_html=True)



# --- Visualization: Most Commonly Used Browsers ---
st.subheader("Most Commonly Used Browsers by Jobseekers")

# Ensure 'js_browser_name' column exists and drop missing values
if 'js_browser_name' in df.columns:
    df_browser = df[['js_browser_name']].dropna().copy()
    browser_counts = df_browser['js_browser_name'].value_counts().reset_index()
    browser_counts.columns = ['Browser', 'Count']

    # Plot bar chart
    fig1 = px.bar(
        browser_counts,
        x='Browser',
        y='Count',
        color='Browser',
        color_discrete_sequence=px.colors.qualitative.Set2,
        text='Count'
    )

    fig1.update_layout(
        xaxis_title="Browser",
        yaxis_title="Number of Users",
        height=400
    )

    # Display in Streamlit
    st.plotly_chart(fig1)
else:
    st.warning("Column 'js_browser_name' not found in the dataset.")

st.markdown("**Summary:**<br>Most of the jobseekers use Chrome browser, followed by Firefox and Edge.", unsafe_allow_html=True)



# --- Visualization: Top 10 Browser + Version Combinations ---
st.subheader("Top 10 Browser & Version Combinations")

# Ensure the necessary columns exist and are not null
if 'js_browser_name' in df.columns and 'js_browser_version' in df.columns:
    # Drop missing values and create a clean copy
    df_browser_combo = df[['js_browser_name', 'js_browser_version']].dropna().copy()

    # Group and get counts
    combo_counts = (
        df_browser_combo
        .groupby(['js_browser_name', 'js_browser_version'], as_index=False)
        .size()
        .rename(columns={'size': 'Count'})
        .sort_values(by='Count', ascending=False)
        .head(10)
    )

    # Create new column for combined browser-version
    combo_counts['Browser_Version'] = combo_counts['js_browser_name'] + " " + combo_counts['js_browser_version'].astype(str)

    # Create plot
    fig2 = px.bar(
        combo_counts,
        x='Browser_Version',
        y='Count',
        color='Browser_Version',
        text='Count',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig2.update_layout(
        xaxis_title="Browser + Version",
        yaxis_title="Number of Users",
        height=450,
        showlegend=False
    )

    st.plotly_chart(fig2)

else:
    st.error("Required columns 'js_browser_name' and 'js_browser_version' not found in DataFrame.")



st.subheader("User Drop-off Funnel: Signup → Verify → Login")

# Make a copy of the DataFrame to avoid chained assignment issues
df_copy = df.copy()

# Ensure necessary columns exist
required_cols = ['clean_insertdate', 'clean_js_first_log_date', 'is_verified']
if all(col in df_copy.columns for col in required_cols):
    # Convert date columns to datetime safely
    df_copy.loc[:, 'clean_insertdate'] = pd.to_datetime(df_copy['clean_insertdate'], errors='coerce')
    df_copy.loc[:, 'clean_js_first_log_date'] = pd.to_datetime(df_copy['clean_js_first_log_date'], errors='coerce')

    # Step 1: Signed Up (has insertdate)
    signup_count = df_copy['clean_insertdate'].notna().sum()

    # Step 2: Verified (is_verified == 0) and has insertdate
    verified_count = df_copy[(df_copy['is_verified'] == 0) & (df_copy['clean_insertdate'].notna())].shape[0]

    # Step 3: Logged In (has login date)
    login_count = df_copy['clean_js_first_log_date'].notna().sum()

    # Prepare funnel data
    funnel_data = pd.DataFrame({
        'Step': ['Logged In', 'Verified', 'Signed Up'],
        'Users': [login_count, verified_count, signup_count]
    })

    # Funnel chart
    fig = px.funnel(
        funnel_data,
        x='Users',
        y='Step',
        text='Users',
        color='Step',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        xaxis_title='Number of Users',
        yaxis_title='Funnel Stage',
        height=500
    )

    st.plotly_chart(fig)

else:
    st.error("One or more required columns are missing in the dataset.")

st.markdown("**Summary:**<br>Out of 100,000 users who signed up, 93.6% got verified and 93.8% logged in, indicating a highly effective process with minimal drop-off.", unsafe_allow_html=True)



st.subheader("Daily User Registrations Over Time")

# Make a safe copy of the DataFrame
df_copy = df.copy()

# Convert insert date to datetime using .loc to avoid chained assignment
df_copy.loc[:, 'clean_insertdate'] = pd.to_datetime(df_copy['clean_insertdate'], errors='coerce')

# Drop rows with missing insert dates
df_clean = df_copy[df_copy['clean_insertdate'].notna()].copy()

# Group by date and count registrations
daily_reg = df_clean.groupby(df_clean['clean_insertdate'].dt.date).size().reset_index(name='Registrations')
daily_reg.rename(columns={daily_reg.columns[0]: 'Date'}, inplace=True)

# Plot using Plotly line chart
fig = px.line(
    daily_reg,
    x='Date',
    y='Registrations',
    labels={'Date': 'Date', 'Registrations': 'Number of Registrations'},
    markers=True
)

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Number of Registrations',
    height=500,
    width=800
)

# Display in Streamlit
st.plotly_chart(fig)

st.markdown("**Summary:**<br>There was a significant spike in daily user registrations starting January 2016, with activity peaking above 1,200 registrations per day. Before this, registrations were relatively stable and lower, suggesting a major campaign, launch, or policy change that drove high user engagement in early 2016.", unsafe_allow_html=True)