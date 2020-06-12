import pandas as pd
import numpy as np
import json
import plotly
import os

import urllib.request
from datetime import datetime

class CovidFr():
    """docstring for CovidFr"""

    ### URL source for loading covid data
    source_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'

    source_url_daily_covid = "https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c"

    def __init__(self):
        self.covid = pd.DataFrame()
        self.daily_covid = pd.DataFrame()

        # Init basic departments data
        data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

        self.department_base_data = pd.read_csv(data_dir + "/departments.csv")
        self.department_base_data.index = self.department_base_data['insee']
        self.department_base_data = self.department_base_data.sort_index()

        self.last_update = last_updated()

        self.features = ["dc", "r_dc_rad", "rad", "hosp", "rea"]
   

    ### Loading dataframe function
    def load_df(self):
        self.covid = pd.read_csv(CovidFr.source_url, sep=';')
        self.daily_covid = pd.read_csv(CovidFr.source_url_daily_covid, sep=';')
    
 
    def overall_departments_data_as_json(self):

        """Get data from departments as a JSON string along with quantiles

        Returns:
            JSON string of departments overall data
        """
        dep_data = self.covid[(self.covid['sexe'] == 0)]

        nat_data = dep_data.copy()
        nat_data = nat_data.groupby("jour").sum()

        dep_data = dep_data \
            .drop(['jour', 'sexe'], axis=1) \
            .groupby('dep') \
            .max()

        dep_data = pd.concat([dep_data, self.department_base_data], axis=1)

        for feature in self.features:
             
            if feature == "dc" or feature == "rad":
                ### added recently for death and or hosp case maps
                dep_data[feature+'_par_habitants'] = (dep_data[feature] / dep_data['population']) * 100000

                data_feature = dep_data.copy()
                
                data_feature = data_feature.set_index("department-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data[feature][-1] / self.department_base_data["population"].sum()) * 100000))
                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]
             
                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

            elif feature == "r_dc_rad":
                ### added recently for rate death case map
                dep_data[feature] = (dep_data['dc'] / (dep_data['dc'] + dep_data['rad']))
               
                data_feature = dep_data.copy()

                data_feature = data_feature.set_index("department-" + data_feature.index)

                data_feature = data_feature.loc[:, ['label', 'dc', 'rad', feature, 'insee']]

                q_feature = np.mean(dep_data[feature].to_numpy() <= (data_feature['dc'].sum() / (data_feature['dc'].sum() + data_feature['rad'].sum())))
                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

                quantiles_feature = data_feature[feature] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature] = data_feature[feature].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

            elif feature == "hosp" or feature == "rea":

                dep_data_j = self.covid[(self.covid['sexe'] == 0) & (self.covid['jour'] == datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"))]
                dep_data_j = dep_data_j \
                    .drop(['jour', 'sexe'], axis=1) \
                    .groupby('dep') \
                    .max()
                dep_data_j = pd.concat([dep_data_j, self.department_base_data], axis=1)


                dep_data_j[feature+'_par_habitants'] = (dep_data_j[feature] / dep_data_j['population']) * 100000
                
                data_feature = dep_data_j.copy()
                
                data_feature = data_feature.set_index("department-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data[feature][-1] / self.department_base_data["population"].sum()) * 100000))
                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

    def charts(self, department):
        
        if department == 'ALL':
            cdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
        else: 
            cdata = self.covid[(self.covid.dep == department) & (self.covid.sexe == 0)].groupby(['jour']).sum().copy()

        cdata = cdata[['hosp', 'rea', 'rad', 'dc']]

        cdata.index = pd.to_datetime(cdata.index)

        dc_j = []
        rad_j = []
        dc_rectif = []
        rad_rectif = []
        for i in range(len(cdata.index)):
            dc_rectif.append(max(cdata.dc[0:i+1]))
            rad_rectif.append(max(cdata.rad[0:i+1]))

            if i == 0:
                dc_j.append(cdata.dc[i])
                rad_j.append(cdata.rad[i])
                
            else:   
                #dc_j.append(max(cdata.dc[i]-cdata.dc[i-1], 0))
                #rad_j.append(max(cdata.rad[i]-cdata.rad[i-1], 0))
                dc_j.append(max(cdata.dc[0:i+1]) - max(cdata.dc[0:i]))
                rad_j.append(max(cdata.rad[0:i+1]) - max(cdata.rad[0:i]))
        
        
        cdata["dc_rectif"] = dc_rectif
        cdata["rad_rectif"] = rad_rectif
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
                        y=cdata['dc_rectif'],#cdata['dc'],
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
                        y=cdata['rad_rectif'],#cdata['rad'],
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
        self.graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        # Add "ids" to each of the graphs to pass up to the client
        # for templating
        #ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

        self.ids = ["Nombre de personnes actuellement hospitalisées",
                    "Nombre de personnes actuellement en réanimation",
                    "Nombre cumulé de personnes décédées à l'hôpital",
                    "Nombre cumulé de personnes retournées à domicile",
                    "Nombre de personnes décédées par jour à l'hôpital",
                    "Nombre de personnes retournées par jour à domicile",
                    ]

        fdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
        popfr = self.department_base_data["population"].sum()
        
        self.counters = {"last_update": {
                                        "day": datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y"),
                                        "day_hour": datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M")
                                        },
                                    
                        "last_dc": cdata['dc_j'][-1],
                        "all_dc": cdata['dc_rectif'][-1],#cdata['dc'][-1],
                        "last_rad": cdata['rad_j'][-1],
                        "all_rad": cdata['rad_rectif'][-1],#cdata['rad'][-1],
                                    
                        "current_hosp": cdata['hosp'][-1],
                        "current_rea": cdata['rea'][-1], 
                    
                        "nat_refs": {"nat_dc": ((fdata.dc[-1] / popfr) * 100000).round(2),
                                     "nat_r_dc_rad": (fdata['dc'][-1] / (fdata['dc'][-1] + fdata['rad'][-1])).round(2),
                                     "nat_rad": ((fdata.rad[-1] / popfr) * 100000).round(2),
                                     "nat_hosp": ((fdata.hosp[-1] / popfr) * 100000).round(2),
                                     "nat_rea": ((fdata.rea[-1] / popfr) * 100000).round(2),
                                     },
                        }

    def department_label(self, department):
        """Get a department label from its insee code

        Returns:
            Department label
        """
        if department in self.department_base_data.index:
            return self.department_base_data.at[department, 'label']
        return ""


     
###############################
   
def last_updated():
    last_update = ""
    with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
        data = json.loads(url.read().decode())  
        for dataset in data['@graph']:
            if 'accessURL' in dataset.keys() and dataset['accessURL'] == CovidFr.source_url:
                last_update = dataset['modified']
    return last_update
        
        