from flask import Flask, render_template, request, redirect, url_for

from cutils.covidclass import CovidFr

#from cutils.rendertemplate import ViewPage
class ViewPage(object):
    """
    docstring
    """
    def __init__(self):
        self.map_covid_reg = map_covid_reg
        self.map_covid_dep = map_covid_dep
        self.map_positive_reg = map_positive_reg
        self.map_positive_dep = map_positive_dep

        self.charts_impacted_dep = charts_impacted_dep
        self.charts_and_parameters_positive_data = charts_and_parameters_positive_data
        self.charts_and_parameters_covid_data = charts_and_parameters_covid_data

        self.charts_pca_global = charts_pca_global
        self.charts_pca_hosp_reg = charts_pca_hosp_reg

        self.label = label

        self.region = region
        self.department = department
        self.first_day_fr = first_day_fr
        self.last_day_fr = last_day_fr
        self.map_choice = map_choice
        self.criterion_choice = criterion_choice
        self.number_all_dep = number_all_dep
        self.global_pc = global_pc
        self.normalize_states = normalize_states
        self.alpha_smooth = alpha_smooth
        self.pc_reg = pc_reg
        self.map_select = map_select
        self.top_dep = top_dep
        self.criterion_select = criterion_select
        self.pcdim = pcdim
        self.normalize = normalize
        self.alpha = alpha
        self.start_d_learn_fr = start_d_learn_fr
        self.end_d_learn_fr = end_d_learn_fr
        self.pcdim_reg = pcdim_reg
        self.normalize_reg = normalize_reg
        self.alpha_reg = alpha_reg
        self.start_d_learn_fr_reg = start_d_learn_fr_reg
        self.end_d_learn_fr_reg = end_d_learn_fr_reg

    def appview(self):
        return render_template(
            "graphs.html",
            map_covid_reg = self.map_covid_reg,
            map_covid_dep = self.map_covid_dep,
            map_positive_reg = self.map_positive_reg,
            map_positive_dep = self.map_positive_dep,
            
            charts_impacted_dep = self.charts_impacted_dep,
            charts_and_parameters_positive_data = self.charts_and_parameters_positive_data,
            charts_and_parameters_covid_data = self.charts_and_parameters_covid_data,

            charts_pca_global = self.charts_pca_global,
            charts_pca_hosp_reg = self.charts_pca_hosp_reg,

            label = self.label,

            region = self.region,
            department = self.department,
            first_day_fr = self.first_day_fr,
            last_day_fr = self.last_day_fr,
            map_choice = self.map_choice,
            criterion_choice = self.criterion_choice,
            number_all_dep = self.number_all_dep,
            global_pc = self.global_pc,
            normalize_states = self.normalize_states,
            alpha_smooth = self.alpha_smooth,
            pc_reg = self.pc_reg,
            map_select = self.map_select,
            top_dep = self.top_dep,
            criterion_select = self.criterion_select,
            pcdim = self.pcdim,
            normalize = self.normalize,
            start_d_learn_fr = self.start_d_learn_fr,
            end_d_learn_fr = self.end_d_learn_fr,
            alpha = self.alpha,
            pcdim_reg = self.pcdim_reg,
            normalize_reg = self.normalize_reg,
            start_d_learn_fr_reg = self.start_d_learn_fr_reg,
            end_d_learn_fr_reg = self.end_d_learn_fr_reg,
            alpha_reg = self.alpha_reg,
        )

app = Flask(__name__)

covfr = CovidFr()

covid = covfr.load_df()
nprate, rprate, dprate = covfr.load_positive_df()

map_covid_reg = covfr.overall_regions_data_as_json()
map_covid_dep = covfr.overall_departments_data_as_json()
map_positive_reg = covfr.overall_regions_positive_data_as_json()
map_positive_dep = covfr.overall_departments_positive_data_as_json()

charts_impacted_dep = covfr.charts_impacted_dep()
charts_and_parameters_covid_data = covfr.charts()
charts_and_parameters_positive_data = covfr.charts_positive_data()

daily = covfr.dailycases(data=covid, pca=True)
daily_reg = covfr.regiondailycases(data=covid, feature='hosp')

charts_pca_global = covfr.pca_charts(data=daily, pcdim=covfr.default_pcdim, normalize=covfr.default_normalize, start_d_learn=covfr.default_start_d_learn_fr, end_d_learn=covfr.default_end_d_learn_fr, alpha=covfr.default_alpha)
charts_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=covfr.default_pcdim_reg, normalize=covfr.default_normalize_reg, start_d_learn=covfr.default_start_d_learn_fr_reg, end_d_learn=covfr.default_end_d_learn_fr_reg, alpha=covfr.default_alpha_reg)

label = covfr.request_label()

##########################################################
# required html page variables
###############################
# map_covid_reg = map_covid_reg
# map_covid_dep = map_covid_dep
# map_positive_reg = map_positive_reg
# map_positive_dep = map_positive_dep

# charts_impacted_dep = charts_impacted_dep
# charts_and_parameters_positive_data = charts_and_parameters_positive_data
# charts_and_parameters_covid_data = charts_and_parameters_covid_data

# charts_pca_global = charts_pca_global
# charts_pca_hosp_reg = charts_pca_hosp_reg

# label = label

department = covfr.default_department
region = covfr.default_region
first_day_fr = covfr.first_day_fr
last_day_fr = covfr.last_day_fr
map_choice = covfr.map_choice
criterion_choice = covfr.criterion_choice
number_all_dep = covfr.number_all_dep
global_pc = covfr.global_pc
normalize_states = covfr.normalize_states
alpha_smooth = covfr.alpha_smooth
pc_reg = covfr.pc_reg
map_select = covfr.default_map_select
top_dep = covfr.default_top_dep
criterion_select = covfr.default_criterion_select
pcdim = covfr.default_pcdim
normalize = covfr.default_normalize
start_d_learn_fr = covfr.default_start_d_learn_fr
end_d_learn_fr = covfr.default_end_d_learn_fr
alpha = covfr.default_alpha
pcdim_reg = covfr.default_pcdim_reg
normalize_reg = covfr.default_normalize_reg
start_d_learn_fr_reg = covfr.default_start_d_learn_fr_reg
end_d_learn_fr_reg = covfr.default_end_d_learn_fr_reg
alpha_reg = covfr.default_alpha_reg
##########################################################

@app.route('/', methods=['GET', 'POST'])
def graphs():
    vp = ViewPage()
    return vp.appview()

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    vp = ViewPage()
    vp.map_select = request.form.get('map_select')
    return vp.appview()

@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():
    vp = ViewPage()
    vp.top_dep = int(request.form.getlist('top_dep_settings')[0])
    vp.criterion_select = request.form.getlist('top_dep_settings')[1]
    vp.charts_impacted_dep = covfr.charts_impacted_dep(top_number=vp.top_dep)
    return vp.appview()
    
@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    global_select = request.form.getlist('global_parameters')
    vp = ViewPage()
    vp.pcdim = int(global_select[0])
    vp.normalize = eval(global_select[1])
    vp.start_d_learn_fr = global_select[2].split(" - ")[0]
    vp.end_d_learn_fr = global_select[2].split(" - ")[1]
    vp.alpha = float(global_select[3])
    vp.charts_pca_global = covfr.pca_charts(data=daily, pcdim=vp.pcdim, normalize=vp.normalize, start_d_learn=vp.start_d_learn_fr, end_d_learn=vp.end_d_learn_fr, alpha=vp.alpha)
    return vp.appview()

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    hosp_select = request.form.getlist('hosp_parameters')
    vp = ViewPage()
    vp.pcdim_reg = int(hosp_select[0])
    vp.normalize_reg = eval(hosp_select[1])
    vp.start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
    vp.end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
    vp.alpha_reg = float(hosp_select[3])
    vp.charts_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=vp.pcdim_reg, normalize=vp.normalize_reg, start_d_learn=vp.start_d_learn_fr_reg, end_d_learn=vp.end_d_learn_fr_reg, alpha=vp.alpha_reg)
    return vp.appview()

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    vp = ViewPage()
    vp.department = department
    vp.charts_and_parameters_covid_data = covfr.charts(department=vp.department)
    vp.charts_and_parameters_positive_data = covfr.charts_positive_data(department=vp.department)
    vp.label = covfr.request_label(department=vp.department)
    return vp.appview()

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    vp = ViewPage()
    vp.region = region
    vp.charts_and_parameters_covid_data = covfr.charts(region=vp.region)
    vp.charts_and_parameters_positive_data = covfr.charts_positive_data(region=vp.region)
    vp.label = covfr.request_label(region=vp.region)
    return vp.appview()

if __name__ == '__main__':
    app.run(debug=True)