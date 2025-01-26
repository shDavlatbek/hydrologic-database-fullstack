<script setup>
import { ref, onMounted, defineExpose, defineProps, toRefs, watch } from 'vue';
import Highcharts from 'highcharts';

const chart = ref(null);

defineExpose({
  chart
})

const props = defineProps({
  wells: {
    type: Array,
    required: true
  }
});

const { wells } = toRefs(props);
const dates = ref(wells.value.map(well => 
    well.parameters.map(parameter => parameter.date)
  ));

const gwls = ref([]);

const drawChart = () => {
  chart.value = Highcharts.chart('home-page-chart', {
      chart:{
        height:300,
        className:'additional'
      },
      lang: {
        locale: 'en',
      },
      title: {
        text: '',
      },
      subtitle: {
        text: '',
      },
      credits: {
        enabled: false
      },
      responsive: {
        rules: [
          {
            condition: {
              maxWidth: 1024
            },
            chartOptions: {

              xAxis:{
                labels: {
                  style:{
                    fontWeight: 400,
                    fontSize:14,
                  },
                },
              },
              legend:{
                itemWidth: 140,
                align: 'center',
                itemStyle:{
                  fontSize:14,
                },
              }
            }
          },
          {
            condition: {
              maxWidth: 1400
            },
            chartOptions: {

              xAxis:{
                labels: {
                  style:{
                    fontWeight: 400,
                    fontSize:14,
                  },
                },
              },
              legend:{
                align: 'center',
                itemStyle:{
                  fontSize:14,
                },
              }
            }
          },
          {
            condition: {
              minWidth: 1930
            },
            chartOptions: {

              chart:{
                height:400
              },
              xAxis:{
                labels: {
                  style:{
                    fontWeight: 400,
                    fontSize:14,
                  },
                },
              },
              legend:{
                align: 'center',
                itemStyle:{
                  fontSize:14,
                },
              }
            }
          },
        ]
      },
      xAxis: {
        lineColor:'#BDC1D4',
        startOnTick:true,
        categories: dates.value,
        crosshair: true,
        type: 'datetime',
        dateTimeLabelFormats: {
            day: '%Y'
        }
      },
      yAxis: [
        {
          title: {
            text: 'Temperature (°C)',
            style: {
              color: '#000'
            }
          },
          opposite: true,
          visible: false,  // Do not display this axis
          labels: {
            style: {
              color: '#000'
            }
          }
        },
        {
          title: {
            text: 'Wind Speed (m/s)',
            style: {
              color: '#000'
            }
          },
          opposite: false,
          visible: false,
          labels: {
            style: {
              color: '#000'
            }
          }
        },
        {
          title: {
            text: 'CO2 (PPM)',
            style: {
              color: '#000'
            }
          },
          opposite: true,
          visible: false,  // Do not display this axis
          labels: {
            style: {
              color: '#000'
            }
          }
        },
        {
          title: {
            text: 'Precipitation (mm)',
            style: {
              color: '#000'
            }
          },
          opposite: false,
          visible: false,  // Do not display this axis
          labels: {
            style: {
              color: '#000'
            }
          }
        },
        {
          title: {
            text: 'Humidity (%)',
            style: {
              color: '#000'
            }
          },
          opposite: true,
          visible: false,  // Do not display this axis
        },
        {
          title: {
            text: '',
            style: {
              fontSize:14,
              fontFamily:'Golos Text',
              color:'rgba(102, 111, 118, 1)'
            }
          },
          opposite: false,
          labels: {
            style: {
              fontSize:14,
              fontFamily:'Golos Text',
              color:'rgba(102, 111, 118, 1)'
            }
          },
          gridLineDashStyle: 'dashed',
          gridLineWidth: 1, // Set the desired grid line width
          gridLineColor: 'rgb(230, 230, 230)' // Set the desired grid line color and opacity
        },
        {
          title: {
            text: 'PM2.5',
          },
          opposite: true,
          visible: false,  // Do not display this axis
        },

        {
          title: {
            text: 'PM1.0',
          },
          opposite: true,
          visible: false,  // Do not display this axis
        },
        {
          title: {
            text: 'Давление',
          },
          opposite: true,
          visible: false,  // Do not display this axis

        },
        {
          title: {
            text: 'CO2',
          },
          opposite: true,
          visible: false,  // Do not display this axis
        },
        {
          title: {
            text: 'UV index',
          },
          opposite: true,
          visible: false,  // Do not display this axis
        },

      ],
      tooltip: {
        shared: true,
        enabled:true,
        borderWidth:0,
        backgroundColor:'transparent',
        style:{
          width:247,
        },
        aligh:'left',
        padding:0,
        shadow:false,
        useHTML:true,
        formatter: function () {
          const list =  this.points.map(item => {
            return ` <li>
                    <div class="circle" style="background-color: ${item.color}"></div>${item.series.name}: <strong style="color:${item.color}">${ item.y}</strong>
                  </li>`
          })
          return `<div class="tooltip">
                  <ul>${list.join('')}</ul>
              </div>`;
        }
      },
      legend: {
        itemStyle:{
          fontSize:14,
          fontFamily:'Golos Text',
          color:'#000'
        },
      },
      series: [{
        name: 'AQI',
        type: 'spline',
        marker:{
          enabled:false
        },
        color:'rgb(223, 133, 0)',
        zones: [{
          value: 50,
          color: 'rgba(159, 211, 92, 1)'
        }, {
          value: 100,
          color: 'rgba(247, 213, 67, 1)'
        }, {
          value: 150,
          color: 'rgba(236, 142, 79, 1)'
        }, {
          value: 201,
          color: 'rgba(233, 95, 94, 1)'
        }, {
          value: 300,
          color: 'rgba(145, 104, 161, 1)'
        }, {
          color: 'rgba(157, 104, 120, 1)'
        }],
        lineWidth:8,
        yAxis: 5,
        data: gwls.value
      },{
        name: 'Влажность (%)',
        type: 'spline',
        colorKey: null,
        lineWidth:4,
        yAxis: 4,
        color:'rgba(0, 192, 255, 1)',
        data: gwls.value
      }, {
        name: 'Осадки (мм)',
        type: 'column',
        borderRadius: 5,
        borderWidth: 0,
        maxPointWidth: 20,
        yAxis: 2,
        color:'rgba(51, 84, 170, 1)',
        data: gwls.value
      }, {
        name: 'Температура (°C)',
        visible: false,
        yAxis: 0,
        marker:{
          enabled:false
        },
        lineWidth:4,
        type: 'spline',
        zones: [{
          value: -40,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: -30,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: -20,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: -10,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: -5,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: 0,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: 5,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          value: 10,
          color: 'rgba(53, 161, 255, 1)'
        },  {
          value: 20,
          color: 'rgba(53, 161, 255, 1)'
        },  {
          value: 30,
          color: 'rgba(53, 161, 255, 1)'
        },  {
          value: 40,
          color: 'rgba(53, 161, 255, 1)'
        },  {
          value: 50,
          color: 'rgba(53, 161, 255, 1)'
        }, {
          color: 'rgba(53, 161, 255, 1)'
        }],
        color:'rgba(53, 161, 255, 1)',
        data: gwls.value
      }, {
        name: 'Скорость ветра (м/с)',
        type: 'spline',
        visible: false,
        yAxis: 1,
        color:'rgba(40, 40, 40, 1)',
        data: gwls.value

      }, {
        name: 'Давление (кПа)',
        color:'rgba(189, 0, 255, 1)',
        type: 'spline',
        visible: false,
        yAxis: 7,
        data: gwls.value
      }, {
        name: 'CO2 (ppm)',
        type: 'spline',
        yAxis: 8,
        visible: false,
        color:'rgba(0, 223, 156, 1)',
        data: gwls.value
      },  {
        name: 'PM2.5 (мкг/м³)',
        type: 'spline',
        yAxis: 6,
        visible: false,
        color:'rgba(236, 142, 79, 1)',
        data: gwls.value
      }, {
        name: 'PM10 (мкг/м³)',
        color:'rgba(233, 95, 94, 1)',
        type: 'spline',
        yAxis: 6,
        visible: false,
        data: gwls.value
      }, {
        name: 'PM1.0 (мкг/м³)',
        type: 'spline',
        yAxis: 6,
        visible: false,
        color:'rgba(243, 200, 47, 1)',
        data: gwls.value
      },{
        name: 'UV индекс',
        type: 'spline',
        yAxis: 6,
        visible: false,
        color:'rgb(243,158,55)',
        data: gwls.value
      },]
    })
  
}

onMounted(() => {
  // const parameters = ref(wells.value.map(well => well.parameters[0]));
  drawChart()
});


watch(wells, (newWells) => {
  if (newWells && newWells.length > 0) {
    gwls.value = Object.values(newWells.flatMap(well => 
      well.parameters.filter(param => param.parameter_name === 1).map(param => param.value)
    ));
    dates.value = Object.values(newWells.flatMap(well => 
      well.parameters.filter(param => param.parameter_name === 1).map(param => param.date)
    ));
    console.log('Filtered Parameters:', gwls.value);
    drawChart()
  }
}, { immediate: true });

</script>

<template>
  <div id="home-page-chart"></div>
</template>

