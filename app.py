from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()



df_circuits=pd.read_csv(r'./Datasets/circuits.csv')
df_races=pd.read_csv(r'./Datasets/races.csv')
df_drivers=pd.read_json('./Datasets/drivers.json',lines=True)
df_constructors=pd.read_json('./Datasets/constructors.json',lines=True)
df_results=pd.read_json('./Datasets/results.json',lines=True)

#Pregunta1

df_1 = df_races.groupby(['year'])['year'].count().reset_index(name='count') \
                             .sort_values(['count'], ascending=False) \
                             .head(1)['year']
                            

#Pregunta2

df_2_1=df_results[df_results.position==1]

df_2=df_2_1.groupby(['driverId'])['driverId'].count().reset_index(name='count') \
                             .sort_values(['count'], ascending=False) \
                             .head(1)



df_primer=pd.merge(df_2,df_drivers,on='driverId')['name']

#Pregunta3


df_3 = df_races.groupby(['circuitId'])['circuitId'].count().reset_index(name='count') \
                             .sort_values(['count'], ascending=False) \
                             .head(1)

df_3_1=pd.merge(df_3,df_circuits,on='circuitId')['name']

#Pregunta4


nation=['American','British']
#con nacionalidad
pd_cn=df_constructors[df_constructors.nationality.isin(nation)]

#resultados nacionalidad
pd_rn=pd.merge(pd_cn,df_results,on='constructorId')

#mayores puntos
pd_mp = pd_rn.groupby(['driverId'])['points'].sum().reset_index(name='sum') \
                             .sort_values(['sum'], ascending=False) \
                             .head(1)

#driverid es 18
#driverconnombre
pd_dcn=pd.merge(pd_mp,df_drivers,on='driverId')['name']

print(pd_dcn)



def parse_csv(df):
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed

@app.get("/circuits")
def circuits():
    return parse_csv(df_circuits)

@app.get("/races")
def races():
    return parse_csv(df_races)

@app.get("/drivers")
def drivers():
    return parse_csv(df_drivers)


@app.get("/pregunta1")
def preguntas():
    return parse_csv(df_1)


@app.get("/pregunta2")
def preguntas():
    return parse_csv(df_primer)


@app.get("/pregunta3")
def preguntas():
    return parse_csv(df_3_1)


@app.get("/pregunta4")
def preguntas():
    return parse_csv(pd_dcn)



