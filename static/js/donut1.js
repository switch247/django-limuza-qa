//import ApexCharts from 'apexcharts'
var getChartOptions = () => {
    return {
      series: [35.1, 23.5, 2.4],
      colors: ["#1C64F2", "#16BDCA", "#FDBA8C", "#E74694"],
      chart: {
        height: 200,
        width: "100%",
        type: "donut",
      },
      stroke: {
        colors: ["transparent"],
        lineCap: "",
      },
      plotOptions: {
        pie: {
          startAngle: 0,
          endAngle: 360,
          expandOnClick: true,
          offsetX: 0,
          offsetY: 0,
          customScale: 1,
          dataLabels: {
              offset: 0,
              minAngleToShowLabel: 10
          }, 
          donut: {
            size: '75%',
            background: 'transparent',
            labels: {
              show: true,
              name: {
                show: true,
                fontSize: '22px',
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 600,
                color: undefined,
                offsetY: -10,
                formatter: function (val) {
                  return val
                }
              },
              value: {
                show: true,
                fontSize: '16px',
                fontFamily: 'Helvetica, Arial, sans-serif',
                fontWeight: 400,
                color: undefined,
                offsetY: 16,
                formatter: function (val) {
                  return val
                }
              },
              total: {
                show: true,
                label: 'Total',
                fontSize: '22px',
                fontFamily: "Inter, sans-serif",
                offsetY: -20,
                color: '#373d3f',
                formatter: function (w) {
                  return w.globals.seriesTotals.reduce((a, b) => {
                    return a + b
                  }, 0)
                }
              }
            }
          },      
        }
      } ,
      grid: {
        padding: {
          top: -2,
        },
      },
      labels: ["Good", "Great", "Poor"],
      dataLabels: {
        enabled: false,
      },
      legend: {
        position: "bottom",
        fontFamily: "Inter, sans-serif",
      },
      yaxis: {
        labels: {
          formatter: function (value) {
            return value + "k"
          },
        },
      },
      xaxis: {
        labels: {
          formatter: function (value) {
            return value  + "k"
          },
        },
        axisTicks: {
          show: false,
        },
        axisBorder: {
          show: false,
        },
      },
    }
  }
  
  if (document.getElementById("donut-chart") && typeof ApexCharts !== 'undefined') {
    const chart = new ApexCharts(document.getElementById("donut-chart"), getChartOptions());
    chart.render();
  
    // Get all the checkboxes by their class name
    const checkboxes = document.querySelectorAll('#topfilter input[type="checkbox"]');
  
    // Function to handle the checkbox change event
    function handleCheckboxChange(event, chart) {
        const checkbox = event.target;
        if (checkbox.checked) {
            switch(checkbox.value) {
              case 'Calls':
                chart.updateSeries([15.1, 22.5, 4.4]);
                break;
              case 'Emails':
                chart.updateSeries([25.1, 26.5, 1.4]);
                break;
              case 'Chats':
                chart.updateSeries([45.1, 27.5, 8.4]);
                break;
              default:
                chart.updateSeries([55.1, 28.5, 1.4]);
            }
  
        } else {
            chart.updateSeries([35.1, 23.5, 2.4]);
        }
    }
  
    // Attach the event listener to each checkbox
    checkboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', (event) => handleCheckboxChange(event, chart));
    });
  }
    