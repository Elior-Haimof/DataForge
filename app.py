import streamlit as st
import pandas as pd
import time
import base64
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
upload_icon_base64 = get_base64_image("assets/upload.png")
DataForgeLogo_base64 = get_base64_image("assets/DataForgeLogo_no_wording.png")


# Checking the uploaded CSV schema to see if we need to go into experiment mode
def check_schema_match(df):
    # checking a good amount of columns
    required_columns = ['price_ils', 'apartment_size_sqm', 'num_rooms', 'floor', 'total_floors','year_built','is_mine']
    # checking if all of the selected columns exist in the uploaded df
    if all(col in df.columns for col in required_columns):
        return True
    return False


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
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(33, 115, 70, 0.3) !important;
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



    /*  ----BIG UPLOAD AREA---- */
            
    /* Main container */
    [data-testid='stFileUploader'] {{
        width: 100%;
        margin-top: 2rem;
    }}
    
    /* Remove borders and padding from wrapper elements */
    [data-testid='stFileUploader'] > div,
    [data-testid='stFileUploader'] section,
    [data-testid='stFileUploader'] section > div {{
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }}
    
    /* Hide the label */
    [data-testid='stFileUploader'] label[data-testid="stWidgetLabel"] {{
        display: none !important;
    }}
    
    /* Style the main dropzone area */
    [data-testid='stFileUploader'] section {{
        position: relative !important;
        min-height: 45vh !important; 
    }}
    
    /* Target the click/drag area */
    [data-testid='stFileUploader'] section > div[data-testid="stFileUploaderDropzone"],
    [data-testid='stFileUploader'] section > div > div {{
        min-height: 45vh !important;
        width: 100% !important;
        background-color: #ffffff !important;
        border: 2px dashed #217346 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.3s ease !important;
        padding: 3rem !important;
        cursor: pointer !important;
        position: relative !important;
    }}
    
    /* Hover effect */
    [data-testid='stFileUploader'] section > div[data-testid="stFileUploaderDropzone"]:hover,
    [data-testid='stFileUploader'] section > div > div:hover {{
        background-color: #a5a5a521 !important;
        border-color: #217346 !important;
    }}
    
    /* Hide ALL default content inside */
    [data-testid='stFileUploader'] section svg,
    [data-testid='stFileUploader'] section span,
    [data-testid='stFileUploader'] section p,
    [data-testid='stFileUploader'] section button,
    [data-testid='stFileUploader'] section small {{
        display: none !important;
    }}
    
    /* Custom upload icon - as Image */
    {f'''
    [data-testid='stFileUploader'] section::before {{
        content: "";
        background-image: url(data:image/png;base64,{upload_icon_base64});
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        width: 100px;
        height: 100px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -80px);
        pointer-events: none;
        z-index: 1;
    }}
    '''}
    
    /* The text below the icon */
    [data-testid='stFileUploader'] section::after {{
        content: "Drag & Drop CSV here or Click to Browse";
        font-size: 1.5rem;
        font-weight: 600;
        color: #217346;
        font-family: 'Segoe UI', sans-serif;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, 20px);
        pointer-events: none;
        z-index: 1;
        white-space: nowrap;
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


</style>
""", unsafe_allow_html=True)


# ----SESSION STATE INITIALIZATION---- #
if 'df' not in st.session_state: # df
    st.session_state['df'] = None
if 'current_row_index' not in st.session_state: # current row for modes and preprocessing stage
    st.session_state['current_row_index'] = 0
if 'mode' not in st.session_state: # current mode
    st.session_state['mode'] = 'A'
if 'delete_list' not in st.session_state:
    st.session_state['delete_list'] = []
if 'processed_ids' not in st.session_state: # for later use in 01_preprocessing.py. this stores the finished negotiation cards
    st.session_state['processed_ids'] = set()
if 'initial_length' not in st.session_state: # for later use in  and 02_export.py. this stores the initial length of the dataframe
    st.session_state['initial_length'] = 0
if 'decision_log' not in st.session_state: # user decision log for the expiriment's metrics
    st.session_state['decision_log'] = []
if 'original_df' not in st.session_state:
    st.session_state['original_df'] = None
if 'experiment_mode' not in st.session_state: # initializng experiment mode to be False unless the experiment csv appears
    st.session_state['experiment_mode'] = False

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
    # If we are at the first stage and csv hasnt been uploaded yet
    if st.session_state['df'] is None:
        st.info("1️⃣ **Upload Data** (Current)")
        st.write("2️⃣ Negotiate Cleaning")
        st.write("3️⃣ Export Results")
        
    else: # second stage after csv upload
        st.success("1️⃣ **Upload Data** (Done)")
        st.info("2️⃣ **Negotiate Cleaning** (Next)")
        st.write("3️⃣ Export Results")
        
        st.divider()
        # Navigation Button 
        st.markdown("### Navigation")
        st.write("Ready to start?")
        st.page_link("pages/01_preprocessing.py", label="🚀 Go to Preprocessing")

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
st.markdown("#### The first step towards the perfect data")


# ----STAGE 1: UPLOAD----

if st.session_state['df'] is None: #No csv was uploaded yet
    st.write("Please upload a CSV file so we can start.")
    
    # The drag & drop section - Limiting files to be CSV only
    uploaded_file = st.file_uploader("Internal Label", type="csv")

    if uploaded_file is not None:
        # Load data with pandas
        df = pd.read_csv(uploaded_file)
        # Saving df to session state so it is accessible
        st.session_state['df'] = df  
        st.session_state['original_df'] = df
        st.session_state['initial_length'] = len(df)   

        # checking if the uploaded csv is the experiment dataset or a random user dataset
        if check_schema_match(df):
            st.session_state['experiment_mode'] = True
            st.toast("🧪 Experiment Dataset Detected: Activating Specialized Real-Estate Rules", icon="🏢")
        else:
            st.session_state['experiment_mode'] = False
            st.toast("📂 Generic Dataset Detected: Activating General Statistical Outlier Rules", icon="📊")
        # sleep so we can see the message
        time.sleep(1)
        # moving to STAGE 2
        
        st.rerun()

# ----STAGE 2: REVIEW AND PROCEED----
else:   # Csv was uploaded
    
    #Success message
    st.success("✅ Dataset loaded successfully!")
    
    # for experiment mode I dont want to show the is_mine and ground_truth columns
    hidden_columns = ['is_mine', 'ground_truth']
    # list comprehension to only drop columns that actually exist - that way generic dataset that isnt the experiment data set will not cause errors
    display_df = st.session_state['df'].drop(columns=[col for col in hidden_columns if col in st.session_state['df'].columns])

    # Data preview
    st.subheader("Data Preview")
    st.dataframe(display_df.head(), use_container_width=True)
    st.divider()
    
    # NEXT STEP / RESET
    col1, col2 = st.columns([2, 1])
    with col1:
        # Next Step Section
        st.markdown("""
        <div class="next-step-box">
            <h3>🚀 Next Step</h3>
            <p style="font-size: 1.1rem; color: #475569;">
                We are ready to start cleaning! <br>
                The system has prepared the suggestion cards for your review.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Buttons section
        st.write("") # spaceing to look more aesthetic

        # Next step
        st.page_link("pages/01_preprocessing.py", label="🚀 Click here to Start Negotiating", use_container_width=True,)
    
        # Reset
        st.markdown("<br><br>", unsafe_allow_html=True) # Push it down to align with text
        if st.button("🔄 Reset / Upload New File", type="secondary", use_container_width=True):
            st.session_state['df'] = None
            st.session_state['initial_length'] = 0
            st.session_state['original_df'] = None
            st.session_state['current_row_index'] = 0
            st.session_state['mode'] = 'A'
            st.session_state['delete_list'] = []
            st.session_state['processed_ids'] = set()
            st.session_state['decision_log'] = []
            st.session_state['experiment_mode'] = False
            st.rerun()