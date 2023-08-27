
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go



df = pd.read_excel("Olympic Athletes.xlsx").drop(["Closing Ceremony Date"], axis = 1) #load dataset
df = df.dropna()
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title= "Olympic EDA",
                   page_icon=":bar_chart:",
                   layout="wide")
#st.title("EDA Olympic Athletes 🏅" )
st.markdown('##')


st.sidebar.header("Please Filtrer Here : ")


annee = st.sidebar.multiselect(
    "Select the Year:",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

#tout = [i for i in df["Country"].unique()]
#pays = st.sidebar.multiselect(
 #   "Select the Country:",
  #  options=df["Country"].unique(),
   # default=tout,

    #)

#sport = st.sidebar.multiselect(
 #   "Select the Sport:",
  #  options=df["Sport"].unique(),
   # default=df["Sport"].unique()
#)

df_selection = df.query("Year == @annee ")

#TOP KPI

total_sport = df_selection['Sport'].nunique()

total_pays = df_selection['Country'].nunique()

total_medaille = df_selection['Total Medals'].sum()

total_med_dor=df_selection['Gold Medals'].sum()

total_med_dar=df_selection['Silver Medals'].sum()

total_med_br = df_selection['Bronze Medals'].sum()

pays_plus_medaille = df_selection.groupby(by=['Country']).sum()[['Total Medals']]

premier_col , deuxieme_col, troisieme_col, quatrieme_col, cinquieme_col, sixieme_col, septieme_col = st.columns(7)

with premier_col :
    st.subheader("Total Sports")
    st.subheader(f'🎯{total_sport}')
with deuxieme_col :
    st.subheader("Total Country")
    st.subheader(f'🌎{total_pays}')
with troisieme_col:
    st.subheader("Gold Medals")
    st.subheader(f'🥇{total_med_dor}')
with quatrieme_col:
    st.subheader("Silver Medals")
    st.subheader(f'🥈{total_med_dar}')
with cinquieme_col:
    st.subheader("Bronze Medals")
    st.subheader(f'🥈{total_med_br}')
with sixieme_col:
    st.subheader("Total Medals")
    st.subheader(f'🏅{total_medaille}')

with septieme_col:
    st.subheader("Pays avec plus de medailles")
    st.subheader(f'🗺️{pays_plus_medaille["Total Medals"].idxmax()}')

st.markdown("----")

with st.container():
   medaille_par_annee=df_selection.groupby(by=['Year']).sum()[['Gold Medals','Silver Medals','Bronze Medals','Total Medals']].sort_values(by=['Gold Medals'],ascending=False)
#fig_med_anne = px.area(medaille_par_annee, facet_col=",  facet_col_wrap=2)
   fig_med_anne = px.bar(medaille_par_annee,
                      title="<b>Medailles par annee</b>"
                      )
   st.plotly_chart(fig_med_anne)

with st.container():
    st.subheader("Repartition par sport : ")
    p_col,d_col = st.columns(2)
    with p_col:
        medaille_par_sport = df_selection.groupby(by=['Sport']).sum()[
        ['Gold Medals','Silver Medals','Bronze Medals','Total Medals']].sort_values(by=['Total Medals'],
                                                                                       ascending=False)
        fig_med_sport= px.bar(medaille_par_sport,
                          title="<b> la répartition des médailles par sport</b>")
        st.plotly_chart(fig_med_sport)
        with d_col:
            sports_by_year = df_selection.pivot_table(index='Year', columns='Sport', values='Total Medals', aggfunc='count',
                                            fill_value=0)
            fig_sby = px.imshow(sports_by_year,
                            labels=dict(x="Sport", y="Année", color="Nombre de sports"),
                            x=sports_by_year.columns,
                            y=sports_by_year.index,
                            color_continuous_scale='Viridis')

            # Ajouter un titre et ajuster la mise en page
            fig_sby.update_layout(title="Sports les plus courants par année",
                              xaxis_title="Sport",
                              yaxis_title="Année")
            st.plotly_chart(fig_sby)

with st.container():
    st.subheader("Analyse Par Pays ")
    a_col,b_col = st.columns(2)
    with a_col:
        medaille_par_pays = df_selection.groupby(by=['Country']).sum()[['Total Medals']].sort_values(by=['Total Medals'],ascending=False)
        # Créer la carte géographique
        fig_med_pays =px.scatter_geo(medaille_par_pays, locations=medaille_par_pays.index, color=medaille_par_pays.index,
                     hover_name='Total Medals',
                     hover_data='Total Medals',
                    locationmode='country names',
                    projection = 'natural earth'
                   )

        fig_med_pays.update_layout(title="Pays avec les plus de médailles")
        st.plotly_chart(fig_med_pays)

    with b_col:
        pays_plus_medaille_orb = df.groupby(by=['Country']).sum()[['Gold Medals','Silver Medals','Bronze Medals']].sort_values(by=['Gold Medals'],ascending=False)
        fig_orb = px.bar(pays_plus_medaille_orb, barmode='group',title='Medailles en fonction des pays',text_auto='.2s')
        fig_orb.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_orb)


with st.container():
    st.subheader("Repartition par Age")
    f_col, s_col = st.columns(2)
    with f_col:

        fig_age = px.histogram(df_selection, x = "Age",title="Distribution de l'age des athletes ")
        st.plotly_chart(fig_age)

    with s_col:
        #Ajout d'une nouvelle colonne
        age_bins = [15, 20, 30,65]
        age_labels = ['15-19', '20-30', '31-65']
        df_selection.loc[df['Age'], 'Age Groupe'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

        medaill_par_age = df_selection.groupby(by=['Age Groupe']).sum()[['Gold Medals','Silver Medals','Bronze Medals']]

        fig_med_age = px.bar(medaill_par_age,
             labels={'index': 'Groupe d\'âge', 'value': 'Nombre de médailles'},
             title="Médailles obtenues par groupe d'âge",
             barmode='stack')
        st.plotly_chart(fig_med_age)




with st.container():
    st.subheader("Correlation entre medailles")
    med = df_selection[['Gold Medals', 'Silver Medals', 'Bronze Medals']]
    med_cor = med.corr()
    fig_med_corr = px.imshow(med_cor, text_auto=True, aspect="auto")
    st.plotly_chart(fig_med_corr)

with st.container():
    st.subheader("Performance Remarquable")
    k = df.groupby(by=['Athlete']).sum()[['Gold Medals', 'Silver Medals', 'Bronze Medals', 'Total Medals']].sort_values(
        by=['Total Medals'], ascending=False)

    fig_k = go.Figure(data=[go.Table(

        columnwidth=[400, 400],
        header=dict(
            values=['<b>Athlete</b>',
                 '<b>Gold Medals</b>', '<b>Silver Medals</b>', '<b>Bronze Medals</b>', '<b>Total Medals</b>'],
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=[k.index, k['Gold Medals'], k['Silver Medals'], k['Bronze Medals'], k['Total Medals']],
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white']),
            align=['left', 'center'],
            font_size=12,
            height=30)
    )
    ])
    fig_k.update_layout(title = "<b>Nombre de medailles par athlete")
    st.plotly_chart(fig_k)
#st.dataframe(df_selection)
