import streamlit as st
import pandas as pd
import random

# Initialize session state variables
if 'step' not in st.session_state:
    st.session_state['step'] = 1

if 'data' not in st.session_state:
    st.session_state['data'] = {}

def next_step():
    st.session_state['step'] += 1

def prev_step():
    if st.session_state['step'] > 1:
        st.session_state['step'] -= 1

def reset_steps():
    st.session_state['step'] = 1
    st.session_state['data'] = {}

st.set_page_config(page_title="IPM - Innovation Portfolio Management")

# Step 1
if st.session_state['step'] == 1:
    st.title('What is the focus of your innovation portfolio?')

    st.write('Please select the focus areas of your innovation portfolio. You can select as many as you want.')

    focus_selected = False  # To ensure at least one focus area is selected

    entire_cgiar = st.checkbox('Entire CGIAR', key='entire_cgiar')
    if entire_cgiar:
        focus_selected = True
        st.session_state['data']['entire_cgiar'] = True

    initiative_program = st.checkbox('Initiative/ Program', key='initiative_program')
    if initiative_program:
        focus_selected = True
        initiatives_list = ['Initiative A', 'Initiative B', 'Initiative C']  # Replace with actual initiatives
        selected_initiatives = st.multiselect('If yes, which Initiative(s)/ Program(s):', initiatives_list, key='selected_initiatives')
        st.session_state['data']['selected_initiatives'] = selected_initiatives

    cgiar_centre = st.checkbox('CGIAR-centre', key='cgiar_centre')
    if cgiar_centre:
        focus_selected = True
        centres_list = ['Centre 1', 'Centre 2', 'Centre 3']  # Replace with actual CGIAR-centre(s)
        selected_centres = st.multiselect('If yes, which CGIAR-centre(s):', centres_list, key='selected_centres')
        st.session_state['data']['selected_centres'] = selected_centres

    country_region = st.checkbox('Country or Region', key='country_region')
    if country_region:
        focus_selected = True
        countries_list = ['Afghanistan', 'Brazil', 'Canada', 'Denmark', 'Ethiopia']  # Replace with actual countries or regions
        selected_countries = st.multiselect('If yes, which country/ies or region(s):', countries_list, key='selected_countries')
        st.session_state['data']['selected_countries'] = selected_countries

    thematic_area = st.checkbox('Thematic Area', key='thematic_area')
    if thematic_area:
        focus_selected = True
        thematic_areas_list = ['Agriculture', 'Climate Change', 'Food Security']  # Replace with actual thematic areas
        selected_thematic_areas = st.multiselect('If yes, which thematic areas:', thematic_areas_list, key='selected_thematic_areas')
        st.session_state['data']['selected_thematic_areas'] = selected_thematic_areas

    funder = st.checkbox('Funder', key='funder')
    if funder:
        focus_selected = True
        funders_list = ['Funder A', 'Funder B', 'Funder C']  # Replace with actual funders
        selected_funders = st.multiselect('If yes, which funders:', funders_list, key='selected_funders')
        st.session_state['data']['selected_funders'] = selected_funders

    fund_type = st.checkbox('Fund-type', key='fund_type')
    if fund_type:
        focus_selected = True
        fund_type_options = ['Pooled', 'Non-pooled']
        selected_fund_type = st.selectbox('Pooled/ non-pooled:', fund_type_options, key='selected_fund_type')
        st.session_state['data']['selected_fund_type'] = selected_fund_type

    # Additional focus
    st.write('Is there a different focus you would like to apply, that is not reflected above?')
    additional_focus = st.text_area('Please specify:', key='additional_focus')
    if additional_focus:
        st.session_state['data']['additional_focus'] = additional_focus

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

# Step 2
elif st.session_state['step'] == 2:
    st.title('Select areas you would like to prioritize in managing your innovation portfolio')

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
        if st.checkbox(option, key=f"option_{option}"):
            selected_options.append(option)

    additional_areas = st.text_input('Are there any areas that you would like to prioritize, but are not reflected in the above options?')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back2'):
            prev_step()
    with col2:
        if st.button('Next', key='next2'):
            if selected_options or additional_areas:
                st.session_state['data']['prioritized_areas'] = selected_options
                st.session_state['data']['additional_prioritized_areas'] = additional_areas
                next_step()
            else:
                st.warning('Please select at least one area to prioritize or specify additional areas.')

# Step 3
elif st.session_state['step'] == 3:
    st.title('Provide details for the selected prioritized areas')

    selected_options = st.session_state['data'].get('prioritized_areas', [])

    for option in selected_options:
        st.subheader(option)
        if 'Scaling readiness' in option:
            scaling_options = ['Early stage research', 'Proven innovation']
            scaling_readiness = st.multiselect('Select scaling readiness levels:', scaling_options, key='scaling_readiness')
            st.session_state['data']['scaling_readiness_detail'] = scaling_readiness
        elif 'Geofocus' in option:
            geofocus_options = ['Regional', 'Specific countries']
            geofocus_detail = st.selectbox('Select geofocus:', geofocus_options, key='geofocus_detail')
            if geofocus_detail == 'Specific countries':
                countries_list = ['Afghanistan', 'Brazil', 'Canada', 'Denmark', 'Ethiopia']
                selected_countries = st.multiselect('Select countries:', countries_list, key='geofocus_countries')
                st.session_state['data']['geofocus_countries_detail'] = selected_countries
            st.session_state['data']['geofocus_detail'] = geofocus_detail
        elif 'Innovation type' in option:
            innovation_types = ['Technology', 'Policy', 'Process', 'Service', 'Other']
            selected_types = st.multiselect('Select innovation types:', innovation_types, key='innovation_types')
            st.session_state['data']['innovation_types_detail'] = selected_types
        elif 'Target client' in option:
            target_clients = ['Farmer', 'Policymaker', 'Researcher', 'Extension worker', 'Other']
            selected_clients = st.multiselect('Select target clients:', target_clients, key='target_clients')
            st.session_state['data']['target_clients_detail'] = selected_clients
        elif 'Sustainable Development Goals' in option:
            sdg_options = [f'SDG {i}' for i in range(1, 18)]
            selected_sdgs = st.multiselect('Select SDGs:', sdg_options, key='sdgs')
            st.session_state['data']['sdgs_detail'] = selected_sdgs
        elif 'Megatrends' in option:
            megatrends = ['Demographic trends', 'Consumption patterns', 'Health challenges', 'Climate change', 'Urbanization', 'Other']
            selected_megatrends = st.multiselect('Select megatrends:', megatrends, key='megatrends')
            st.session_state['data']['megatrends_detail'] = selected_megatrends
        elif 'Commodity' in option:
            commodities = ['Potato', 'Rice', 'Vegetables', 'Livestock', 'Wheat', 'Maize', 'Other']
            selected_commodities = st.multiselect('Select commodities:', commodities, key='commodities')
            st.session_state['data']['commodities_detail'] = selected_commodities

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back3'):
            prev_step()
    with col2:
        if st.button('Next', key='next3'):
            next_step()

# Step 4
elif st.session_state['step'] == 4:
    st.title('Please select your innovation portfolio restrictions')

    # Pooled USD investment available
    st.subheader('Pooled USD investment available')
    min_value = st.number_input('Minimum investment amount ($):', min_value=0, max_value=5000000, value=0, key='min_investment')
    max_value = st.number_input('Maximum investment amount ($):', min_value=0, max_value=5000000, value=5000000, key='max_investment')
    st.session_state['data']['investment_min'] = min_value
    st.session_state['data']['investment_max'] = max_value

    # Priority Partnerships
    st.subheader('Priority Partnerships')
    partnership_options = ['Private sector', 'Government', 'NGO', 'Universities', 'Other']
    priority_partnership = st.selectbox('Select priority partnership:', partnership_options, key='priority_partnership')
    if priority_partnership == 'Other':
        other_partnership = st.text_input('Please specify other partnerships:', key='other_partnership')
        st.session_state['data']['priority_partnership'] = other_partnership
    else:
        st.session_state['data']['priority_partnership'] = priority_partnership

    # Risk profile
    st.subheader('Risk profile')
    risk_profile = st.radio('Select risk profile:', ['Low', 'Medium', 'High'], key='risk_profile')
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

# Step 5
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
    st.dataframe(st.session_state['data_df'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Back', key='back5'):
            prev_step()
    with col2:
        if st.button('Restart', key='restart'):
            reset_steps()

# Footer or Navigation (Optional)
st.sidebar.title('Navigation')
if st.sidebar.button('Restart', key='restart_sidebar'):
    reset_steps()
