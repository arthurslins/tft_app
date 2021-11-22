import streamlit as st
import pandas as pd
import numpy as np
import json
import requests




lista_server=["BR1","EUW1","JP1","KR","NA1"]

server = st.selectbox(
    'Escolha um server?',
    lista_server)


def criar(server):
    
    lista_chaa=requests.get(f"https://{server}.api.riotgames.com/tft/league/v1/challenger?api_key=RGAPI-68951cc5-0345-4a6e-af85-d9e541ec159c").json()
    lista_gm=requests.get(f"https://{server}.api.riotgames.com/tft/league/v1/grandmaster?api_key=RGAPI-68951cc5-0345-4a6e-af85-d9e541ec159c").json()
   
    nick=[]
    for i in range(len(lista_chaa["entries"])):
        nick.append(lista_chaa['entries'][i]["summonerName"])
    
    lp=[]
    for i in range(len(lista_chaa["entries"])):
        lp.append(lista_chaa['entries'][i]["leaguePoints"])
    
    df=pd.DataFrame(lp,nick).reset_index().rename(columns={"index":"nick",0:"lp"})
    df=df.sort_values("lp",ascending=False).reset_index(drop=True)  
    nick=[]
    
    for i in range(len(lista_gm["entries"])):
        
        nick.append(lista_gm['entries'][i]["summonerName"])
    lp=[]
    for i in range(len(lista_gm["entries"])):
        lp.append(lista_gm['entries'][i]["leaguePoints"])
    
    df1=pd.DataFrame(lp,nick).reset_index().rename(columns={"index":"nick",0:"lp"})
    df1=df1.sort_values("lp",ascending=False).reset_index(drop=True)
    dff=df.append(df1).reset_index(drop=True)
    # dff.index += 1
    
    return dff

def day(server):
    # for server in lista_server:
    df=criar(server)
    dia_ant = pd.read_csv(f"dia_ant{server}.csv")
    # dia_ant.index += 1
    parcial =  df.set_index('nick').subtract(dia_ant.set_index('nick'), fill_value=0).reset_index().sort_values("Unnamed: 0",ascending = False).reset_index(drop=True)
    parcial=parcial[["nick","lp"]]
    parcial.rename(columns={"lp":"lp_diario"},inplace=True)
    parcial["lp"]=(dia_ant["lp"]+parcial["lp_diario"])
    parcial=parcial.sort_values("lp_diario",ascending=False).reset_index(drop=True)
    parcial.sort_values(['lp_diario', 'lp'], ascending=[False, False], inplace=True)
    # parcial.index += 1
    
    parcial.to_csv(f"parcial{server}.csv")
           
    
  
    return parcial,df


if st.button("Calcular lps diários"):
    parcial,df = day(server)

    parcial.reset_index(drop=True)
    parcial.index += 1
    st.write(parcial)

def troca(df):
    dia_ant=df
    dia_ant = dia_ant.to_csv(f"dia_ant{server}.csv")
    return

if st.button("Atualizar o dia"):
    troca(df)
    







# import schedule
# import time
# hora = st.text_input("Insira um horario")
# parcial = schedule.every().day.at(hora).do(day(server))
# st.write(parcial)



# while 1:
#     schedule.run_pending()
#     time.sleep(1)