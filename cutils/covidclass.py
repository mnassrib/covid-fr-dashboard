import pandas as pd
import numpy as np
import json
import plotly
import os

import urllib.request
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from scipy.stats import chi2
from numpy.linalg import inv

class CovidFr():
    """docstring for CovidFr"""

    ### URL sources for loading covid data
    synthesis_covid_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'

    daily_covid_url = "https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c"

    def __init__(self):
        # Init basic departments data
        data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

        self.department_base_data = pd.read_csv(data_dir + "/departments.csv")
        self.department_base_data.index = self.department_base_data['insee']
        self.department_base_data = self.department_base_data.sort_index()

        self.last_update = last_updated()

        self.features = ["dc", "r_dc_rad", "rad", "hosp", "rea"]
   
    def load_df(self):
        """
        Loading dataframes
        """
        self.covid = pd.read_csv(CovidFr.synthesis_covid_url, sep=';')
        self.daily_covid = pd.read_csv(CovidFr.daily_covid_url, sep=';')
        return self.covid
    
    def overall_departments_data_as_json(self, data=None):
        """
        Get data from departments as a JSON string along with quantiles
        Returns:
            JSON string of departments overall data
        """
        if data is None:
            dep_data = self.covid[(self.covid['sexe'] == 0)]
        else:
            dep_data = data[(data['sexe'] == 0)]

        nat_data = dep_data.copy()
        nat_data = nat_data.groupby("jour").sum()

        dep_data = dep_data \
            .drop(['jour', 'sexe'], axis=1) \
            .groupby('dep') \
            .max()

        dep_data = pd.concat([dep_data, self.department_base_data], axis=1)

        overall_dep_data_as_json_dict = {}

        for feature in self.features:         
            if feature == "dc" or feature == "rad":
                ### For death and or rad case maps
                dep_data[feature+'_par_habitants'] = (dep_data[feature] / dep_data['population']) * 100000

                data_feature = dep_data.copy()
                
                data_feature = data_feature.set_index("department-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), feature] / self.department_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]
             
                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})
         
            elif feature == "r_dc_rad":
                ### For rate death case map
                dep_data[feature] = (dep_data['dc'] / (dep_data['dc'] + dep_data['rad']))
               
                data_feature = dep_data.copy()

                data_feature = data_feature.set_index("department-" + data_feature.index)

                data_feature = data_feature.loc[:, ['label', 'dc', 'rad', feature, 'insee']]

                q_feature = np.mean(dep_data[feature].to_numpy() <= (data_feature['dc'].sum() / (data_feature['dc'].sum() + data_feature['rad'].sum())))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+2*(.979-q_feature)/3, .979]

                quantiles_feature = data_feature[feature] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature] = data_feature[feature].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

            elif feature == "hosp" or feature == "rea":
                ### For hosp and or rea case map
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
                    <= ((nat_data.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), feature] / self.department_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

        return overall_dep_data_as_json_dict

    @staticmethod
    def dailycases(data=None):
        cdata = data[data.sexe == 0].groupby(['jour']).sum().copy()
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
                dc_j.append(max(cdata.dc[0:i+1]) - max(cdata.dc[0:i]))
                rad_j.append(max(cdata.rad[0:i+1]) - max(cdata.rad[0:i]))

        cdata["dc_rectif"] = dc_rectif
        cdata["rad_rectif"] = rad_rectif
        cdata["dc_j"] = dc_j
        cdata["rad_j"] = rad_j
        cdata = cdata[['hosp', 'rea', 'rad_j', 'dc_j']]
        cdata.rename(columns={'rad_j':'rad', 'dc_j':'dc'})
        return cdata

    def charts(self, data=None, department=None): 
        if department is None:  
            if data is None:
                cdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
            else: 
                cdata = data[data.sexe == 0].groupby(['jour']).sum().copy()
        else:
            if data is None:
                cdata = self.covid[(self.covid.dep == department) & (self.covid.sexe == 0)].groupby(['jour']).sum().copy()
            else: 
                cdata = data[(data.dep == department) & (data.sexe == 0)].groupby(['jour']).sum().copy()

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
                dc_j.append(max(cdata.dc[0:i+1]) - max(cdata.dc[0:i]))
                rad_j.append(max(cdata.rad[0:i+1]) - max(cdata.rad[0:i]))

        cdata["dc_rectif"] = dc_rectif
        cdata["rad_rectif"] = rad_rectif
        cdata["dc_j"] = dc_j
        cdata["rad_j"] = rad_j

        graphs = [
            dict(
                id= "Nombre de personnes actuellement hospitalisées",
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
                id="Nombre de personnes actuellement en réanimation",
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
                id="Nombre cumulé de personnes décédées à l'hôpital",
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
                id="Nombre cumulé de personnes retournées à domicile",
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
                id="Nombre de personnes décédées par jour à l'hôpital",
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
                id="Nombre de personnes retournées par jour à domicile",
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

        fdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
        popfr = self.department_base_data["population"].sum()
        
        self.counters = {
                        "last_update_fr": {
                                           "day": datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y"),
                                           "day_hour": datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M")
                                           },
                                    
                        "last_dc": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'dc_j'],
                        "all_dc": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'dc_rectif'],
                        "last_rad": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rad_j'],
                        "all_rad": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rad_rectif'],          
                        "current_hosp": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'hosp'],
                        "current_rea": cdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rea'], 
                    
                        "nat_refs": {
                                    "nat_dc": ((fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'dc'] / popfr) * 100000).round(2),
                                    "nat_r_dc_rad": (fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'dc'] / (fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'dc'] + fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rad'])).round(2),
                                    "nat_rad": ((fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rad'] / popfr) * 100000).round(2),
                                    "nat_hosp": ((fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'hosp'] / popfr) * 100000).round(2),
                                    "nat_rea": ((fdata.at[datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d"), 'rea'] / popfr) * 100000).round(2),
                                    },
                        }
        return {"graphJSON": self.graphJSON, 
                "counters": self.counters,
                }

    def department_label(self, department):
        """Get a department label from its insee code
        Returns:
            Department label
        """
        if department in self.department_base_data.index:
            return self.department_base_data.at[department, 'label']
        return ""

    def acp(self, data, pcdim, q=0.975, normalize=False, start_d_learn='2020-05-14', end_d_learn='2020-06-14', alpha=1-0.4):
        
        dataindex = data.index
        learn_data = data[(data.index>=start_d_learn) & (data.index<=end_d_learn)].copy()
        
        if normalize == True:
            std = StandardScaler().fit(learn_data)
            learn_data = std.transform(learn_data)
            data = std.transform(data)
        
        u, s, vh = np.linalg.svd(np.dot(np.transpose(learn_data), learn_data)/(learn_data.shape[0]), full_matrices=True)
        
        u_tilde = u[:, pcdim:]
        c_tilde = np.dot(u_tilde, np.transpose(u_tilde))
        spe = np.diag(np.dot(np.dot(data, c_tilde), np.transpose(data)))
        
        numgspe = np.trace(np.square(np.diag(s[pcdim:])))
        dengspe = np.trace(np.diag(s[pcdim:]))
        gspe = numgspe/dengspe

        numhspe = np.square(dengspe)
        denhspe = numgspe
        hspe = numhspe/denhspe

        u_hat = u[:, :pcdim]
        c_hat_Hotelling =np.dot(np.dot(u_hat, inv(np.diag(s[:pcdim]))), np.transpose(u_hat))     
        t2 = np.diag(np.dot(np.dot(data, c_hat_Hotelling), np.transpose(data)))

        graphs = [
            dict(
                id = 'SPE',
                data=[
                    dict(
                        x = dataindex,
                        y = spe,
                        type='line',
                        name='score',
                        marker=dict(
                        color='#02056D',
                        line=dict(color='#02056D', width=3)
                        ),
                        hovertemplate =
                            #'<b>Score</b>: %{y:.2f}<br>'+
                            '<b>%{text}</b><extra></extra>',
                            text = ['uncontrolled' if spe[i]>gspe*chi2.ppf(q, df=hspe) else 'controlled' for i in range(len(dataindex))],
                    ),

                    dict(
                        x = dataindex,
                        y = ewma_filter(data=spe, alpha=alpha),
                        type='line',
                        name="score filtré",
                        marker=dict(
                        color='#026D2F',
                        line=dict(color='#026D2F', width=3)
                        ),
                        hovertemplate =
                            #'<b>Score</b>: %{y:.2f}<br>'+
                            '<b>%{text}</b><extra></extra>',
                            text = ['uncontrolled' if ewma_filter(data=spe, alpha=alpha)[i]>gspe*chi2.ppf(q, df=hspe) else 'controlled' for i in range(len(dataindex))],
                    ),

                    dict(
                        x = dataindex,
                        y = np.repeat(gspe*chi2.ppf(q, df=hspe), spe.shape[0]),
                        type='line',
                        name='seuil',
                        marker=dict(
                        color='#ff0000',
                        line=dict(color='#ff0000', width=3)
                        ),
                        hovertemplate =
                            #'<b>Score</b>: %{y:.2f}<br>'+
                            '<b>%{text}</b><extra></extra>',
                            text = ['seuil' for i in range(len(dataindex))],
                        showlegend = False,
                    ),
                ],
                layout=dict(
                    #title="Indice SPE",
                    legend=dict(orientation="h"),
                    linemode='overlay',
                    margin=dict(l=30, r=30, b=30, t=30),      
                )
            ),
        ]

        # Convert the figures to JSON
        # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
        # objects to their JSON equivalents
        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return {'graphJSON': graphJSON,
                'explained variance': ((np.trace(np.diag(s[:pcdim]))/np.trace(np.diag(s)))*100).round(2),
                'SPE': {'spe': spe,
                        'filtered_spe': ewma_filter(data=spe, alpha=alpha),
                        'threshold': gspe*chi2.ppf(q, df=hspe),
                       },
                'Hotelling': {'t2': t2, 
                              'filtered_t2': ewma_filter(data=t2, alpha=alpha), 
                              'threshold': chi2.ppf(q, df=pcdim)
                             },
               }
 
###############################
   
def last_updated():
    last_update = ""
    with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
        data = json.loads(url.read().decode())  
        for dataset in data['@graph']:
            if 'accessURL' in dataset.keys() and dataset['accessURL'] == CovidFr.synthesis_covid_url:
                last_update = dataset['modified']
    return last_update


def ewma_filter(data, alpha, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a vector.
    Will fail for large inputs.
    :param data: Input data
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param offset: optional
        The offset for the moving average, scalar. Defaults to data[0].
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the input. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if data.ndim > 1:
        # flatten input
        data = data.reshape(-1, order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        # empty input, return empty array
        return out

    if offset is None:
        offset = data[0]

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # scaling_factors -> 0 as len(data) gets large
    # this leads to divide-by-zeros below
    scaling_factors = np.power(1. - alpha, np.arange(data.size + 1, dtype=dtype),
                               dtype=dtype)
    # create cumulative sum array
    np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
                dtype=dtype, out=out)
    np.cumsum(out, dtype=dtype, out=out)

    # cumsums / scaling
    out /= scaling_factors[-2::-1]

    if offset != 0:
        offset = np.array(offset, copy=False).astype(dtype, copy=False)
        # add offsets
        out += offset * scaling_factors[1:]

    return out



