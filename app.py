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
    st.session_state['step'] -= 1

def reset_steps():
    st.session_state['step'] = 1
    st.session_state['data'] = {}

st.set_page_config(page_title="IPM - Innovation Portfolio Management")

# Step 1
if st.session_state['step'] == 1:
    st.title('Please select your innovation portfolio characteristics and criteria')

    # Geofocus
    geofocus_options = [
        'Balanced across initiatives countries',
        'Balance across CGIAR regions',
        'Focus on selected countries'
    ]
    geofocus = st.selectbox('Geofocus:', geofocus_options)

    if geofocus == 'Focus on selected countries':
        countries_list = ['Afghanistan', 'Brazil', 'Canada', 'Denmark', 'Ethiopia']  # Replace with actual country names
        selected_countries = st.multiselect('Select countries:', countries_list)
    else:
        selected_countries = None

    # Innovation Readiness
    innovation_readiness_options = [
        'Balanced across Innovation readiness levels',
        'Tailored innovation readiness focus'
    ]
    innovation_readiness = st.selectbox('Innovation Readiness:', innovation_readiness_options)

    if innovation_readiness == 'Tailored innovation readiness focus':
        st.write('Please select the focus areas and specify the percentage for each (total must sum to 100%):')
        focus_areas = {}
        total_percentage = 0
        cols = st.columns(2)
        with cols[0]:
            if st.checkbox('Ideation and research'):
                percentage = st.number_input('Percentage for Ideation and research (%)', min_value=0, max_value=100, value=0, key='Ideation')
                focus_areas['Ideation and research'] = percentage
                total_percentage += percentage
            if st.checkbox('Incubation'):
                percentage = st.number_input('Percentage for Incubation (%)', min_value=0, max_value=100, value=0, key='Incubation')
                focus_areas['Incubation'] = percentage
                total_percentage += percentage
        with cols[1]:
            if st.checkbox('Acceleration'):
                percentage = st.number_input('Percentage for Acceleration (%)', min_value=0, max_value=100, value=0, key='Acceleration')
                focus_areas['Acceleration'] = percentage
                total_percentage += percentage
            if st.checkbox('Scaling-ready'):
                percentage = st.number_input('Percentage for Scaling-ready (%)', min_value=0, max_value=100, value=0, key='Scaling-ready')
                focus_areas['Scaling-ready'] = percentage
                total_percentage += percentage
        if total_percentage != 100:
            st.warning('Total percentage must sum to 100%')
    else:
        focus_areas = None

    # End of Initiative Outcomes (EoIO)
    eoio_options = [
        'Balanced across End of Initiative Outcomes (EoIO)',
        'Tailored End of Initiative Outcomes (EoIO)'
    ]
    eoio = st.selectbox('End of Initiative Outcomes (EoIO):', eoio_options)

    if eoio == 'Tailored End of Initiative Outcomes (EoIO)':
        st.write('Please select the EoIOs and specify the percentage for each (total must sum to 100%):')
        eoio_areas = {}
        total_eoio_percentage = 0
        cols = st.columns(2)
        with cols[0]:
            if st.checkbox('EoIO1'):
                percentage = st.number_input('Percentage for EoIO1 (%)', min_value=0, max_value=100, value=0, key='EoIO1')
                eoio_areas['EoIO1'] = percentage
                total_eoio_percentage += percentage
            if st.checkbox('EoIO2'):
                percentage = st.number_input('Percentage for EoIO2 (%)', min_value=0, max_value=100, value=0, key='EoIO2')
                eoio_areas['EoIO2'] = percentage
                total_eoio_percentage += percentage
        with cols[1]:
            if st.checkbox('EoIO3'):
                percentage = st.number_input('Percentage for EoIO3 (%)', min_value=0, max_value=100, value=0, key='EoIO3')
                eoio_areas['EoIO3'] = percentage
                total_eoio_percentage += percentage
            if st.checkbox('EoIO4'):
                percentage = st.number_input('Percentage for EoIO4 (%)', min_value=0, max_value=100, value=0, key='EoIO4')
                eoio_areas['EoIO4'] = percentage
                total_eoio_percentage += percentage
        if total_eoio_percentage != 100:
            st.warning('Total percentage must sum to 100%')
    else:
        eoio_areas = None

    if st.button('Next'):
        st.session_state['data']['geofocus'] = geofocus
        if selected_countries:
            st.session_state['data']['selected_countries'] = selected_countries
        st.session_state['data']['innovation_readiness'] = innovation_readiness
        if focus_areas:
            st.session_state['data']['focus_areas'] = focus_areas
        st.session_state['data']['eoio'] = eoio
        if eoio_areas:
            st.session_state['data']['eoio_areas'] = eoio_areas

        valid = True
        if innovation_readiness == 'Tailored innovation readiness focus' and total_percentage != 100:
            valid = False
            st.warning('Please ensure total percentages sum to 100% for Innovation Readiness.')
        if eoio == 'Tailored End of Initiative Outcomes (EoIO)' and total_eoio_percentage != 100:
            valid = False
            st.warning('Please ensure total percentages sum to 100% for EoIO.')

        if valid:
            next_step()

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
        if st.checkbox(option):
            selected_options.append(option)

    additional_areas = st.text_input('Are there any areas that you would like to prioritize, but are not reflected in the above options?')

    if st.button('Next'):
        if selected_options:
            st.session_state['data']['prioritized_areas'] = selected_options
            st.session_state['data']['additional_prioritized_areas'] = additional_areas
            next_step()
        else:
            st.warning('Please select at least one area to prioritize.')

    if st.button('Back'):
        prev_step()

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
            sdg_options = [f'SDG {i}' for i in range(1,18)]
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

    if st.button('Next'):
        next_step()
    if st.button('Back'):
        prev_step()

# Step 4
elif st.session_state['step'] == 4:
    st.title('Please select your innovation portfolio restrictions')

    # Polled USD investment available
    st.subheader('Polled USD investment available')
    min_value = st.number_input('Minimum investment amount ($):', min_value=0, max_value=5000000, value=0)
    max_value = st.number_input('Maximum investment amount ($):', min_value=0, max_value=5000000, value=5000000)
    st.session_state['data']['investment_min'] = min_value
    st.session_state['data']['investment_max'] = max_value

    # Priority Partnerships
    st.subheader('Priority Partnerships')
    partnership_options = ['Private sector', 'Government', 'NGO', 'Universities', 'Other']
    priority_partnership = st.selectbox('Select priority partnership:', partnership_options)
    if priority_partnership == 'Other':
        other_partnership = st.text_input('Please specify other partnerships:')
        st.session_state['data']['priority_partnership'] = other_partnership
    else:
        st.session_state['data']['priority_partnership'] = priority_partnership

    # Risk profile
    st.subheader('Risk profile')
    risk_profile = st.radio('Select risk profile:', ['Low', 'Medium', 'High'])
    st.session_state['data']['risk_profile'] = risk_profile

    if st.button('Submit'):
        # Output JSON and store data in pandas DataFrame
        data_df = pd.DataFrame([st.session_state['data']])
        st.session_state['data_df'] = data_df
        st.success('Your data has been collected successfully.')
        st.json(st.session_state['data'])
        next_step()

    if st.button('Back'):
        prev_step()

# Step 5
elif st.session_state['step'] == 5:
    st.title('Innovation Portfolio Overview')

    st.write('Below you find a proposed overview of innovations that meet your criteria and restrictions.')

    # Display map (placeholder)
    st.subheader('Countries that benefit from this proposal')
    st.map()  # Placeholder map

    # Display Action Areas (placeholder)
    st.subheader('Action Areas')
    action_areas = ['Nutrition, Health & Food Security',
                    'Poverty Reduction, Livelihoods & Jobs',
                    'Gender Equality, Youth & Social Inclusion',
                    'Climate Adaptation & Mitigation',
                    'Environmental Health & Biodiversity']
    action_percentages = [random.randint(10,30) for _ in action_areas]
    action_data = pd.DataFrame({
        'Action Area': action_areas,
        'Percentage': action_percentages
    })
    st.bar_chart(action_data.set_index('Action Area'))

    # Placeholder for SDGs
    st.subheader('Sustainable Development Goals (SDGs)')
    sdg_data = pd.DataFrame({
        'SDG': [f'SDG {i}' for i in range(1, 8)],
        'Value': [random.randint(1,10) for _ in range(1,8)]
    })
    st.line_chart(sdg_data.set_index('SDG'))

    # Display collected data (placeholder)
    st.subheader('Your Input Summary')
    st.dataframe(st.session_state['data_df'])

    if st.button('Refresh information'):
        reset_steps()

    if st.button('Back'):
        prev_step()

# Footer or Navigation (Optional)
st.sidebar.title('Navigation')
if st.sidebar.button('Restart'):
    reset_steps()