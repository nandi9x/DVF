#Projet data visualisation - Ananda YEANN DS5 20181070
#Ventes immobilières en IDF sur l'année 2019/2020 
#https://github.com/nandi9x/DVF.git



from os import defpath
import pandas as pd
#from pandas.core.base import DataError
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px
import time 
from datetime import datetime
from datetime import datetime as dt



st.set_page_config(
    
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="ventes IDF",
    page_icon=None, 
)

#data loading sur jupyter notebook, TROP DE TEMPS A CHARGER ICI 
#

# #----------------- data loading -----------------#
def timer(func):
    def wrapper(*args, **kwargs):
        with open("temps_charge.txt", "a") as f:
            before = time.time()
            val = func(*args, **kwargs)
            timefin= time.time() - before
            f.write('at : '+ str(datetime.now()) + ' the function ' + func.__name__ + ' took:  ' + str(timefin) + ' second \n')
        return val
    return wrapper

@timer
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loading(path):
    return pd.read_csv(path, low_memory = False)

def loading_state(df):
    return df.sample(100000)



# #----------------- explore and process -----------------#

# #on supprime les colonnes avec beaucoup de valeurs nulles
# def process (df):
#     df= df.drop(['id_mutation','numero_disposition','adresse_numero', 'adresse_suffixe','adresse_code_voie','code_postal',
#                 'code_commune','lot1_numero','lot1_surface_carrez','id_parcelle','ancien_id_parcelle','numero_volume',
#                 'lot2_numero','lot2_surface_carrez', 'adresse_suffixe','lot3_numero', 'lot3_surface_carrez',
#                 'nombre_pieces_principales','lot4_numero','lot4_surface_carrez','lot5_numero','lot5_surface_carrez',
#                 'nombre_lots','code_type_local','surface_reelle_bati', 'code_nature_culture_speciale', 'nature_culture',
#                 'nature_culture_speciale','code_nature_culture','ancien_code_commune', 'nombre_lots','ancien_nom_commune',], axis=1)
                        

#         #suppression valeurs manquantes et on garde que type vente

@st.cache(suppress_st_warning=True)
def post_cleaning(df):
     df.dropna(subset = ["longitude"], inplace=True) #necessaire pour st.map
     df.dropna(subset = ["latitude"], inplace=True)
     df.dropna(subset = ["adresse_nom_voie"], inplace=True)
   


#     df.dropna(subset = ["type_local"], inplace=True)
#     df.drop(df.loc[df['nature_mutation']!='Vente'].index, inplace=True)


#         #analyse que IDF donc suppression des autres départements 
#     df.drop(df.loc[ 
#             (df['code_departement']!='91') & (df['code_departement']!='92') & (df['code_departement']!='93') &
#             (df['code_departement']!='94') & (df['code_departement']!='95') & (df['code_departement']!='75') &
#             (df['code_departement']!='77') & (df['code_departement']!='78')].index, inplace= True)


#         #changement dtype
#     df['code_departement']=df['code_departement'].astype('int')


    #df2020 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2020.csv')
    #df2019 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2019.csv')
    #process(df2019)
    #process(df2020)

    #création csv normalisé et fusion des 2 dans un dvf.csv : celui que l'on utilisera tout au long
    #df2020.to_csv('2020new.csv', index = False)
    #df2019.to_csv('2019new.csv', index = False)
    
    #a= pd.read_csv("2019new.csv")
    #b = pd.read_csv("2020new.csv")
    #df = a.merge(b,how='outer')

    #df.to_csv('dvf.csv', index=False)

 #----------------- data vizualisation and analysis -----------------#

# functions for analysis #
def get_year(dt):
   return dt.year

def get_month(dt):
    return dt.month

    
def transformation(df):
    df['date_mutation']= pd.to_datetime(df['date_mutation'])
    #df['latitude']=pd.to_numeric(df['latitude'])
    #df['longitude']=pd.to_numeric(df['longitude'])
    df['year']=df['date_mutation'].map(get_year)
    df['month']=df['date_mutation'].map(get_month)


def count_rows(rows):
    return len(rows)

@st.cache(suppress_st_warning=True)
def map_by(laptime, df):
    return df.groupby(laptime).apply(count_rows)

 
###–----------functions graphics----------###

#NOMBRE VENTE#

#fig1 : quel type est le plus vendu 2019
def ext1_type_2019 ():
    fig = plt.figure(figsize=(5,5))
    labels = [ 'Maison', 'Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé']
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fffc52']
    #a = df19['type_local'].value_counts(dropna = False, normalize = True)
    area = [44.3, 29.1, 19.3, 7]
    plt.pie(area, labels=labels, colors= colors, startangle=70, autopct='%1.1f%%')
    plt.title(label= 'Répartition du type de local vendus')
    plt.legend()
    plt.show()
    st.pyplot(fig)


#fig2: nb ventes par mois   
def ext2_monthcount(df):
    fig= plt.figure(figsize=(5,5))
    plt.title (label= 'Nombre de ventes totaux par mois')
    sb.countplot(x='month',data=df)
    st.pyplot(fig)

#fig3: par departement
def ext3_countdep(df):
    fig = plt.figure(figsize=(10,10))
    plt.title(label= 'Nombre de ventes totaux par département')
    sb.countplot(x='code_departement', data=df)
    st.pyplot(fig)

#fig7: hist   
def ext7(df):
    plt.grid(True)
    fig = plt.figure(figsize =(5,5))
    plt.hist(df.month, bins = 12, range = (1, 12), color = 'red' )
    plt.xlabel('mois')
    plt.ylabel('nombre')
    plt.title('nombre de vente par mois')
    st.pyplot(fig)


#VALFONCIERES#

#fig4: lien entre valeurs et département probleme - ne s'affiche pas pourtant marche 
def ext4_valdep(df):
    fig = plt.figure(figsize=(10,10))
    sb.catplot(x='code_departement',y='valeur_fonciere', data=df,kind='strip')
    st.pyplot(fig)

#fig5: par mois 
def ext5_val(df):
    nature = df.groupby('month')['valeur_fonciere'].sum()
    fig = px.bar(nature,y='valeur_fonciere')
    st.plotly_chart(fig)

#fig6: par departement 
def ext6_val(df):
    fig = plt.figure(figsize=(10,10))
    sb.barplot(x='code_departement',y='valeur_fonciere',data=df, estimator=np.mean)
    st.pyplot(fig)




###–----------map----------###

@st.cache(suppress_st_warning=True)
def map(df):
    df = df.astype({'latitude':float,'longitude':float})
    gpspoints={'latitude':df['latitude'],'longitude':df['longitude']}
    map_data = pd.DataFrame(data=gpspoints)
    st.map(map_data)

def heat(df):
    fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='valeur_fonciere', radius=5,
    center=dict(lat=48.8499198, lon=2.6370411), zoom=7, 
    mapbox_style="open-street-map")
    st.plotly_chart(fig)


#filtrage département, a la main car n'a pas réussi à faire en une fois 

def mask2(df, option):
    mask_dep = df['code_departement'].isin(option)
    df = df[mask_dep]

#departement
def filtre_dep(df):
    mask = (df['code_departement'] == '91')
    df = df[mask]
    return df

#type
def filtre_type_appart(df):
    mask = (df['type_local']=='Appartement')
    df = df[mask]
    return df 

def filtre_type_local(df):
    mask = (df['type_local']=='Local industriel. commercial ou assimilé')
    df = df[mask]
    return df 

def filtre_type_maison(df):
    mask = (df['type_local']=='Maison')
    df = df[mask]
    return df 

def filtre_type_dependance(df):
    mask = (df['type_local']=='Dépendance')
    df = df[mask]
    return df 

#valeurs foncieres 
def filtre_val1(df):
    mask = (df['valeur_fonciere']<300000)
    df = df[mask]
    return df

def filtre_val2(df):
    mask = (df['valeur_fonciere']>300000) & (df['valeur_fonciere']< 800000)
    df = df[mask]
    return df

def filtre_val3(df):
    mask = (df['valeur_fonciere']>800000) & (df['valeur_fonciere']< 10000000)
    df = df[mask]
    return df

def filtre_val4(df):
    mask = (df['valeur_fonciere']>10000000) & (df['valeur_fonciere']< 400000000)
    df = df[mask]
    return df

    




#--------------main --------------#

def main():
    st.title('Ventes immobilières en IDF 2019-2020 🏘️')
    st.markdown('Depuis mai 2019, le gouvernement a mis en ligne les données "Demande de Valeurs Foncières" (DVF)')
    st.write('Voici un aperçu des ventes de 2016 à 2020')
    col1, col2, col3, col4, col5 = st.columns(5)
    #fonction count_rows pour connaître 
    col1.metric("2016", "341 038")
    col2.metric("2017", "379 022", "11.14 %")
    col3.metric("2018", "373 267", "-1.58 %")
    col4.metric("2019", "393 325", "+6.97 %")
    col5.metric("2020", "312 428", "-20.61 %")

    #st.table(df.columns)
    #st.write(df.isnull().sum())



    'Pour les visualisations suivantes, nous nous concentrons sur les années 2019/2020. Le dataset a été réduit à 100000 échantillons'
    nav = st.selectbox('Que veux-tu visualiser?',['','Graphique','Data', 'Map'])

    if nav == 'Graphique' :
        annee = st.selectbox('Quelle année?',['','2019','2020'])

        if annee == '2019':
            df2019 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2019new.csv') 
            df2019 = loading_state(df2019)
            transformation(df2019)
            post_cleaning(df2019)
            #st.write(count_rows(df2019))

            ##regroupement par 
            by_month = map_by('month', df2019)
            by_department = map_by('code_departement', df2019)
            by_type = map_by('type_local', df2019)

            ##--nombres ventes--##
            st.title('Nombre de ventes par:')        
            choix = st.radio(' ',['mois', 'type de local', 'département'])
            if choix == 'mois':
                ext2_monthcount(df2019)

            elif choix == 'type de local':
                ext1_type_2019()

            elif choix == 'département':
                ext3_countdep(df2019)
                #st.bar_chart(by_department)

            ##--valeurs foncieres--##
            st.title('Valeurs foncières par:')
            choix = st.radio(' ',['mois', 'département'])
            if choix == 'mois':
                st.line_chart(by_month)

            elif choix == 'département':
                #ext4_valdep(df2019) #ne s'affiche pas mais marche sur jupyter. pb d'affichage? 
                ext6_val(df2019)
        #------------------#
        if annee == '2020':
            df2020 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2020new.csv')
            df2020 = loading_state(df2020)
            transformation(df2020)
            post_cleaning(df2020)

            #regroupement par:
            by_month = map_by('month', df2020)
            by_department = map_by('code_departement', df2020)
            by_type = map_by('type_local', df2020)

            st.title('Nombre de ventes par:')        
            choix = st.radio(' ',['mois', 'type de local', 'département'])
            if choix == 'mois':
                ext7(df2020)

            elif choix == 'type de local':
                st.area_chart(by_type)

            elif choix == 'département':
                st.bar_chart(by_department)

            ##--valeurs foncieres--##
            st.title('Valeurs foncières par:')
            choix = st.radio(' ',['mois', 'département'])
            if choix == 'mois':
                ext5_val(df2020)


            elif choix == 'département':
                ext6_val(df2020)


        
    if nav == 'Data':
        df = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2019new.csv')
        df = loading_state(df)
        transformation(df)
        post_cleaning(df)
        #st.write(count_rows(df))

        st.title('Dataset de 2019')
        a = st.checkbox('afficher le dataset de 2020')
        df20 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2020new.csv')
        df20 = loading_state(df20)
        transformation(df20)
        post_cleaning(df20)
        if a ==True:
            st.dataframe(df20)
        else:
            st.dataframe(df)
        
        
        b = st.checkbox('voir plus')
        if b == True:
            st.title('Informations complémentaires')
            st.header('statistiques de 2019')
            c = st.checkbox('afficher les stats de 2020')
            if c == True:
                st.dataframe(df20.describe())
            else :
                st.dataframe(df.describe())
            
            st.markdown('** valeurs foncieres ** : Il s’agit du montant ou de l’évaluation déclaré(e) dans le cadre d’une mutation à titre onéreux.')
            'La valeur foncière inclut : les frais d’agence (s’ils sont à la charge du vendeur), l’éventuelle TVA'
            'exclut : les frais d’agence (s’ils sont à la charge de l’acquéreur), les frais de notaires'
            st.markdown('** nature_mutation ** : vente, vente en l’état futur d’achèvement, vente de terrain à bâtir, adjudication, expropriation ou échange')
            st.markdown('** surface_terrain** : contenance du terrain')
            st.caption('plus d\'informations sur  https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/ ')

    

    if nav == "Map" :
        st.title('Map des ventes en Ile-De-France')
        st.sidebar.title('Filtre')
        op = st.sidebar.selectbox ('choisis l\'année',['', '2019','2020']) 
    
        #année 2019
        if op == '2019':
            df19 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2019new.csv')
            df19 = loading_state(df19)
            transformation(df19)
            post_cleaning(df19)
            df19 = df19.sample(100000, replace=True)

            #date - streamlit crash, trop de temps à charger
            #min_ts = datetime.timestamp(min(df19["date_mutation"]))
            #max_ts=  datetime.timestamp(max(df19["date_mutation"]))
            #min_selection, max_selection = st.sidebar.slider("Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts])
            #df = df19[(df19["date_mutation"] >= min_selection) & (df19["date_mutation"] <= max_selection)]
            #st.map(df19)
            
            #departement - ne marche pas  
            #dep =st.sidebar.select_slider(' choisis le département', df19['code_departement'].unique())
            #if dep == '91':
             #   newdata = filtre_dep(df19)
              #  st.map(newdata)
            
            #type_local
            type = st.sidebar.selectbox('choisis le type', df19['type_local'].unique())
            if type == 'Appartement' :
                newdata = filtre_type_appart(df19)
                #st.dataframe(newdata.tail())
                t = st.map(newdata)

            if type == 'Local industriel. commercial ou assimilé' :
                newdata = filtre_type_local(df19)
                #st.dataframe(newdata.tail())
                t = st.map(newdata)

            if type == 'Maison' :
                newdata = filtre_type_maison(df19)
                #st.dataframe(newdata.tail())
                t= st.map(newdata)

            if type == 'Dépendance' :
                newdata = filtre_type_dependance(df19)
                #st.dataframe(newdata.tail())
                t= st.map(newdata)
            else:
                ''
            
            #valeurs foncieres
            a = st.sidebar.checkbox('filtre avec valeurs foncières ?')
            if a == True:

                val = st.sidebar.select_slider('choisis un intervalle de valeurs foncières', ['0 €','300 000 €', '800 000 €', '10 000 000 €','400 000 000 €'])
                if val == '300 000 €' :
                    newdata = filtre_val1(df19)
                    #st.dataframe(newdata.tail())
                    heat(newdata)
                
                if val == '800 000 €' :
                    newdata = filtre_val2(df19)
                    #st.dataframe(newdata.tail())
                    heat(newdata)

                if val == '10 000 000 €' :
                    newdata = filtre_val3(df19)
                    #st.dataframe(newdata.tail())
                    heat(newdata)
                
                if val == '400 000 000 €' :
                    newdata = filtre_val4(df19)
                    #st.dataframe(newdata.tail())
                    heat(newdata)
            else :
                ' '

        if op == '2020':
            df20 = loading('/Users/winnie/Documents/nandi/EFREI/M1/data vizualisation/projet/2020new.csv')
            df20 = loading_state(df20)
            transformation(df20)
            post_cleaning(df20)
            
            #departement - ne marche pas  
            #dep =st.sidebar.select_slider(' choisis le département', df20['code_departement'].unique())
            #if dep == '91':
                #newdata = filtre_dep(df20)
                #st.map(newdata)
            
            #type_local
            type = st.sidebar.selectbox('choisis ton type', df20['type_local'].unique())
            if type == 'Appartement' :
                newdata = filtre_type_appart(df20)
                #st.dataframe(newdata.tail())
                st.map(newdata)

    
            if type == 'Local industriel. commercial ou assimilé' :
                newdata = filtre_type_local(df20)
                #st.dataframe(newdata.tail())
                st.map(newdata)

    
            if type == 'Maison' :
                newdata = filtre_type_maison(df20)
                #st.dataframe(newdata.tail())
                st.map(newdata)

            if type == 'Dépendance' :
                newdata = filtre_type_dependance(df20)
                #st.dataframe(newdata.tail())
                st.map(newdata)
            else:
                ''
            
             #valeurs foncieres

            b = st.sidebar.checkbox('filtre avec valeurs foncieres ?')
            if b == True :

                val = st.sidebar.select_slider('choisis un intervalle de valeurs foncières', ['300 000€', '800 000€', '10 000 000€','400 000 000€'] )
                if val == '300 000€' :
                    newdata = filtre_val1(df20)
                    #st.dataframe(newdata.tail())
                    st.sidebar.write('ton intervalle est entre 0€ et 300 000€')
                    heat(newdata)

                
                
                if val == '800 000€' :
                    newdata = filtre_val2(df20)
                    #st.dataframe(newdata.tail())
                    st.sidebar.write('ton intervalle est entre 300 000€ et 800 000€')
                    heat(newdata)


                if val == '10 000 000€' :
                    newdata = filtre_val3(df20)
                    #st.dataframe(newdata.tail())
                    st.sidebar.write('ton intervalle est entre 800 000€ et 10 000 000€')
                    heat(newdata)
                
                if val == '400 000 000€' :
                    newdata = filtre_val4(df20)
                    #st.dataframe(newdata.tail())
                    st.sidebar.write('ton intervalle est entre 10 000 000€ et 400 000 000€')
                    heat(newdata)
            else:
                ''



if __name__ == "__main__":
    main()



    



    
    

