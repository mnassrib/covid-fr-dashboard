from flask import Flask, render_template, request, redirect, url_for

from cutils.cvcreation import CvCreation
from cutils.rendertemplate import RenderPage

app = Flask(__name__)

covfr, daily, daily_reg, cv = CvCreation().cv_load()

@app.route('/', methods=['GET', 'POST'])
def graphs():
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        rp = RenderPage("graphs.html", **upcv)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    return rp.appview()

@app.route('/maps', methods=['GET', 'POST'])
def maps():
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        rp = RenderPage("graphs.html", **upcv)
        rp.map_select = request.form.get('map_select')
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.map_select = request.form.get('map_select')
    return rp.appview()

@app.route("/top_dep_settings", methods=['GET', 'POST'])
def top_dep_settings():
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        rp = RenderPage("graphs.html", **upcv)
        rp.top_dep = int(request.form.getlist('top_dep_settings')[0])
        rp.criterion_select = request.form.getlist('top_dep_settings')[1]
        rp.charts_impacted_dep = upcovfr.charts_impacted_dep(top_number=rp.top_dep)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.top_dep = int(request.form.getlist('top_dep_settings')[0])
    rp.criterion_select = request.form.getlist('top_dep_settings')[1]
    rp.charts_impacted_dep = covfr.charts_impacted_dep(top_number=rp.top_dep)
    return rp.appview()
    
@app.route("/global_monitoring_settings", methods=['GET', 'POST'])
def global_monitoring_settings():
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        global_select = request.form.getlist('global_parameters')
        rp = RenderPage("graphs.html", **upcv)
        rp.pcdim = int(global_select[0])
        rp.normalize = eval(global_select[1])
        rp.start_d_learn_fr = global_select[2].split(" - ")[0]
        rp.end_d_learn_fr = global_select[2].split(" - ")[1]
        rp.alpha = float(global_select[3])
        rp.charts_pca_global = upcovfr.pca_charts(data=updaily, pcdim=rp.pcdim, normalize=rp.normalize, start_d_learn=rp.start_d_learn_fr, end_d_learn=rp.end_d_learn_fr, alpha=rp.alpha)
        return rp.appview()

    global_select = request.form.getlist('global_parameters')
    rp = RenderPage("graphs.html", **cv)
    rp.pcdim = int(global_select[0])
    rp.normalize = eval(global_select[1])
    rp.start_d_learn_fr = global_select[2].split(" - ")[0]
    rp.end_d_learn_fr = global_select[2].split(" - ")[1]
    rp.alpha = float(global_select[3])
    rp.charts_pca_global = covfr.pca_charts(data=daily, pcdim=rp.pcdim, normalize=rp.normalize, start_d_learn=rp.start_d_learn_fr, end_d_learn=rp.end_d_learn_fr, alpha=rp.alpha)
    return rp.appview()

@app.route("/hosp_monitoring_settings", methods=['GET', 'POST'])
def hosp_monitoring_settings():
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        hosp_select = request.form.getlist('hosp_parameters')
        rp = RenderPage("graphs.html", **upcv)
        rp.pcdim_reg = int(hosp_select[0])
        rp.normalize_reg = eval(hosp_select[1])
        rp.start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
        rp.end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
        rp.alpha_reg = float(hosp_select[3])
        rp.charts_pca_hosp_reg = upcovfr.pca_charts(data=updaily_reg, pcdim=rp.pcdim_reg, normalize=rp.normalize_reg, start_d_learn=rp.start_d_learn_fr_reg, end_d_learn=rp.end_d_learn_fr_reg, alpha=rp.alpha_reg)
        return rp.appview()

    hosp_select = request.form.getlist('hosp_parameters')
    rp = RenderPage("graphs.html", **cv)
    rp.pcdim_reg = int(hosp_select[0])
    rp.normalize_reg = eval(hosp_select[1])
    rp.start_d_learn_fr_reg = hosp_select[2].split(" - ")[0]
    rp.end_d_learn_fr_reg = hosp_select[2].split(" - ")[1]
    rp.alpha_reg = float(hosp_select[3])
    rp.charts_pca_hosp_reg = covfr.pca_charts(data=daily_reg, pcdim=rp.pcdim_reg, normalize=rp.normalize_reg, start_d_learn=rp.start_d_learn_fr_reg, end_d_learn=rp.end_d_learn_fr_reg, alpha=rp.alpha_reg)
    return rp.appview()

@app.route('/departement/<string:department>', methods=['GET', 'POST'])
def view_department(department):
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        rp = RenderPage("graphs.html", **upcv)
        rp.department = department
        rp.charts_and_parameters_covid_data = upcovfr.charts_and_parameters_covid_data(department=rp.department)
        rp.charts_and_parameters_positive_data = upcovfr.charts_and_parameters_positive_data(department=rp.department)
        rp.label = upcovfr.request_label(department=rp.department)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.department = department
    rp.charts_and_parameters_covid_data = covfr.charts_and_parameters_covid_data(department=rp.department)
    rp.charts_and_parameters_positive_data = covfr.charts_and_parameters_positive_data(department=rp.department)
    rp.label = covfr.request_label(department=rp.department)
    return rp.appview()

@app.route('/region/<string:region>', methods=['GET', 'POST'])
def view_region(region):
    if covfr.covid_need_update() or covfr.positive_need_update():
        upcovfr, updaily, updaily_reg, upcv = CvCreation().cv_load(covid_state=covfr.covid_need_update(), positive_state=covfr.positive_need_update())
        rp = RenderPage("graphs.html", **upcv)
        rp.region = region
        rp.charts_and_parameters_covid_data = upcovfr.charts_and_parameters_covid_data(region=rp.region)
        rp.charts_and_parameters_positive_data = upcovfr.charts_and_parameters_positive_data(region=rp.region)
        rp.label = upcovfr.request_label(region=rp.region)
        return rp.appview()

    rp = RenderPage("graphs.html", **cv)
    rp.region = region
    rp.charts_and_parameters_covid_data = covfr.charts_and_parameters_covid_data(region=rp.region)
    rp.charts_and_parameters_positive_data = covfr.charts_and_parameters_positive_data(region=rp.region)
    rp.label = covfr.request_label(region=rp.region)
    return rp.appview()

if __name__ == '__main__':
    app.run(debug=True)