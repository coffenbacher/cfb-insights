$.getJSON('/api/data/matrix/', function(data){
    console.log(data);
    var chart = d3.chart.dependencyWheel();
    d3.select('#coaches_wheel')
      .datum(data)
      .call(chart);
});