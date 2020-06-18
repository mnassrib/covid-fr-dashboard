from flask import Flask, render_template, request

from cutils.covidclass import CovidFr

app = Flask(__name__)

covfr = CovidFr()
covid = covfr.load_df()
oddaj = covfr.overall_departments_data_as_json()
daily = covfr.dailycases(data=covid)

graphJSONquadratics = covfr.acp(data=daily, pcdim=2, normalize=True)["graphJSON"]

@app.route('/')
def graphs():
    """Country page of the app"""

    chartreqs = covfr.charts()
    
    return render_template(
        "graphs.html", 
        graphJSON = chartreqs["graphJSON"],  
        counters = chartreqs["counters"],
        label = "France",
        department = '',

        overall_departments_data_dc = oddaj["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj["overall_departments_dc_as_json"]['quantiles_dc'],
        
        overall_departments_data_hosp = oddaj["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj["overall_departments_hosp_as_json"]['quantiles_hosp'],
        
        overall_departments_data_rad = oddaj["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj["overall_departments_rad_as_json"]['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = oddaj["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rea = oddaj["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj["overall_departments_rea_as_json"]['quantiles_rea'],

        graphJSONquadratics = graphJSONquadratics,
    )

@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""

    chartreqs = covfr.charts(data=None, department=department)

    label = covfr.department_label(department)
    if label == "":
        label = "France"
        department = ""

    return render_template(
        "graphs.html", 
        graphJSON = chartreqs["graphJSON"], 
        counters = chartreqs["counters"],
        label = label,
        department = department,

        overall_departments_data_dc = oddaj["overall_departments_dc_as_json"]['data_dc'],
        overall_departments_quantiles_dc = oddaj["overall_departments_dc_as_json"]['quantiles_dc'],
        
        overall_departments_data_hosp = oddaj["overall_departments_hosp_as_json"]['data_hosp'],
        overall_departments_quantiles_hosp = oddaj["overall_departments_hosp_as_json"]['quantiles_hosp'],
        
        overall_departments_data_rad = oddaj["overall_departments_rad_as_json"]['data_rad'],
        overall_departments_quantiles_rad = oddaj["overall_departments_rad_as_json"]['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = oddaj["overall_departments_r_dc_rad_as_json"]['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = oddaj["overall_departments_r_dc_rad_as_json"]['quantiles_r_dc_rad'],

        overall_departments_data_rea = oddaj["overall_departments_rea_as_json"]['data_rea'],
        overall_departments_quantiles_rea = oddaj["overall_departments_rea_as_json"]['quantiles_rea'],

        graphJSONquadratics = graphJSONquadratics,
    )

if __name__ == '__main__':
    app.run(debug=True)
