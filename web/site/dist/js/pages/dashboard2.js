'use strict';
$(function () {

  /* ChartJS
   * -------
   * Here we will create a few charts using ChartJS
   */

  //-------------------------
  //- BIWEEKLY PRONTO CHART -
  //-------------------------

  // Get context with jQuery - using jQuery's .get() method.
  var biweeklyChartCanvas = $("#biweeklyChart").get(0).getContext("2d");
  // This will get the first returned node in the jQuery collection.
  // var salesChart = new Chart(salesChartCanvas);

  var biweeklyChartData = {
    labels: ["jan2", "jan4", "feb2", "feb4", "mar2", "mar4",
             "apr2", "apr4", "may2", "may4", "jun2", "jun4",
             "jul2", "jul4", "aug2", "aug4", "sep2", "sep4",
             "oct2", "oct4", "nov2", "nov4", "dec2", "dec4"],

    datasets: [
      {
        label: "A Severity",//#dd4b39 progress-bar-red
        fillColor: "rgba(221, 75, 57, 0.85)",
        strokeColor: "rgb(221, 75, 57)",
        data: [55, 40, 65, 59, 80, 56,
               55, 40, 65, 59, 80, 56,
               55, 40, 65, 59, 80, 56,
               55, 40, 65, 59, 80, 56]
      },
      {
        label: "B Severity",//#f39c12 progress-bar-yellow
        fillColor: "rgba(243, 156, 18, 0.9)",
        strokeColor: "rgb(243, 156, 18)",
        data: [27, 90, 28, 48, 40, 86,
               27, 90, 28, 48, 40, 86,
               27, 90, 28, 48, 40, 86,
               27, 90, 28, 48, 40, 86]
      },
      {
        label: "C Severity",//#00a65a progress-bar-green
        fillColor: "rgba(0, 166, 90, 0.9)",
        strokeColor: "rgb(0, 166, 90)",
        data: [22, 35, 11, 52, 12, 18,
               22, 35, 11, 52, 12, 18,
               22, 35, 11, 52, 12, 18,
               22, 35, 11, 52, 12, 18]
      }        
    ]
  };

  var biweeklyChartOptions = {
    //Boolean - If we should show the scale at all
    showScale: true,
    //Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines: true,
    //String - Colour of the grid lines
    scaleGridLineColor: "rgba(0,0,0,.05)",
    //Number - Width of the grid lines
    scaleGridLineWidth: 1,
    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,
    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: false,
    //Boolean - Whether the line is curved between points
    bezierCurve: true,
    //Number - Tension of the bezier curve between points
    bezierCurveTension: 0.3,
    //Boolean - Whether to show a dot for each point
    pointDot: false,
    //Number - Radius of each point dot in pixels
    pointDotRadius: 4,
    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth: 1,
    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius: 20,
    //Boolean - Whether to show a stroke for datasets
    datasetStroke: true,
    //Number - Pixel width of dataset stroke
    datasetStrokeWidth: 2,
    //Boolean - Whether to fill the dataset with a color
    datasetFill: true,
    //String - A legend template
    //legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>;padding-left: 1.2em;\"></span>&nbsp;<%=datasets[i].label%></li><%}%></ul>",
    //Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
    maintainAspectRatio: false,
    //Boolean - whether to make the chart responsive to window resizing
    responsive: true,

    totalColor: "rgba(0,0,0,0.8)",
    showTotal: true
  };

  //Create the line chart
  //salesChart.StackedBar(salesChartData, salesChartOptions);
  var biweeklyChart = new Chart(biweeklyChartCanvas).StackedBar(biweeklyChartData, biweeklyChartOptions);
  //var legend = salesChart.generateLegend();

  //$("#salesChartLegend").append(legend);

  //-----------------------------
  //- END BIWEEKLY PRONTO CHART -
  //-----------------------------  






  //-----------------------------
  //- PRONTO DISTRIBUTION CHART -
  //-----------------------------

  // Get context with jQuery - using jQuery's .get() method.
  var distributionChartCanvas = $("#distributionChart").get(0).getContext("2d");

  var distributionChartData = {
    labels: ["Ma16.1", "Md16.1 EP1", "M16.2", "MSS15", "MSS17"],

    datasets: [
      {
        label: "A Severity",//#dd4b39 progress-bar-red
        fillColor: "rgba(221, 75, 57, 0.85)",
        strokeColor: "rgb(221, 75, 57)",
        data: [55, 40, 65, 59, 0]
      },
      {
        label: "B Severity",//#f39c12 progress-bar-yellow
        fillColor: "rgba(243, 156, 18, 0.9)",
        strokeColor: "rgb(243, 156, 18)",
        data: [27, 90, 28, 48, 0]
      },
      {
        label: "C Severity",//#00a65a progress-bar-green
        fillColor: "rgba(0, 166, 90, 0.9)",
        strokeColor: "rgb(0, 166, 90)",
        data: [22, 35, 11, 52, 0]
      }        
    ]
  };

  var distributionChartOptions = {
    //Boolean - If we should show the scale at all
    showScale: true,
    //Boolean - Whether grid lines are shown across the chart
    scaleShowGridLines: true,
    //String - Colour of the grid lines
    scaleGridLineColor: "rgba(0,0,0,.05)",
    //Number - Width of the grid lines
    scaleGridLineWidth: 1,
    //Boolean - Whether to show horizontal lines (except X axis)
    scaleShowHorizontalLines: true,
    //Boolean - Whether to show vertical lines (except Y axis)
    scaleShowVerticalLines: false,
    //Boolean - Whether the line is curved between points
    bezierCurve: true,
    //Number - Tension of the bezier curve between points
    bezierCurveTension: 0.3,
    //Boolean - Whether to show a dot for each point
    pointDot: false,
    //Number - Radius of each point dot in pixels
    pointDotRadius: 4,
    //Number - Pixel width of point dot stroke
    pointDotStrokeWidth: 1,
    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    pointHitDetectionRadius: 20,
    //Boolean - Whether to show a stroke for datasets
    datasetStroke: true,
    //Number - Pixel width of dataset stroke
    datasetStrokeWidth: 2,
    //Boolean - Whether to fill the dataset with a color
    datasetFill: true,
    //String - A legend template
    //legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>;padding-left: 1.2em;\"></span>&nbsp;<%=datasets[i].label%></li><%}%></ul>",
    //Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
    maintainAspectRatio: false,
    //Boolean - whether to make the chart responsive to window resizing
    responsive: true,

    totalColor: "rgba(0,0,0,0.8)",
    showTotal: true
  };

  //Create the line chart
  //salesChart.StackedBar(salesChartData, salesChartOptions);
  var distributionChart = new Chart(distributionChartCanvas).StackedBar(distributionChartData, distributionChartOptions);


  //---------------------------------
  //- END PRONTO DISTRIBUTION CHART -
  //---------------------------------





  //-------------
  //- PIE CHART -
  //-------------
  // Get context with jQuery - using jQuery's .get() method.
//   var pieChartCanvas = $("#pieChart").get(0).getContext("2d");
//   var pieChart = new Chart(pieChartCanvas);
//   var PieData = [
//     {
//       value: 700,
//       color: "#f56954",
//       highlight: "#f56954",
//       label: "Chrome"
//     },
//     {
//       value: 500,
//       color: "#00a65a",
//       highlight: "#00a65a",
//       label: "IE"
//     },
//     {
//       value: 400,
//       color: "#f39c12",
//       highlight: "#f39c12",
//       label: "FireFox"
//     },
//     {
//       value: 600,
//       color: "#00c0ef",
//       highlight: "#00c0ef",
//       label: "Safari"
//     },
//     {
//       value: 300,
//       color: "#3c8dbc",
//       highlight: "#3c8dbc",
//       label: "Opera"
//     },
//     {
//       value: 100,
//       color: "#d2d6de",
//       highlight: "#d2d6de",
//       label: "Navigator"
//     }
//   ];
//   var pieOptions = {
//     //Boolean - Whether we should show a stroke on each segment
//     segmentShowStroke: true,
//     //String - The colour of each segment stroke
//     segmentStrokeColor: "#fff",
//     //Number - The width of each segment stroke
//     segmentStrokeWidth: 1,
//     //Number - The percentage of the chart that we cut out of the middle
//     percentageInnerCutout: 50, // This is 0 for Pie charts
//     //Number - Amount of animation steps
//     animationSteps: 100,
//     //String - Animation easing effect
//     animationEasing: "easeOutBounce",
//     //Boolean - Whether we animate the rotation of the Doughnut
//     animateRotate: true,
//     //Boolean - Whether we animate scaling the Doughnut from the centre
//     animateScale: false,
//     //Boolean - whether to make the chart responsive to window resizing
//     responsive: true,
//     // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
//     maintainAspectRatio: false,
//     //String - A legend template
//     legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>",
//     //String - A tooltip template
//     tooltipTemplate: "<%=value %> <%=label%> users"
//   };
//   //Create pie or douhnut chart
//   // You can switch between pie and douhnut using the method below.  
//   pieChart.Doughnut(PieData, pieOptions);
//   //-----------------
//   //- END PIE CHART -
//   //-----------------

//   /* jVector Maps
//    * ------------
//    * Create a world map with markers
//    */
//   $('#world-map-markers').vectorMap({
//     map: 'world_mill_en',
//     normalizeFunction: 'polynomial',
//     hoverOpacity: 0.7,
//     hoverColor: false,
//     backgroundColor: 'transparent',
//     regionStyle: {
//       initial: {
//         fill: 'rgba(210, 214, 222, 1)',
//         "fill-opacity": 1,
//         stroke: 'none',
//         "stroke-width": 0,
//         "stroke-opacity": 1
//       },
//       hover: {
//         "fill-opacity": 0.7,
//         cursor: 'pointer'
//       },
//       selected: {
//         fill: 'yellow'
//       },
//       selectedHover: {
//       }
//     },
//     markerStyle: {
//       initial: {
//         fill: '#00a65a',
//         stroke: '#111'
//       }
//     },
//     markers: [
//       {latLng: [41.90, 12.45], name: 'Vatican City'},
//       {latLng: [43.73, 7.41], name: 'Monaco'},
//       {latLng: [-0.52, 166.93], name: 'Nauru'},
//       {latLng: [-8.51, 179.21], name: 'Tuvalu'},
//       {latLng: [43.93, 12.46], name: 'San Marino'},
//       {latLng: [47.14, 9.52], name: 'Liechtenstein'},
//       {latLng: [7.11, 171.06], name: 'Marshall Islands'},
//       {latLng: [17.3, -62.73], name: 'Saint Kitts and Nevis'},
//       {latLng: [3.2, 73.22], name: 'Maldives'},
//       {latLng: [35.88, 14.5], name: 'Malta'},
//       {latLng: [12.05, -61.75], name: 'Grenada'},
//       {latLng: [13.16, -61.23], name: 'Saint Vincent and the Grenadines'},
//       {latLng: [13.16, -59.55], name: 'Barbados'},
//       {latLng: [17.11, -61.85], name: 'Antigua and Barbuda'},
//       {latLng: [-4.61, 55.45], name: 'Seychelles'},
//       {latLng: [7.35, 134.46], name: 'Palau'},
//       {latLng: [42.5, 1.51], name: 'Andorra'},
//       {latLng: [14.01, -60.98], name: 'Saint Lucia'},
//       {latLng: [6.91, 158.18], name: 'Federated States of Micronesia'},
//       {latLng: [1.3, 103.8], name: 'Singapore'},
//       {latLng: [1.46, 173.03], name: 'Kiribati'},
//       {latLng: [-21.13, -175.2], name: 'Tonga'},
//       {latLng: [15.3, -61.38], name: 'Dominica'},
//       {latLng: [-20.2, 57.5], name: 'Mauritius'},
//       {latLng: [26.02, 50.55], name: 'Bahrain'},
//       {latLng: [0.33, 6.73], name: 'São Tomé and Príncipe'}
//     ]
//   });

//   /* SPARKLINE CHARTS
//    * ----------------
//    * Create a inline charts with spark line
//    */

//   //-----------------
//   //- SPARKLINE BAR -
//   //-----------------
//   $('.sparkbar').each(function () {
//     var $this = $(this);
//     $this.sparkline('html', {
//       type: 'bar',
//       height: $this.data('height') ? $this.data('height') : '30',
//       barColor: $this.data('color')
//     });
//   });

//   //-----------------
//   //- SPARKLINE PIE -
//   //-----------------
//   $('.sparkpie').each(function () {
//     var $this = $(this);
//     $this.sparkline('html', {
//       type: 'pie',
//       height: $this.data('height') ? $this.data('height') : '90',
//       sliceColors: $this.data('color')
//     });
//   });

//   //------------------
//   //- SPARKLINE LINE -
//   //------------------
//   $('.sparkline').each(function () {
//     var $this = $(this);
//     $this.sparkline('html', {
//       type: 'line',
//       height: $this.data('height') ? $this.data('height') : '90',
//       width: '100%',
//       lineColor: $this.data('linecolor'),
//       fillColor: $this.data('fillcolor'),
//       spotColor: $this.data('spotcolor')
//     });
//   });
});