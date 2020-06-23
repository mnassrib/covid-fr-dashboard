import pandas as pd
import numpy as np
import json
import plotly
from datetime import datetime
import os


# Covid charts
source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'
covidata = pd.read_csv(source_url, sep=';')

cdata = covidata[covidata.sexe == 0].groupby(['jour']).sum().copy()
cdata = cdata[['hosp', 'rea', 'rad', 'dc']]

cdata.index = pd.to_datetime(cdata.index)

dc_j = []
rad_j = []
for i in range(len(cdata.index)):
    if i == 0:
        dc_j.append(cdata.dc[i])
        rad_j.append(cdata.rad[i])
    else:   
        dc_j.append(cdata.dc[i]-cdata.dc[i-1])
        rad_j.append(cdata.rad[i]-cdata.rad[i-1])

cdata["dc_j"] = dc_j
cdata["rad_j"] = rad_j


#####################################"

def overall_departments_data_as_json():
    """Get data from departments as a JSON string along with quantiles

    Returns:
        JSON string of departments overall data
    """
    
    data_dir = os.path.realpath(os.path.dirname(__file__) + "/data/")

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

    return data.to_json(orient='index'), quantiles.to_json(orient='index')
#####################################"









def graph():
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
                #title="Nombre journalier de personnes décédées à l'hôpital",
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
                #title="Nombre journalier de personnes retournées à domicile",
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
            "Nombre journalier de personnes décédées à l'hôpital",
            "Nombre journalier de personnes retournées à domicile",
            ]
    
    counters = {"last_day": cdata.index[-1].strftime("%d/%m/%Y"),
            "last_dc": cdata['dc_j'][-1],
            "all_dc": cdata['dc'][-1],
            "current_hosp": cdata['hosp'][-1],
            "current_rea": cdata['rea'][-1], 
            "current_rad": cdata['rad'][-1]-cdata['rad'][-2],         
    }

    return graphJSON, ids, counters