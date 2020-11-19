
function plotGraphs(graphjson, text) {
	// Init charts
	var plotlyConfig = {
		"locale": "fr",
		"modeBarButtonsToRemove": ["sendDataToCloud", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "lasso2d", "select2d"],
		"displaylogo": false,
		"showTips": false,
	};
	var graphs = graphjson;  
  var gp = [];
  for(var i in graphs) {
      gp[i] = Plotly.newPlot(
          graphs[i].id + text, // the ID of the div, created above
          graphs[i].data,
          graphs[i].layout || {}, 
          plotlyConfig,
      );
  };
  return gp;
}
///////////////////////
function plotDepMap(mapDiv, departments, quantiles, current_label, text, feature_name, feature_par_habitants, colors, fill_slices) {
    // Init map 
    var departments = departments; 
    var quantiles = quantiles; 
    quantiles = Object.values(quantiles);
    var slices = [
        {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " " + text + " *", attrs: {fill: fill_slices}}
    ];
    colors = colors;
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " " + text + " *";
        } else {
            slice.label = "Plus de " + slice.min + " " + text + " *";
        }
        slices.push(slice);
    }
    for (var id in departments) {
        departments[id]['value'] = departments[id][feature_par_habitants];
        departments[id]['tooltip'] = {
            "content": departments[id]['label'] + " : " + "<b>" + departments[id][feature_name] + "</b>" + " " + text + " (" + "<b>" + departments[id][feature_par_habitants] + "</b>" + " pour 100 000 habitants)"
        };
        departments[id]['href'] = "/departement/" + departments[id]['insee'] + "#"; 
        if (departments[id]['insee'] === current_label) {
            departments[id]['href'] = "/";
            delete departments[id]['value'];
            departments[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }       
    return $(mapDiv).mapael({
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
};
///////////////////////  
function plotRegMap(mapDiv, regions, quantiles, current_label, text, feature_name, feature_par_habitants, colors, fill_slices) {
    // Init map
    var regions = regions; 
    var quantiles = quantiles; 
    quantiles = Object.values(quantiles);
    var slices = [
            {"max": quantiles[0], "label": "Moins de " + quantiles[0] + " " + text + " *", attrs: {fill: fill_slices}}
        ];
    colors = colors;
    for (var i = 0; i < quantiles.length; i++) {
        var slice = {
                attrs: {
                    fill: colors[i]
                }
            };
        slice.min = quantiles[i];
        if (i < quantiles.length -1) {
            slice.max = quantiles[i + 1];
            slice.label = "Entre " + slice.min + " et " + slice.max + " " + text + " *";
        } else {
            slice.label = "Plus de " + slice.min + " " + text + " *";
        }
        slices.push(slice);
    }
    for (var id in regions) {
        regions[id]['value'] = regions[id][feature_par_habitants];
        regions[id]['tooltip'] = {
            "content": regions[id]['label'] + " : " + "<b>" + regions[id][feature_name] + "</b>" + " " + text + " (" + "<b>" + regions[id][feature_par_habitants] + "</b>" + " pour 100 000 habitants)"
        };
        regions[id]['href'] = "/region/" + regions[id]['insee'] + "#"; 
        if (regions[id]['insee'] === current_label) {
            regions[id]['href'] = "/";
            delete regions[id]['value'];
            regions[id]['attrs'] = {
                "fill": "#004a9b", 
            };
        }
    }       
    return $(mapDiv).mapael({
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
};

///////////////////////////////////////////////////////////////////////
// function changeCouleur(nouvelleCouleur) {
//   document.getElementById("paragraphe").style.color = nouvelleCouleur;
// }
// function drawLines(myDiv) {
//   var trace1 = {
//       x: [1, 2, 3, 4],
//       y: [10, 15, 13, 17],
//       type: 'scatter'
//   };
//   var trace2 = {
//       x: [1, 2, 3, 4],
//       y: [16, 5, 11, 9],
//       type: 'scatter'
//   };
//   var data = [trace1, trace2];
//   return Plotly.newPlot(document.getElementById(myDiv), data);
// }
// function drawplots(data) {
//   // Init charts
// 	var plotlyConfig = {
// 		"locale": "fr",
// 		"modeBarButtonsToRemove": ["sendDataToCloud", "autoScale2d", "hoverClosestCartesian", "hoverCompareCartesian", "lasso2d", "select2d"],
// 		"displaylogo": false,
// 		"showTips": false,
//   };
//   var data = data;
//   return Plotly.plot("testplot", data, plotlyConfig);
// }
// function hosp_parameters_calendar(startDate, endDate, minDate, maxDate) {

//     return $('input[name="hosp_parameters"]').daterangepicker({
//         "showDropdowns": true,
//         "autoApply": true,
//         "startDate": startDate,
//         "endDate": endDate,
//         "minDate": minDate,
//         "maxDate": maxDate,
//         "showCustomRangeLabel": true,
//         "autoUpdateInput": true,
//         locale: {   
//             format: 'DD/MM/YYYY', 
//             daysOfWeek: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
//             monthNames: ['Janv', 'Févr', 'Mars', 'Avr', 'Mai', 'Juin',
//                         'Juill', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
//             firstDay: 1
//         },
//     });
// };

{/* <script type="text/javascript">
var trace1 = {
    x: [1, 2, 3, 4],
    y: [10, 15, 13, 17],
    type: 'scatter'
};
var trace2 = {
    x: [1, 2, 3, 4],
    y: [16, 5, 11, 9],
    type: 'scatter'
};

drawplots([trace1, trace2]);
</script>

<script>
drawLines('myDiv2');
</script> */}


{/* <p id="paragraphe">Un peu de texte</p>
<button onclick="changeCouleur('blue');">blue</button>
<button onclick="changeCouleur('red');">red</button>

<h3>div1 (drawLines() function)</h3> 
<div id="myDiv2"> </div>

<h3>div2 (drawplots() function)</h3>
<div id="testplot"></div> */}