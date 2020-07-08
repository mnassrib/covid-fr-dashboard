// calendar for input with name="global_parameters"
$(function() {
    $('input[name="global_parameters"]').daterangepicker({
        "showDropdowns": true,
        "autoApply": true,
        "startDate": "14/05/2020",
        "endDate": "14/06/2020",
        "minDate": {{ first_day|safe }},
        "maxDate": {{ last_day|safe }},
        "showCustomRangeLabel":true,
        autoUpdateInput: true,
        locale: {   format: 'DD/MM/YYYY', 
                    daysOfWeek: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
                    monthNames: ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin',
                        'Juill', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
                    firstDay: 1},
    });
});


// calendar for input with name="hosp_parameters"
$(function() {
    $('input[name="hosp_parameters"]').daterangepicker({
        "showDropdowns": true,
        "autoApply": true,
        "startDate": "14/05/2020",
        "endDate": "14/06/2020",
        "minDate": {{ first_day|safe }},
        "maxDate": {{ last_day|safe }},   
        "showCustomRangeLabel":true,
        autoUpdateInput: true,
        locale: {   format: 'DD/MM/YYYY', 
                    daysOfWeek: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
                    monthNames: ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin',
                        'Juill', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
                    firstDay: 1},
    });
});


//<!-- death map regions-->
$(function() {
    // Init map
    var regions = {{ overall_regions_data_dc|safe }};
    var quantiles = {{ overall_regions_quantiles_dc|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " décès *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " décès *";
        } else {
            slice.label = "Plus de " + slice.min + " décès *";
        }
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id]['dc_par_habitants'];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : <b>" + regions[id]['dc'] + "</b> décès (<b>" + regions[id]['dc_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#";
        if (regions[id]['insee'] === '{{ region }}') {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b",
            };
        }
    }
    $("#death_map_reg").mapael({
        "map": {
            "name": "france_regions_2016_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices,
            }
        },
        "areas": regions
    });
});

//<!-- rate dc map regions -->
$(function() {
    // Init map
    var regions = {{ overall_regions_data_r_dc_rad|safe }};
    var quantiles = {{ overall_regions_quantiles_r_dc_rad|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Taux inférieur à " + quantiles[0], attrs: {fill: '#D6F77F'}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303'] 
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Taux entre " + slice.min + " et " + slice.max;
        } else {
            slice.label = "Taux supérieur à " + slice.min;
        }
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id]['r_dc_rad'];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : <b>" + regions[id]['dc'] + "</b> décès, <b>" + regions[id]['rad'] + "</b> guérisons (Taux régional : <b>" + regions[id]['r_dc_rad'] + "</b>)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#"; 
        if (regions[id]['insee'] === '{{ region }}') {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }      
    $("#rate_death_map_reg").mapael({
        "map": {
            "name": "france_regions_2016_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },  
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": regions
    });
});

//<!-- rad map regions-->
$(function() {
    // Init map
    var regions = {{ overall_regions_data_rad|safe }};
    var quantiles = {{ overall_regions_quantiles_rad|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
        {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " guérisons *", attrs: {fill: "#FEB653"}}
        ];
    colors = ["#FED674", '#F5F50A', '#A4F905', '#06BF06', '#146806']  
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " guérisons *";
        } else {
            slice.label = "Plus de " + slice.min + " guérisons *";
        }
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id]['rad_par_habitants'];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : <b>" + regions[id]['rad'] + "</b> guérisons (<b>" + regions[id]['rad_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#"; 
        if (regions[id]['insee'] === '{{ region }}') {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }   
    $("#rad_map_reg").mapael({
        "map": {
            "name": "france_regions_2016_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },
        
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": regions
    });
});

//<!-- hosp map regions-->
$(function() {
    // Init map
    var regions = {{ overall_regions_data_hosp|safe }};
    var quantiles = {{ overall_regions_quantiles_hosp|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " hospitalisations *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " hospitalisations *";
        } else {
            slice.label = "Plus de " + slice.min + " hospitalisations *";
        }
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id]['hosp_par_habitants'];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : <b>" + regions[id]['hosp'] + "</b> hospitalisations (<b>" + regions[id]['hosp_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#"; 
        if (regions[id]['insee'] === '{{ region }}') {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }        
    $("#hosp_map_reg").mapael({
        "map": {
            "name": "france_regions_2016_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },      
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },          
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": regions
    });
});

//<!-- rea map regions-->
$(function() {
    // Init map
    var regions = {{ overall_regions_data_rea|safe }};
    var quantiles = {{ overall_regions_quantiles_rea|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": quantiles[0] + " réanimations *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " réanimations *";
        } else {
            slice.label = "Plus de " + slice.min + " réanimations *";
        }
        if (i == 0) {
            slice.max = quantiles[i + 1];
            slice.label = "Moins de " + slice.max + " réanimations *";
        }           
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id]['rea_par_habitants'];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : <b>" + regions[id]['rea'] + "</b> réanimations (<b>" + regions[id]['rea_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#"; 
        if (regions[id]['insee'] === '{{ region }}') {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }       
    $("#rea_map_reg").mapael({
        "map": {
            "name": "france_regions_2016_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },                  
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },  
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": regions
    });
});

//<!-- death map departments-->
$(function() {
    // Init map
    var departments = {{ overall_departments_data_dc|safe }};
    var quantiles = {{ overall_departments_quantiles_dc|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " décès *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " décès *";
        } else {
            slice.label = "Plus de " + slice.min + " décès *";
        }
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id]['dc_par_habitants'];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : <b>" + departments[id]['dc'] + "</b> décès (<b>" + departments[id]['dc_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#";
        if (departments[id]['insee'] === '{{ department }}') {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b",
            };
        }
    }
    $("#death_map_dep").mapael({
        "map": {
            "name": "france_departments_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": departments
    });
});

//<!-- rate dc map departments-->
$(function() {
    // Init map
    var departments = {{ overall_departments_data_r_dc_rad|safe }};
    var quantiles = {{ overall_departments_quantiles_r_dc_rad|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Taux inférieur à " + quantiles[0], attrs: {fill: '#D6F77F'}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303'] 
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Taux entre " + slice.min + " et " + slice.max;
        } else {
            slice.label = "Taux supérieur à " + slice.min;
        }
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id]['r_dc_rad'];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : <b>" + departments[id]['dc'] + "</b> décès, <b>" + departments[id]['rad'] + "</b> guérisons (Taux départemental : <b>" + departments[id]['r_dc_rad'] + "</b>)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#"; 
        if (departments[id]['insee'] === '{{ department }}') {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }      
    $("#rate_death_map_dep").mapael({
        "map": {
            "name": "france_departments_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },  
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": departments
    });
});

//<!-- rad map departments -->
$(function() {
    // Init map
    var departments = {{ overall_departments_data_rad|safe }};
    var quantiles = {{ overall_departments_quantiles_rad|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
        {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " guérisons *", attrs: {fill: "#FEB653"}}
        ];
    colors = ["#FED674", '#F5F50A', '#A4F905', '#06BF06', '#146806']  
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " guérisons *";
        } else {
            slice.label = "Plus de " + slice.min + " guérisons *";
        }
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id]['rad_par_habitants'];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : <b>" + departments[id]['rad'] + "</b> guérisons (<b>" + departments[id]['rad_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#"; 
        if (departments[id]['insee'] === '{{ department }}') {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }   
    $("#rad_map_dep").mapael({
        "map": {
            "name": "france_departments_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },
        
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": departments
    });
});
        
//<!-- hosp map departments-->
$(function() {
    // Init map
    var departments = {{ overall_departments_data_hosp|safe }};
    var quantiles = {{ overall_departments_quantiles_hosp|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " hospitalisations *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " hospitalisations *";
        } else {
            slice.label = "Plus de " + slice.min + " hospitalisations *";
        }
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id]['hosp_par_habitants'];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : <b>" + departments[id]['hosp'] + "</b> hospitalisations (<b>" + departments[id]['hosp_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#"; 
        if (departments[id]['insee'] === '{{ department }}') {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }        
    $("#hosp_map_dep").mapael({
        "map": {
            "name": "france_departments_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },      
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },          
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": departments
    });
});
    
//<!-- rea map departments-->
$(function() {
    // Init map
    var departments = {{ overall_departments_data_rea|safe }};
    var quantiles = {{ overall_departments_quantiles_rea|safe }};
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": quantiles[0] + " réanimations *", attrs: {fill: "#D6F77F"}}
        ];
    colors = ["#f2f53a", '#df891a', '#e61919', '#680000', '#1d0303']
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " réanimations *";
        } else {
            slice.label = "Plus de " + slice.min + " réanimations *";
        }
        if (i == 0) {
            slice.max = quantiles[i + 1];
            slice.label = "Moins de " + slice.max + " réanimations *";
        }           
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id]['rea_par_habitants'];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : <b>" + departments[id]['rea'] + "</b> réanimations (<b>" + departments[id]['rea_par_habitants'] + "</b> pour 100 000 habitants)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#"; 
        if (departments[id]['insee'] === '{{ department }}') {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }       
    $("#rea_map_dep").mapael({
        "map": {
            "name": "france_departments_domtom",
            zoom: {
                enabled: true,
                maxLevel: 10
            },                  
            "defaultArea": {
                "attrs": {
                    "fill": "#f4f4e8",
                    "stroke": "#ced8d0",
                },
                "attrsHover": {
                    "fill": "#004a9b",
                },
                "text": {
                    "attrs": {
                        "fill": "#505444"
                    },
                    "attrsHover": {
                        "fill": "#000",
                    }
                }
            }   
        },  
        "legend": {
            "area": {
                "marginBottom": 20,
                "slices": slices
            }
        },
        "areas": departments
    });
});


//<!-- charts -->
// Init charts
var plotlyConfig = {
        "locale": "fr",
        "modeBarButtonsToRemove": ["sendDataToCloud", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "lasso2d", "select2d"],
        "displaylogo": false,
        "showTips": false,
    };
var graphs = {{ graphJSON | safe }};
for(var i in graphs) {
    Plotly.plot(
        graphs[i].id, // the ID of the div, created above
        graphs[i].data,
        graphs[i].layout || {}, 
        plotlyConfig);
}


//<!-- charts pca global-->
var graphs = {{ graphJSONquadratics["graphJSON"] | safe }};
for(var i in graphs) {
    Plotly.plot(
        graphs[i].id, // the ID of the div, created above
        graphs[i].data,
        graphs[i].layout || {}, 
        plotlyConfig);
}

//<!-- charts pca regions-->
var graphs = {{ graphJSONquadratics_reg["graphJSON"] | safe }};
for(var i in graphs) {
    Plotly.plot(
        graphs[i].id + '_reg', // the ID of the div, created above
        graphs[i].data,
        graphs[i].layout || {}, 
        plotlyConfig);
}