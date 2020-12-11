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
import plotly.graph_objs as go
from functools import reduce

class CovidFr():
    """
    docstring for CovidFr
    """
    ### URL source for loading covid data
    synthesis_covid_url = 'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7'
    synthesis_dprate_url = 'https://www.data.gouv.fr/fr/datasets/r/19a91d64-3cd3-42fc-9943-d635491a4d76'
    synthesis_rprate_url = 'https://www.data.gouv.fr/fr/datasets/r/ad09241e-52fa-4be8-8298-e5760b43cae2'
    synthesis_nprate_url = 'https://www.data.gouv.fr/fr/datasets/r/57d44bd6-c9fd-424f-9a72-7834454f9e3c'

    def __init__(self):
        # Init basic departments data
        data_dir = os.path.realpath(os.path.dirname(__file__) + "/../data/")

        #self.department_base_data = pd.read_csv(data_dir + "/departments.csv")
        department_base_data = pd.read_csv(data_dir + "/departments_rectif_pop.csv")
        department_base_data.index = department_base_data['insee']
        self.department_base_data = department_base_data.sort_index()

        #self.region_base_data = pd.read_csv(data_dir + "/regions.csv", dtype={'insee': "string"})
        region_base_data = pd.read_csv(data_dir + "/regions_rectif_pop.csv", dtype={'insee': "string"})
        region_base_data.index = region_base_data['insee']
        self.region_base_data = region_base_data.sort_index()

        self.last_update = CovidFr.updatechecking(json_url="https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json", data_request_url=CovidFr.synthesis_covid_url)
        #self.last_update = ""

        self.features = ["rad", "dc", "hosp", "rea"]

        self.positive_last_update = CovidFr.updatechecking(json_url="https://www.data.gouv.fr/datasets/5ed1175ca00bbe1e4941a46a/rdf.json", data_request_url=CovidFr.synthesis_dprate_url)
        #self.positive_last_update = ""
        
        ###############################
        # required process settings
        ###############################
        self.number_all_dep = list(range(1, self.department_base_data.shape[0]+1))
        self.global_pc = list(range(1, len(self.features)+1))
        self.normalize_states = [True, False]
        self.alpha_smooth = list(np.arange(0.1, 1, 0.05).round(2))
        self.pc_reg = list(range(1, self.region_base_data.shape[0]+1))
        ##############################
        # independent default settings
        ##############################
        ## default selected number of top departments
        self.default_top_dep = 10
        #-- default settings for pca-based global monitoring
        self.default_pcdim = 2
        self.default_normalize = self.normalize_states[0]
        self.default_start_d_learn_fr = '15/05/2020'
        self.default_end_d_learn_fr = '25/08/2020'
        self.default_alpha = 0.6
        #-- default settings for pca-based region hospitalization monitoring
        self.default_pcdim_reg = 3
        self.default_normalize_reg = self.normalize_states[0]
        self.default_start_d_learn_fr_reg = '15/05/2020'
        self.default_end_d_learn_fr_reg = '25/08/2020'
        self.default_alpha_reg = 0.7
        #-- other default settings
        self.default_department = None
        self.default_region = None

    def load_df(self):
        """
        Loading dataframes
        """
        covid = pd.read_csv(CovidFr.synthesis_covid_url, sep=';').dropna()
        covid['jour'] = pd.to_datetime(covid['jour'])
        covid = covid.drop_duplicates()

        self.covid = CovidFr.regionadd(data=covid)

        self.first_day_fr = self.covid.jour.min().strftime("%d/%m/%Y")

        self.last_day_fr = self.covid.jour.max().strftime("%d/%m/%Y")

        self.last_day = self.covid.jour.max().strftime("%Y-%m-%d")

        return self.covid 
        
    def load_positive_df(self):
        """
        Loading dataframes
        """
        #national df
        nprate = pd.read_csv(CovidFr.synthesis_nprate_url, sep=';', usecols=['jour', 'P', 'cl_age90']).dropna()
        nprate['jour'] = pd.to_datetime(nprate['jour'])
        self.nprate = nprate.drop_duplicates()

        #regional df
        rprate = pd.read_csv(CovidFr.synthesis_rprate_url, sep=';', dtype={'reg': "string"}, usecols=['reg', 'jour', 'P', 'cl_age90']).dropna()
        rprate['jour'] = pd.to_datetime(rprate['jour'])
        rprate = rprate.drop_duplicates()
        self.rprate = rprate.loc[rprate['reg'].isin(list(self.region_base_data.index))]

        #departmental df
        dprate = pd.read_csv(CovidFr.synthesis_dprate_url, sep=';', dtype={'dep': "string"}, usecols=['dep', 'jour', 'P', 'cl_age90']).dropna()
        dprate['jour'] = pd.to_datetime(dprate['jour'])
        dprate = dprate.drop_duplicates()
        self.dprate = dprate.loc[dprate['dep'].isin(list(self.department_base_data.index))]

        #other parameters
        self.positive_last_day = self.dprate.jour.max().strftime("%Y-%m-%d")
        self.positive_last_day_fr =  self.dprate.jour.max().strftime("%d/%m/%Y")
        
        ###############################
        # required process settings
        ###############################
        self.map_choice = ["Nombre de guérisons", "Nombre de décès", "Taux décès / (décès + guérisons)", "Nombre d'hospitalisations le "+self.last_day_fr, "Nombre de réanimations le "+self.last_day_fr, "Nombre de cas positifs le "+self.positive_last_day_fr]
        self.criterion_choice = ["Cas positifs au "+self.positive_last_day_fr, "Hospitalisations au "+self.last_day_fr, "Réanimations au "+self.last_day_fr]
        self.default_map_select = self.map_choice[5]
        self.default_criterion_select = self.criterion_choice[0]

        return self.nprate, self.rprate, self.dprate

    def covid_need_update(self):
        """Check the last update of the datasets on data.gouv.fr and tells whether we need to refresh the data or not
        Returns:
            True if the data need to be updated, False instead
        """
        with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5e7e104ace2080d9162b61d8/rdf.json") as url:
            data = json.loads(url.read().decode())
            for dataset in data['@graph']:
                if 'accessURL' in dataset.keys() and dataset['accessURL'] == CovidFr.synthesis_covid_url:
                    if self.last_update == "" or self.last_update < dataset['modified']:
                        return True
        return False

    def positive_need_update(self):
        """Check the last update of the datasets on data.gouv.fr and tells whether we need to refresh the data or not
        Returns:
            True if the data need to be updated, False instead
        """
        with urllib.request.urlopen("https://www.data.gouv.fr/datasets/5ed1175ca00bbe1e4941a46a/rdf.json") as url:
            data = json.loads(url.read().decode())
            for dataset in data['@graph']:
                if 'accessURL' in dataset.keys() and dataset['accessURL'] == CovidFr.synthesis_dprate_url:
                    if self.positive_last_update == "" or self.positive_last_update < dataset['modified']:
                        return True
        return False

    def map_covid_reg(self, data=None):
        """
        Get data from regions as a JSON string along with quantiles
        Returns:
            JSON string of regions overall data
        """
        if data is None:
            reg_data = self.covid[(self.covid['sexe'] == 0)]
        else:
            reg_data = data[(data['sexe'] == 0)]

        nat_data = reg_data.copy()
        nat_data = nat_data.groupby("jour").sum()

        reg_data = reg_data \
            .drop(['jour', 'sexe'], axis=1) \
            .groupby(['reg','dep']) \
            .max() \
            .groupby('reg') \
            .sum()

        reg_data = pd.concat([reg_data, self.region_base_data], axis=1)

        overall_reg_data_as_json_dict = {}

        features = self.features.copy()
        features.append("r_dc_rad")
        for feature in features:         
            if feature == "dc" or feature == "rad":
                ### For death and or rad case maps
                reg_data[feature+'_par_habitants'] = (reg_data[feature] / reg_data['population']) * 100000

                data_feature = reg_data.copy()
                
                data_feature = data_feature.set_index("region-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data.at[self.last_day, feature] / self.region_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]
                             
                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                #setattr(self, 'overall_regions_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_reg_data_as_json_dict.update({'overall_regions_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})
         
            elif feature == "r_dc_rad":
                ### For rate death case map
                reg_data[feature] = (reg_data['dc'] / (reg_data['dc'] + reg_data['rad']))
               
                data_feature = reg_data.copy()

                data_feature = data_feature.set_index("region-" + data_feature.index)

                data_feature = data_feature.loc[:, ['label', 'dc', 'rad', feature, 'insee']]

                q_feature = np.mean(reg_data[feature].to_numpy() <= (data_feature['dc'].sum() / (data_feature['dc'].sum() + data_feature['rad'].sum())))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+2*(.979-q_feature)/3, .979]

                quantiles_feature = data_feature[feature] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature] = data_feature[feature].round(2)

                #setattr(self, 'overall_regions_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_reg_data_as_json_dict.update({'overall_regions_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

            elif feature == "hosp" or feature == "rea":
                ### For hosp and or rea case map
                reg_data_j = self.covid[(self.covid['sexe'] == 0) & (self.covid['jour'] == self.last_day)]
                
                reg_data_j = reg_data_j \
                    .drop(['dep', 'jour', 'sexe'], axis=1) \
                    .groupby('reg') \
                    .sum()

                reg_data_j = pd.concat([reg_data_j, self.region_base_data], axis=1)

                reg_data_j[feature+'_par_habitants'] = (reg_data_j[feature] / reg_data_j['population']) * 100000
                
                data_feature = reg_data_j.copy()
                
                data_feature = data_feature.set_index("region-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data.at[self.last_day, feature] / self.region_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                #setattr(self, 'overall_regions_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_reg_data_as_json_dict.update({'overall_regions_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

        return overall_reg_data_as_json_dict

    def map_covid_dep(self, data=None):
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
            .drop(['reg', 'jour', 'sexe'], axis=1) \
            .groupby('dep') \
            .max()

        dep_data = pd.concat([dep_data, self.department_base_data], axis=1)

        overall_dep_data_as_json_dict = {}

        features = self.features.copy()
        features.append("r_dc_rad")
        for feature in features:         
            if feature == "dc" or feature == "rad":
                ### For death and or rad case maps
                dep_data[feature+'_par_habitants'] = (dep_data[feature] / dep_data['population']) * 100000

                data_feature = dep_data.copy()
                
                data_feature = data_feature.set_index("department-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data.at[self.last_day, feature] / self.department_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]
             
                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                #setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

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

                #setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

            elif feature == "hosp" or feature == "rea":
                ### For hosp and or rea case map
                dep_data_j = self.covid[(self.covid['sexe'] == 0) & (self.covid['jour'] == self.last_day)]
                dep_data_j = dep_data_j \
                    .drop(['reg', 'jour', 'sexe'], axis=1) \
                    .groupby('dep') \
                    .max()
                dep_data_j = pd.concat([dep_data_j, self.department_base_data], axis=1)

                dep_data_j[feature+'_par_habitants'] = (dep_data_j[feature] / dep_data_j['population']) * 100000
                
                data_feature = dep_data_j.copy()
                
                data_feature = data_feature.set_index("department-" + data_feature.index)
                
                data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

                q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() \
                    <= ((nat_data.at[self.last_day, feature] / self.department_base_data["population"].sum()) * 100000))

                q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

                quantiles_feature = data_feature[feature+'_par_habitants'] \
                    .quantile(q_feature_list) \
                    .round(2)

                data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

                #setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

                overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

        return overall_dep_data_as_json_dict

    def charts_impacted_dep(self, top_number=None): 
        if top_number is None:
            top_number = self.default_top_dep
        ratedf = self.covid[(self.covid.sexe == 0) & (self.covid.jour == self.last_day)].groupby(['dep']).sum().copy()
        ratedf = ratedf.drop(['sexe',], axis=1)
        ratedf = (ratedf[['hosp', 'rea', 'rad', 'dc']].div(self.department_base_data['population'], axis=0) * 100000).round(2)
        ratedf = pd.concat([ratedf, self.department_base_data], axis=1)
        ratedf.sort_values(by=['hosp'], inplace=True, ascending=False)

        dep_data_norm = {department: ((self.covid[(self.covid.dep == department) & (self.covid.sexe == 0)].groupby(['jour']).sum() / self.department_base_data.at[department, 'population']) * 100000).round(2) for department in self.department_base_data.insee}
        dep_data_norm_col = CovidFr.normrate(ddn=dep_data_norm, cdu=list(self.covid.dep.unique()), featurelist = ['hosp', 'rea', 'rad', 'dc'])

        tddv_hosp = CovidFr.topdepdataviz(data=dep_data_norm_col["hosp"], top=True, top_number=top_number, threshold=65)
        tddv_rea = CovidFr.topdepdataviz(data=dep_data_norm_col["rea"], top=True, top_number=top_number, threshold=65)

        # start of integration of the positive cases
        pratedf = self.dprate[(self.dprate.cl_age90 == 0) & (self.dprate.jour == self.positive_last_day)].groupby(['dep']).sum().copy()
        pratedf = pratedf.drop(['cl_age90'], axis=1)
        pratedf = (pratedf[['P']].div(self.department_base_data['population'], axis=0) * 100000).round(2)
        pratedf = pd.concat([pratedf, self.department_base_data], axis=1)

        dep_positive_norm = {department: ((self.dprate[(self.dprate.dep == department) & (self.dprate.cl_age90 == 0)].groupby(['jour']).sum() / self.department_base_data.at[department, 'population']) * 100000).round(2) for department in self.department_base_data.insee}
        dep_positive_norm_col = CovidFr.normrate(ddn=dep_positive_norm, cdu=list(self.dprate.dep.unique()), featurelist = ['P'])

        tddv_positive = CovidFr.topdepdataviz(data=dep_positive_norm_col["P"], top=True, top_number=top_number, threshold=65)
        # end integration of the positive cases

        graphs = [
            dict(
                id = "Dernier nombre de patients pour 100 000 habitants par département",
                data = [
                    CovidFr.dataviz(x=ratedf.label, y=ratedf['hosp'], curve_type='bar', color='#ff7f00', width=1.5, name="Nbre d'hospitalisations", opacity=0.9, text = [i for i in ratedf.index], hovertemplate = '<b>%{y:.2f}</b> hospitalisations<br>dépt. <b>%{x} (FR-%{text})</b><extra></extra>'), 

                    CovidFr.dataviz(x=ratedf.label, y=ratedf['dc'], curve_type='bar', color='#730800', width=1.5, name="Nbre de décès", opacity=0.9, text = [i for i in ratedf.index], hovertemplate = '<b>%{y:.2f}</b> décès<br>dépt. <b>%{x} (FR-%{text})</b><extra></extra>'), 

                    CovidFr.dataviz(x=ratedf.label, y=ratedf['rea'], curve_type='bar', color='#ff0000', width=1.5, name="Nbre de réanimations", opacity=0.9, text = [i for i in ratedf.index], hovertemplate = '<b>%{y:.2f}</b> réanimations<br>dépt. <b>%{x} (FR-%{text})</b><extra></extra>'),

                    CovidFr.dataviz(x=pratedf.label, y=pratedf['P'], curve_type='bar', color='#f84ed3', width=1.5, name="Nbre de cas positifs", opacity=0.9, text = [i for i in pratedf.index], hovertemplate = '<b>%{y:.2f}</b> cas positifs<br>dépt. <b>%{x} (FR-%{text})</b><extra></extra>'),
                ],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=10, b=30, t=30), barmode='group', linemode='overlay', legend_orientation="h"),
            ),

            dict(
                id = "Top des départements selon le nombre d'hospitalisations pour 100 000 habitants",
                data = [CovidFr.dataviz(x=tddv_hosp.index, y=tddv_hosp[dep], curve_type='Scatter', name=self.department_base_data.at[dep, "label"], text=[self.department_base_data.at[dep, "label"]+" (FR-"+dep+")"]*len(tddv_hosp.index), hovertemplate='<b>%{y:.2f}</b> '+'hospitalisations'+'<br>'+'dépt. %{text}<extra></extra>') for dep in list(tddv_hosp.columns.unique())],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=10, b=30, t=30), linemode='overlay', legend_orientation="h"),
            ),

            dict(
                id = "Top des départements selon le nombre de réanimations pour 100 000 habitants",
                data = [CovidFr.dataviz(x=tddv_rea.index, y=tddv_rea[dep], curve_type='Scatter', name=self.department_base_data.at[dep, "label"], text=[self.department_base_data.at[dep, "label"]+" (FR-"+dep+")"]*len(tddv_rea.index), hovertemplate='<b>%{y:.2f}</b> '+'réanimations'+'<br>'+'dépt. %{text}<extra></extra>') for dep in list(tddv_rea.columns.unique())],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=10, b=30, t=30), linemode='overlay', legend_orientation="h"),
            ),

            dict(
                id = "Top des départements selon le nombre de cas positifs pour 100 000 habitants",
                data = [CovidFr.dataviz(x=tddv_positive.index, y=tddv_positive[dep], curve_type='Scatter', name=self.department_base_data.at[dep, "label"], text=[self.department_base_data.at[dep, "label"]+" (FR-"+dep+")"]*len(tddv_positive.index), hovertemplate='<b>%{y:.2f}</b> '+'cas positifs'+'<br>'+'dépt. %{text}<extra></extra>') for dep in list(tddv_positive.columns.unique())],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=10, b=30, t=30), linemode='overlay', legend_orientation="h"),
            ),
        ]
        #############################################################
        gJ = {}
        for g in range(len(graphs)):
            gJ.update({'graphJSON{}'.format(g): json.dumps([graphs[g]], cls=plotly.utils.PlotlyJSONEncoder)})
        #############################################################
        return gJ

    def charts_and_parameters_covid_data(self, data=None, department=None, region=None): 
        if region is None and department is None:
            if data is None:
                cdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.department_base_data["population"].sum()
            else: 
                cdata = data[data.sexe == 0].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.department_base_data["population"].sum()
        elif region is None and not department is None:
            if data is None:
                cdata = self.covid[(self.covid.dep == department) & (self.covid.sexe == 0)].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.department_base_data.at[department, 'population']
            else: 
                cdata = data[(data.dep == department) & (data.sexe == 0)].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.department_base_data.at[department, 'population']
        elif not region is None and department is None:
            if data is None:
                # regdep = []
                # for d in self.covid[self.covid.reg==region].dep.unique():
                #     regdep.append(CovidFr.dailycases(data=self.covid[(self.covid.dep == d) & (self.covid.sexe == 0)].groupby(['jour']).sum(), pca=False))
                # cdata = reduce(lambda x, y: x.add(y, fill_value=0), regdep)
                cdata = self.covid[(self.covid.reg == region) & (self.covid.sexe == 0)].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.region_base_data.at[region, 'population']
            else: 
                # regdep = []
                # for d in data[data.reg==region].dep.unique():
                #     regdep.append(CovidFr.dailycases(data=data[(data.dep == d) & (data.sexe == 0)].groupby(['jour']).sum(), pca=False))
                # cdata = reduce(lambda x, y: x.add(y, fill_value=0), regdep)
                cdata = data[(data.reg == region) & (data.sexe == 0)].groupby(['jour']).sum().copy()
                cdata = CovidFr.dailycases(data=cdata, pca=False)
                cpop = self.region_base_data.at[region, 'population']

        graphs = [
            dict(
                id = "Nombre de personnes actuellement hospitalisées",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['hosp'], curve_type='line', color='#ff7f00', width=3)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30)),
            ),   

            dict(
                id = "Nombre de personnes actuellement en réanimation",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['rea'], curve_type='line', color='#ff0000', width=3)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30)),
            ),   

            dict(
                id = "Nombre cumulé de personnes décédées à l'hôpital",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['dc_rectif'], curve_type='line', color='#730800', width=3)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30)),
            ),

            dict(
                id = "Nombre cumulé de personnes retournées à domicile",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['rad_rectif'], curve_type='line', color='#57d53b', width=3)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30)),
            ),

            dict(
                id = "Nombre quotidien de personnes décédées à l'hôpital",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['dc_j'], curve_type='bar', color='#730800', width=1)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=15, b=30, t=30), barmode='overlay',linemode='overlay', legend_orientation="h"),
            ),

            dict(
                id = "Nombre quotidien de personnes retournées à domicile",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['rad_j'], curve_type='bar', color='#57d53b', width=1, opacity=0.8)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=15, b=30, t=30), barmode='overlay',linemode='overlay', legend_orientation="h"),
            ),
        ]
        #############################################################
        gJ = {}
        for g in range(len(graphs)):
            gJ.update({'graphJSON{}'.format(g): json.dumps([graphs[g]], cls=plotly.utils.PlotlyJSONEncoder)})
        #############################################################

        fdata = self.covid[self.covid.sexe == 0].groupby(['jour']).sum().copy()
        popfr = self.department_base_data["population"].sum()

        before_last_day = cdata.index[-2].strftime("%Y-%m-%d")

        counters = {
                    "last_update_fr": datetime.strptime(self.last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M"),
                                
                    "last_dc": cdata.at[self.last_day, 'dc_j'],
                    "diff_dc": cdata.at[self.last_day, 'dc_j'] - cdata.at[before_last_day, 'dc_j'],
                    "all_dc": cdata.at[self.last_day, 'dc_rectif'],
                    "last_rad": cdata.at[self.last_day, 'rad_j'],
                    "diff_rad": cdata.at[self.last_day, 'rad_j'] - cdata.at[before_last_day, 'rad_j'],
                    "all_rad": cdata.at[self.last_day, 'rad_rectif'],          
                    "current_hosp": cdata.at[self.last_day, 'hosp'],
                    "diff_hosp": cdata.at[self.last_day, 'hosp'] - cdata.at[before_last_day, 'hosp'],
                    "current_rea": cdata.at[self.last_day, 'rea'], 
                    "diff_rea": cdata.at[self.last_day, 'rea'] - cdata.at[before_last_day, 'rea'],

                    "rates": {
                                "dc": ((cdata.at[self.last_day, 'dc_rectif'] / cpop) * 100000).round(2),
                                "d_dc": (((cdata.at[self.last_day, 'dc_rectif'] - cdata.at[before_last_day, 'dc_rectif']) / cpop) * 100000).round(2),
                                "rea": ((cdata.at[self.last_day, 'rea'] / cpop) * 100000).round(2),
                                "d_rea": (((cdata.at[self.last_day, 'rea'] - cdata.at[before_last_day, 'rea']) / cpop) * 100000).round(2),
                                "hosp": ((cdata.at[self.last_day, 'hosp'] / cpop) * 100000).round(2),
                                "d_hosp": (((cdata.at[self.last_day, 'hosp'] - cdata.at[before_last_day, 'hosp']) / cpop) * 100000).round(2),
                                "rad": ((cdata.at[self.last_day, 'rad_rectif'] / cpop) * 100000).round(2),
                                "d_rad": (((cdata.at[self.last_day, 'rad_rectif'] - cdata.at[before_last_day, 'rad_rectif']) / cpop) * 100000).round(2),
                                "r_dc_rad": ((cdata.at[self.last_day, 'dc_rectif'] / (cdata.at[self.last_day, 'dc_rectif'] + cdata.at[self.last_day, 'rad_rectif']))*100).round(2),
                                "d_r_dc_rad": ((cdata.at[self.last_day, 'dc_rectif'] / (cdata.at[self.last_day, 'dc_rectif'] + cdata.at[self.last_day, 'rad_rectif']))*100 - (cdata.at[before_last_day, 'dc_rectif'] / (cdata.at[before_last_day, 'dc_rectif'] + cdata.at[before_last_day, 'rad_rectif']))*100).round(2),
                            },
                
                    "nat_refs": {
                                "nat_dc": ((fdata.at[self.last_day, 'dc'] / popfr) * 100000).round(2),
                                "nat_r_dc_rad": (fdata.at[self.last_day, 'dc'] / (fdata.at[self.last_day, 'dc'] + fdata.at[self.last_day, 'rad'])).round(2),
                                "nat_rad": ((fdata.at[self.last_day, 'rad'] / popfr) * 100000).round(2),
                                "nat_hosp": ((fdata.at[self.last_day, 'hosp'] / popfr) * 100000).round(2),
                                "nat_rea": ((fdata.at[self.last_day, 'rea'] / popfr) * 100000).round(2),
                                },
                    }
        gJ.update({'counters': counters})

        return gJ

    ##############################
    # positive case study starting
    ##############################
    def map_positive_reg(self, data=None):
        """
        Get data from regions as a JSON string along with quantiles
        Returns:
            JSON string of regions overall data
        """     
        if data is None:
            reg_data = self.rprate[(self.rprate['cl_age90'] == 0)].copy()
        else:
            reg_data = data[(data['cl_age90'] == 0)]

        overall_reg_data_as_json_dict = {}

        for feature in ["P"]:         
            ### For positive case map
            reg_data_j = self.rprate[(self.rprate['cl_age90'] == 0) & (self.rprate['jour'] == self.positive_last_day)]
            reg_data_j = reg_data_j.drop(["jour", "cl_age90"], axis=1).groupby('reg').max()
            reg_data_j = pd.concat([reg_data_j, self.region_base_data], axis=1)

            reg_data_j[feature+'_par_habitants'] = (reg_data_j[feature] / reg_data_j['population']) * 100000
            
            data_feature = reg_data_j.copy()
            
            data_feature = data_feature.set_index("region-" + data_feature.index)
            
            data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

            nat = (reg_data.groupby("jour").sum().at[self.positive_last_day, feature] / self.region_base_data["population"].sum()) * 100000

            q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() <= nat)

            q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

            quantiles_feature = data_feature[feature+'_par_habitants'] \
                .quantile(q_feature_list) \
                .round(2)

            data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

            #setattr(self, 'overall_regions_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

            overall_reg_data_as_json_dict.update({'overall_regions_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

        return overall_reg_data_as_json_dict

    def map_positive_dep(self, data=None):
        """
        Get data from regions as a JSON string along with quantiles
        Returns:
            JSON string of departments overall data
        """     
        if data is None:
            dep_data = self.dprate[(self.dprate['cl_age90'] == 0)].copy()
        else:
            dep_data = data[(data['cl_age90'] == 0)]

        overall_dep_data_as_json_dict = {}

        for feature in ["P"]:         
            ### For positive case map
            dep_data_j = self.dprate[(self.dprate['cl_age90'] == 0) & (self.dprate['jour'] == self.positive_last_day)]
            dep_data_j = dep_data_j.drop(["jour", "cl_age90"], axis=1).groupby('dep').max()
            dep_data_j = pd.concat([dep_data_j, self.department_base_data], axis=1)

            dep_data_j[feature+'_par_habitants'] = (dep_data_j[feature] / dep_data_j['population']) * 100000
            
            data_feature = dep_data_j.copy()
            
            data_feature = data_feature.set_index("department-" + data_feature.index)
            
            data_feature = data_feature.loc[:, ['label', feature, feature+'_par_habitants', 'insee']]

            nat = (dep_data.groupby("jour").sum().at[self.positive_last_day, feature] / self.department_base_data["population"].sum()) * 100000

            q_feature = np.mean(data_feature[feature+'_par_habitants'].to_numpy() <= nat)

            q_feature_list = [0.1, 0.1+(q_feature-0.1)/2, q_feature, q_feature+(.949-q_feature)/2, .949]

            quantiles_feature = data_feature[feature+'_par_habitants'] \
                .quantile(q_feature_list) \
                .round(2)

            data_feature[feature+'_par_habitants'] = data_feature[feature+'_par_habitants'].round(2)

            #setattr(self, 'overall_departments_{}'.format(feature)+"_as_json", {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')})

            overall_dep_data_as_json_dict.update({'overall_departments_{}'.format(feature)+"_as_json": {"data_"+feature: data_feature.to_json(orient='index'), "quantiles_"+feature: quantiles_feature.to_json(orient='index')}})

        return overall_dep_data_as_json_dict

    def charts_and_parameters_positive_data(self, data=None, department=None, region=None): 
        if region is None and department is None:
            if data is None:
                cdata = self.nprate[self.nprate.cl_age90 == 0].groupby(['jour']).sum().copy()
                cpop = self.department_base_data["population"].sum()
            else: 
                cdata = data[data.cl_age90 == 0].groupby(['jour']).sum().copy()
                cpop = self.department_base_data["population"].sum()
        elif region is None and not department is None:
            if data is None:
                cdata = self.dprate[(self.dprate.dep == department) & (self.dprate.cl_age90 == 0)].groupby(['jour']).sum().copy()
                cpop = self.department_base_data.at[department, 'population']
            else: 
                cdata = data[(data.dep == department) & (data.cl_age90 == 0)].groupby(['jour']).sum().copy()
                cpop = self.department_base_data.at[department, 'population']
        elif not region is None and department is None:
            if data is None:
                cdata = self.rprate[(self.rprate.reg == region) & (self.rprate.cl_age90 == 0)].groupby(['jour']).sum().copy()
                cpop = self.region_base_data.at[region, 'population']
            else: 
                cdata = data[(data.reg == region) & (data.cl_age90 == 0)].groupby(['jour']).sum().copy()
                cpop = self.region_base_data.at[region, 'population']

        graphs = [
            dict(
                id = "Nombre de personnes actuellement positives",
                data = [CovidFr.dataviz(x=cdata.index, y=cdata['P'], curve_type='bar', color='#f84ed3', width=1, opacity=0.8)],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=15, b=30, t=30), barmode='overlay',linemode='overlay', legend_orientation="h"),
            ),   
        ]
        #############################################################
        gJ = {}
        for g in range(len(graphs)):
            gJ.update({'graphJSON{}'.format(g): json.dumps([graphs[g]], cls=plotly.utils.PlotlyJSONEncoder)})
        #############################################################

        fdata = self.nprate[self.nprate.cl_age90 == 0].groupby(['jour']).sum().copy()
        popfr = self.department_base_data["population"].sum()

        before_last_day = cdata.index[-2].strftime("%Y-%m-%d")

        counters = {
                "positive_last_day_fr": self.positive_last_day_fr,
                "positive_last_update_fr": datetime.strptime(self.positive_last_update, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y à %Hh%M"),
                            
                "current_positive": cdata.at[self.positive_last_day, 'P'],
                "diff_positive": cdata.at[self.positive_last_day, 'P'] - cdata.at[before_last_day, 'P'],

                "rates": {
                        "positive": ((cdata.at[self.positive_last_day, 'P'] / cpop) * 100000).round(2),
                        "d_positive": (((cdata.at[self.positive_last_day, 'P'] - cdata.at[before_last_day, 'P']) / cpop) * 100000).round(2),
                        },
            
                "nat_refs": {
                            "nat_positive": ((fdata.at[self.positive_last_day, 'P'] / popfr) * 100000).round(2),
                            },
                }

        gJ.update({'counters': counters})

        return gJ
    ##############################
    # positive case study ending
    ##############################

    def request_label(self, department=None, region=None):
        """Get a department or a region label from its insee code
        Returns:
            Department or Region label
        """
        if not department is None and region is None:
            if department in self.department_base_data.index:
                return {"prefix": "dépt.", "type": "department", "name": self.department_base_data.at[department, 'label']}
            return ""
        elif department is None and not region is None:
            if region in self.region_base_data.index:
                return {"prefix": "région", "type": "region", "name": self.region_base_data.at[region, 'label']}
            return ""
        return "France"

    def pca_charts(self, data, pcdim, q=0.975, normalize=False, start_d_learn='15/05/2020', end_d_learn='20/08/2020', alpha=1-0.4):
        
        results = CovidFr.pca(data, pcdim, q, normalize, start_d_learn, end_d_learn, alpha)

        annotations = [
            go.layout.Annotation(
                #x = max(results["Hotelling"]["dataindex"])-(max(results["Hotelling"]["dataindex"])-min(results["Hotelling"]["dataindex"]))/4,
                x = results["Hotelling"]["dataindex"][-30],
                y = 3*max(results["Hotelling"]["t2"])/4,
                xref = "x",
                yref = "y",
                text = 'rpc: {} pc (ev: {}%)<br>normalized data: {}<br>model building: {} <br>to {}<br>smoothing filter: {}'.format(pcdim, ((np.trace(np.diag(results["eigenvalues"][:pcdim]))/np.trace(np.diag(results["eigenvalues"])))*100).round(2), normalize, start_d_learn, end_d_learn, alpha),
                showarrow = False,
                font = dict(
                    family = "Courier New, monospace",
                    size = 10,
                    color = "#ffffff",
                    ),
                align = "left",
                arrowhead = 2,
                arrowsize = 1,
                arrowwidth = 2,
                arrowcolor = "#636363",
                ax = 20,
                ay = 30,
                bordercolor = "#c7c7c7",
                borderwidth = 2,
                borderpad = 4,
                bgcolor = '#000080',
                opacity = 0.3,
            )
        ]

        graphs = [
            dict(
                id = 'Hotelling',
                data=[
                    CovidFr.dataviz(x=results["Hotelling"]["dataindex"], y=results["Hotelling"]["t2"], curve_type='line', color='#02056D', name='score t', width=3, text=['situation anormale' if results["Hotelling"]["t2"][i]>results["Hotelling"]["threshold"] else 'situation normale' for i in range(len(results["Hotelling"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>'),

                    CovidFr.dataviz(x=results["Hotelling"]["dataindex"], y=results["Hotelling"]["smoothed_t2"], curve_type='line', color='#026D2F', name='score t filtré', width=3, text=['situation anormale' if results["Hotelling"]["smoothed_t2"][i]>results["Hotelling"]["threshold"] else 'situation normale' for i in range(len(results["Hotelling"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>'),

                    CovidFr.dataviz(x=results["Hotelling"]["dataindex"], y=np.repeat(results["Hotelling"]["threshold"], results["Hotelling"]["t2"].shape[0]), curve_type='line', color='#ff0000', name='seuil', width=3, text=['seuil' for i in range(len(results["Hotelling"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>', showlegend = False),
                ],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30), linemode='overlay', legend=dict(orientation="h"), annotations=annotations),
            ),

            dict(
                id = 'SPE',
                data=[
                    CovidFr.dataviz(x=results["SPE"]["dataindex"], y=results["SPE"]["spe"], curve_type='line', color='#02056D', name='score s', width=3, text=['situation anormale' if results["SPE"]["spe"][i]>results["SPE"]["threshold"] else 'situation normale' for i in range(len(results["SPE"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>'),

                    CovidFr.dataviz(x=results["SPE"]["dataindex"], y=results["SPE"]["smoothed_spe"], curve_type='line', color='#026D2F', name='score s filtré', width=3, text=['situation anormale' if results["SPE"]["smoothed_spe"][i]>results["SPE"]["threshold"] else 'situation normale' for i in range(len(results["SPE"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>'),

                    CovidFr.dataviz(x=results["SPE"]["dataindex"], y=np.repeat(results["SPE"]["threshold"], results["SPE"]["spe"].shape[0]), curve_type='line', color='#ff0000', name='seuil', width=3, text=['seuil' for i in range(len(results["SPE"]["dataindex"]))], hovertemplate='<b>%{text}</b><extra></extra>', showlegend = False),
                ],
                layout = CovidFr.layoutoption(margin=dict(l=30, r=30, b=30, t=30), linemode='overlay', legend=dict(orientation="h")),
            ),
        ]

        graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

        return {'graphJSON': graphJSON,
                'retained PCs': pcdim,
                'normalized': normalize,
                'explained variance': ((np.trace(np.diag(results["eigenvalues"][:pcdim]))/np.trace(np.diag(results["eigenvalues"])))*100).round(2),
                'SPE': {'spe': results["SPE"]["spe"],
                        'smoothed_spe': results["SPE"]["smoothed_spe"],
                        'threshold': results["SPE"]["threshold"],
                       },
                'Hotelling': {'t2': results["Hotelling"]["t2"], 
                              'smoothed_t2': results["Hotelling"]["smoothed_t2"], 
                              'threshold': results["Hotelling"]["threshold"],
                             },
               }

    @staticmethod
    def normrate(ddn, cdu, featurelist):
        dep_data_norm_col = {}
        for col in featurelist:
            data = []
            for dep in cdu:
                data.append(ddn[dep][col])
            dep_data_norm_col.update({col: pd.concat(data, axis=1, keys=cdu)})
        return dep_data_norm_col

    @staticmethod
    def regionadd(data):
        regions = {
            "01": {"Guadeloupe": ['971']},
            "02": {"Martinique": ['972']},
            "03": {"Guyane": ['973']},
            "04": {"La Réunion": ['974']},
            "06": {"Mayotte": ['976']},
            "11": {"Île-de-France": ['92', '93', '94', '78', '75', '77', '91', '95']},
            "24": {"Centre-Val de Loire": ['41', '28', '45', '18', '37', '36']},
            "27": {"Bourgogne-Franche-Comté": ['71', '58', '25', '70', '90', '39', '89', '21']},
            "28": {"Normandie": ['76', '61', '50', '14', '27']},
            "32": {"Hauts-de-France": ['60', '59', '02', '62', '80']},
            "44": {"Grand Est": ['54', '68', '51', '55', '08', '57', '67', '52', '88', '10']},
            "52": {"Pays de la Loire": ['49', '85', '44', '72', '53']},
            "53": {"Bretagne": ['29', '56', '35', '22']},
            "75": {"Nouvelle-Aquitaine": ['24', '17', '33', '64', '16', '40', '19', '79', '87', '86', '47', '23']},
            "76": {"Occitanie": ['34', '48', '46', '82', '11', '12', '32', '09', '81', '65', '30', '66', '31']}, 
            "84": {"Auvergne-Rhône-Alpes": ['38', '01', '42', '74', '73', '43', '03', '26', '69', '07', '63', '15']},
            "93": {"Provence-Alpes-Côte d'Azur": ['13', '05', '06', '84', '04', '83']},
            "94": {"Corse": ['2B', '2A']},
            }
        for key, value in regions.items():
            for k, v in value.items():
                data.loc[data.loc[data['dep'].isin(v)].index, 'reg'] = key
        data = data[["reg", "dep", "sexe", "jour", "hosp", "rea", "rad", "dc"]]
        return data
    
    @staticmethod
    def dailycases(data=None, pca=False):
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

        cdata["rad_rectif"] = rad_rectif
        cdata["dc_rectif"] = dc_rectif
        cdata["rad_j"] = rad_j
        cdata["dc_j"] = dc_j

        if pca is True:
            cdata = cdata[['hosp', 'rea', 'rad_j', 'dc_j']]
            cdata = cdata.rename(columns={'rad_j':'rad', 'dc_j':'dc'})
            return cdata
        return cdata

    @staticmethod
    def ewma_filter(data, alpha, offset=None, dtype=None, order='C', out=None):
        """
        Calculates the exponential moving average over a vector.
        Will fail for large inputs.
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

    @staticmethod
    def pca(data, pcdim, q, normalize, start_d_learn, end_d_learn, alpha):
        """
        Get PCA on data
        """
        dataindex = data.index
        #learn_data = data[(data.index>=start_d_learn) & (data.index<=end_d_learn)].copy()
        learn_data = data[(data.index>=datetime.strptime(start_d_learn, '%d/%m/%Y').strftime("%Y-%m-%d")) & (data.index<=datetime.strptime(end_d_learn, '%d/%m/%Y').strftime("%Y-%m-%d"))].copy()
        if normalize is True:
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

        return {"SPE": {
                        "dataindex": dataindex,
                        "spe": spe,
                        "smoothed_spe": CovidFr.ewma_filter(data=spe, alpha=alpha),
                        "threshold": gspe*chi2.ppf(q, df=hspe),
                        },
                "Hotelling": {
                        "dataindex": dataindex,
                        "t2": t2,
                        "smoothed_t2": CovidFr.ewma_filter(data=t2, alpha=alpha),
                        "threshold": chi2.ppf(q, df=pcdim),
                        },
                "eigenvalues": s,
                }

    @staticmethod
    def regiondailycases(data, feature):
        if feature in ["dc", "rad"]:   
            dr = {}
            for r in data.reg.unique():
                regdep = []
                for d in data[data.reg==r].dep.unique():
                    regdep.append(CovidFr.dailycases(data=data[(data.dep == d) & (data.sexe == 0)].groupby(['jour']).sum(), pca=True))
                cdata = reduce(lambda x, y: x.add(y, fill_value=0), regdep)
                dr.update({"reg-"+r: cdata[feature]})
            return pd.DataFrame.from_dict(dr)
        elif feature in ["hosp", "rea"]:
            data_reg = pd.DataFrame()
            for r in data.reg.unique():
                dep_reg = []
                for d in data[data.reg==r].dep.unique():
                    dep_reg.append(data[(data.sexe == 0) & (data.dep == d)][feature].reset_index(drop=True))
                data_reg['reg-{}'.format(r)] = reduce(lambda x, y: x.add(y, fill_value=0), dep_reg)
            data_reg["jour"] = pd.unique(data.jour)
            return data_reg.groupby("jour").max()
    
    @staticmethod
    def topdepdataviz(data, **kwargs):
        top = kwargs.get('top', False)
        top_number = kwargs.get('top_number', None)
        threshold = kwargs.get('threshold', None)

        if top:
            df = data.sort_values(by=data.index.max(), axis=1, ascending=False)
            select_dep_data_norm_col = df[df.columns[:top_number]]
        else:
            select_dep_data_norm_col = data[data.columns[[item for elem in (data[-1:] > threshold).values.tolist() for item in elem]]]

        return select_dep_data_norm_col
    
    @staticmethod
    def dataviz(x, y, curve_type, **kwargs):
        name = kwargs.get('name', None)
        color = kwargs.get('color', None)
        width = kwargs.get('width', None)
        opacity = kwargs.get('opacity', None)
        hovertemplate = kwargs.get('hovertemplate', None)
        text = kwargs.get('text', None)
        showlegend = kwargs.get('showlegend', None)

        output = dict(
            x = x,
            y = y,
            type = curve_type,
            name = name,
            marker = dict(
                color = color,
                line = dict(
                    color = color, 
                    width = width,
                ),
                opacity = opacity,
            ),
            hovertemplate = hovertemplate,
            text = text,
            showlegend = showlegend,
        )
        return output

    @staticmethod
    def layoutoption(**kwargs):
        title = kwargs.get('title', None)
        barmode = kwargs.get('barmode', None)
        linemode = kwargs.get('linemode', None)
        legend_orientation = kwargs.get('legend_orientation', None)
        legend = kwargs.get('legend', None)
        margin = kwargs.get('margin', None)
        annotations = kwargs.get('annotations', None)

        output = dict(
            title = title,
            barmode = barmode,
            linemode = linemode,
            legend_orientation = legend_orientation,
            legend = legend,
            margin = margin,
            annotations = annotations,
        )
        return output 

    @staticmethod
    def updatechecking(json_url, data_request_url):
        with urllib.request.urlopen(json_url) as url:
            data = json.loads(url.read().decode())
            for dataset in data['@graph']:
                if 'accessURL' in dataset.keys() and dataset['accessURL'] == data_request_url:
                    return dataset['modified']