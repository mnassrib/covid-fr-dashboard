from flask import Flask, render_template, request


from cutils.covidclass import CovidFr


app = Flask(__name__)


@app.route('/')
def graphs():
    """Country page of the app"""
    covfr = CovidFr()
    covfr.load_df()
    covfr.charts(department='ALL')
    
    return render_template(
        "graphs.html", 
        graphJSON = covfr.graphJSON, 
        ids = covfr.ids, 
        counters = covfr.counters,
        label = "France",
        department = '',

        overall_departments_data_dc = covfr.overall_departments_data_as_json("dc")['data_dc'],
        overall_departments_quantiles_dc = covfr.overall_departments_data_as_json("dc")['quantiles_dc'],
        
        overall_departments_data_hosp = covfr.overall_departments_data_as_json("hosp")['data_hosp'],
        overall_departments_quantiles_hosp = covfr.overall_departments_data_as_json("hosp")['quantiles_hosp'],
        
        overall_departments_data_rad = covfr.overall_departments_data_as_json("rad")['data_rad'],
        overall_departments_quantiles_rad = covfr.overall_departments_data_as_json("rad")['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = covfr.overall_departments_data_as_json("r_dc_rad")['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = covfr.overall_departments_data_as_json("r_dc_rad")['quantiles_r_dc_rad'],

        overall_departments_data_rea = covfr.overall_departments_data_as_json("rea")['data_rea'],
        overall_departments_quantiles_rea = covfr.overall_departments_data_as_json("rea")['quantiles_rea'],
    )


@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""

    covfr = CovidFr()
    covfr.load_df()
    covfr.charts(department)

    label = covfr.department_label(department)
    if label == "":
        label = "France"
        department = ""

    return render_template(
        "graphs.html", 
        graphJSON = covfr.graphJSON, 
        ids = covfr.ids, 
        counters = covfr.counters,
        label = label,
        department = department,

        overall_departments_data_dc = covfr.overall_departments_data_as_json("dc")['data_dc'],
        overall_departments_quantiles_dc = covfr.overall_departments_data_as_json("dc")['quantiles_dc'],
        
        overall_departments_data_hosp = covfr.overall_departments_data_as_json("hosp")['data_hosp'],
        overall_departments_quantiles_hosp = covfr.overall_departments_data_as_json("hosp")['quantiles_hosp'],
        
        overall_departments_data_rad = covfr.overall_departments_data_as_json("rad")['data_rad'],
        overall_departments_quantiles_rad = covfr.overall_departments_data_as_json("rad")['quantiles_rad'],
        
        overall_departments_data_r_dc_rad = covfr.overall_departments_data_as_json("r_dc_rad")['data_r_dc_rad'],
        overall_departments_quantiles_r_dc_rad = covfr.overall_departments_data_as_json("r_dc_rad")['quantiles_r_dc_rad'],

        overall_departments_data_rea = covfr.overall_departments_data_as_json("rea")['data_rea'],
        overall_departments_quantiles_rea = covfr.overall_departments_data_as_json("rea")['quantiles_rea'],
    )


if __name__ == '__main__':
    app.run(debug=True)
