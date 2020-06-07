from flask import Flask, render_template, request

from futils.covidfunctions import charts, overall_departments_data_as_json, department_label


app = Flask(__name__)


@app.route('/')
def graphs():
    """Country page of the app"""
    graphJSON, ids, counters = charts(department='ALL')
    #overall_departments_data, overall_departments_quantiles = overall_departments_data_as_json()
    overall_departments_data, overall_departments_quantiles, overall_departments_data_hosp, overall_departments_quantiles_hosp, overall_departments_data_rad, overall_departments_quantiles_rad, overall_departments_data_r_dc_rad, overall_departments_quantiles_r_dc_rad = overall_departments_data_as_json()
    
    return render_template(
        "graphs.html", 
        graphJSON = graphJSON, 
        ids = ids, 
        counters = counters,
        label = "France",
        department = '',
        overall_departments_data = overall_departments_data,
        overall_departments_quantiles = overall_departments_quantiles,
        
        overall_departments_data_hosp = overall_departments_data_hosp,
        overall_departments_quantiles_hosp = overall_departments_quantiles_hosp,
        
        overall_departments_data_rad = overall_departments_data_rad,
        overall_departments_quantiles_rad = overall_departments_quantiles_rad,
        
        overall_departments_data_r_dc_rad = overall_departments_data_r_dc_rad,
        overall_departments_quantiles_r_dc_rad = overall_departments_quantiles_r_dc_rad,
    )


@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""
    graphJSON, ids, counters = charts(department)
    #overall_departments_data, overall_departments_quantiles = overall_departments_data_as_json()
    overall_departments_data, overall_departments_quantiles, overall_departments_data_hosp, overall_departments_quantiles_hosp, overall_departments_data_rad, overall_departments_quantiles_rad, overall_departments_data_r_dc_rad, overall_departments_quantiles_r_dc_rad = overall_departments_data_as_json()

    label = department_label(department)
    if label == "":
        label = "France"
        department = ""

    return render_template(
        "graphs.html", 
        graphJSON = graphJSON, 
        ids = ids, 
        counters = counters,
        label = label,
        department = department,
        overall_departments_data = overall_departments_data,
        overall_departments_quantiles = overall_departments_quantiles,
        
        overall_departments_data_hosp = overall_departments_data_hosp,
        overall_departments_quantiles_hosp = overall_departments_quantiles_hosp,
        
        overall_departments_data_rad = overall_departments_data_rad,
        overall_departments_quantiles_rad = overall_departments_quantiles_rad,
        
        overall_departments_data_r_dc_rad = overall_departments_data_r_dc_rad,
        overall_departments_quantiles_r_dc_rad = overall_departments_quantiles_r_dc_rad,
    )


if __name__ == '__main__':
    app.run(debug=True)
