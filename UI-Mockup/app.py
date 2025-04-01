import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import uuid
import urllib.parse
import webbrowser

# Set page configuration
st.set_page_config(
    page_title="Class WiFi Tracker",
    page_icon="📶",
    layout="wide"
)

# Application title and description
st.title("Student WiFi Connectivity Tracker")
st.markdown("Monitor which students are connected to the WiFi network in real-time")

# Initialize session state for notifications
if 'notifications' not in st.session_state:
    st.session_state.notifications = {}

if 'notification_history' not in st.session_state:
    st.session_state.notification_history = []

# Simulate student contact info
if 'student_contacts' not in st.session_state:
    st.session_state.student_contacts = {}

# Sidebar for controls
st.sidebar.header("Controls")
refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 5, 60, 10)

# WhatsApp configuration
st.sidebar.header("WhatsApp Settings")
use_real_whatsapp = st.sidebar.checkbox("Enable WhatsApp Click-to-Chat", value=False)
default_whatsapp = st.sidebar.text_input("Your WhatsApp Number (for testing)", placeholder="e.g. +1234567890")

# Notification methods in sidebar
st.sidebar.header("Notification Settings")
notification_methods = st.sidebar.multiselect(
    "Notification Methods",
    ["App", "WhatsApp", "Email"],
    default=["App"]
)

# Program filter in sidebar
st.sidebar.header("Filters")
program_filter = st.sidebar.multiselect(
    "Filter by Program",
    ["Masters", "Bachelors"],
    default=["Masters", "Bachelors"]
)

# Add career filter
careers = ["Computer Science", "Engineering", "Business", "Arts", "Medicine", "Physics", "Mathematics"]
career_filter = st.sidebar.multiselect(
    "Filter by Career",
    careers,
    default=careers
)

show_only_online = st.sidebar.checkbox("Show only online students")

# Function to simulate checking WiFi status
def check_wifi_status(student_id):
    # In a real application, this would check actual WiFi connectivity
    # For demo purposes, we're using random status with persistence
    random.seed(student_id + int(time.time() / refresh_rate))
    return random.random() > 0.3  # 70% chance of being online

# Sample student data with more students
@st.cache_data
def load_student_data():
    # First names and last names for generating more students
    first_names = [
        "John", "Emma", "Michael", "Sophia", "Robert", "Olivia", "William", "Ava", 
        "James", "Isabella", "Alex", "Mia", "David", "Charlotte", "Joseph", "Amelia",
        "Daniel", "Harper", "Matthew", "Evelyn", "Andrew", "Abigail", "Ethan", "Emily",
        "Jacob", "Elizabeth", "Noah", "Sofia", "Logan", "Avery", "Benjamin", "Ella",
        "Samuel", "Scarlett", "Henry", "Grace", "Jackson", "Chloe", "Sebastian", "Victoria"
    ]
    
    last_names = [
        "Smith", "Johnson", "Brown", "Williams", "Jones", "Davis", "Miller", "Wilson",
        "Moore", "Taylor", "Rodriguez", "Martinez", "Anderson", "Thomas", "Jackson", "White",
        "Harris", "Martin", "Thompson", "Garcia", "Clark", "Lewis", "Lee", "Walker",
        "Hall", "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker",
        "Adams", "Nelson", "Hill", "Ramirez", "Campbell", "Mitchell", "Roberts", "Carter"
    ]
    
    # Generate 40 students
    num_students = 40
    data = {
        'name': [],
        'student_id': list(range(1001, 1001 + num_students)),
        'program': [],
        'career': [],
        'last_seen': [],
        'attendance_record': []
    }
    
    # Generate random student data
    for i in range(num_students):
        # Random name
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        data['name'].append(name)
        
        # Random program
        program = random.choice(["Masters", "Bachelors"])
        data['program'].append(program)
        
        # Random career
        career = random.choice(careers)
        data['career'].append(career)
        
        # Initial last seen time
        data['last_seen'].append(datetime.now().strftime("%H:%M:%S"))
        
        # Attendance record (0-100%)
        data['attendance_record'].append(random.randint(70, 100))
    
    return pd.DataFrame(data)

students = load_student_data()

# Generate simulated contact info for students
def generate_student_contacts():
    contacts = {}
    for student_id in students['student_id']:
        student_name = students.loc[students['student_id'] == student_id, 'name'].values[0]
        first_name = student_name.split()[0].lower()
        last_name = student_name.split()[1].lower()
        
        # Create simulated WhatsApp number and email
        # Using consistent numbers helps with testing
        whatsapp = f"+1{student_id}000000"  # Use student ID as part of number for consistency
        email = f"{first_name}.{last_name}@university.edu"
        
        contacts[student_id] = {
            'whatsapp': whatsapp,
            'email': email
        }
    
    return contacts

# Initialize student contacts if not exists
if not st.session_state.student_contacts:
    st.session_state.student_contacts = generate_student_contacts()

# Function to create WhatsApp click-to-chat link
def get_whatsapp_chat_link(phone_number, message):
    # Format the message for URL
    encoded_message = urllib.parse.quote(message)
    # WhatsApp click-to-chat URL format
    whatsapp_url = f"https://wa.me/{phone_number.replace('+', '')}?text={encoded_message}"
    return whatsapp_url

# Function to create notification message based on type
def create_notification_message(student_name, message_type):
    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%H:%M")
    
    if message_type == "absent":
        return (f"Dear {student_name},\n\n"
                f"Our records indicate that you have been absent from class on {current_date}. "
                f"Please be reminded that regular attendance is required as per university policy. "
                f"If you have any concerns, please contact your instructor.\n\n"
                f"Time of notification: {current_time}")
    else:  # late
        return (f"Dear {student_name},\n\n"
                f"This is a friendly reminder about your attendance. Our records show inconsistent "
                f"attendance patterns. Please note that maintaining good attendance is important "
                f"for your academic success.\n\n"
                f"Time of notification: {current_time}")

# Function to simulate sending a notification via different channels
def simulate_send_notification(student_id, channels, message_type):
    status = []
    student_name = students.loc[students['student_id'] == student_id, 'name'].values[0]
    notification_text = create_notification_message(student_name, message_type)
    
    whatsapp_link = None
    
    for channel in channels:
        if channel == "WhatsApp":
            # Get the WhatsApp number (either default or student's)
            if use_real_whatsapp and default_whatsapp:
                whatsapp_num = default_whatsapp.strip()
                if not whatsapp_num.startswith("+"):
                    whatsapp_num = "+" + whatsapp_num
            else:
                whatsapp_num = st.session_state.student_contacts[student_id]['whatsapp']
            
            # Create WhatsApp click-to-chat link
            whatsapp_link = get_whatsapp_chat_link(whatsapp_num, notification_text)
            status.append(f"WhatsApp message ready for {whatsapp_num}")
        
        elif channel == "Email":
            # Simulate email sending
            email = st.session_state.student_contacts[student_id]['email']
            # In a real app, you would use SMTP or an email service like SendGrid
            status.append(f"Email sent to {email}")
    
    return status, whatsapp_link

# Function to send notification
def send_notification(student_id, message_type):
    student_name = students.loc[students['student_id'] == student_id, 'name'].values[0]
    notification_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if message_type == "absent":
        message = f"Absence notification sent to {student_name}"
    else:  # late
        message = f"Attendance warning sent to {student_name}"
    
    # Get the selected notification methods
    channels = notification_methods
    
    # Simulate sending notifications via selected channels
    delivery_status = []
    whatsapp_link = None
    if "WhatsApp" in channels or "Email" in channels:
        delivery_status, whatsapp_link = simulate_send_notification(student_id, channels, message_type)
    
    # Add to notification history
    st.session_state.notification_history.append({
        'id': notification_id,
        'student_name': student_name,
        'student_id': student_id,
        'message': message,
        'type': message_type,
        'timestamp': timestamp,
        'channels': ", ".join(channels),
        'delivery_status': ", ".join(delivery_status) if delivery_status else "App notification only",
        'whatsapp_link': whatsapp_link
    })
    
    # Limit history to last 20 notifications
    if len(st.session_state.notification_history) > 20:
        st.session_state.notification_history = st.session_state.notification_history[-20:]
    
    # Mark as sent in session state
    st.session_state.notifications[student_id] = {
        'sent': True,
        'timestamp': timestamp,
        'type': message_type,
        'channels': channels,
        'whatsapp_link': whatsapp_link
    }
    
    return notification_id, delivery_status, whatsapp_link

# Function to update status
def update_status():
    now = datetime.now().strftime("%H:%M:%S")
    now_dt = datetime.now()
    
    for i, student in enumerate(students['student_id']):
        is_online = check_wifi_status(student)
        if is_online:
            students.at[i, 'last_seen'] = now
    
    students['status'] = students['student_id'].apply(lambda id: check_wifi_status(id))
    students['status_display'] = students['status'].apply(
        lambda x: "🟢 Online" if x else "🔴 Offline"
    )
    
    # Calculate how long since last seen
    students['time_difference'] = students['last_seen'].apply(
        lambda x: (now_dt - datetime.strptime(x, "%H:%M:%S")).total_seconds() if x else 0
    )
    
    return students

# Create auto-refresh mechanism
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
if current_time - st.session_state.last_refresh > refresh_rate:
    st.session_state.last_refresh = current_time

# Update and display student data
updated_students = update_status()

# Apply all filters
display_students = updated_students

# Filter by program
if program_filter:
    display_students = display_students[display_students['program'].isin(program_filter)]

# Filter by career
if career_filter:
    display_students = display_students[display_students['career'].isin(career_filter)]

# Filter by online status
if show_only_online:
    display_students = display_students[display_students['status'] == True]

# Tabs for main content
tab1, tab2, tab3 = st.tabs(["Student Status", "Notification History", "Contact Info"])

with tab1:
    # Display automatic refresh indicator
    st.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')} (auto-refreshes every {refresh_rate} seconds)")
    col_refresh, _ = st.columns([1, 3])
    with col_refresh:
        if st.button("Refresh Now"):
            st.experimental_rerun()

    # Display student information with styling
    online_count = len(display_students[display_students['status'] == True])
    total_count = len(display_students)
    st.header(f"Students ({online_count}/{total_count} online)")

    # Create two columns for better visualization
    col1, col2 = st.columns([3, 1])

    with col1:
        # Create a styled dataframe with notification status column
        display_df = display_students.copy()
        
        # Add a column that shows if notification has been sent
        display_df['notification_status'] = display_df['student_id'].apply(
            lambda x: "Sent" if x in st.session_state.notifications else ""
        )
        
        # Create styled dataframe
        styled_df = display_df[['name', 'program', 'career', 'status_display', 'attendance_record', 'last_seen', 'notification_status']].copy()
        styled_df.columns = ['Name', 'Program', 'Career', 'Status', 'Attendance %', 'Last Seen', 'Notification']
        
        # Create a function for conditional coloring
        def highlight_status(val):
            if val == "🟢 Online":
                return 'background-color: #d4edda; color: #155724'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        
        def highlight_attendance(val):
            if val >= 90:
                return 'background-color: #d4edda; color: #155724'
            elif val >= 80:
                return 'background-color: #fff3cd; color: #856404'
            else:
                return 'background-color: #f8d7da; color: #721c24'
        
        def highlight_notification(val):
            if val == "Sent":
                return 'background-color: #cfe2ff; color: #084298'
            else:
                return ''
        
        # Apply styling
        styled = styled_df.style.applymap(
            highlight_status, 
            subset=['Status']
        ).applymap(
            highlight_attendance,
            subset=['Attendance %']
        ).applymap(
            highlight_notification,
            subset=['Notification']
        )
        
        st.dataframe(
            styled, 
            height=500,
            use_container_width=True,
            hide_index=True
        )
        
        # Create a separate section for notification actions
        st.subheader("Send Notifications")
        
        # Notification container
        notification_container = st.container()
        
        with notification_container:
            notif_col1, notif_col2, notif_col3 = st.columns(3)
            
            with notif_col1:
                selected_student = st.selectbox(
                    "Select Student", 
                    options=display_df['student_id'].tolist(),
                    format_func=lambda x: display_df.loc[display_df['student_id'] == x, 'name'].iloc[0]
                )
                
            with notif_col2:
                notification_type = st.selectbox(
                    "Notification Type",
                    options=["Absence Alert", "Attendance Warning"]
                )
                
            with notif_col3:
                st.write("")  # Add some space
                st.write("")  # Add some space
                if st.button("Send Notification"):
                    message_type = "absent" if notification_type == "Absence Alert" else "late"
                    notification_id, delivery_status, whatsapp_link = send_notification(selected_student, message_type)
                    
                    success_message = f"Notification sent! ID: {notification_id[:8]}"
                    if delivery_status:
                        success_message += f"\n{'; '.join(delivery_status)}"
                    
                    st.success(success_message)
                    
                    # Display WhatsApp link if available
                    if whatsapp_link and "WhatsApp" in notification_methods:
                        st.markdown(f"[Click here to open WhatsApp and send message]({whatsapp_link})", unsafe_allow_html=True)

    with col2:
        # Show summary statistics
        total = len(display_students)
        online = len(display_students[display_students['status'] == True])
        
        st.metric("Total Students", total)
        st.metric("Online Students", online, f"{int(online/total*100)}%" if total > 0 else "0%")
        
        # Stats by program
        st.subheader("By Program")
        for program in program_filter:
            prog_total = len(display_students[display_students['program'] == program])
            prog_online = len(display_students[(display_students['program'] == program) & 
                                            (display_students['status'] == True)])
            if prog_total > 0:
                st.metric(f"{program}", f"{prog_online}/{prog_total}", 
                        f"{int(prog_online/prog_total*100)}%")
        
        # Stats by career
        st.subheader("By Career")
        for career in career_filter:
            career_total = len(display_students[display_students['career'] == career])
            career_online = len(display_students[(display_students['career'] == career) & 
                                            (display_students['status'] == True)])
            if career_total > 0:
                st.metric(f"{career}", f"{career_online}/{career_total}", 
                        f"{int(career_online/career_total*100)}%" if career_total > 0 else "0%")

with tab2:
    # Display notification history
    st.header("Notification History")
    
    if st.session_state.notification_history:
        # Display notification history cards for better UI
        for i, notification in enumerate(reversed(st.session_state.notification_history)):
            with st.container():
                cols = st.columns([2, 3])
                
                with cols[0]:
                    st.subheader(f"{notification['student_name']}")
                    st.caption(f"Time: {notification['timestamp']}")
                    st.caption(f"ID: {notification['id'][:8]}")
                
                with cols[1]:
                    message_color = "#721c24" if notification['type'] == 'absent' else "#856404"
                    st.markdown(f"<div style='color: {message_color};'>{notification['message']}</div>", unsafe_allow_html=True)
                    st.caption(f"Channels: {notification['channels']}")
                    st.caption(f"Status: {notification['delivery_status']}")
                    
                    # Show WhatsApp link if available
                    if notification.get('whatsapp_link') and "WhatsApp" in notification['channels']:
                        st.markdown(f"[Send WhatsApp Message]({notification['whatsapp_link']})", unsafe_allow_html=True)
                
                st.markdown("---")
        
        if st.button("Clear History"):
            st.session_state.notification_history = []
            st.session_state.notifications = {}
            st.experimental_rerun()
    else:
        st.info("No notifications have been sent yet.")

with tab3:
    # Display student contact information
    st.header("Student Contact Information")
    
    contact_data = []
    for student_id in display_students['student_id']:
        student_name = display_students.loc[display_students['student_id'] == student_id, 'name'].values[0]
        whatsapp = st.session_state.student_contacts[student_id]['whatsapp']
        email = st.session_state.student_contacts[student_id]['email']
        
        contact_data.append({
            'Student ID': student_id,
            'Name': student_name,
            'WhatsApp': whatsapp,
            'Email': email
        })
    
    contact_df = pd.DataFrame(contact_data)
    
    # Create two columns for contact list and actions
    contact_col1, contact_col2 = st.columns([3, 1])
    
    with contact_col1:
        st.dataframe(contact_df, use_container_width=True, hide_index=True)
    
    with contact_col2:
        st.subheader("Actions")
        
        # Option to download contact info as CSV
        csv = contact_df.to_csv(index=False)
        st.download_button(
            label="Download Contact List",
            data=csv,
            file_name="student_contacts.csv",
            mime="text/csv"
        )
        
        # Option to update contacts
        if st.button("Reset Contact Info"):
            st.session_state.student_contacts = generate_student_contacts()
            st.experimental_rerun()
        
        st.write("---")
        
        # WhatsApp test section
        st.subheader("Test WhatsApp")
        test_message = st.text_area("Test message", "Hello! This is a test message from the WiFi Tracker system.")
        test_number = st.text_input("WhatsApp number", default_whatsapp if default_whatsapp else "", placeholder="+1234567890")
        
        if st.button("Open WhatsApp"):
            if test_number:
                test_link = get_whatsapp_chat_link(test_number, test_message)
                webbrowser.open(test_link)
                st.success("WhatsApp should open in your browser or app!")
            else:
                st.error("Please enter a WhatsApp number")

# Footer
st.markdown("---")
st.caption("For demonstration purposes only. In a real application, this would connect to your WiFi network API, WhatsApp Business API, and email services.")