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

# Lists for Step 1 conditional questions
primary_centers = get_unique_values(df, 'Primary center')  # Column U
impact_areas = get_unique_values(df, 'Impact areas')       # Column Y
countries = get_unique_values(df, 'Countries')             # Column AB
regions = get_unique_values(df, 'Regions')                 # Column AC

if 'Lead contact person' in df.columns:
    contacts = df['Lead contact person'].dropna().unique()
    contacts = sorted(contacts, key=lambda x: str(x))
    contacts = ["All"] + contacts
else:
    contacts = ["All"]

if 'step' not in st.session_state:
    st.session_state.step = 1

# --- Session State Initialization ---
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

if 'keywords' not in st.session_state:
    st.session_state.keywords = ""
if 'description_filter' not in st.session_state:
    st.session_state.description_filter = ""

# New Step 1 variables:
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
    st.session_state.keywords = ""
    st.session_state.description_filter = ""
    st.session_state.focus_options = []
    st.session_state.science_program_initiatives = ""
    st.session_state.selected_centers = []
    st.session_state.selected_countries = []
    st.session_state.selected_regions = []
    st.session_state.selected_thematic_areas = []
    st.session_state.funder_specification = ""
    st.session_state.fund_type_selection = []
    st.session_state.other_focus_text = ""

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

    # Main checkboxes for focus selection
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

    # Conditional questions based on selection
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

    # Final text box in Step 1
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
    st.header("Step 2: Classification Criteria")

    st.session_state.gender_selected = st.selectbox(
        "Gender level", 
        options=genders, 
        index=genders.index(st.session_state.gender_selected) if st.session_state.gender_selected in genders else 0
    )
    st.session_state.readiness_selected = st.selectbox(
        "Readiness level", 
        options=readiness_levels, 
        index=readiness_levels.index(st.session_state.readiness_selected) if st.session_state.readiness_selected in readiness_levels else 0
    )
    st.session_state.partners_selected = st.selectbox(
        "Partners", 
        options=partners, 
        index=partners.index(st.session_state.partners_selected) if st.session_state.partners_selected in partners else 0
    )
    st.session_state.center_selected = st.selectbox(
        "Primary center", 
        options=centers, 
        index=centers.index(st.session_state.center_selected) if st.session_state.center_selected in centers else 0
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
    st.header("Step 3: Developers and Collaborators Information")

    st.session_state.developers = st.text_input("Developers", value=st.session_state.developers, placeholder="Enter names or emails")
    st.session_state.collaborators = st.text_input("Collaborators", value=st.session_state.collaborators, placeholder="Enter names or emails")
    st.session_state.contact_person_selected = st.selectbox(
        "Lead contact person", 
        options=contacts, 
        index=contacts.index(st.session_state.contact_person_selected) if st.session_state.contact_person_selected in contacts else 0
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
    st.header("Step 4: Description and Keywords")

    st.session_state.keywords = st.text_input("Keywords", value=st.session_state.keywords, placeholder="Enter relevant terms")
    st.session_state.description_filter = st.text_area("Description contains", value=st.session_state.description_filter, placeholder="Enter part of the description")

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        st.button("Next", on_click=next_step, type='primary')
    with col_reset:
        st.button("Reset", on_click=reset_filters)

# ------ STEP 5 ------
elif st.session_state.step == 5:
    st.header("Step 5: Results Visualization")

    filtered_df = df.copy()

    # Filters based on session state (from previous original code)
    if st.session_state.year_interest != "All":
        filtered_df = filtered_df[filtered_df['Year'] == st.session_state.year_interest]

    if st.session_state.level_selected != "All":
        filtered_df = filtered_df[filtered_df['Level'] == st.session_state.level_selected]

    if st.session_state.type_selected != "All":
        filtered_df = filtered_df[filtered_df['Type'] == st.session_state.type_selected]

    if st.session_state.gender_selected != "All" and 'Gender level' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Gender level'] == st.session_state.gender_selected]

    if st.session_state.readiness_selected != "All" and 'Readiness level' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Readiness level'] == st.session_state.readiness_selected]

    if st.session_state.partners_selected != "All" and 'Partners' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['Partners'].astype(str).str.contains(st.session_state.partners_selected, case=False, na=False)
        ]

    if st.session_state.center_selected != "All" and 'Primary center' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['Primary center'].astype(str).str.contains(st.session_state.center_selected, case=False, na=False)
        ]

    if st.session_state.developers and 'Developers' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['Developers'].astype(str).str.contains(st.session_state.developers, case=False, na=False)
        ]

    if st.session_state.collaborators and 'Collaborators' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['Collaborators'].astype(str).str.contains(st.session_state.collaborators, case=False, na=False)
        ]

    if st.session_state.contact_person_selected != "All" and 'Lead contact person' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Lead contact person'] == st.session_state.contact_person_selected]

    if st.session_state.keywords:
        mask_keywords = pd.Series([False]*len(filtered_df))
        if 'Title' in filtered_df.columns:
            mask_keywords = mask_keywords | filtered_df['Title'].astype(str).str.contains(st.session_state.keywords, case=False, na=False)
        if 'Description' in filtered_df.columns:
            mask_keywords = mask_keywords | filtered_df['Description'].astype(str).str.contains(st.session_state.keywords, case=False, na=False)
        filtered_df = filtered_df[mask_keywords]

    if st.session_state.description_filter and 'Description' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df['Description'].astype(str).str.contains(st.session_state.description_filter, case=False, na=False)
        ]

    st.write("Filtered Results:")

    if filtered_df.empty:
        st.warning("No results match the selected criteria.")
    else:
        cols_to_show = ['Result id', 'Year', 'Title', 'Lead contact person', 'Readiness level', 'PDF link']
        existing_cols = [c for c in cols_to_show if c in filtered_df.columns]
        df_show = filtered_df[existing_cols].copy()

        def make_clickable(link):
            if pd.isna(link) or link == "":
                return ""
            return f"[Open PDF]({link})"

        if 'PDF link' in df_show.columns:
            df_show['PDF link'] = df_show['PDF link'].apply(make_clickable)

        st.markdown(df_show.to_html(escape=False, index=False), unsafe_allow_html=True)

        st.write("Download filtered results:")
        def to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        def to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        col_down1, col_down2 = st.columns(2)
        with col_down1:
            st.download_button(
                label="Download Excel",
                data=to_excel(filtered_df),
                file_name='filtered_results.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        with col_down2:
            st.download_button(
                label="Download CSV",
                data=to_csv(filtered_df),
                file_name='filtered_results.csv',
                mime='text/csv'
            )

    col_prev, col_next, col_reset = st.columns([1,1,1])
    with col_prev:
        st.button("Previous", on_click=prev_step, type='primary')
    with col_next:
        st.button("Next", type='primary', disabled=True)
    with col_reset:
        st.button("Reset", on_click=reset_filters)
