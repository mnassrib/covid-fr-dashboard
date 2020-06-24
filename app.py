from flask import Flask, render_template, request

from cutils.covidclass import CovidFr

app = Flask(__name__)

covfr = CovidFr()
covid = covfr.load_df()
oddaj_dep = covfr.overall_departments_data_as_json()
oddaj_reg = covfr.overall_regions_data_as_json()

daily = covfr.dailycases(data=covid, pca=True)

graphJSONquadratics = covfr.pca_charts(data=daily, pcdim=2, normalize=True)

@app.route('/')
def graphs():
    """Country page of the app"""
    charts_and_parameters = covfr.charts()
    
    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"],  
        counters = charts_and_parameters["counters"],
        label = covfr.request_label(department=None, region=None),

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],
        
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        graphJSONquadratics = graphJSONquadratics,

        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
    )

@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=department, region=None)
    label = covfr.request_label(department=department, region=None)

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        label = label,
        department = department,

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],
        
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        graphJSONquadratics = graphJSONquadratics,

        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
    )

@app.route('/region/<string:region>')
def view_region(region):
    """Region page of the app"""
    charts_and_parameters = covfr.charts(data=None, department=None, region=region)
    label = covfr.request_label(department=None, region=region)

    return render_template(
        "graphs.html", 
        graphJSON = charts_and_parameters["graphJSON"], 
        counters = charts_and_parameters["counters"],
        label = label,
        region = region,

        overall_departments_data_dc = oddaj_dep["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj_dep["overall_departments_dc_as_json"]['quantiles_dc'],
        
        overall_departments_data_hosp = oddaj_dep["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj_dep["overall_departments_hosp_as_json"]['quantiles_hosp'],
        
        overall_departments_data_rad = oddaj_dep["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj_dep["overall_departments_rad_as_json"]['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj_dep["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rea = oddaj_dep["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj_dep["overall_departments_rea_as_json"]['quantiles_rea'],

        graphJSONquadratics = graphJSONquadratics,

        overall_regions_data_dc = oddaj_reg["overall_regions_dc_as_json"]['data_dc'],
        overall_regions_quantiles_dc = oddaj_reg["overall_regions_dc_as_json"]['quantiles_dc'],

        overall_regions_data_hosp = oddaj_reg["overall_regions_hosp_as_json"]['data_hosp'],
        overall_regions_quantiles_hosp = oddaj_reg["overall_regions_hosp_as_json"]['quantiles_hosp'],

        overall_regions_data_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_regions_quantiles_r_dc_rad = oddaj_reg["overall_regions_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_regions_data_rad = oddaj_reg["overall_regions_rad_as_json"]['data_rad'],
        overall_regions_quantiles_rad = oddaj_reg["overall_regions_rad_as_json"]['quantiles_rad'],

        overall_regions_data_rea = oddaj_reg["overall_regions_rea_as_json"]['data_rea'],
        overall_regions_quantiles_rea = oddaj_reg["overall_regions_rea_as_json"]['quantiles_rea'],
    )

if __name__ == '__main__':
    app.run(debug=True)
