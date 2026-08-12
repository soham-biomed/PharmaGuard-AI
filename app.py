# ╔══════════════════════════════════════════════════════════════════╗
# ║         PharmaGuard AI  ·  Drug-Drug Interaction Checker         ║
# ║    Stack: Python + Streamlit + Pandas  |  Educational Use Only   ║
# ╚══════════════════════════════════════════════════════════════════╝

# ── STEP 1: IMPORT LIBRARIES ─────────────────────────────────────────────────
# "import" = tell Python to load an external toolbox into your program
import streamlit as st  # Streamlit = framework that builds the entire web app UI
import pandas as pd      # Pandas = creates and styles data tables (like Excel in Python)

# ── STEP 2: PAGE SETUP ───────────────────────────────────────────────────────
# set_page_config controls the browser tab text and the small icon next to it
st.set_page_config(page_title="PharmaGuard AI", page_icon="💊", layout="centered")
st.title("💊 PharmaGuard AI")  # st.title = big bold heading displayed on the page
st.caption("Drug-Drug Interaction Checker for Pharmacy Students & Pharmacists")
st.sidebar.title("About")
st.sidebar.write("Developer: Soham Deshmukh")
st.sidebar.write("B.Pharm → M.Tech Biomedical Devices (IIT Indore)")
st.sidebar.write("Version: 1.0")

# ── STEP 3: DRUG INTERACTION DATABASE ────────────────────────────────────────
# A Python "dictionary" (dict) = like a pharmacy reference book stored in code
# Key   = (drug_A, drug_B) — always sorted A→Z so input order never matters
# Value = {severity level, pharmacist counseling advice}
INTERACTIONS = {
    ("aspirin", "warfarin")      : {"severity": "Major",    "advice": "High bleeding risk. Monitor PT/INR closely. Avoid unless clearly justified by prescriber."},
    ("ibuprofen", "warfarin")    : {"severity": "Major",    "advice": "NSAIDs potentiate anticoagulation → GI bleed risk. Substitute Paracetamol as safer analgesic."},
    ("metformin", "alcohol")     : {"severity": "Moderate", "advice": "Lactic acidosis risk. Counsel patient to strictly avoid alcohol during Metformin therapy."},
    ("amlodipine", "simvastatin"): {"severity": "Moderate", "advice": "CYP3A4 inhibition raises Simvastatin plasma levels → myopathy risk. Cap dose at 20 mg/day."},
    ("fluoxetine", "tramadol")   : {"severity": "Major",    "advice": "Serotonin Syndrome risk — agitation, hyperthermia, tachycardia. Avoid this combination."},
    ("antacid", "ciprofloxacin") : {"severity": "Moderate", "advice": "Divalent cations chelate Ciprofloxacin → reduced absorption. Separate by 2 h before or 6 h after."},
    ("amiodarone", "digoxin")    : {"severity": "Major",    "advice": "P-gp inhibition doubles Digoxin levels. Reduce Digoxin by 50%. Monitor ECG and serum levels."},
    ("lisinopril", "potassium")  : {"severity": "Major",    "advice": "ACE inhibitor + K⁺ supplement = Hyperkalemia risk. Monitor serum potassium closely."},
    ("nitrate", "sildenafil")    : {"severity": "Major",    "advice": "CONTRAINDICATED. Dual vasodilation → fatal hypotension. Absolute contraindication."},
    ("aspirin", "ibuprofen")     : {"severity": "Moderate", "advice": "Ibuprofen competes at COX-1 → blocks aspirin cardioprotection. Take aspirin 30 min before NSAID."},
    ("clopidogrel", "omeprazole"): {"severity": "Moderate", "advice": "CYP2C19 inhibition reduces Clopidogrel activation. Switch PPI to Pantoprazole."},
    ("ibuprofen", "lithium")     : {"severity": "Major",    "advice": "NSAIDs reduce renal Lithium clearance → toxicity. Monitor Lithium levels. Use Paracetamol."},
}

# ── STEP 4: PATIENT INFORMATION INPUT ────────────────────────────────────────
st.subheader("👤 Patient Information")
# st.number_input = creates a numeric box on screen | value=30 is the default shown
age = st.number_input("Patient Age (years)", min_value=1, max_value=110, value=30)

# ── STEP 5: MEDICINE NAME INPUTS ─────────────────────────────────────────────
st.subheader("💊 Medicines Prescribed")
# st.columns(3) = divides the page into 3 equal sections displayed side by side
col1, col2, col3 = st.columns(3)
with col1:
    med1 = st.text_input("Medicine 1").strip().lower()   # .strip() removes leading/trailing spaces
with col2:
    med2 = st.text_input("Medicine 2").strip().lower()   # .lower() converts to lowercase
with col3:
    med3 = st.text_input("Medicine 3 (optional)").strip().lower()  # so 'Aspirin' = 'aspirin'

st.divider()  # Draws a horizontal separator line for visual clarity

# ── STEP 6: CHECK INTERACTIONS BUTTON ────────────────────────────────────────
# Everything inside this if-block runs ONLY when user clicks the button
if st.button("🔍 Check Interactions", use_container_width=True):

    # List comprehension = concise way to build a list of only non-empty medicine names
    medicines = [m for m in [med1, med2, med3] if m]

    if len(medicines) < 2:
        st.warning("⚠️ Please enter at least 2 medicines to check for interactions.")
    else:
        results = []  # Empty list — will be filled with each detected interaction

        # Nested loop checks every unique pair: (0,1), (0,2), (1,2) — no duplicates
        for i in range(len(medicines)):
            for j in range(i + 1, len(medicines)):
                # sorted() = alphabetical order | tuple() = converts list to a dict key
                key = tuple(sorted([medicines[i], medicines[j]]))

                if key in INTERACTIONS:               # Is this pair in our database?
                    info = INTERACTIONS[key]
                    results.append({
                        "Drug Pair"        : f"{medicines[i].title()} + {medicines[j].title()}",
                        "Severity"         : info["severity"],
                        "Pharmacist Advice": info["advice"]
                    })

        # ── STEP 7: DISPLAY RESULTS ───────────────────────────────────────────
        if results:
            st.error("🚨 Interaction(s) Detected! Review counseling advice below.")

            # pd.DataFrame = converts our list of dicts into a structured table
            df = pd.DataFrame(results)

            # Function that returns a CSS color string based on severity text
            def color_severity(val):
                return {"Major"   : "background-color:#C62828;color:white",
                        "Moderate": "background-color:#EF6C00;color:white",
                        "Minor"   : "background-color:#2E7D32;color:white"}.get(val, "")

            # .style.map() applies color_severity() to each cell in "Severity" column only
            styled = df.style.map(color_severity, subset=["Severity"])
            st.dataframe(styled, use_container_width=True, hide_index=True)

            # Geriatric pharmacology alert — drug handling changes with age
            if age >= 65:
                st.info("👴 Elderly Patient Alert: Reduced renal/hepatic clearance may amplify these interactions. Review all doses with prescriber.")
        else:
            st.success("✅ No known interactions found in PharmaGuard database.")
            st.caption("Always verify with Micromedex, Drugs.com, or your clinical pharmacist for complete screening.")

# ── STEP 8: DISCLAIMER FOOTER ────────────────────────────────────────────────
st.divider()
st.caption("⚠️ PharmaGuard AI is for educational purposes only. Not a substitute for clinical judgment or licensed pharmacy software.")

