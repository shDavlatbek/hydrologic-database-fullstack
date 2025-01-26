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
const numbers = ref(wells.value.map(well => well.number));

const gwls = ref([]);
const rain = ref([]);
const avt = ref([]);

const tempColor = (val) => {
  if(val > 50){
    return '#232323'
  }else if(val < 50 && val >= 40){
    return '#6b1527'
  }else if(val < 40 && val >= 30){
    return '#be3066'
  }else if(val < 30 && val >= 25){
    return '#e56d53'
  }else if(val < 25 && val >= 20){
    return '#eaa43e'
  }else if(val < 20 && val >= 15){
    return '#ebd735'
  }else if(val < 15 && val >= 10){
    return '#bee43d'
  }else if(val < 10 && val >= 5){
    return '#59d049'
  }else if(val < 5 && val >= 0){
    return '#4bb698'
  }else if(val < 0 && val >= -5){
    return '#3e79c6'
  }else if(val < -5 && val >= -10){
    return '#554eb1'
  }else if(val < -10 && val >= -15){
    return '#24186a'
  }else if(val < -15 && val >= -20){
    return '#ffaaff'
  }else if(val < -20 && val >= -30){
    return '#ffaaff'
  }else if(val < -30 && val >= -40){
    return '#eeeeee'
  }
}

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
        categories: numbers.value,
        crosshair: true,
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
        // backgroundColor:'transparent',
        style:{
          width:247,
        },
        aligh:'left',
        // padding:0,
        // shadow:false,
        // useHTML:true,
        // formatter: function () {
        //   const list =  this.points.map(item => {
        //     return ` <li>
        //             <div class="circle" style="background-color: ${item.color}"></div>${item.series.name}: <strong style="color:${item.color}">${ item.y}</strong>
        //           </li>`
        //   })
        //   return `<div class="tooltip">
        //           <ul>${list.join('')}</ul>
        //       </div>`;
        // }
      },
      legend: {
        itemStyle:{
          fontSize:14,
          fontFamily:'Golos Text',
          color:'#000'
        },
      },
      series: [{
        name: 'GWL (м)',
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
        data: gwls.value,
        zIndex:12,
      }, {
        name: 'Осадки (мм)',
        type: 'column',
        borderRadius: 5,
        borderWidth: 0,
        maxPointWidth: 20,
        yAxis: 2,
        color:'rgba(51, 84, 170, 1)',
        data: rain.value,
        zIndex:11,
      }, {
        name: 'Температура (°C)',
        yAxis: 0,
        marker:{
          enabled:false
        },
        lineWidth:4,
        zIndex:10,
        type: 'spline',
        zones: [{
          value: -40,
          color: tempColor(-40)
        }, {
          value: -30,
          color: tempColor(-30)
        }, {
          value: -20,
          color: tempColor(-20)
        }, {
          value: -10,
          color: tempColor(-10)
        }, {
          value: -5,
          color: tempColor(-5)
        }, {
          value: 0,
          color: tempColor(0)
        }, {
          value: 5,
          color: tempColor(5)
        }, {
          value: 10,
          color: tempColor(10)
        },  {
          value: 20,
          color: tempColor(20)
        },  {
          value: 30,
          color: tempColor(30)
        },  {
          value: 40,
          color: tempColor(40)
        },  {
          value: 50,
          color: tempColor(50)
        }, {
          color: tempColor(60)
        }],
        color:tempColor(70),
        data: avt.value
      }]
    })
  
}

onMounted(() => {
  // const parameters = ref(wells.value.map(well => well.parameters[0]));
  drawChart()
});


watch(wells, (newWells) => {
  if (newWells && newWells.length > 0) {
    gwls.value = Object.values(newWells.flatMap(well => 
      well?.parameters?.filter(param => param.parameter_name === 1).map(param => param.value)
    ));
    rain.value = Object.values(newWells.flatMap(well => 
      well?.parameters?.filter(param => param.parameter_name === 2).map(param => param.value)
    ));
    avt.value = Object.values(newWells.flatMap(well => 
      well?.parameters?.filter(param => param.parameter_name === 3).map(param => param.value)
    ));
    numbers.value = newWells.map(well => well.number)
    console.log('Filtered Parameters:', gwls.value);
    drawChart()
  }
}, { immediate: true });

</script>

<template>
  <div id="home-page-chart"></div>
</template>

