import streamlit as st
import pandas as pd
import io
import base64

logo_path = "static/CGIAR-logo.png"  # Path to the logo

@st.cache_data
def load_data():
    df = pd.read_excel("export_data_table_results_20241312_000124CET.xlsx", sheet_name="data", engine="openpyxl")
    return df

df = load_data()

def get_unique_values_with_all(df, column_name):
    if column_name in df.columns:
        vals = df[column_name].dropna().unique()
        vals = sorted(vals, key=lambda x: str(x))
        return ["All"] + list(vals)
    else:
        return ["All"]

def get_unique_values(df, column_name):
    if column_name in df.columns:
        vals = df[column_name].dropna().unique()
        vals = sorted(vals, key=lambda x: str(x))
        return vals
    else:
        return []

years = get_unique_values_with_all(df, 'Year')
levels = get_unique_values_with_all(df, 'Level')
types = get_unique_values_with_all(df, 'Type')
genders = get_unique_values_with_all(df, 'Gender level')
readiness_levels = get_unique_values_with_all(df, 'Readiness level')
partners = get_unique_values_with_all(df, 'Partners')
centers = get_unique_values_with_all(df, 'Primary center')

primary_centers = get_unique_values(df, 'Primary center')
impact_areas = get_unique_values(df, 'Impact areas')
countries = get_unique_values(df, 'Countries')
regions = get_unique_values(df, 'Regions')

if 'Lead contact person' in df.columns:
    contacts = df['Lead contact person'].dropna().unique()
    contacts = sorted(contacts, key=lambda x: str(x))
    contacts = ["All"] + contacts
else:
    contacts = ["All"]

if 'step' not in st.session_state:
    st.session_state.step = 1

# --- Session State Initialization ---
# Basic filters (not really used now but kept for reference)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'year_interest' not in st.session_state:
    st.session_state.year_interest = "All"
if 'level_selected' not in st.session_state:
    st.session_state.level_selected = "All"
if 'type_selected' not in st.session_state:
    st.session_state.type_selected = "All"
if 'gender_selected' not in st.session_state:
    st.session_state.gender_selected = "All"
if 'readiness_selected' not in st.session_state:
    st.session_state.readiness_selected = "All"
if 'partners_selected' not in st.session_state:
    st.session_state.partners_selected = "All"
if 'center_selected' not in st.session_state:
    st.session_state.center_selected = "All"
if 'developers' not in st.session_state:
    st.session_state.developers = ""
if 'collaborators' not in st.session_state:
    st.session_state.collaborators = ""
if 'contact_person_selected' not in st.session_state:
    st.session_state.contact_person_selected = "All"

# Step 1 variables
if 'focus_options' not in st.session_state:
    st.session_state.focus_options = []
if 'science_program_initiatives' not in st.session_state:
    st.session_state.science_program_initiatives = ""
if 'selected_centers' not in st.session_state:
    st.session_state.selected_centers = []
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = []
if 'selected_regions' not in st.session_state:
    st.session_state.selected_regions = []
if 'selected_thematic_areas' not in st.session_state:
    st.session_state.selected_thematic_areas = []
if 'funder_specification' not in st.session_state:
    st.session_state.funder_specification = ""
if 'fund_type_selection' not in st.session_state:
    st.session_state.fund_type_selection = []
if 'other_focus_text' not in st.session_state:
    st.session_state.other_focus_text = ""

# Step 2 variables
if 'classification_criteria' not in st.session_state:
    st.session_state.classification_criteria = []
if 'other_priority_areas' not in st.session_state:
    st.session_state.other_priority_areas = ""

# Step 3 variables
if 'readiness_focus' not in st.session_state:
    st.session_state.readiness_focus = "Balanced across Innovation Readiness levels"
if 'ideation' not in st.session_state:
    st.session_state.ideation = ""
if 'proof_of_concept' not in st.session_state:
    st.session_state.proof_of_concept = ""
if 'controlled_pilot' not in st.session_state:
    st.session_state.controlled_pilot = ""
if 'semi_controlled_pilot' not in st.session_state:
    st.session_state.semi_controlled_pilot = ""
if 'scaling_ready' not in st.session_state:
    st.session_state.scaling_ready = ""
if 'selected_regions_step3' not in st.session_state:
    st.session_state.selected_regions_step3 = []
if 'selected_countries_step3' not in st.session_state:
    st.session_state.selected_countries_step3 = []
if 'innovation_type_focus' not in st.session_state:
    st.session_state.innovation_type_focus = "Balanced across innovation types"
if 'tech_innov_percent' not in st.session_state:
    st.session_state.tech_innov_percent = ""
if 'cap_dev_innov_percent' not in st.session_state:
    st.session_state.cap_dev_innov_percent = ""
if 'policy_innov_percent' not in st.session_state:
    st.session_state.policy_innov_percent = ""
if 'target_clients_selected' not in st.session_state:
    st.session_state.target_clients_selected = "Balanced across target clients"
if 'sdg_focus' not in st.session_state:
    st.session_state.sdg_focus = "Balanced across SDGs"
if 'sdg_values' not in st.session_state:
    st.session_state.sdg_values = {f"SDG {i}": 0 for i in range(1, 18)}
megatrends_options = {
    "Demographic trends": "The innovation is expected to address challenges related to population growth, aging, migration, and urbanization.",
    "Changing consumption patterns": "The innovation is expected to improve access to healthy diets.",
    "Market concentration in the agri-food system": "The innovation is expected to create opportunities for smallholders in agri-food value chains.",
    "Climate change": "The innovation is expected to address climate (change) impacts on agriculture and rural livelihoods.",
    "Environmental degradation": "The innovation is expected to address land and water degradation while promoting sustainable resource use.",
    "Shifting global health challenges": "The innovation is expected to tackle global health risks and challenges.",
    "Geopolitical instability": "The innovation is expected to mitigate the effects of conflicts on food security and vulnerable populations.",
    "Growing inequalities": "The innovation is expected to reduce disparities by improving access to resources for disadvantaged groups.",
    "Frontier technology and innovation": "The innovation is expected to foster technologies and other types of innovations to transform agri-food systems.",
    "Other": "The innovation is expected to address problems/offer solutions that are not captured in the above megatrends."
}
if 'megatrends_selected' not in st.session_state:
    st.session_state.megatrends_selected = []
if 'commodities_selected' not in st.session_state:
    st.session_state.commodities_selected = []
if 'other_commodities_text' not in st.session_state:
    st.session_state.other_commodities_text = ""

# Step 4 variables
if 'usd_available' not in st.session_state:
    st.session_state.usd_available = 0
if 'usd_pooled' not in st.session_state:
    st.session_state.usd_pooled = 0
if 'usd_non_pooled' not in st.session_state:
    st.session_state.usd_non_pooled = 0
if 'risk_appetite' not in st.session_state:
    st.session_state.risk_appetite = "Low (Incremental 70%; Radical 20%; Disruptive 10%)"
if 'innovations_considered' not in st.session_state:
    st.session_state.innovations_considered = "Active"
if 'partner_co_investment' not in st.session_state:
    st.session_state.partner_co_investment = "Very important (67-100% of total investment)"

def next_step():
    st.session_state.step += 1

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

def reset_filters():
    st.session_state.step = 1
    st.session_state.user_name = ""
    st.session_state.year_interest = "All"
    st.session_state.level_selected = "All"
    st.session_state.type_selected = "All"
    st.session_state.gender_selected = "All"
    st.session_state.readiness_selected = "All"
    st.session_state.partners_selected = "All"
    st.session_state.center_selected = "All"
    st.session_state.developers = ""
    st.session_state.collaborators = ""
    st.session_state.contact_person_selected = "All"
    st.session_state.focus_options = []
    st.session_state.science_program_initiatives = ""
    st.session_state.selected_centers = []
    st.session_state.selected_countries = []
    st.session_state.selected_regions = []
    st.session_state.selected_thematic_areas = []
    st.session_state.funder_specification = ""
    st.session_state.fund_type_selection = []
    st.session_state.other_focus_text = ""
    st.session_state.classification_criteria = []
    st.session_state.other_priority_areas = ""
    st.session_state.readiness_focus = "Balanced across Innovation Readiness levels"
    st.session_state.ideation = ""
    st.session_state.proof_of_concept = ""
    st.session_state.controlled_pilot = ""
    st.session_state.semi_controlled_pilot = ""
    st.session_state.scaling_ready = ""
    st.session_state.selected_regions_step3 = []
    st.session_state.selected_countries_step3 = []
    st.session_state.innovation_type_focus = "Balanced across innovation types"
    st.session_state.tech_innov_percent = ""
    st.session_state.cap_dev_innov_percent = ""
    st.session_state.policy_innov_percent = ""
    st.session_state.target_clients_selected = "Balanced across target clients"
    st.session_state.sdg_focus = "Balanced across SDGs"
    st.session_state.sdg_values = {f"SDG {i}": 0 for i in range(1, 18)}
    st.session_state.megatrends_selected = []
    st.session_state.commodities_selected = []
    st.session_state.other_commodities_text = ""
    st.session_state.usd_available = 0
    st.session_state.usd_pooled = 0
    st.session_state.usd_non_pooled = 0
    st.session_state.risk_appetite = "Low (Incremental 70%; Radical 20%; Disruptive 10%)"
    st.session_state.innovations_considered = "Active"
    st.session_state.partner_co_investment = "Very important (67-100% of total investment)"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded

encoded_image = get_base64_image(logo_path)
img_html = f"<img src='data:image/png;base64,{encoded_image}' width='200px' style='display:block; margin:auto;' />"

st.markdown(
    f"""
    <div style="text-align: center;">
        {img_html}
        <h1>Innovation Portfolio Management</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ------ STEP 1 ------
if st.session_state.step == 1:
    st.header("Step 1: Portfolio Focus")

    st.write("What is the focus of your innovation portfolio? (Select all that apply)")
    focus_list = [
        "Entire CGIAR",
        "Science Program",
        "CGIAR-centre",
        "Country or Region",
        "Thematic Area",
        "Funder",
        "Fund-type"
    ]

    selected_foci = []
    for focus_item in focus_list:
        checked = focus_item in st.session_state.focus_options
        if st.checkbox(focus_item, value=checked):
            selected_foci.append(focus_item)

    st.session_state.focus_options = selected_foci

    if "Science Program" in st.session_state.focus_options:
        st.session_state.science_program_initiatives = st.text_input(
            "Which Initiative(s)/ Program(s)?",
            value=st.session_state.science_program_initiatives
        )

    if "CGIAR-centre" in st.session_state.focus_options:
        st.session_state.selected_centers = st.multiselect(
            "Which CGIAR-centre(s)?",
            options=primary_centers,
            default=st.session_state.selected_centers
        )

    if "Country or Region" in st.session_state.focus_options:
        col_country, col_region = st.columns(2)
        with col_country:
            st.session_state.selected_countries = st.multiselect(
                "Which country/ies?",
                options=countries,
                default=st.session_state.selected_countries
            )
        with col_region:
            st.session_state.selected_regions = st.multiselect(
                "Which region(s)?",
                options=regions,
                default=st.session_state.selected_regions
            )

    if "Thematic Area" in st.session_state.focus_options:
        st.session_state.selected_thematic_areas = st.multiselect(
            "Which thematic areas?",
            options=impact_areas,
            default=st.session_state.selected_thematic_areas
        )

    if "Funder" in st.session_state.focus_options:
        st.session_state.funder_specification = st.text_input(
            "Which funders?",
            value=st.session_state.funder_specification
        )

    if "Fund-type" in st.session_state.focus_options:
        st.session_state.fund_type_selection = st.multiselect(
            "Select the fund-type:",
            options=["Pooled", "Non-pooled"],
            default=st.session_state.fund_type_selection
        )

    st.session_state.other_focus_text = st.text_area(
        "Is there a different focus you would like to apply, that is not reflected above?",
        value=st.session_state.other_focus_text
    )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary', disabled=True)
    with col_next:
        st.button("Next", on_click=next_step, type='primary')
    with col_reset:
        st.button("Reset", on_click=reset_filters)

# ------ STEP 2 ------
elif st.session_state.step == 2:
    st.header("Step 2: Portfolio Priority Area(s)")

    criteria_options = [
        "Scaling readiness of the innovation (e.g. early stage research or proven innovation)",
        "Geofocus (e.g. regional or specific countries)",
        "Innovation type (e.g. technology, policy, etc.)",
        "Target client (e.g. farmer, policymaker, research, etc.)",
        "Sustainable Development Goals (SDGs)",
        "Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)",
        "Commodity (e.g. potato, rice, vegetables, livestock)"
    ]

    selected_criteria = []
    st.write("Which of the following areas would you like to prioritize in managing your innovation portfolio? (Select all that apply):")
    for c_item in criteria_options:
        checked = c_item in st.session_state.classification_criteria
        if st.checkbox(c_item, value=checked):
            selected_criteria.append(c_item)
    st.session_state.classification_criteria = selected_criteria

    st.session_state.other_priority_areas = st.text_area(
        "Are there any areas that you would like to prioritize, but are not reflected in the above options?",
        value=st.session_state.other_priority_areas
    )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        st.button("Next", on_click=next_step, type='primary')
    with col_reset:
        st.button("Reset", on_click=reset_filters)

# ------ STEP 3 ------
elif st.session_state.step == 3:
    st.header("Step 3: Ideal Portfolio")

    if "Scaling readiness of the innovation (e.g. early stage research or proven innovation)" in st.session_state.classification_criteria:
        readiness_focus_options = ["Balanced across Innovation Readiness levels", "Tailored innovation readiness focus"]
        st.session_state.readiness_focus = st.selectbox(
            "Scaling readiness of the innovation (e.g. early stage research or proven innovation)",
            options=readiness_focus_options,
            index=readiness_focus_options.index(st.session_state.readiness_focus) if st.session_state.readiness_focus in readiness_focus_options else 0
        )

        if st.session_state.readiness_focus == "Tailored innovation readiness focus":
            st.write("Please indicate the percentage of the portfolio assigned to each readiness level:")
            cols_1 = st.columns(3)
            cols_2 = st.columns(3)
            with cols_1[0]:
                st.session_state.ideation = st.text_input("Ideation/basic research (0-1):", value=st.session_state.ideation)
            with cols_1[1]:
                st.session_state.proof_of_concept = st.text_input("Proof of concept (2-3):", value=st.session_state.proof_of_concept)
            with cols_1[2]:
                st.session_state.controlled_pilot = st.text_input("Controlled pilot (4-5):", value=st.session_state.controlled_pilot)
            with cols_2[0]:
                st.session_state.semi_controlled_pilot = st.text_input("Semi-controlled pilot (6-7):", value=st.session_state.semi_controlled_pilot)
            with cols_2[1]:
                st.session_state.scaling_ready = st.text_input("Scaling-ready (8-9):", value=st.session_state.scaling_ready)

    if "Geofocus (e.g. regional or specific countries)" in st.session_state.classification_criteria:
        st.write("Geofocus (e.g. regional or specific countries)")
        col_geo1, col_geo2 = st.columns(2)
        with col_geo1:
            st.session_state.selected_regions_step3 = st.multiselect(
                "CGIAR regions, specify _______",
                options=regions,
                default=st.session_state.selected_regions_step3
            )
        with col_geo2:
            st.session_state.selected_countries_step3 = st.multiselect(
                "Countries, specify __________",
                options=countries,
                default=st.session_state.selected_countries_step3
            )

    if "Innovation type (e.g. technology, policy, etc.)" in st.session_state.classification_criteria:
        innovation_type_options = ["Balanced across innovation types", "Tailored innovation type focus"]
        st.session_state.innovation_type_focus = st.selectbox(
            "Innovation type (e.g. technology, policy, etc.)",
            options=innovation_type_options,
            index=innovation_type_options.index(st.session_state.innovation_type_focus) if st.session_state.innovation_type_focus in innovation_type_options else 0
        )

        if st.session_state.innovation_type_focus == "Tailored innovation type focus":
            col_innov1, col_innov2 = st.columns(2)
            with col_innov1:
                st.session_state.tech_innov_percent = st.text_input(
                    "Technological innovation (breeds, varieties, management practices, etc.): ___%",
                    value=st.session_state.tech_innov_percent
                )
            with col_innov2:
                st.session_state.cap_dev_innov_percent = st.text_input(
                    "Capacity Development innovations (decision support tools, e-learning courses, etc.): ___%",
                    value=st.session_state.cap_dev_innov_percent
                )

            col_innov3, _ = st.columns(2)
            with col_innov3:
                st.session_state.policy_innov_percent = st.text_input(
                    "Policy, organizational and institutional innovations (business models, certification schemes, finance solutions, etc.): ___%",
                    value=st.session_state.policy_innov_percent
                )

    if "Target client (e.g. farmer, policymaker, research, etc.)" in st.session_state.classification_criteria:
        st.session_state.target_clients_selected = st.selectbox(
            "Target client (e.g. farmer, policymaker, research, etc.)",
            options=[
                "Balanced across target clients",
                "Farmers",
                "Policy-makers",
                "Private sector",
                "Researchers/ NARS",
                "Other"
            ],
            index=[
                "Balanced across target clients",
                "Farmers",
                "Policy-makers",
                "Private sector",
                "Researchers/ NARS",
                "Other"
            ].index(st.session_state.target_clients_selected) if st.session_state.target_clients_selected in [
                "Balanced across target clients",
                "Farmers",
                "Policy-makers",
                "Private sector",
                "Researchers/ NARS",
                "Other"
            ] else 0
        )

    if "Sustainable Development Goals (SDGs)" in st.session_state.classification_criteria:
        sdg_options = ["Balanced across SDGs", "Tailored SDG focus"]
        st.session_state.sdg_focus = st.selectbox(
            "Sustainable Development Goals (SDGs)",
            options=sdg_options,
            index=sdg_options.index(st.session_state.sdg_focus) if st.session_state.sdg_focus in sdg_options else 0
        )

        if st.session_state.sdg_focus == "Tailored SDG focus":
            sdg_names = [f"SDG {i}" for i in range(1, 18)]
            for i in range(0, 17, 4):
                cols = st.columns(4)
                for j, col in enumerate(cols):
                    if i+j < 17:
                        sdg_key = sdg_names[i+j]
                        st.session_state.sdg_values[sdg_key] = col.number_input(
                            sdg_key,
                            value=st.session_state.sdg_values[sdg_key],
                            format="%d"
                        )

    if "Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)" in st.session_state.classification_criteria:
        st.write("Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)")

        selected_megatrends = []
        for m_option in megatrends_options.keys():
            checked = m_option in st.session_state.megatrends_selected
            if st.checkbox(m_option, value=checked, help=megatrends_options[m_option]):
                selected_megatrends.append(m_option)
        st.session_state.megatrends_selected = selected_megatrends

    if "Commodity (e.g. potato, rice, vegetables, livestock)" in st.session_state.classification_criteria:
        st.write("Commodity (e.g. potato, rice, vegetables, livestock)")

        commodity_options = [
            "Potato",
            "Rice",
            "Cassava",
            "Wheat",
            "Maize",
            "Livestock",
            "Vegetables",
            "Other(s)"
        ]

        selected_commodities = []
        for c_option in commodity_options:
            checked = c_option in st.session_state.commodities_selected
            if st.checkbox(c_option, value=checked):
                selected_commodities.append(c_option)
        st.session_state.commodities_selected = selected_commodities

        if "Other(s)" in st.session_state.commodities_selected:
            st.session_state.other_commodities_text = st.text_input(
                "Please specify what other commodities:",
                value=st.session_state.other_commodities_text
            )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        st.button("Next", on_click=next_step, type='primary')
    with col_reset:
        st.button("Reset", on_click=reset_filters)

# ------ STEP 4 ------
elif st.session_state.step == 4:
    st.header("Step 4: Resource Availability")

    st.write("What is your resource availability?")
    col_avail, col_pooled, col_nonpooled = st.columns(3)
    with col_avail:
        st.session_state.usd_available = st.number_input("USD available:", value=st.session_state.usd_available, format="%d")
    with col_pooled:
        st.session_state.usd_pooled = st.number_input("USD pooled:", value=st.session_state.usd_pooled, format="%d")
    with col_nonpooled:
        st.session_state.usd_non_pooled = st.number_input("USD non-pooled:", value=st.session_state.usd_non_pooled, format="%d")

    risk_appetite_options = [
        "Low (Incremental 70%; Radical 20%; Disruptive 10%)",
        "Medium (Incremental 33%; Radical 33%; Disruptive 33%)",
        "High (Incremental 10%; Radical 20%; Disruptive 70%)"
    ]
    st.session_state.risk_appetite = st.selectbox(
        "What is your risk appetite?",
        options=risk_appetite_options,
        index=risk_appetite_options.index(st.session_state.risk_appetite) if st.session_state.risk_appetite in risk_appetite_options else 0
    )

    innovations_considered_options = ["Active", "Active and Inactive"]
    st.session_state.innovations_considered = st.selectbox(
        "What innovations should be considered?",
        options=innovations_considered_options,
        index=innovations_considered_options.index(st.session_state.innovations_considered) if st.session_state.innovations_considered in innovations_considered_options else 0
    )

    partner_co_investment_options = [
        "Very important (67-100% of total investment)",
        "Important (33-66% of total investment)",
        "Not so important (0-33% of total investment)"
    ]
    st.session_state.partner_co_investment = st.selectbox(
        "How important is partner co-investment?",
        options=partner_co_investment_options,
        index=partner_co_investment_options.index(st.session_state.partner_co_investment) if st.session_state.partner_co_investment in partner_co_investment_options else 0
    )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        st.button("Next", on_click=next_step, type='primary')
    with col_reset:
        st.button("Reset", on_click=reset_filters)

# ------ STEP 5 ------
elif st.session_state.step == 5:
    st.header("Step 5: Summary of Responses")

    # Build responses conditionally, only add if they were visible.

    responses = {}

    # Step 1 always visible
    responses["Focus Options"] = ", ".join(st.session_state.focus_options)
    if "Science Program" in st.session_state.focus_options:
        responses["Science Program Initiatives"] = st.session_state.science_program_initiatives
    if "CGIAR-centre" in st.session_state.focus_options:
        responses["Selected Centers"] = ", ".join(st.session_state.selected_centers)
    if "Country or Region" in st.session_state.focus_options:
        responses["Selected Countries (Step 1)"] = ", ".join(st.session_state.selected_countries)
        responses["Selected Regions (Step 1)"] = ", ".join(st.session_state.selected_regions)
    if "Thematic Area" in st.session_state.focus_options:
        responses["Selected Thematic Areas"] = ", ".join(st.session_state.selected_thematic_areas)
    if "Funder" in st.session_state.focus_options:
        responses["Funder Specification"] = st.session_state.funder_specification
    if "Fund-type" in st.session_state.focus_options:
        responses["Fund Type Selection"] = ", ".join(st.session_state.fund_type_selection)
    responses["Other Focus Text"] = st.session_state.other_focus_text

    # Step 2 always visible
    responses["Classification Criteria"] = ", ".join(st.session_state.classification_criteria)
    responses["Other Priority Areas"] = st.session_state.other_priority_areas

    # Step 3 visible conditions
    if "Scaling readiness of the innovation (e.g. early stage research or proven innovation)" in st.session_state.classification_criteria:
        responses["Readiness Focus"] = st.session_state.readiness_focus
        if st.session_state.readiness_focus == "Tailored innovation readiness focus":
            responses["Ideation (%)"] = st.session_state.ideation
            responses["Proof of Concept (%)"] = st.session_state.proof_of_concept
            responses["Controlled Pilot (%)"] = st.session_state.controlled_pilot
            responses["Semi-controlled Pilot (%)"] = st.session_state.semi_controlled_pilot
            responses["Scaling Ready (%)"] = st.session_state.scaling_ready

    if "Geofocus (e.g. regional or specific countries)" in st.session_state.classification_criteria:
        responses["Selected Regions (Step 3)"] = ", ".join(st.session_state.selected_regions_step3)
        responses["Selected Countries (Step 3)"] = ", ".join(st.session_state.selected_countries_step3)

    if "Innovation type (e.g. technology, policy, etc.)" in st.session_state.classification_criteria:
        responses["Innovation Type Focus"] = st.session_state.innovation_type_focus
        if st.session_state.innovation_type_focus == "Tailored innovation type focus":
            responses["Technological Innovation (%)"] = st.session_state.tech_innov_percent
            responses["Capacity Development Innovation (%)"] = st.session_state.cap_dev_innov_percent
            responses["Policy/Institutional Innovation (%)"] = st.session_state.policy_innov_percent

    if "Target client (e.g. farmer, policymaker, research, etc.)" in st.session_state.classification_criteria:
        responses["Target Clients Selected"] = st.session_state.target_clients_selected

    if "Sustainable Development Goals (SDGs)" in st.session_state.classification_criteria:
        responses["SDG Focus"] = st.session_state.sdg_focus
        if st.session_state.sdg_focus == "Tailored SDG focus":
            for i in range(1, 18):
                responses[f"SDG {i}"] = st.session_state.sdg_values[f"SDG {i}"]

    if "Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)" in st.session_state.classification_criteria:
        responses["Megatrends Selected"] = ", ".join(st.session_state.megatrends_selected)

    if "Commodity (e.g. potato, rice, vegetables, livestock)" in st.session_state.classification_criteria:
        responses["Commodities Selected"] = ", ".join(st.session_state.commodities_selected)
        if "Other(s)" in st.session_state.commodities_selected:
            responses["Other Commodities Text"] = st.session_state.other_commodities_text

    # Step 4 always visible
    responses["USD Available"] = st.session_state.usd_available
    responses["USD Pooled"] = st.session_state.usd_pooled
    responses["USD Non-pooled"] = st.session_state.usd_non_pooled
    responses["Risk Appetite"] = st.session_state.risk_appetite
    responses["Innovations Considered"] = st.session_state.innovations_considered
    responses["Partner Co-investment Importance"] = st.session_state.partner_co_investment

    # Convert dictionary to DataFrame
    responses_df = pd.DataFrame(list(responses.items()), columns=["Question", "Response"])

    st.write("Below is a summary of all your *visible* responses:")
    st.dataframe(responses_df, width=800, height=600)

    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    def to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    st.write("Download your responses:")
    col_down1, col_down2 = st.columns(2)
    with col_down1:
        st.download_button(
            label="Download Excel",
            data=to_excel(responses_df),
            file_name='responses_summary.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    with col_down2:
        st.download_button(
            label="Download CSV",
            data=to_csv(responses_df),
            file_name='responses_summary.csv',
            mime='text/csv'
        )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        # No further steps
        st.button("Next", type='primary', disabled=True)
    with col_reset:
        st.button("Reset", on_click=reset_filters)
