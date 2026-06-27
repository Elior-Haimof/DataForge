import pandas as pd
import json
import requests
import time
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import os
from typing import Any, Dict, List, Optional
from Rule_Based_Flag import get_flagged_rows
from datetime import datetime


# ----FUNCTIONS---- #

# gets a text and returns a dictionary or none
# this function searches the text that was returned from the llm, if it finds a box labled json it continues to load the first capture group
# as we remember the regex has a () in it which means capture group, which says extract and keep whats inside. so here, we try to convert it
# to a dictionary with try and if it fails, with catch we return none.

# defining json structure
JSON_BLOCK_RE = re.compile(r"```\w*\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)

def clean_and_load(json_str):
        #Helper function that fixes JSON syntax errors
        # We use regex to only target values after a colon, to avoid changing the reasoning text
        # Fix Boolean capitalization (TRUE -> true, False -> false)
        json_str = re.sub(r':\s*TRUE\b', ': true', json_str, flags=re.IGNORECASE)
        json_str = re.sub(r':\s*FALSE\b', ': false', json_str, flags=re.IGNORECASE)
        json_str = re.sub(r':\s*True\b', ': true', json_str) 
        json_str = re.sub(r':\s*False\b', ': false', json_str)      
        # Fix the null type mismatch
        json_str = re.sub(r':\s*None\b', ': null', json_str)
        
        return json.loads(json_str)


def parse_multiple_structured_blocks(txt: str) -> List[Dict[str, Any]]:
    m = JSON_BLOCK_RE.findall(txt)
    results = []
    if m:
        for match in m:
            try:
                results.append(clean_and_load(match))
            except Exception:
                continue
        return results
    # sometimes it skipped some rows
    try:
        start_index = txt.find('{')
        end_index = txt.rfind('}')
        if start_index != -1 and end_index != -1:
            json_str = txt[start_index : end_index + 1]
            results.append(clean_and_load(json_str))
    except Exception:
        pass
        
    return results



# This function invokes the lllm with one row at a time and returns its response
def invoke_llm(row,flag_reason, chain):
    # saving the row data to a string
    row_str = f"""
    City: {row.get('city')}
    Neighborhood: {row.get('neighborhood')}
    Size: {row.get('apartment_size_sqm')} sqm
    Rooms: {row.get('num_rooms')}
    Floor: {row.get('floor')}
    Total floors: {row.get('total_floors')}
    Price: {row.get('price_ils')} ILS
    Year Built: {row.get('year_built')}
    has_elevator: {row.get('has_elevator')}
    """
    # creating user input
    user_input = f"Analyze this row:\n{row_str}"

    # adding the specific neighborhood context of the row, preventing 'lost in the middle'
    neighborhood = row.get('neighborhood')
    current_neighborhood_context = NEIGHBORHOOD_CONTEXT.get(neighborhood)

    current_reason_mapping = REASON_MAPPING.get(flag_reason)
    
    # Invoking the llm
    # printing for debug
    print(f"Invoking Listing {row.get('listing_id', 'Unknown')}...")

    # printing to debug what is getting sent to the llm
    print(f"ID: {row.get('listing_id')} | Flag: {flag_reason}")
    print(f"Instruction: {current_reason_mapping[:60]}...") # Print first 60 chars
    
    try:
        # invoking the llm and returning its response
        response = chain.invoke({
        "user_input": user_input,
        "json_schema_guide": JSON_GUIDE,
        "DOMAIN_RULES" : DOMAIN_RULES,
        "CURRENT_NEIGHBORHOOD_CONTEXT" : current_neighborhood_context,
        "flag_reason": flag_reason,
        "CURRENT_REASON_MAPPING" : current_reason_mapping
        }) 
        return response
    # if the invoke didnt work
    except Exception as e:
        print(f"[ERROR] Failed to parse LLM response: {e}")
        return {
            "suggestion_type": "Keep",
            "short_title": "Analysis Failed",
            "reasoning": "Manual review required.",
            "suggested_value": None
        }


# ---- LLM GUIDENCE ---- #

# guiding the agent to return Json in this format
JSON_GUIDE = """```json
{
    "suggestion_type": "Delete" | "Keep" | "Edit",
    "short_title": "A 3-5 word summary",
    "reasoning": "Max 1 sentence explaining WHY based on the Neighborhood/Context",
    "suggested_value": "null (if Keep/Delete)" | "corrected Value (if Edit)"
}
```"""
#giving it some context about the neighborhoods, as in real implementation the agent has the web so it can search there
#This dictionary represents "Domain Knowledge Injection".
NEIGHBORHOOD_CONTEXT = {
    "Neve Tzedek": "Ultra-luxury, historic district, very high price per sqm is normal.",
    "Old North": "High-end, established residential, expensive but not Neve Tzedek level.",
    "Lev Hair": "Heart of the city, historic, eclectic mix of Bauhaus luxury and old buildings. High demand.",
    "Florentin": "Hipster, gentrifying, older buildings, usually lower/mid prices, small apartments.",
    "Ramat Aviv": "Upscale, family oriented, near university, newer builds.",
    "Kerem HaTeimanim": "Historic, very old/small houses, high value but never above 40M+ due to location but often poor condition."
}

# Writing down the domain rules
DOMAIN_RULES = """
1. **Boolean Fixes:** If 'has_elevator' is 'yes'|'no'|'Yes'|'No', suggest EDIT to TRUE/FALSE. yes needs to be changed to TRUE and no to FALSE.
1. **Micro-Apartments:** In Tel Aviv, apartment_size between 17-25 sqm is LEGAL and VALID if they have 1 room (Studios). Do NOT flag them as storage/errors unless they are <17 sqm.
3. **Luxury Areas:** High prices in 'Neve Tzedek', 'Lev Hair', or 'Old North' are likely VALID, even if statistically high. THEY ARE NOT VALID IF ABOVE 50,000,000 YOU SHOULD SUGGEST 'Delete' IF SO. They might be penthouses, checking the size in sqm can help identify if the listing is valid.
4. **Price/Sqm Logic:** - Even in Luxury areas, Price per SQM cannot exceed 250,000 ILS. 
   - If Price is > 30,000,000 ILS AND Size is < 80 sqm, it is a Data Error -> Suggest DELETE.
5. price under 500000 is low.
6. Do not reference rules, write like a human, bad: "price exceeds threshold". good: "Price of 54M is likely a data entry error (extra zero) for this neighborhood."
"""

# takes the reasons from the statistical rule based model and explains it
REASON_MAPPING = {
    "Inconsistent": "You MUST suggest 'Edit' with TRUE for yes and FALSE for no to fix this schema error. The 'has_elevator' column contains a string ('yes'/'no') instead of a boolean.",
    "Invalid_year": "You MUST suggest 'Delete' .The 'year_built' is logically impossible.'",
    "High_price": "Step 1) If Price > 50,000,000 -> DELETE (Error). Step 2) If Price > 30,000,000 AND Size < 90 sqm -> DELETE (Impossible Price/Sqm). Step 3) Only if price is physically possible, check Neighborhood. If Luxury -> Keep.",
    "Small_size": "You MUST suggest 'Keep' if The size is 16-25sqm  In Tel Aviv,Size of 16-25sqm is a LEGAL Studio (Keep). You MUST suggest 'Delete' if size is Below 16sqm - it is likely Storage .",
    "Invalid_size": "You MUST suggest 'Delete'.Size is physically impossible (<10sqm).",
    "Too_big": "You MUST suggest 'Delete'. Size is huge (>600sqm).",
    "Invalid_rooms": "You MUST suggest 'Delete'.0 rooms is impossible for an apartment",
    "Invalid_total_floors": "You MUST suggest 'Delete'.Total floors cannot be 0.",
    "Invalid_location": "You MUST suggest 'Delete'.Apartment floor is higher than Total Floors. This is physically impossible and is bot due to the building's design or layout.",
    "Low_price": "Suggest 'Delete'. Price is < 500,000. This is a data error (probably missing digit). it is not possible in tel Aviv to have apartments with this low price"
}

# the template that is going to be sent to the LLM in every invoke
base_template = """

You are an expert Data Cleaning Auditor. Your job is to catch errors.
Your task is to analyze specific database rows that have been flagged by statistical rules.
You Determine if the flag is a REAL ERROR or a VALID OUTLIER.
The system has flagged a row. You must verify the specific error code below.


**FLAG CODE**: {flag_reason}
**STRICT INSTRUCTIONS:** {CURRENT_REASON_MAPPING}

*RULES*: {DOMAIN_RULES}

and your context: {CURRENT_NEIGHBORHOOD_CONTEXT} 

**YOUR TASK:**

You Determine if the flag is a REAL ERROR or a VALID OUTLIER.
Based strictly on the "STRICT INSTRUCTION" above, determine the action.
- If the instruction says "MUST suggest Edit", do not suggest Keep.
- If the instruction says "Impossible", do not suggest Keep.
- **Example:** If Year is 20225, this is an error. Suggest Delete.
- If the flag is "Inconsistent" for has_elevator, you MUST suggest "Edit" with the currrect boolean value: TRUE for yes and FALSE for no.
- If flag is "High_price" use the neighborhood context and the apartment size to decide if it is a valid listing or an invalid outlier
- If flag is "Small_size" use the Domain rules and check regarding the legal Tel-Aviv apartment size rule.

Explain why it was flagged as you look at other columns like apartment_size and mention if the explain the high value.
Suggest what the user should do with the row - Delete if the row is garbage, Keep if it is a valid data point that looks like an invalid outlier, Edit if the row got flagged for mismatching categorical has_elevator value (e.g. yes instead of TRUE)
Good example: when there is yes instead of True in has_elevator: "The value 'yes' is semantically clear but breaks the boolean schema. I suggest keeping the row and correcting this to TRUE to maintain data integrity." While you suggest Edit.

Output JSON ONLY.
Always include your structured JSON in triple backticks:
{json_schema_guide}

User: {user_input}
"""
# ----MAIN LOGIC---- #

# Defining model and model hyper parameters
model = OllamaLLM(model="llama3.1",temperature=0.1,num_predict=500)

# creating the prompt
prompt = ChatPromptTemplate.from_template(base_template)
# creating the chain using syntax that says send the prompt (left of |) to the model (right of |)
chain = prompt | model

# initiating a dictionary of llm reasoning
Agent_reasoning = {}
#Loading data
df = pd.read_csv('Apartments_dataset.csv')
# using get_flagged_rows to flag the rows with the rule based statisticla model
flagged_rows = get_flagged_rows(df)
# invoking LLM for each flagged row
for item in flagged_rows:
    #saving the listind_id and row data to know which row we are using
    listing_id = item['listing_id']
    row = item['data']
    #Invoking and getting the llm response
    flag_reason = item.get('rule_triggered')
    response = invoke_llm(row,flag_reason,chain)

    # llms can sometimes return more than 1 json per response as it is a statistical machine
    json_blocks = parse_multiple_structured_blocks(response)

    struct = json_blocks[-1] if json_blocks else None # saving the last Json block
    if struct:
        # storing the current row reasoning in the dictionary
        Agent_reasoning[str(listing_id)] = struct
    else:
        print(response) # Print first 200 chars to see what went wrong

output_folder = "Agent_reasoning"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"Agent_reasoning_{timestamp}.json"
full_path = os.path.join(output_folder, output_file)
with open(full_path, "w", encoding='utf-8') as f:
        json.dump(Agent_reasoning, f, indent=4, ensure_ascii=False)

print("File saved")