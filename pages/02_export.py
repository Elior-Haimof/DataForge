import streamlit as st
import time
import base64
import pandas as pd
import os
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="DataForge | Data Intake", layout="wide", page_icon="⚒️")



# Helper function to load images
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None
# Loading images 
Export_icon_base64 = get_base64_image("assets/Export.png")
DataForgeLogo_base64 = get_base64_image("assets/DataForgeLogo_no_wording.png")

# ---- CUSTOM CSS ---- #

st.markdown(f"""
<style>

    /* 1. ----TITLE---- */
            
    /* Removes DEFAULT PADDING to make title in the an asthethic position */
    .block-container {{
        padding-top: 4rem;
        padding-bottom: 3rem;
    }}
        
           
    /* ----SIDEBAR---- */
            
    /* Hides the automatic Streamlit page navigation list */
    [data-testid="stSidebarNav"] {{
        display: none;
    }}

    /* styling */  
    [data-testid="stSidebar"] {{
        background-color: #a5a5a521 !important;
        border-right: 1px solid #e5e7eb;
    }}
    /* smakes it fixed sized and unchangeable */        
    section[aria-expanded="true"]
            {{min-width: 17rem !important;
            width: 17rem !important;}}
    

                       
    /* ----BUTTONS---- */
            
    div.stButton > button {{
        background-color: #ffffff !important;
        border-bottom: 2px solid #e5e7eb !important;
        position: relative !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
        border: solid 2px #a5a5a521 !important;
        font-weight: 600 !important;
        display: flex !important; 
        justify-content: center !important;
        align-items: center !important;
        margin-top: -14px !important;
    }}

    div.stButton > button:hover {{
        background-color: #a5a5a521 !important;
        border-bottom: 2px solid #e5e7eb !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(33, 115, 70, 0.3) !important;
    }}

    /* ----PAGE LINKS---- */
            
    a[data-testid="stPageLink-NavLink"] {{
        background-color: #ffffff !important;
        position: relative !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
        border: solid 2px #a5a5a521 !important;
        font-weight: 600 !important; 
        display: flex !important; 
        justify-content: center !important;
        align-items: center !important;
    }}
    
    a[data-testid="stPageLink-NavLink"]:hover {{
        background-color: #a5a5a521 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important;
    }}



 


    /* ----SUCCESS & DATA CARD---- */
    .success-card {{
        padding: 20px;
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        color: #166534;
        margin-bottom: 20px;
    }}
    
    .next-step-box {{
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
    }}


    /* ---- Summary CARD CONTAINER ---- */

    /* outer box */
 
    div[data-testid="stHorizontalBlock"]:has(.left-section):has(.right-section) {{
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 40px !important;
    box-shadow: 0px 0px 40px 10px rgba(0, 0, 0, 0.05)  !important;
    max-width: 1400px !important;
    margin: 10px auto !important;
    }}

    /* data display (LEFT COLUMN)  */
    .data-row {{
        display: flex;
        justify-content: space-between;
        align-items:center;
        align-text:center;
        padding: 12px 0;
        border-bottom: 1px solid #f1f5f9;
    }}
    .data-label {{
        font-weight: 600;
        color: #64748b;
        font-size: 0.95rem;
    }}
    .data-value {{
        font-weight: 500;
        color: #1e293b;
        font-size: 1rem;
        text-align: left;
    }}
    /* vertical divider (MIDDLE COLUMN) */
    .vertical-divider {{
        background-color: #e2e8f0;
        width: 1px;
        height: 525px;
        margin: 0 auto;
    }}
    /* system analysis (RIGHT COLUMN)  */
    .flag-box {{
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 15px;
        border-radius: 6px;
        color: #991b1b;
        margin-bottom: 20px;
    }}
    
    .ai-box {{
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 6px;
        color: #1e40af;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }}

</style>
""", unsafe_allow_html=True)


if 'df' not in st.session_state:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col1,col2 = st.columns([5, 8])
    with col2:
        st.image("assets/redirect_if_user_entered_preprocessing_first.png",width=300)

    st.markdown("""
    <div style="padding: 15px; border-radius: 5px; background-color: #FFCCCC; border-left: 5px solid #FF0000; color: black; text-align: center;">
        <b>⚠️ Looks like you tried to preprocess without uploading a CSV file!</b> Please upload one at the home page
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    if st.button("📉 Click Here to start cleaning!", type="secondary", use_container_width=True):
        st.switch_page("app.py")
        st.rerun()
    st.stop()  

# making it rain :) 
rain(    
    emoji="🎈", 
    font_size=54,
    falling_speed=5,
    animation_length=1,
)

# st.balloons()  

# ----SIDEBAR---- #
with st.sidebar:

    st.markdown("""
    <style>
        /* DataForge-Logo and text style */
        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-top: -5px !important;
            width:100px !important;
        }
        
        [data-testid="stSidebar"] h1 {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ----PROGRESS TRACKER---- #
    st.markdown("### The Workflow")
    st.success("1️⃣ **Upload Data** (Done)")
    st.success("2️⃣ **Negotiate Cleaning** (Done)")
    st.info("3️⃣ Export Results (Current)")   
    st.divider()

    # Navigation Button 

    st.markdown("### Navigation")
    st.write("Wrong Dataset?")
    st.write("")
    # Resetting the session state df if the user uploaded and continued with the wrong df (even tough he had a chance to reset last page too)
    with stylable_container(
                key='Upload_new_df',css_styles=["""
                    button{
                            background-color: #ffffff !important;
                            position: relative !important;
                            padding: 0.5rem 1rem !important;
                            border-radius: 0.5rem !important;
                            transition: all 0.3s ease !important;
                            border: solid 2px #a5a5a521 !important;
                            font-weight: 600 !important;
                            display: flex !important; 
                            justify-content: center !important;
                            align-items: center !important;
                            margin-top: -14px !important;
                            border-bottom: 2px solid #f0f2f6 !important;
                    } 
                """,
                """
                    button:hover{
                            background-color: #a5a5a521 !important;
                            border-bottom: 2px solid #e5e7eb !important;
                            transform: translateY(-2px) !important;
                            box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important;
                    }
                """,]
                ):
                    if st.button("🔄 Upload a new data set", type="secondary", use_container_width=True):
                        st.session_state['df'] = None
                        st.session_state['original_df'] = None
                        st.session_state['initial_length'] = 0
                        st.session_state['current_row_index'] = 0
                        st.session_state['mode'] = 'A'
                        st.session_state['delete_list'] = []
                        st.session_state['processed_ids'] = set()
                        del st.session_state['clean_start_time']
                        st.session_state['decision_log'] = []
                        del st.session_state['data_saved'] 
                        del st.session_state['total_flags_count']
                        st.session_state['experiment_mode'] = False
                        st.switch_page("app.py")
                        st.rerun()

    # Lower logo and branding
    st.divider()
    col1, col2 = st.columns([0.85, 3])
    with col1:
        st.image("assets/DataForgeLogo_no_wording.png", width=100)
    with col2:
        st.title("DataForge")
    
# ----HEADER AND TITLE---- #

logo_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 20px; margin-left: -15px;">
    <img src="data:image/png;base64,{DataForgeLogo_base64}" 
         style="width: 80px; height: auto; margin-right: 15px;">
    <h1 style=" padding: 0; font-size: calc(1.8rem + 1.5vw); white-space: nowrap;margin-top: 25px;">
        DataForge: Upload Data
    </h1>
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)
st.markdown("#### Congratulations! You are ready to start working")

# ----LOGS AND METRICS---- #

def calculate_metrics(log_df):
    # st.write(log_df)

    #Saving the mines as df and also calculating the amount of mines
    mines = log_df[log_df["is_mine"] == True]
    # st.write(mines)
    total_mines = len(mines)
    # st.write(total_mines)
    #False Acceptance Rate - user chose to Delete the mine when he should have Kept the row.
    Delete_on_mines =  len(mines[mines['decision'] == 'Delete'])
    False_Acceptance_Rate = (Delete_on_mines / total_mines) * 100 if total_mines > 0 else 0
    # st.write(False_Acceptance_Rate)

    #Correct Rejection Rate - user chose to Keep the mine when he should have kept it. or to Edit when he should have editted it
    Correct_mines_decision_count = 0 
    for _,row in mines.iterrows():
         if row['decision'] == row['ground_truth']: # keep on keep, edit on edit. no mine can have ground truth of delete, its against the definition of mines
            Correct_mines_decision_count +=1
     
    Correct_Rejection_Rate = (Correct_mines_decision_count / total_mines) * 100 if total_mines > 0 else 0
    # st.write(Correct_Rejection_Rate)

    #Decision Accuracy - how many times out of the negotiation card the user chose correctly
    Correct_all_decision_count = 0 
    for _,row in log_df.iterrows():
         if row['decision'] == row['ground_truth']: # keep on keep, edit on edit. no mine can have ground truth of delete, its against the definition of mines
            Correct_all_decision_count +=1
     
    Decision_Accuracy = (Correct_all_decision_count / len(log_df)) * 100 if len(log_df) > 0 else 0
    # st.write(Decision_Accuracy)
    return False_Acceptance_Rate, Correct_Rejection_Rate, Decision_Accuracy, total_mines


# ----MAIN LOGIC---- #
#saving the final df to a variable
final_df = st.session_state['df']



# ----LOGS AND METRICS---- #
log_df = pd.DataFrame(st.session_state['decision_log'])

# Total Metrics:
Total_False_Acceptance_Rate, Total_Correct_Rejection_Rate, Total_Decision_Accuracy, Total_total_mines = calculate_metrics(log_df)

# Mode A Metrics:
Mode_A_df = log_df[log_df['mode'] == 'A']
Mode_A_False_Acceptance_Rate, Mode_A_Correct_Rejection_Rate, Mode_A_Decision_Accuracy, Mode_A_total_mines = calculate_metrics(Mode_A_df)

# Mode B Metrics:
Mode_B_df = log_df[log_df['mode'] == 'B']
Mode_B_False_Acceptance_Rate, Mode_B_Correct_Rejection_Rate, Mode_B_Decision_Accuracy, Mode_B_total_mines = calculate_metrics(Mode_B_df)

# ----SAVE THE METRICS AND LOG TO A FILE---- #

output_folder = 'Study_Results'
if not os.path.exists(output_folder):
        os.makedirs(output_folder)

# Add timestamp to file name
timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{output_folder}/User_{timestamp_str}.csv"

# creating the summary dataframe
summary_data = {
    'Metric': ['False_Acceptance_Rate (%)', 'Correct_Rejection_Rate (%)', 'Decision_Accuracy (%)', 'Total Mines', 'Total Rows'],
    'Total': [Total_False_Acceptance_Rate, Total_Correct_Rejection_Rate, Total_Decision_Accuracy, Total_total_mines ,len(log_df)],
    'Mode_A': [Mode_A_False_Acceptance_Rate, Mode_A_Correct_Rejection_Rate, Mode_A_Decision_Accuracy, Mode_A_total_mines, len(Mode_A_df)],
    'Mode_B': [Mode_B_False_Acceptance_Rate, Mode_B_Correct_Rejection_Rate, Mode_B_Decision_Accuracy, Mode_B_total_mines, len(Mode_B_df)]
}
summary_df = pd.DataFrame(summary_data)

# saving only if we did not save already (prevents duplicate saves on st.rerun())
if 'data_saved' not in st.session_state:
    try:
        # saving the metrics and the log
        with open(filename, 'w', newline='') as f:
            f.write("---- STUDY SUMMARY ----\n")
            summary_df.to_csv(f, index=False)
            f.write("\n\n---- DETAILED INTERACTION LOG ----\n")
            log_df.to_csv(f, index=False)
        # updating session variable
        st.session_state['data_saved'] = True
    except Exception as e:
        st.error(f"Error saving file: {e}")




# ----SUMMARY CARD---- #

# using a container with border to contain the card
st.markdown("""
<div class="negotiation-card-wrapper">
""", unsafe_allow_html=True)

# creating 3 columns: Left (Summary) | Middle (Divider) | Right (Actions)
left,middle,right = st.columns([0.87,0.1,1])

#LEFT SECTION: Summary
with left:

    st.markdown('<div class="card-section left-section">', unsafe_allow_html=True)
    st.subheader("📃 Session Summary")
    st.markdown("---")
    
    # Stats calculation
    final_df = st.session_state['df']
    final_row_num = len(final_df)
    total_cols = len(final_df.columns)
    actions_taken = len(st.session_state.get('processed_ids', 0))
    initial_length = st.session_state['initial_length']
    rows_deleted = initial_length - final_row_num
    # calculating cleaning time
    if 'clean_start_time' in st.session_state:
        duration = datetime.now() - st.session_state['clean_start_time']
        clean_time = str(duration).split('.')[0] 
    else:
        clean_time = "0:00:00"

    # Displaying the stats

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{actions_taken}</div>
            <div class="stat-label">Cards Reviewed</div>
        </div>
        """, unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{initial_length}</div>
            <div class="stat-label">Total Initial Rows</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{final_row_num }</div>
            <div class="stat-label">Rows Preserved</div>
        </div>

        """, unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{total_cols}</div>
            <div class="stat-label">Total Columns</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{rows_deleted}</div>
            <div class="stat-label">Rows Deleted</div>
        </div>
        """, unsafe_allow_html=True)
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{clean_time}</div>
            <div class="stat-label">Clean Time</div>
        </div>
        """, unsafe_allow_html=True)
#MIDDLE SECTION: DIVIDER
with middle:
    st.markdown('<div class="vertical-divider"></div>', unsafe_allow_html=True)

#RIGHT SECTION: ACTIONS
with right:
    st.markdown('<div class="card-section right-section">', unsafe_allow_html=True)

    st.subheader("🎯Whats next?")
    st.divider()
    st.success("Cleaning complete! Download your results below.")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        # CSV Download with an uploaded picture
        st.write('')
        with stylable_container(
        key="custom_download_btn",
        css_styles=[f"""
            button {{

                background-image: url("data:image/png;base64,{Export_icon_base64}") !important;
                background-repeat: no-repeat !important;
                background-position: 5px center !important; /* Position: 15px from left, centered vertically */
                background-size: 24px 24px !important; /* Size of the icon */                
                padding-left: 50px !important;
                border: 1px solid #e2e8f0 !important;
                transition: all 0.3s ease !important;
                background-color: #ffffff !important;
                position: relative !important;
                padding: 0.5rem 1rem !important;
                border-radius: 0.5rem !important;
                box-shadow: 0px 0px 1.5px 1.5px rgba(0,0,0,0.3);
                transition: all 0.3s ease !important;
                border: solid 2px #a5a5a521 !important;
                font-weight: 750 !important;
                display: flex !important; 
                justify-content: center !important;
                align-items: center !important;
                margin-top: -14px !important;
                    }}
            
            button:hover {{
                background-color: #a5a5a521 !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important;
                /* Re-apply image on hover so it doesn't disappear */
                background-image: url("data:image/png;base64,{Export_icon_base64}") !important;
            }}
        """]
    ): 

            st.download_button('Download your perfectly cleaned data',final_df.to_csv(index=False).encode('utf-8'),'Preprocessed_data.csv', use_container_width=True)
        
    with col2:    
        # Reset everything and go back to mainpage to upload a new df
        st.write('')
        if st.button("Clean a new File 🧹", type="secondary", use_container_width=True):
            st.session_state['df'] = None
            st.session_state['original_df'] = None
            st.session_state['initial_length'] = 0
            st.session_state['current_row_index'] = 0
            st.session_state['mode'] = 'A'
            st.session_state['delete_list'] = []
            st.session_state['processed_ids'] = set()
            del st.session_state['clean_start_time']
            st.session_state['decision_log'] = []
            del st.session_state['data_saved'] 
            del st.session_state['total_flags_count']
            st.session_state['experiment_mode'] = False
            st.switch_page("app.py")
            st.rerun()

    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    
    st.divider()
    st.markdown(f"""
    <div class="system-flag-box">
        <strong style="color: rgb(0 39 200); font-size: 1.3rem;">😁 Thanks for using DataForge! </strong><br>
        <span style="color: rgb(0 39 200);font-size: 1.3rem;margin-left: 34px;">  We are happy we could help, come back anytime!<b></b> </span>
    </div>
    """, unsafe_allow_html=True)


    