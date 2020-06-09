import pandas as pd
import numpy as np
import json
import plotly
import os

import urllib.request
from datetime import datetime


### URL source for loading covid data
source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'

source_url2 = "https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c"


### Loading dataframe function
def load_df():
        
    covidata = pd.read_csv(source_url, sep=';')
        
    data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")
        
    department_base_data = pd.read_csv(data_dir + "/departments.csv")
        
    return {"covidata": covidata, 
            "department_base_data": department_base_data, 
            "daily_data": pd.read_csv(source_url2, sep=';')}
        

### Loading covid and france department dataframes
#covidata = load_df()["covidata"]
#department_base_data = load_df()["department_base_data"]


#####################################

def last_update():
    last_update = ""
    with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
        data = json.loads(url.read().decode())
        
        for dataset in data['@graph']:
            if 'accessURL' in dataset.keys() and dataset['accessURL'] == source_url:
                last_update = dataset['modified']
    return last_update


#####################################

def overall_departments_data_as_json():
    """Get data from departments as a JSON string along with quantiles

    Returns:
        JSON string of departments overall data
    """

    department_base_data = load_df()["department_base_data"]
    department_base_data.index = department_base_data['insee']
    department_base_data = department_base_data.sort_index()
    

    ### death case map
    covidata = load_df()["covidata"]

    dep_data = covidata[(covidata['sexe'] == 0)]

    nat_data = dep_data.copy()
    nat_data = nat_data.groupby("jour").sum()

    dep_data = dep_data \
        .drop(['jour', 'sexe'], axis=1) \
        .groupby('dep') \
        .max()

    dep_data = pd.concat([dep_data, department_base_data], axis=1)


    dep_data['dc_par_habitants'] = (dep_data['dc'] / dep_data['population']) * 100000

    data_dc = dep_data.copy()
    
    data_dc = data_dc.set_index("department-" + data_dc.index)
    
    data_dc = data_dc.loc[:, ['label', 'dc', 'dc_par_habitants', 'insee']]

    q_dc = np.mean(data_dc['dc_par_habitants'].to_numpy() \
        <= ((nat_data['dc'][-1] / department_base_data["population"].sum()) * 100000))
    q_dc_list = [0.1, 0.1+(q_dc-0.1)/2, q_dc, q_dc+(.949-q_dc)/2, .949]
 
    quantiles_dc = data_dc['dc_par_habitants'] \
        .quantile(q_dc_list) \
        .round(2)

    data_dc['dc_par_habitants'] = data_dc['dc_par_habitants'].round(2)
    
    
    ### added recently for rad case map
    dep_data['rad_par_habitants'] = (dep_data['rad'] / dep_data['population']) * 100000
  
    data_rad = dep_data.copy()
    
    data_rad = data_rad.set_index("department-" + data_rad.index)
    
    data_rad = data_rad.loc[:, ['label', 'rad', 'rad_par_habitants', 'insee']]

    q_rad = np.mean(data_rad['rad_par_habitants'].to_numpy() \
        <= ((nat_data['rad'][-1] / department_base_data["population"].sum()) * 100000))
    q_rad_list = [0.1, 0.1+(q_rad-0.1)/2, q_rad, q_rad+(.949-q_rad)/2, .949]

    quantiles_rad = data_rad['rad_par_habitants'] \
        .quantile(q_rad_list) \
        .round(2)

    data_rad['rad_par_habitants'] = data_rad['rad_par_habitants'].round(2)
    

    ### added recently for rate death case map
    dep_data['r_dc_rad'] = (dep_data['dc'] / (dep_data['dc'] + dep_data['rad']))
   
    data_r_dc_rad = dep_data.copy()

    data_r_dc_rad = data_r_dc_rad.set_index("department-" + data_r_dc_rad.index)

    data_r_dc_rad = data_r_dc_rad.loc[:, ['label', 'dc', 'rad', 'r_dc_rad', 'insee']]

    q_r_dc_rad = np.mean(dep_data['r_dc_rad'].to_numpy() <= (data_r_dc_rad['dc'].sum() / (data_r_dc_rad['dc'].sum() + data_r_dc_rad['rad'].sum())))
    q_r_dc_rad_list = [0.1, 0.1+(q_r_dc_rad-0.1)/2, q_r_dc_rad, q_r_dc_rad+(.949-q_r_dc_rad)/2, .949]

    quantiles_r_dc_rad = data_r_dc_rad['r_dc_rad'] \
        .quantile(qlist) \
        .round(2)

    data_r_dc_rad['r_dc_rad'] = data_r_dc_rad['r_dc_rad'].round(2)
    
    
    ### added recently for last day hospitalisation case map
    covidata = load_df()["covidata"]

    dep_data_j = covidata[(covidata['sexe'] == 0) & (covidata['jour'] == datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"))]
    dep_data_j = dep_data_j \
        .drop(['jour', 'sexe'], axis=1) \
        .groupby('dep') \
        .max()
    dep_data_j = pd.concat([dep_data_j, department_base_data], axis=1)


    dep_data_j['hosp_par_habitants'] = (dep_data_j['hosp'] / dep_data_j['population']) * 100000
    
    data_hosp = dep_data_j.copy()
    
    data_hosp = data_hosp.set_index("department-" + data_hosp.index)
    
    data_hosp = data_hosp.loc[:, ['label', 'hosp', 'hosp_par_habitants', 'insee']]

    q_hosp = np.mean(data_hosp['hosp_par_habitants'].to_numpy() \
        <= ((nat_data['hosp'][-1] / department_base_data["population"].sum()) * 100000))
    q_hosp_list = [0.1, 0.1+(q_hosp-0.1)/2, q_hosp, q_hosp+(.949-q_hosp)/2, .949]

    quantiles_hosp = data_hosp['hosp_par_habitants'] \
        .quantile(q_hosp_list) \
        .round(2)

    data_hosp['hosp_par_habitants'] = data_hosp['hosp_par_habitants'].round(2)
    

    ### added recently for last day reanimation case map
    dep_data_j['rea_par_habitants'] = (dep_data_j['rea'] / dep_data_j['population']) * 100000
  
    data_rea = dep_data_j.copy()
    
    data_rea = data_rea.set_index("department-" + data_rea.index)
    
    data_rea = data_rea.loc[:, ['label', 'rea', 'rea_par_habitants', 'insee']]

    q_rea = np.mean(data_rea['rea_par_habitants'].to_numpy() \
        <= ((nat_data['rea'][-1] / department_base_data["population"].sum()) * 100000))
    q_rea_list = [0.1, 0.1+(q_rea-0.1)/2, q_rea, q_rea+(.949-q_rea)/2, .949]

    quantiles_rea = data_rea['rea_par_habitants'] \
        .quantile(q_rea_list) \
        .round(2)

    data_rea['rea_par_habitants'] = data_rea['rea_par_habitants'].round(2)

    
    return data_dc.to_json(orient='index'), quantiles_dc.to_json(orient='index'), data_rad.to_json(orient='index'), quantiles_rad.to_json(orient='index'), data_r_dc_rad.to_json(orient='index'), quantiles_r_dc_rad.to_json(orient='index'), data_hosp.to_json(orient='index'), quantiles_hosp.to_json(orient='index'), data_rea.to_json(orient='index'), quantiles_rea.to_json(orient='index')
    
#####################################

def department_label(department):
    """Get a department label from its insee code

    Returns:
        Department label
    """
    department_base_data = load_df()["department_base_data"]
    department_base_data.index = department_base_data['insee']
    department_base_data = department_base_data.sort_index()
     
    if department in department_base_data.index:
        return department_base_data.at[department, 'label']
    return ""

#####################################"

def charts(department):
    covidata = load_df()["covidata"]

    if department == 'ALL':
        cdata = covidata[covidata.sexe == 0].groupby(['jour']).sum().copy()
    else: 
        cdata = covidata[(covidata.dep == department) & (covidata.sexe == 0)].groupby(['jour']).sum().copy()

    cdata = cdata[['hosp', 'rea', 'rad', 'dc']]

    cdata.index = pd.to_datetime(cdata.index)

    dc_j = []
    rad_j = []
    for i in range(len(cdata.index)):
        if i == 0:
            dc_j.append(cdata.dc[i])
            rad_j.append(cdata.rad[i])
        else:   
            dc_j.append(max(cdata.dc[i]-cdata.dc[i-1],0))
            rad_j.append(max(cdata.rad[i]-cdata.rad[i-1],0))
    
    cdata["dc_j"] = dc_j
    cdata["rad_j"] = rad_j
    
    graphs = [

        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['hosp'],
                    type='line',
                    marker=dict(
                    color='#ff7f00',
                    line=dict(color='#ff7f00', width=3)
                    )
                ),
            ],
            layout=dict(
                #title="Nombre de personnes actuellement hospitalisées",
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),
        
        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['rea'],
                    type='line',
                    marker=dict(
                    color='#ff0000',
                    line=dict(color='#ff0000', width=3)
                    )
                ),
            ],
            layout=dict(
                #title="Nombre de personnes actuellement en réanimation ou soins intensifs",
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),
        
        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['dc'],
                    type='line',
                    marker=dict(
                    color='#730800',
                    line=dict(color='#730800', width=3)
                    )
                ),
            ],
            layout=dict(
                #title="Nombre cumulé de personnes décédées à l'hôpital",
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),

        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['rad'],
                    type='line',
                    marker=dict(
                    color='#57d53b',
                    line=dict(color='#57d53b', width=3)
                    )
                ),
            ],
            layout=dict(
                #title="Nombre cumulé de personnes retournées à domicile",
                #autosize=False,
                #width=600,
                #height=600,
                margin=dict(l=30, r=30, b=30, t=30),
            )
        ),

        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['dc_j'],
                    type='bar',
                    marker=dict(
                    color='#730800',
                    line=dict(color='#730800', width=1)
                    )
                ),
            ],
            layout=dict(
                #title="Nombre de personnes décédées par jour à l'hôpital",
                margin=dict(l=30, r=10, b=30, t=30),
                barmode='overlay',
                linemode='overlay',
                legend_orientation="h",
            )
        ),

        dict(
            data=[
                dict(
                    x=cdata.index,
                    y=cdata['rad_j'],
                    type='bar',
                    marker=dict(
                    color='#57d53b',
                    line=dict(color='#57d53b', width=1),
                    opacity=0.8,
                    )
                ),
            ],
            layout=dict(
                #title="Nombre de personnes retournées par jour à domicile",
                margin=dict(l=30, r=10, b=30, t=30),
                barmode='overlay',
                linemode='overlay',
                legend_orientation="h",
            )
        ),
    ]
    
    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    #ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    ids = ["Nombre de personnes actuellement hospitalisées",
           "Nombre de personnes actuellement en réanimation ou soins intensifs",
           "Nombre cumulé de personnes décédées à l'hôpital",
           "Nombre cumulé de personnes retournées à domicile",
           "Nombre de personnes décédées par jour à l'hôpital",
           "Nombre de personnes retournées par jour à domicile",
           ]

    fdata = covidata[covidata.sexe == 0].groupby(['jour']).sum().copy()
    popfr = load_df()["department_base_data"]["population"].sum()
    
    counters = {"last_update": {"day": datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y"),  
                                "day_hour": datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M")
                                },
                                
                "last_dc": cdata['dc_j'][-1],
                "all_dc": cdata['dc'][-1],
                "last_rad": cdata['rad_j'][-1],
                "all_rad": cdata['rad'][-1],
                                
                "current_hosp": cdata['hosp'][-1],
                "current_rea": cdata['rea'][-1], 
                
                #"dep_r_dc_rad": (cdata['dc'][-1] / (cdata['dc'][-1] + cdata['rad'][-1])).round(2),
                "nat_refs": {"nat_dc": ((fdata.dc[-1] / popfr) * 100000).round(2),
                            "nat_r_dc_rad": (fdata['dc'][-1] / (fdata['dc'][-1] + fdata['rad'][-1])).round(2),
                            "nat_rad": ((fdata.rad[-1] / popfr) * 100000).round(2),
                            "nat_hosp": ((fdata.hosp[-1] / popfr) * 100000).round(2),
                            "nat_rea": ((fdata.rea[-1] / popfr) * 100000).round(2),
                            },
                }
     
    return graphJSON, ids, counters