//Plot.ly Javascript plot used to display latest measurements
//Original sounced from "aqi" fork: https://github.com/jtme/aqi

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        PlotGraph(myArr);
    }
};

xmlhttp.open("GET", "aqi.json", true);
xmlhttp.send();



function PlotGraph(data) {
  let trace1 = {
    x: [],
    y: [],
    //mode: "lines"
    type: "scatter"
  };
  let trace2 = {
    x: [],
    y: [],
    //mode: "lines"
    type: "scatter"
  };
    data.forEach(function(val) {
    trace1.x.push(Date.parse(val["time"]));
    trace1.y.push(val["pm25"]);
    trace2.x.push(Date.parse(val["time"]));
    trace2.y.push(val["pm10"]);
    });
  Plotly.newPlot('AQIplot', [trace1, trace2]);
}; 