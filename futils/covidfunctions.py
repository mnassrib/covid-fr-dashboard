import pandas as pd
import json
import plotly
import os

import urllib.request
from datetime import datetime


# Loading covid dataframe
source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'
covidata = pd.read_csv(source_url, sep=';')

#####################################"

def last_update():
    last_update = ""
    with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
        data = json.loads(url.read().decode())
        
        for dataset in data['@graph']:
            if 'accessURL' in dataset.keys() and dataset['accessURL'] == source_url:
                last_update = dataset['modified']
    return last_update

#####################################"

def overall_departments_data_as_json():
    """Get data from departments as a JSON string along with quantiles

    Returns:
        JSON string of departments overall data
    """
    
    data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

    department_base_data = pd.read_csv(data_dir + "/departments.csv")
    department_base_data.index = department_base_data['insee']
    department_base_data = department_base_data.sort_index()


    dep_data = covidata[(covidata['sexe'] == 0)]
    dep_data = dep_data \
        .drop(['jour', 'sexe'], axis=1) \
        .groupby('dep') \
        .max()

    dep_data = pd.concat([dep_data, department_base_data], axis=1)

    dep_data['dc_par_habitants'] = (dep_data['dc'] / dep_data['population']) * 100000

    overall_data_departments = dep_data
    
    data = overall_data_departments.copy()
    
    data = data.set_index("department-" + data.index)
    
    data = data.loc[:, ['label', 'dc', 'dc_par_habitants', 'insee']]

    quantiles = data['dc_par_habitants'] \
        .quantile([.25, .5, .75, .949]) \
        .round(2)

    data['dc_par_habitants'] = data['dc_par_habitants'].round(2)
    
    
    #added recently for hospitalisation case map
    dep_data_j = covidata[(covidata['sexe'] == 0) & (covidata['jour'] == datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"))]
    dep_data_j = dep_data_j \
        .drop(['jour', 'sexe'], axis=1) \
        .groupby('dep') \
        .max()
    dep_data_j = pd.concat([dep_data_j, department_base_data], axis=1)

    dep_data_j['hosp_par_habitants'] = (dep_data_j['hosp'] / dep_data['population']) * 100000

    overall_data_departments_hosp = dep_data_j
    
    data_hosp = overall_data_departments_hosp.copy()
    
    data_hosp = data_hosp.set_index("department-" + data_hosp.index)
    
    data_hosp = data_hosp.loc[:, ['label', 'hosp', 'hosp_par_habitants', 'insee']]

    quantiles_hosp = data_hosp['hosp_par_habitants'] \
        .quantile([.25, .5, .75, .949]) \
        .round(2)

    data_hosp['hosp_par_habitants'] = data_hosp['hosp_par_habitants'].round(2)
    
    #################
    
    dep_data['rad_par_habitants'] = (dep_data['rad'] / dep_data['population']) * 100000

    overall_data_departments_rad = dep_data
    
    data_rad = overall_data_departments_rad.copy()
    
    data_rad = data_rad.set_index("department-" + data_rad.index)
    
    data_rad = data_rad.loc[:, ['label', 'rad', 'rad_par_habitants', 'insee']]

    quantiles_rad = data_rad['rad_par_habitants'] \
        .quantile([.25, .5, .75, .949]) \
        .round(2)

    data_rad['rad_par_habitants'] = data_rad['rad_par_habitants'].round(2)

    #return data.to_json(orient='index'), quantiles.to_json(orient='index')
    return data.to_json(orient='index'), quantiles.to_json(orient='index'), data_hosp.to_json(orient='index'), quantiles_hosp.to_json(orient='index'), data_rad.to_json(orient='index'), quantiles_rad.to_json(orient='index')
    
#####################################"

def department_label(department):
    """Get a department label from its insee code

    Returns:
        Department label
    """
    data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

    department_base_data = pd.read_csv(data_dir + "/departments.csv")
    department_base_data.index = department_base_data['insee']
    department_base_data = department_base_data.sort_index()
     
    if department in department_base_data.index:
        return department_base_data.at[department, 'label']
    return ""

#####################################"

def charts(department):
    
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
    
    counters = {"last_update": {"day": datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y"),  
                                "day_hour": datetime.strptime(last_update(), "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M")
                                },
                                
                "last_dc": cdata['dc_j'][-1],
                "all_dc": cdata['dc'][-1],
                "last_rad": cdata['rad_j'][-1],
                "all_rad": cdata['rad'][-1],
                                
                "current_hosp": cdata['hosp'][-1],
                "current_rea": cdata['rea'][-1],          
                }
     
    return graphJSON, ids, counters