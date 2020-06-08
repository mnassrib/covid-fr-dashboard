from flask import Flask, render_template, request

from importlib import reload
import futils.covidfunctions
reload(futils.covidfunctions)

from futils.covidfunctions import charts, overall_departments_data_as_json, department_label


app = Flask(__name__)


@app.route('/')
def graphs():
    """Country page of the app"""
    graphJSON, ids, counters = charts(department='ALL')
    overall_departments_data_dc, overall_departments_quantiles_dc, overall_departments_data_rad, overall_departments_quantiles_rad, overall_departments_data_r_dc_rad, overall_departments_quantiles_r_dc_rad, overall_departments_data_hosp, overall_departments_quantiles_hosp, overall_departments_data_rea, overall_departments_quantiles_rea = overall_departments_data_as_json()
    
    return render_template(
        "graphs.html", 
        graphJSON = graphJSON, 
        ids = ids, 
        counters = counters,
        label = "France",
        department = '',

        overall_departments_data_dc = overall_departments_data_dc,
        overall_departments_quantiles_dc = overall_departments_quantiles_dc,
        
        overall_departments_data_hosp = overall_departments_data_hosp,
        overall_departments_quantiles_hosp = overall_departments_quantiles_hosp,
        
        overall_departments_data_rad = overall_departments_data_rad,
        overall_departments_quantiles_rad = overall_departments_quantiles_rad,
        
        overall_departments_data_r_dc_rad = overall_departments_data_r_dc_rad,
        overall_departments_quantiles_r_dc_rad = overall_departments_quantiles_r_dc_rad,

        overall_departments_data_rea = overall_departments_data_rea,
        overall_departments_quantiles_rea = overall_departments_quantiles_rea,
    )


@app.route('/departement/<string:department>')
def view_department(department):
    """Department page of the app"""
    graphJSON, ids, counters = charts(department)
    overall_departments_data_dc, overall_departments_quantiles_dc, overall_departments_data_rad, overall_departments_quantiles_rad, overall_departments_data_r_dc_rad, overall_departments_quantiles_r_dc_rad, overall_departments_data_hosp, overall_departments_quantiles_hosp, overall_departments_data_rea, overall_departments_quantiles_rea = overall_departments_data_as_json()

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

        overall_departments_data_dc = overall_departments_data_dc,
        overall_departments_quantiles_dc = overall_departments_quantiles_dc,
        
        overall_departments_data_hosp = overall_departments_data_hosp,
        overall_departments_quantiles_hosp = overall_departments_quantiles_hosp,
        
        overall_departments_data_rad = overall_departments_data_rad,
        overall_departments_quantiles_rad = overall_departments_quantiles_rad,
        
        overall_departments_data_r_dc_rad = overall_departments_data_r_dc_rad,
        overall_departments_quantiles_r_dc_rad = overall_departments_quantiles_r_dc_rad,

        overall_departments_data_rea = overall_departments_data_rea,
        overall_departments_quantiles_rea = overall_departments_quantiles_rea,
    )


if __name__ == '__main__':
    app.run(debug=True)
