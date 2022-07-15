import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go

# configuration
st.set_page_config(
    page_title='GetAround',
    layout='wide'
)

# set title and introduction
st.title('Users Checkout Delay Analysis')

st.markdown('''
    * Late returns at checkout can generate high friction for the next driver.
    * Users are dissatisfied for waiting for the car to come back from the previous rental or they even had to cancel their rental because the car wasn’t returned on time.
    * Thus, we’ve decided to implement a minimum delay between two rentals.
    * The following data analysis is used to help determine the selection of threshold and scope.
''')
  
# import dataset and show dataset  
@st.cache
def load_data():
    df = pd.read_excel('get_around_delay_analysis.xlsx')
    return df

df = load_data()
st.subheader('Load and showcase data')
data_load_state = st.text('Loading data...')
data = df.iloc[0:20,:]
data_load_state.text("") 

if st.checkbox('Show raw data'):
    st.write(data)      


# data insights
# Qestion 1 
st.subheader('Data Insights')
st.write('**1. Which share of our owner’s revenue would potentially be affected by the feature ?**')
st.write(" * When the state is 'ended', because delays occur when the state is completed")
fig = px.histogram(df,x='state',y='delay_at_checkout_in_minutes',text_auto='.2s')
fig.update_layout(title={
        'text': "The relationship between delay and state",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)


# Question 2 
st.write('**2. How many rentals would be affected by the feature depending on the threshold and scope we choose?**')
st.markdown('''
   * All vehicle orders that are delayed at checkout may be affected which means 52.58% rentals may be affected
   * Of this 52.58%, 'mobile' counts 84%, connect counts 16%
''' )

df_ended = df.loc[df['state']=='ended',:]
df_ended['is_delayed'] = df_ended['delay_at_checkout_in_minutes'].apply(lambda x: 'delayed' if x>=0 
                                                                        else 'non_delayed' if x<0
                                                                        else 'NaN') 
col1, col2 = st.columns(2)
with col1:
    fig = go.Figure(data=[go.Pie(labels=df_ended['is_delayed'].value_counts().index, 
                             values=df_ended['is_delayed'].value_counts().values, 
                             hole=.3)])
    fig.update_layout(title={
        'text': "Checkout Status",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig= px.histogram(df_ended.loc[df_ended['is_delayed']=='delayed',:],
                      x='checkin_type',
                      histnorm ='percent',
                      text_auto='.2',
                      )
    fig.update_layout(title={
        'text': "Delay at checkout according to different checkin type",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)


# Question 3
st.write('**3. How often are drivers late for the next check-in?**')
st.markdown('''
            * Drivers are often late under 100 minutes for the next check-in
''')

df_delay = df.loc[df['delay_at_checkout_in_minutes']>=0,:]

fig = px.histogram(df_delay,x='delay_at_checkout_in_minutes', 
                   histnorm='percent', 
                   text_auto='.2',
                   )
fig.update_layout(title={
    'text': "Distribution of delay at checkout in minutes",
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)

st.markdown('''
            * To be more precise, drivers are usually less than 20 minutes late
''')
fig = px.histogram(df_delay.loc[df_delay['delay_at_checkout_in_minutes'].between(0,300)], #delay time between 0 and 300 represents around 90% values
                   x='delay_at_checkout_in_minutes',
                   nbins=20,
                  )
fig.update_layout(title={
    'text': "Distribution of delay at checkout in minutes under 300 minutes",
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
st.plotly_chart(fig, use_container_width=True)

# Question 4
st.write('**4. How does the delay impact the next driver?**')
# define a function to do the aggregation
def line_agg(df,mask):
    df_new = df.sort_values(['car_id','rental_id']).loc[mask,['car_id','checkin_type','state','delay_at_checkout_in_minutes']]
    df_new = df_new.groupby(['car_id','checkin_type']).agg({'state':lambda x:x.to_list(),'delay_at_checkout_in_minutes':lambda x: x.tolist()})
    df_new = df_new.reset_index()
    return df_new

col1, col2 = st.columns(2)
with col1:   
    st.markdown('''
                * It maybe caused delay of checkout for the next driver
    ''')

    mask = df.delay_at_checkout_in_minutes>0
    delay_impact1 = line_agg(df,mask)
    mask = [delay_impact1['state'][i] for i in range(len(delay_impact1)) if 'canceled' not in delay_impact1['state'][i]]
    data_show = delay_impact1.loc[delay_impact1['state'].isin(mask),:]
    st.dataframe(data_show) 

with col2:
    st.markdown('''
                * It maybe caused cancelation of next booking
    ''')
    mask = (~((df['state']=='ended') & (df['delay_at_checkout_in_minutes'].isnull()))) & (~(df.delay_at_checkout_in_minutes<0))
    delay_impact2 = line_agg(df,mask)

    mask=[]
    for x in delay_impact2.state:
        for i in range(len(x)-1):
            if x[i]=='ended' and x[i+1]=='canceled':
                mask.append(x)
                
    delay_impact2 = delay_impact2.loc[delay_impact2['state'].isin(mask),:]
    data_show = delay_impact2.reset_index(drop=True)
    st.dataframe(data_show)

# Question 5
st.write('**5. How many problematic cases will it solve depending on the chosen threshold and scope?**')

# define 2 functions to calculate solved cases  
def ceses_solved_ended(df,threshold,scope):
    mask = (df['delay_at_checkout_in_minutes']>threshold) & (df['checkin_type']==scope)
    cases_solved = df.loc[mask,'delay_at_checkout_in_minutes'].count()
    return cases_solved


def cases_solved_canceled(df,threshold,scope):
    mask = (~((df['state']=='ended') & (df['delay_at_checkout_in_minutes'].isnull()))) & (~(df.delay_at_checkout_in_minutes<threshold))
    delay_impact2 = line_agg(df,mask)

    mask=[]
    for x in delay_impact2.state:
        for i in range(len(x)-1):
            if x[i]=='ended' and x[i+1]=='canceled':
                mask.append(x)
            
    delay_impact2 = delay_impact2.loc[delay_impact2['state'].isin(mask),:]
    delay_impact2 = delay_impact2.loc[delay_impact2['checkin_type']==scope,:]
    return delay_impact2.shape[0]

st.markdown("""
            * First let's look at what happens when the threshold is 300 minutes
            * It means we ignore 10% of the delayed values 
            """)
col1,col2 = st.columns(2)
with col1:
    threshold = 300

    scope1 = 'connect'
    cases_solved_connect = ceses_solved_ended(df,threshold,scope1) + cases_solved_canceled(df,threshold,scope1)

    scope2 = 'mobile'
    cases_solved_mobile = ceses_solved_ended(df,threshold,scope2) + cases_solved_canceled(df,threshold,scope2)

    total_num_delay = df.loc[df['delay_at_checkout_in_minutes']>0,:].shape[0] 
    values = [cases_solved_connect,cases_solved_mobile,total_num_delay-(cases_solved_mobile+cases_solved_connect)]
    names = ['cases_resolved_connect','cases_resolved_mobile','unresolved delays']
    fig = px.pie(values=values, names=names)
    st.plotly_chart(fig,use_container_width=True)

with col2:
    fig = px.histogram(df_delay.loc[df_delay['delay_at_checkout_in_minutes'].between(0,300)], 
                   x='delay_at_checkout_in_minutes', 
                   histnorm='percent', 
                   text_auto='.2', 
                   nbins=10,)
    fig.update_layout(title={
    'text': "Distribution of delay at checkout in minutes under 300 minutes",
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
    st.plotly_chart(fig,use_container_width=True)


# show results according to threshold
st.subheader('Result')
col1,col2 = st.columns(2)
threshold_values = [250,200,150,100,50,25]
with col1:
    with st.form("Show resolved cases according to threshold and scope"):
        st.write('**Show resolved cases according to threshold**')
        threshold = st.selectbox("Select a threshold", threshold_values)
        submit = st.form_submit_button("submit")

        if submit:
            scope1 = 'connect'
            cases_solved_connect = ceses_solved_ended(df,threshold,scope1) + cases_solved_canceled(df,threshold,scope1)

            scope2 = 'mobile'
            cases_solved_mobile = ceses_solved_ended(df,threshold,scope2) + cases_solved_canceled(df,threshold,scope2)

            total_num_delay = df.loc[df['delay_at_checkout_in_minutes']>0,:].shape[0] 
            values = [cases_solved_connect,cases_solved_mobile,total_num_delay-(cases_solved_mobile+cases_solved_connect)]
            names = ['cases_resolved_connect','cases_resolved_mobile','unresolved delays']
            

with col2:
    fig = px.pie(values=values, names=names)
    st.plotly_chart(fig,use_container_width=True)