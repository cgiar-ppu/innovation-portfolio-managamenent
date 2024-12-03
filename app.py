import streamlit as st
import pandas as pd
import random

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state['step'] = 1

if 'data' not in st.session_state:
    st.session_state['data'] = {}

def next_step():
    if st.session_state['step'] < 5:
        st.session_state['step'] += 1

def prev_step():
    if st.session_state['step'] > 1:
        st.session_state['step'] -= 1

def reset_steps():
    st.session_state['step'] = 1
    st.session_state['data'] = {}

st.set_page_config(page_title="IPM - Innovation Portfolio Management")

# Main header
st.title("INNOVATION PORTFOLIO MANAGEMENT")

# Load dataset from 'data' sheet
ipm_dataset = pd.read_excel('data/ipm-dataset.xlsx', sheet_name='data')

# Display number of rows
st.write(f"Dataset loaded with {len(ipm_dataset)} rows.")

# Process 'Countries' column
countries = []
for entry in ipm_dataset['Countries'].dropna():
    clean_entry = entry.strip().rstrip(',')
    individual_countries = [country.strip() for country in clean_entry.split(',')]
    countries.extend(individual_countries)
countries = sorted(set(countries))  # Remove duplicates and sort

# Process 'Regions' column
regions = []
for entry in ipm_dataset['Regions'].dropna():
    clean_entry = entry.strip().rstrip(',')
    individual_regions = [region.strip() for region in clean_entry.split(',')]
    regions.extend(individual_regions)
regions = sorted(set(regions))  # Remove duplicates and sort

# Simulate pages or tabs for the steps
steps = ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5']

# Step 1 content
if st.session_state['step'] == 1:

    st.markdown(f"### {steps[st.session_state['step'] - 1]} - What is the focus of your innovation portfolio?")
    st.write('##### Please select the focus areas of your innovation portfolio. You can select as many as you want.')

    focus_selected = False  # To ensure at least one focus area is selected

    # Entire CGIAR
    entire_cgiar_value = st.session_state['data'].get('entire_cgiar', False)
    entire_cgiar = st.checkbox('Entire CGIAR', value=entire_cgiar_value, key='entire_cgiar')
    st.session_state['data']['entire_cgiar'] = entire_cgiar
    if entire_cgiar:
        focus_selected = True

    # Science Program
    science_program_value = st.session_state['data'].get('science_program', False)
    science_program = st.checkbox('Science Program', value=science_program_value, key='science_program')
    st.session_state['data']['science_program'] = science_program
    if science_program:
        focus_selected = True
        selected_science_programs_value = st.session_state['data'].get('selected_science_programs', '')
        selected_science_programs = st.text_input('Please specify which Initiative(s)/ Program(s):', value=selected_science_programs_value, key='selected_science_programs')
        st.session_state['data']['selected_science_programs'] = selected_science_programs

    # CGIAR-centre
    cgiar_centre_value = st.session_state['data'].get('cgiar_centre', False)
    cgiar_centre = st.checkbox('CGIAR-centre', value=cgiar_centre_value, key='cgiar_centre')
    st.session_state['data']['cgiar_centre'] = cgiar_centre
    if cgiar_centre:
        focus_selected = True
        centres = ipm_dataset['Primary center'].dropna().unique().tolist()
        selected_centres_value = st.session_state['data'].get('selected_centres', [])
        selected_centres = st.multiselect('Please select which CGIAR-centre(s):', options=centres, default=selected_centres_value, key='selected_centres')
        st.session_state['data']['selected_centres'] = selected_centres

    # Country or Region
    country_region_value = st.session_state['data'].get('country_region', False)
    country_region = st.checkbox('Country or Region', value=country_region_value, key='country_region')
    st.session_state['data']['country_region'] = country_region
    if country_region:
        focus_selected = True

        # Combine countries and regions, remove duplicates, and sort
        options = sorted(set(countries + regions))

        selected_countries_value = st.session_state['data'].get('selected_countries', [])
        selected_countries = st.multiselect('Please select which country/ies or region(s):', options=options, default=selected_countries_value, key='selected_countries')
        st.session_state['data']['selected_countries'] = selected_countries

    # Thematic Area
    thematic_area_value = st.session_state['data'].get('thematic_area', False)
    thematic_area = st.checkbox('Thematic Area', value=thematic_area_value, key='thematic_area')
    st.session_state['data']['thematic_area'] = thematic_area
    if thematic_area:
        focus_selected = True
        # Load options from 'thematic_areas' sheet, Column A
        thematic_areas_df = pd.read_excel('data/ipm-dataset.xlsx', sheet_name='thematic_areas')
        options = thematic_areas_df.iloc[:, 0].dropna().tolist()
        selected_thematic_areas_value = st.session_state['data'].get('selected_thematic_areas', [])
        selected_thematic_areas = st.multiselect('Please specify which thematic areas:', options, default=selected_thematic_areas_value, key='selected_thematic_areas')
        st.session_state['data']['selected_thematic_areas'] = selected_thematic_areas

    # Funder
    funder_value = st.session_state['data'].get('funder', False)
    funder = st.checkbox('Funder', value=funder_value, key='funder')
    st.session_state['data']['funder'] = funder
    if funder:
        focus_selected = True
        # Load options from 'funders' sheet, Column A
        funders_df = pd.read_excel('data/ipm-dataset.xlsx', sheet_name='funders')
        options = funders_df.iloc[:, 0].dropna().tolist()
        selected_funders_value = st.session_state['data'].get('selected_funders', [])
        selected_funders = st.multiselect('Please specify which funders:', options, default=selected_funders_value, key='selected_funders')
        st.session_state['data']['selected_funders'] = selected_funders

    # Fund-type
    fund_type_value = st.session_state['data'].get('fund_type', False)
    fund_type = st.checkbox('Fund-type', value=fund_type_value, key='fund_type')
    st.session_state['data']['fund_type'] = fund_type
    if fund_type:
        focus_selected = True
        fund_type_options = ['Pooled', 'Non-pooled']
        selected_fund_type_value = st.session_state['data'].get('selected_fund_type', fund_type_options[0])
        selected_fund_type = st.selectbox('Please specify the type of funding:', fund_type_options, index=fund_type_options.index(selected_fund_type_value) if selected_fund_type_value in fund_type_options else 0, key='selected_fund_type')
        st.session_state['data']['selected_fund_type'] = selected_fund_type

    # Additional focus
    additional_focus_value = st.session_state['data'].get('additional_focus', '')
    additional_focus = st.text_area('Is there a different focus you would like to apply, that is not reflected above?', value=additional_focus_value, key='additional_focus')
    st.session_state['data']['additional_focus'] = additional_focus
    if additional_focus:
        focus_selected = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back1'):
            prev_step()
    with col2:
        if st.button('Next', key='next1'):
            if focus_selected or additional_focus:
                next_step()
            else:
                st.warning('Please select at least one focus area or provide an additional focus.')

# Step 2 content
elif st.session_state['step'] == 2:
    st.markdown(f"### {steps[st.session_state['step'] - 1]} - Select areas you would like to prioritize in managing your innovation portfolio:")
    st.write('You can select as many as you want.')
    options = [
        'Scaling readiness of the innovation (e.g. early stage research or proven innovation)',
        'Geofocus (e.g. regional or specific countries)',
        'Innovation type (e.g. technology, policy, etc.)',
        'Target client (e.g. farmer, policymaker, research, etc.)',
        'Sustainable Development Goals (SDGs)',
        'Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)',
        'Commodity (e.g. potato, rice, vegetables, livestock)'
    ]

    selected_options = []
    for option in options:
        option_key = f"option_{option}"
        option_value = st.session_state['data'].get(option_key, False)
        is_selected = st.checkbox(option, value=option_value, key=option_key)
        st.session_state['data'][option_key] = is_selected
        if is_selected:
            selected_options.append(option)

    additional_areas_value = st.session_state['data'].get('additional_prioritized_areas', '')
    additional_areas = st.text_input('Are there any areas that you would like to prioritize, but are not reflected in the above options?', value=additional_areas_value, key='additional_areas')
    st.session_state['data']['additional_prioritized_areas'] = additional_areas

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back2'):
            prev_step()
    with col2:
        if st.button('Next', key='next2'):
            if selected_options or additional_areas:
                st.session_state['data']['prioritized_areas'] = selected_options
                next_step()
            else:
                st.warning('Please select at least one area to prioritize or specify additional areas.')

# Step 3 content
elif st.session_state['step'] == 3:
    st.markdown(f"### {steps[st.session_state['step'] - 1]} - Please indicate what your ideal innovation portfolio would look like:")


    scaling_readiness_options = ['Balanced across Innovation Readiness levels', 'Tailored innovation readiness focus']

    scaling_readiness_choice_value = st.session_state['data'].get('scaling_readiness_choice', 'Balanced across Innovation Readiness levels')

    scaling_readiness_choice = st.radio(
        'Scaling readiness of the innovation',
        options=scaling_readiness_options,
        index=scaling_readiness_options.index(scaling_readiness_choice_value),
        key='scaling_readiness_choice'
    )
    st.session_state['data']['scaling_readiness_choice'] = scaling_readiness_choice

    if scaling_readiness_choice == 'Tailored innovation readiness focus':
        categories = [
            'Ideation/ basic research',
            'Proof of concept',
            'Controlled pilot',
            'Semi-controlled pilot',
            'Scaling-ready'
        ]
        scaling_readiness_percentages = st.session_state['data'].get('scaling_readiness_percentages', {})
        total_percentage = 0

        for i in range(0, len(categories), 3):
            cols = st.columns(3)
            row_categories = categories[i:i+3]
            for idx, category in enumerate(row_categories):
                with cols[idx]:
                    key = f'scaling_readiness_{category}'
                    previous_value = scaling_readiness_percentages.get(category, 0)
                    percentage = st.number_input(
                        f'{category}: ___%', min_value=0, max_value=100, value=int(previous_value), key=key
                    )
                    scaling_readiness_percentages[category] = percentage
                    total_percentage += percentage

        st.session_state['data']['scaling_readiness_percentages'] = scaling_readiness_percentages

        if total_percentage < 100:
            st.warning('The total percentage is less than 100%. Please adjust your inputs.')
        elif total_percentage > 100:
            st.warning('The total percentage exceeds 100%. Please adjust your inputs.')
        else:
            st.success('The total percentage is 100%.')


    # Geofocus question
    geofocus_options = ['Countries', 'Regions']
    geofocus_choice_value = st.session_state['data'].get('geofocus_choice', [])
    st.write('Geofocus (e.g. regional or specific countries)')

    countries_checked_value = 'Countries' in geofocus_choice_value
    regions_checked_value = 'Regions' in geofocus_choice_value

    countries_checked = st.checkbox('Countries', value=countries_checked_value, key='countries_checkbox')
    regions_checked = st.checkbox('Regions', value=regions_checked_value, key='regions_checkbox')

    geofocus_choice = []
    if countries_checked:
        geofocus_choice.append('Countries')
    if regions_checked:
        geofocus_choice.append('Regions')
    st.session_state['data']['geofocus_choice'] = geofocus_choice

    if geofocus_choice:
        num_selections = len(geofocus_choice)
        cols = st.columns(num_selections)
        for idx, choice in enumerate(geofocus_choice):
            with cols[idx]:
                if choice == 'Regions':
                    # CGIAR regions, specify:
                    selected_regions_value = st.session_state['data'].get('selected_regions', [])
                    selected_regions = st.multiselect('CGIAR regions, specify:', options=regions, default=selected_regions_value, key='selected_regions')
                    st.session_state['data']['selected_regions'] = selected_regions
                elif choice == 'Countries':
                    # Countries, specify:
                    selected_countries_value = st.session_state['data'].get('selected_countries', [])
                    selected_countries = st.multiselect('Countries, specify:', options=countries, default=selected_countries_value, key='selected_countries')
                    st.session_state['data']['selected_countries'] = selected_countries

    # Innovation type
    innovation_type_value = st.session_state['data'].get('innovation_type', '')
    innovation_type = st.text_input('Innovation type (e.g. technology, policy, etc.)', value=innovation_type_value, key='innovation_type')
    st.session_state['data']['innovation_type'] = innovation_type

    # Target client
    target_client_value = st.session_state['data'].get('target_client', '')
    target_client = st.text_input('Target client (e.g. farmer, policymaker, researcher, etc.)', value=target_client_value, key='target_client')
    st.session_state['data']['target_client'] = target_client

    # Sustainable Development Goals (SDGs)
    sdgs_value = st.session_state['data'].get('sdgs', '')
    sdgs = st.text_input('Sustainable Development Goals (SDGs)', value=sdgs_value, key='sdgs')
    st.session_state['data']['sdgs'] = sdgs

    # Megatrends
    megatrends_value = st.session_state['data'].get('megatrends', '')
    megatrends = st.text_input('Megatrends (e.g. demographic trends, consumption patterns, health challenges, climate change, etc.)', value=megatrends_value, key='megatrends')
    st.session_state['data']['megatrends'] = megatrends

    # Commodity
    commodity_value = st.session_state['data'].get('commodity', '')
    commodity = st.text_input('Commodity (e.g. potato, rice, vegetables, livestock)', value=commodity_value, key='commodity')
    st.session_state['data']['commodity'] = commodity

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back3'):
            prev_step()
    with col2:
        if st.button('Next', key='next3'):
            next_step()

# Step 4 content
elif st.session_state['step'] == 4:
    st.title('Please select your innovation portfolio restrictions')

    # Pooled USD investment available
    st.subheader('Pooled USD investment available')
    investment_min_value = st.session_state['data'].get('investment_min', 0)
    investment_max_value = st.session_state['data'].get('investment_max', 5000000)
    min_value = st.number_input('Minimum investment amount ($):', min_value=0, max_value=5000000, value=investment_min_value, key='min_investment')
    max_value = st.number_input('Maximum investment amount ($):', min_value=0, max_value=5000000, value=investment_max_value, key='max_investment')
    st.session_state['data']['investment_min'] = min_value
    st.session_state['data']['investment_max'] = max_value

    # Priority Partnerships
    st.subheader('Priority Partnerships')
    partnership_options = ['Private sector', 'Government', 'NGO', 'Universities', 'Other']
    priority_partnership_value = st.session_state['data'].get('priority_partnership', partnership_options[0])
    priority_partnership = st.selectbox('Select priority partnership:', partnership_options, index=partnership_options.index(priority_partnership_value) if priority_partnership_value in partnership_options else 0, key='priority_partnership')
    if priority_partnership == 'Other':
        other_partnership_value = st.session_state['data'].get('other_partnership', '')
        other_partnership = st.text_input('Please specify other partnerships:', value=other_partnership_value, key='other_partnership')
        st.session_state['data']['priority_partnership'] = other_partnership
    else:
        st.session_state['data']['priority_partnership'] = priority_partnership

    # Risk profile
    st.subheader('Risk profile')
    risk_profile_value = st.session_state['data'].get('risk_profile', 'Low')
    risk_profile = st.radio('Select risk profile:', ['Low', 'Medium', 'High'], index=['Low', 'Medium', 'High'].index(risk_profile_value), key='risk_profile')
    st.session_state['data']['risk_profile'] = risk_profile

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back4'):
            prev_step()
    with col2:
        if st.button('Submit', key='submit'):
            # Output JSON and store data in pandas DataFrame
            data_df = pd.DataFrame([st.session_state['data']])
            st.session_state['data_df'] = data_df
            st.success('Your data has been collected successfully.')
            st.json(st.session_state['data'])
            next_step()

# Step 5 content
elif st.session_state['step'] == 5:
    st.title('Innovation Portfolio Overview')

    st.write('Below you find a proposed overview of innovations that meet your criteria and restrictions.')

    # Display map (placeholder)
    st.subheader('Countries that benefit from this proposal')
    st.map()  # Placeholder map

    # Display Action Areas (placeholder)
    st.subheader('Action Areas')
    action_areas = [
        'Nutrition, Health & Food Security',
        'Poverty Reduction, Livelihoods & Jobs',
        'Gender Equality, Youth & Social Inclusion',
        'Climate Adaptation & Mitigation',
        'Environmental Health & Biodiversity'
    ]
    action_percentages = [random.randint(10, 30) for _ in action_areas]
    action_data = pd.DataFrame({
        'Action Area': action_areas,
        'Percentage': action_percentages
    })
    st.bar_chart(action_data.set_index('Action Area'))

    # Placeholder for SDGs
    st.subheader('Sustainable Development Goals (SDGs)')
    sdg_data = pd.DataFrame({
        'SDG': [f'SDG {i}' for i in range(1, 8)],
        'Value': [random.randint(1, 10) for _ in range(1, 8)]
    })
    st.line_chart(sdg_data.set_index('SDG'))

    # Display collected data
    st.subheader('Your Input Summary')
    st.dataframe(st.session_state.get('data_df', pd.DataFrame()))

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back5'):
            prev_step()
    with col2:
        if st.button('Restart', key='restart'):
            reset_steps()

# Footer or Navigation
st.sidebar.title('Current Page')

# Retrieve the theme's primary color
primaryColor = st.get_option("theme.primaryColor") or '#F63366'  # Default Streamlit primary color

# Display steps in the sidebar, highlighting the current step
for i, step in enumerate(steps, start=1):
    if i == st.session_state['step']:
        # Highlight the current step using the theme's primary color
        st.sidebar.markdown(
            f"""
            <div style="background-color: {primaryColor}; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">
                {step}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.markdown(
            f"""
            <div style="padding: 10px;">
                {step}
            </div>
            """,
            unsafe_allow_html=True
        )

if st.sidebar.button('Restart', key='restart_sidebar'):
    reset_steps()
