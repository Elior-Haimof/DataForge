import pandas as pd
import numpy as np
import streamlit as st

def get_flagged_rows(df):

    # This function represents the statistical rule-based existing solutions that analyzes the dataframe
    # And flaggs rows that satisfy certain conditions.
    # The rules are basic and use statistical, semantic and physical detection.
    df.dropna()
    flagged_rows = [] # initializing a list of flagged rows
    # checking to see if we are handling the Expiriment dataset
    is_experiment = st.session_state.get('experiment_mode', False)
    # if it is the Expiriment dataset:
    if is_experiment:
        

        # casting to numeric to enable operations
        numeric_cols = ['price_ils', 'year_built', 'apartment_size_sqm', 'num_rooms', 'floor', 'total_floors']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Statistical stats on the price
        price_mean = df['price_ils'].mean()
        price_std = df['price_ils'].std()

        # This section goes over each categorical feature except 'is_mine', 'ground_truth', 'city','neighborhood'
        # And flags boolean inconsistencies. Such As 'Yes' instead of 'True' or 'False' 

        rare_values_map = {} # initializing a dictionary to hold those values
        
        # Defining the categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [c for c in categorical_cols if c not in ['is_mine', 'ground_truth', 'city','neighborhood']]

        for col in categorical_cols:
            # Count of each unique value
            counts = df[col].value_counts()
            total_rows = len(df)

            # RARE VALUE = appears less than 10% of the time
            # filtering and saving the rare items
            rare_items = counts[counts < (total_rows * 0.10)].index.tolist()

            if rare_items:
                rare_values_map[col] = rare_items #adding for each column its rare values to the dictionary


        # ----Flag Rows---- #
        #For each row
        for index, row in df.iterrows():
            reason_code = None # why it was flagged
            flagged_Col_name = None # Which column triggered the flag
            
            # ----RULE 1: The "Micro-Studio" Detector (Targets mines 1001 & 1016)---- #
            # Logic: Apartment size is under 20sqm, which should be impossible to buy as it is tiny, but it is valid in Tel-Aviv
            if row['apartment_size_sqm'] < 20:
                reason_code = "Small_size"
                flagged_Col_name = 'apartment_size_sqm'
                
            # ----RULE 2: The "Penthouse" Detector - Contexual mines (Target mines 1005 & 1018 )---- #
            # Logic: Flag if price is > 3 Standard Deviations OR > 10 Million
            elif row['price_ils'] > (price_mean + (3 * price_std)) or row['price_ils'] > 10000000:
                reason_code = "High_price"
                flagged_Col_name = 'price_ils'
                


            # ----RULE 3: The general obvious error detector (Targets the non mines)---- #
            elif row['year_built'] > 2026 or row['year_built'] < 1900:
                reason_code = 'Invalid_year'
                flagged_Col_name = 'year_built'
            elif row['apartment_size_sqm'] < 10:
                reason_code = 'Invalid_size'
                flagged_Col_name = 'apartment_size_sqm'
            elif  row['apartment_size_sqm'] > 600 :
                reason_code = 'Too_big'
                flagged_Col_name = 'apartment_size_sqm'
            elif row['num_rooms'] == 0 :
                reason_code ='Invalid_rooms'
                flagged_Col_name = 'num_rooms'
            elif  row['price_ils'] < 500000:
                reason_code ='Low_price'
                flagged_Col_name = 'price_ils'
            elif row['total_floors'] == 0:
                reason_code = 'Invalid_total_floors'
                flagged_Col_name = 'total_floors'
            elif row['floor'] > row['total_floors']:
                reason_code = 'Invalid_location'
                flagged_Col_name = 'total_floors'

            # ----RULE 4: boolean inconsistency (Target mines 1015 & 1030 ) ---- #
            # Logic: We check if this row contains one of the "Rare Values" we found earlier.
            elif any(row[col] in rare_values_map.get(col, []) for col in rare_values_map):
                reason_code = "Inconsistent"
                flagged_Col_name = next(col for col in rare_values_map if row[col] in rare_values_map[col])
            
                        
            
            # If any rule triggered, add to the list
            if reason_code:
                flagged_rows.append({
                    'index': index,
                    'listing_id': row['listing_id'],
                    'data': row,
                    'reason_key': str(row['listing_id']),
                    'rule_triggered': reason_code,
                    'flagged_Col_name': flagged_Col_name
                })
            flagged_rows.sort(key =lambda x:float(x['listing_id']))
        # Return the final list        
        return flagged_rows
    
    else: # User uploaded a different dataset that isnt the experiment one
        # here we apply a generic z-score test
        
        # Identifying numeric columns 
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # for each row
        for index, row in df.iterrows():
            reason_code = None
            flagged_Col_name = None
            
            # for each numeric col, check for outliers
            for col in numeric_cols:
                # Skip nulls
                if pd.isna(row[col]):
                    continue
                
                col_mean = df[col].mean()
                col_std = df[col].std()
                
                # Avoid division by zero
                if col_std == 0:
                    continue
                    
                # Calculate Z-Score
                z_score = (row[col] - col_mean) / col_std
                
                # Generic Threshold: > 3 Standard Deviations
                if abs(z_score) > 3:
                    reason_code = "Statistical_Outlier"
                    flagged_Col_name = col
                    break # Stop at the first error found in this row
            
            if reason_code:
                flagged_rows.append({
                    'index': index,
                    'listing_id': row.get('listing_id', index), # Use index as ID for generic data
                    'data': row,
                    'reason_key': str(index),
                    'rule_triggered': reason_code,
                    'flagged_Col_name': flagged_Col_name
                })

    # Sort results for consistency (if listing_id exists and is numeric)
    try:
        flagged_rows.sort(key=lambda x: float(x['listing_id']))
    except:
        pass # Skip sorting if IDs are not numeric
        
    return flagged_rows