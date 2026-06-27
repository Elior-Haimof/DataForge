import streamlit as st
import time
import base64
import pandas as pd
from Models.Rule_Based_Flag import get_flagged_rows
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime
import json
import os

# Page Configuration
st.set_page_config(page_title="DataForge | Data preprocessing", layout="wide", page_icon="⚒️")

# for later use in  02_export.py. this stores the initial time the user started cleaning
if 'clean_start_time' not in st.session_state: 
    st.session_state['clean_start_time'] = datetime.now()

# Helper function to load images
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


# Loading images 
DataForgeLogo_base64 = get_base64_image("assets/DataForgeLogo_no_wording.png")
Redirect_picture_base64 = get_base64_image("assets/redirect_if_user_entered_preprocessing_first.png")

# function to load the Agent_reasoning.json, caching so we dont load it every rerun
@st.cache_data
def load_agent_reasoning():
    file_path = "Agent_reasoning/Agent_reasoning.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

# calling the function toi load the reasoning
agent_reasoning_data = load_agent_reasoning()

# --- CUSTOM CSS --- #

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

    /* ---- NEGOTIATION CARD CONTAINER ---- */
            
    
    /* outer box */
 
    div[data-testid="stHorizontalBlock"]:has(.left-section):has(.right-section) {{
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 40px !important;
    box-shadow: 0px 0px 40px 10px rgba(0, 0, 0, 0.05)  !important;
    max-width: 1400px !important;
    margin: 20px auto !important;
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




# Check if user entered this page first, if so, present an error and home page redirect button
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
    st.info("2️⃣ **Negotiate Cleaning** (Current)")
    st.write("3️⃣ Export Results")   
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
                    } 
                """,
                """
                    button:hover{
                            background-color: #a5a5a521 !important;
                            transform: translateY(-2px) !important;
                            box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important;
                    }
                """,]
                ):
                    if st.button("📉 Upload a different one", type="secondary", use_container_width=True):
                        st.session_state['df'] = None
                        st.session_state['original_df'] = None
                        st.session_state['initial_length'] = 0
                        st.session_state['current_row_index'] = 0
                        st.session_state['mode'] = 'A'
                        st.session_state['delete_list'] = []
                        st.session_state['processed_ids'] = set()
                        st.session_state['clean_start'] = datetime.now()
                        st.session_state['decision_log'] = []
                        del st.session_state['clean_start_time']
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
    


# ----Log Decisions Function---- #
# This functions logs everything the user does so I can calculate the expiriment metrics

def log_decision(listing_id,row_data,decision,mode,edited_value = None,old_value = None,edited_col_name = None,edited_row_index=None):
    is_mine = row_data.get('is_mine', False)
    ground_truth = row_data.get('ground_truth', 'Unknown')
    new_log = {
        'listing_id' : listing_id,
        'decision' : decision, # if edit: I Log edit, edited_to_value
        'is_mine': is_mine,
        'mode': mode,
        'edited_value': edited_value,
        'old_value':old_value, # for undo button
        'edited_col_name':edited_col_name,   # for undo button
        'edited_row_index': edited_row_index, # for undo button
        'ground_truth': ground_truth
    }
    st.session_state['decision_log'].append(new_log)




# ----HEADER AND TITLE---- #
logo_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 20px; margin-left: -15px;">
    <img src="data:image/png;base64,{DataForgeLogo_base64}" 
         style="width: 80px; height: auto; margin-right: 15px;">
    <h1 style=" padding: 0; font-size: calc(1.8rem + 1.5vw); white-space: nowrap;margin-top: 25px;">
        DataForge: Data Preprocessing
    </h1>
</div>
"""
st.markdown(logo_html, unsafe_allow_html=True)
st.markdown("#### We suggest, you decide")


# ----SESSION STATE VARIABLES---- #
df = st.session_state['df'] # the uploaded DF
current_row_index = st.session_state['current_row_index'] # Corrent row index, to determine if mode A or B needs to be initiated




# ----MAIN LOGIC---- #

flagged_rows = get_flagged_rows(df) # Calling my statistical rule based model to flag the anomaly rows

# negotiation card counter and progress
if 'total_flags_count' not in st.session_state or len(st.session_state['processed_ids']) == 0:
    st.session_state['total_flags_count'] = len(flagged_rows)

# current negotiation card number and out of how many cards
current_card_num = len(st.session_state['processed_ids']) + 1
total_cards = st.session_state['total_flags_count']


if current_row_index < len(flagged_rows): # only showing flagged rows

    # Saving current row as a variable
    flagged_row = flagged_rows[current_row_index]
    flag_reason =''
    if flagged_row['rule_triggered'] == 'Small_size':
        flag_reason = 'Apartment is too small to be valid'
    elif flagged_row['rule_triggered'] == 'High_price':
        flag_reason = 'Apartment price is 3-std bigger then the Mean'
    elif flagged_row['rule_triggered'] == 'Inconsistent':
        flag_reason = 'Invalid Categorical value'
    elif flagged_row['rule_triggered'] == 'Invalid_size':
        flag_reason = 'Apartment is too small to be valid' 
    elif flagged_row['rule_triggered'] == ' Too_big':
        flag_reason = 'Apartment size is too big' 
    elif flagged_row['rule_triggered'] == 'Invalid_rooms':
        flag_reason = 'Rooms can not be 0' 
    elif flagged_row['rule_triggered'] == 'Low_price':
        flag_reason = 'Apartment price is too low' 
    elif flagged_row['rule_triggered'] == 'Invalid_total_floors':
        flag_reason = 'Total floors are invalid' 
    elif flagged_row['rule_triggered'] == 'Invalid_location':
        flag_reason = 'Apartment floor is higher than the Total floors' 
    elif flagged_row['rule_triggered'] == 'Invalid_year':
        flag_reason = 'Impossible Year Built'  
    elif flagged_row['rule_triggered'] == 'Too_big':    
        flag_reason = 'Apartment is too big to be valid'  
    elif flagged_row['rule_triggered'] == 'Statistical_Outlier':
        flag_reason= 'Value deviates significantly from mean (Z-Score > 3)'


    #saving the row data
    row_data = flagged_row["data"]
    flagged_Col_name = flagged_row.get('flagged_Col_name')

    is_experiment = st.session_state.get('experiment_mode', False)
    # saving listing id from flagged_row, for experiment mode it is indeed the listing id but for general csv it is just the row index
    listing_id = flagged_row['listing_id']
    if is_experiment:
        # if uploaded ddata set is the experiment dataset
        # Saving individual relevant data to display
        
        listing_id = row_data['listing_id']
        neighborhood = row_data['neighborhood']
        apartment_size = row_data['apartment_size_sqm']
        num_rooms = row_data['num_rooms']
        floor = row_data['floor']
        total_floors = row_data['total_floors']
        price=row_data['price_ils']
        year_built=row_data['year_built']
        has_elevator = row_data['has_elevator']

        # Defining the current mode - defult as we run the app is Mode = 'A' (row index 0-14) 
        # When we move on to row index of 15-29 , mode needs to be 'B'
        # we only switch modes for the experiment
        if len(st.session_state['processed_ids']) > 14:
            st.session_state['mode'] = 'B' 
        else:       
            st.session_state['mode'] = 'A' 

    else:
         # for other datasets, we will use mode B only
         st.session_state['mode'] = 'B'
    Mode = st.session_state['mode'] 


    # ----NEGOTIATION CARD---- #

    # using a container with border to contain the card
    st.markdown("""
    <div class="negotiation-card-wrapper">
    """, unsafe_allow_html=True)

    # creating 3 columns: Left (Data) | Middle (Divider) | Right (System)
    left,middle,right = st.columns([0.87,0.1,1])

    #LEFT SECTION: THE DATA
    with left:
        st.markdown('<div class="card-section left-section">', unsafe_allow_html=True)
        # subheader and card number out of how many cards there are to clean
        st.subheader(f"📃 Row Details ({current_card_num} / {total_cards})")
        # progress bar
        progress_pct = min(len(st.session_state['processed_ids']) / total_cards, 1.0)
        st.progress(progress_pct)
        st.caption(f"Listing ID: {listing_id}")
       
        
        # helper function to print the relevant label and a value
        def display_field(label, value):
            st.markdown(f"""
            <div class="data-row">
            <span class="data-label">{label}</span>
            <span class="data-value">{value}</span>
            </div>
            """, unsafe_allow_html=True)
        if is_experiment: # use the column names for the experiment dataset
            display_field("Neighborhood", neighborhood)
            display_field("Price", f"₪ {price:,}")
            display_field("Size", f"{apartment_size} sqm")
            display_field("Year Built", year_built)
            display_field("Rooms", num_rooms)
            floor_txt = f"{floor} out of {total_floors}" # using apartment floor out of total floors for better visuals
            display_field("Floor", floor_txt)
            display_field("Has Elevator", has_elevator)
        else: # for every other dataset
            #Loop through the available columns
            # We skip 'listing_id' since it's already saved
            # We show the first 8 columns to avoid overcrowding
            count = 0
            for col_name, val in row_data.items():
                if col_name != 'listing_id' and count < 8:
                    display_field(col_name, val)
                    count += 1
            
        st.write("")

    #MIDDLE SECTION: DIVIDER
    with middle:
        st.markdown('<div class="vertical-divider"></div>', unsafe_allow_html=True)
    
    #RIGHT SECTION: SUGGESTIONS & ACTIONS
    with right:
        st.markdown('<div class="card-section right-section">', unsafe_allow_html=True)

        st.subheader("✅ System Analysis")
        
        #Statistical rule based flag box:
        #We present system suggestion to delete the row, as in the expiriment, we will only suggest to delete
        st.markdown(f"""
        <div class="system-flag-box">
            <strong style="color: #991b1b; font-size: 1.3rem;">⚠️ Issue Detected: {flag_reason}</strong><br>
            <span style="color: #7f1d1d;font-size: 1.3rem;">The system suggests to <b></b>delete the row</span>
        </div>
        """, unsafe_allow_html=True)

        if Mode == "A":
            st.write("")
            st.write("")
            st.write("")
            st.write("")

        # Handling Mode B logic
        if Mode == 'B':
            st.write("")
            st.write("")

            # if we are in experiment mode with the dedicated dataset
            if st.session_state.get('experiment_mode', False):
                # saving the llm reasoning from the frozen json file.
                #casting to string because json keys are string
                row_reasoning = agent_reasoning_data.get(str(listing_id))

                if row_reasoning:
                    # saving the short title and the agent generated explanation with a fallback string
                    short_title = row_reasoning.get("short_title", "System analysis:")
                    llm_reason = row_reasoning.get("reasoning", "Analysis unavailable.")
                    suggestion_type = row_reasoning.get("suggestion_type", "Review")
                    # there is the optional key of "suggested_value" which the agent sometimes forgets to generate, as it is a statistical model so we save it here and later check if it is None
                    val = row_reasoning.get("suggested_value")
                    # Dynamic colors, icons and text for each llm response
                    if suggestion_type == "Keep":
                        verdict_icon = "✅"
                        verdict_color = "#137236"  # Strong Green
                        verdict_bg = "#dcfce7"     # Light Green background
                        verdict_text = "KEEP ROW"
                    elif suggestion_type == "Delete":
                        verdict_icon = "❌"
                        verdict_color = "#b91c1cc1"  # Strong Red
                        verdict_bg = "#fee2e2"     # Light Red background
                        verdict_text = "DELETE ROW"
                    else:  # Edit
                        verdict_icon = "✏️"
                        verdict_color = "#b45309"  # Strong Brown
                        verdict_bg = "#fef3c7e8"     # Light Brown background
                        # Adding what value the llm wants the user to change to
                        if val is not None:
                            verdict_text = f"EDIT TO: {val}"
                        else:
                            verdict_text = "MANUAL EDIT"

                    # display it all in a markdown
                    st.markdown(f"""
                    <div class="ai-box" style="border-left: 5px solid #3b82f6; background-color: #eff6ff; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 1.5rem;">🧠</span>
                    <div>
                    <strong style="color: #1e40af; font-size: 1.0rem; text-transform: uppercase; letter-spacing: 0.05em;">Contextual Analysis</strong><br>
                    <span style="color: #1e3a8a; font-weight: 600;">{short_title}</span>
                    </div>
                    </div>
                    <div style="font-size: 0.95rem; color: #172554; line-height: 1.4; margin-bottom: 15px;">
                    {llm_reason}
                    </div>
                    <hr style="margin: 10px 0; border-color: #bfdbfe;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 0.85rem; color: #1e40af; font-weight: 600;">AI Suggestion:</span>
                    <span style="background-color: {verdict_bg}; color: {verdict_color}; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.9rem;">
                    {verdict_icon} {verdict_text}
                    </span>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("")
                    
                else:
                    # if there is no reasoning data for this row
                    st.warning(f"We are aaaaaaaaa sorry, the agent failed to generate reasoning for this row. Please pick an action or try again later")

            else: 
                #For every other dataset
                
                # getting the data for the specific row
                col_name = flagged_row.get('flagged_Col_name', 'Unknown Column')
                val = row_data.get(col_name, 'N/A')

                # Generic explanation
                short_title = "Statistical Outlier Detected"
                llm_reason = f"The value <b>'{val}'</b> in column <b>'{col_name}'</b> deviates significantly from the statistical mean (Z-Score > 3).<br><br>Without specific domain definitions, the system cannot verify if this is a valid edge-case or an error."
                
                # Generic verdict that just says review
                verdict_icon = "⚠️"
                verdict_text = "REVIEW ROW"
                verdict_bg = "#fef9c3"    # Light Yellow
                verdict_color = "#854d0e" # Dark Brown
                
                # And finally, display using the same html code but with different colors
                st.markdown(f"""
                <div class="ai-box" style="border-left: 5px solid #f59e0b; background-color: #fffbeb; padding: 15px; border-radius: 5px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 1.5rem;">📊</span>
                <div>
                <strong style="color: #b45309; font-size: 1.0rem; text-transform: uppercase; letter-spacing: 0.05em;">Statistical Analysis</strong><br>
                <span style="color: #92400e; font-weight: 600;">{short_title}</span>
                </div>
                </div>
                
                <div style="font-size: 0.95rem; color: #451a03; line-height: 1.4; margin-bottom: 15px;">
                    {llm_reason}
                </div>
            
                <hr style="margin: 10px 0; border-color: #fcd34d;">
                    
                <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 0.85rem; color: #b45309; font-weight: 600;">System Suggestion:</span>
                <span style="background-color: {verdict_bg}; color: {verdict_color}; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.9rem;">
                {verdict_icon} {verdict_text}
                </span>
                </div>
                </div>
                """, unsafe_allow_html=True)
                st.write("")




        # else:
            # Mode A: Blurred/Locked state
            # st.markdown("""
            # <div style="filter: blur(4px); opacity: 0.5; background: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            #     <strong>💡 AI Context:</strong><br>
            #     This explanation is hidden in Mode A.
            # </div>
            # """, unsafe_allow_html=True)
            # st.caption("🔒 Contextual reasoning is disabled in this mode.")
        
    
        # ----USER ACTIONS---- #
        st.markdown("### What would you like to do?")
        st.write("")

        #Action Buttons
        b1, b2, b3 = st.columns(3)
        
        with b1:
            # using stylable container to target the css of this button only for different hover colors (I wish streamlit was more friendly)
            with stylable_container(
                key='Delete_button',css_styles=["""
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
                    } 
                """,
                """
                    button:hover{
                            background-color: #a5a5a521 !important;
                            transform: translateY(-2px) !important;
                            box-shadow: 0 4px 12px #8913134f !important;
                    }
                """,]
                ):
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                #creating a button to delete the row
                if st.button("🗑️ Delete row", use_container_width=True): # if pressed
                    #updating delete_list, incrementing the row index and adding the card to the processed ids set
                    st.session_state['delete_list'].append(listing_id)
                    st.session_state['current_row_index'] += 1
                    st.session_state['processed_ids'].add(listing_id)
                    log_decision(listing_id,row_data,'Delete',Mode)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            
        
        with b2:
            # using stylable container to target the css of this button only for different hover colors (I wish streamlit was more friendly)
            with stylable_container(
                key='Keep_button',css_styles=["""
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
                    } 
                """,
                """
                    button:hover{
                            background-color: #a5a5a521 !important;
                            transform: translateY(-2px) !important;
                            box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important; !important;
                    }
                """,]
                ):            

                st.markdown('<div class="keep-btn">', unsafe_allow_html=True)
                #creating a button to keep the row
                if st.button("✅ Keep row", use_container_width=True):
                    st.session_state['current_row_index'] += 1
                    #incrementing the row index and adding the card to the processed ids set
                    st.session_state['processed_ids'].add(listing_id)
                    log_decision(listing_id,row_data,'Keep',Mode)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        with b3:
            # using stylable container to target the css of this button only for different hover colors (I wish streamlit was more friendly)
            with stylable_container(
                key='Edit_button',css_styles=["""
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
                    } 
                """,
                """
                    button:hover{
                            background-color: #a5a5a521 !important;
                            transform: translateY(-2px) !important;
                            box-shadow: 0 4px 12px #4faaeb57 !important;
                    }
                """,]
                ):  

                    st.markdown('<div class="edit-btn">', unsafe_allow_html=True)
                # Toggle Edit Mode
                    if st.button("✏️ Manual Edit", use_container_width=True):
                        st.session_state['edit_mode'] = not st.session_state.get('edit_mode', False)
                    st.markdown('</div>', unsafe_allow_html=True)


        # ----UNDO BUTTON---- #
        if st.session_state.get('decision_log'): 
            #only active when there is a log
            st.divider()
            st.write('Changed your mind regarding last decision?')
            
            # saving the last log entry
            last_entry = st.session_state['decision_log'][-1]
            
            
            # Mode check, I dont allow going back from mode B to mode A so if the last entry is from mode A and user is in mode B, undo is unavailable
            can_undo = True
            if st.session_state['mode'] == 'B' and last_entry['mode'] == 'A' and is_experiment:
                can_undo = False
                st.info("🚫 You cannot go back to the previous Mode.")

            if can_undo: # styling the button using the styleable container
                with stylable_container(
                    key='Undo_button',css_styles=["""
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
                        } 
                    """,
                    """
                        button:hover{
                                background-color: #a5a5a521 !important;
                                transform: translateY(-2px) !important;
                                box-shadow: 0 4px 12px #8913134f !important;
                        }
                    """,]
                    ):
                    if st.button("↩️ Undo Last Action", use_container_width=True):
                        # pop the last log entry
                        last_entry = st.session_state['decision_log'].pop()
                        
                        last_id = last_entry['listing_id']
                        action_type = last_entry['decision']

                        # Removing from processed_ids
                        if last_id in st.session_state['processed_ids']:
                            st.session_state['processed_ids'].remove(last_id)

                        # Delete and Edit needs special care
                        if action_type in ['Delete', 'Keep']:
                            #
                            st.session_state['current_row_index'] -= 1
                            # if the user chose to Delete, we remove the delete id from the session variable delete list
                            if action_type == 'Delete':
                                if last_id in st.session_state['delete_list']:
                                    st.session_state['delete_list'].remove(last_id)
                        # if the user chose Edit, we revert the changes and update the df with the old values
                        elif action_type == 'Edit':
                            idx = last_entry['edited_row_index']
                            col = last_entry['edited_col_name']
                            old_val = last_entry['old_value']
                            
                            if idx is not None and col is not None:
                                st.session_state['df'].at[idx, col] = old_val

                        st.rerun()



        # Edit section - only available when edit button is pressed
        if st.session_state.get('edit_mode', False):

            with st.form(key=f"edit_form_{listing_id}"):
                    
                #saving relevant variables            
                current_val = row_data[flagged_Col_name]
                clean_val = current_val
                #saving distinct values to determine boolean columns
                unique_vals = df[flagged_Col_name].dropna().unique().tolist()
                is_dropdown = False
                
                # Using a drop-down only on boolean columns. <=5 to catch the bollean columns
                if len(unique_vals) <= 5:
                    is_dropdown = True
                    # the option list of the dropdown are the existing values
                    options = [str(x) for x in unique_vals]
                    # dropdown
                    new_value = st.selectbox(
                        f"Select value for '{flagged_Col_name}':",
                        options=options,
                        index=0, 
                        key=f"edit_select_{listing_id}"
                    )
                    

                # if not boolean column
                else:
                    new_value = st.text_input(
                        label=f"Enter correct value for '{flagged_Col_name}':", 
                        value=str(current_val),
                        key=f"edit_text_{listing_id}"
                    )
 

                submitted = st.form_submit_button("💾 Apply Correction", use_container_width=True)
                
                if submitted:

                #value type conversion and saving it
                    try:
                            # If it came from the dropdown, it iss already a boolean
                            if isinstance(new_value, bool):
                                clean_val = new_value
                                
                            # If its a number column, convert to float/int
                            elif flagged_Col_name == 'price_ils':
                                clean_val = float(new_value)
                                if clean_val.is_integer(): 
                                    clean_val = int(clean_val)
                            else:
                                #stays as string
                                clean_val = new_value
                    except:
                            clean_val = new_value
                    
                    
                    edited_col_name = flagged_Col_name
                    edited_row_index = flagged_row['index']
                    old_value = st.session_state['df'].at[edited_row_index, edited_col_name]
                    
                #updating the DF
                    st.session_state['df'].at[flagged_row['index'], flagged_Col_name] = clean_val
                # If the user updated the row using a wrong value that will get flagged I block the advancement to the next flag
                # And I dont append it to the session variable set of processed_ids. so I scall the get_flagged_rows function again, and if the current
                #ID isnt in it, we move on, if it is still invalid, we let the user fix it and only when it is fixed we proceeed
                    
                    updated_flags = get_flagged_rows(st.session_state['df'])
                    will_be_flagged_again = any(item['listing_id'] == listing_id for item in updated_flags)

                    if  will_be_flagged_again:
                        st.warning(f"Updated to {clean_val}, but the row still contains an impossible value. Please try again.")
                        time.sleep(0.4)

                    else:
                        log_decision(listing_id,row_data,'Edit', Mode, edited_value = clean_val,old_value=old_value,edited_col_name=edited_col_name,edited_row_index=edited_row_index)
                        st.session_state['processed_ids'].add(listing_id)
                        st.success(f"Updated {flagged_Col_name} to {clean_val}")

                    time.sleep(0.8)
                    st.session_state['edit_mode'] = False 
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

else:  # No more Flagged Rows. Cleaning completed,  applying deletion and sending to export page 
    # applying user selected row deletion
    if st.session_state['delete_list']:
        st.session_state['df'] = st.session_state['df'][~st.session_state['df']['listing_id'].isin(st.session_state['delete_list'])]
        st.session_state['delete_list'] = []

    # auto move on to the last page
    st.switch_page("pages/02_export.py")