<script setup>
import { ref, watch, defineExpose, defineProps, toRefs } from 'vue'
import ApexChart from 'vue3-apexcharts'

const chart = ref(null)
defineExpose({ chart })

const props = defineProps({
  wells: {
    type: Array,
    required: true
  }
})

const { wells } = toRefs(props)
const numbers = ref(wells.value.map(well => well.number))

const gwls = ref([])
const rain = ref([])
const avt = ref([])

const tempColor = (val) => {
  if (val > 50) {
    return '#232323'
  } else if (val < 50 && val >= 40) {
    return '#6b1527'
  } else if (val < 40 && val >= 30) {
    return '#be3066'
  } else if (val < 30 && val >= 25) {
    return '#e56d53'
  } else if (val < 25 && val >= 20) {
    return '#eaa43e'
  } else if (val < 20 && val >= 15) {
    return '#ebd735'
  } else if (val < 15 && val >= 10) {
    return '#bee43d'
  } else if (val < 10 && val >= 5) {
    return '#59d049'
  } else if (val < 5 && val >= 0) {
    return '#4bb698'
  } else if (val < 0 && val >= -5) {
    return '#3e79c6'
  } else if (val < -5 && val >= -10) {
    return '#554eb1'
  } else if (val < -10 && val >= -15) {
    return '#24186a'
  } else if (val < -15 && val >= -20) {
    return '#ffaaff'
  } else if (val < -20 && val >= -30) {
    return '#ffaaff'
  } else if (val < -30 && val >= -40) {
    return '#eeeeee'
  }
}

// Chart options for an area chart with a clean, minimal look
const chartOptions = ref({
  chart: {
    height: 300,
    type: 'area',
    toolbar: { 
      show: true,
      offsetY: 30,
    },
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 800,
      animateGradually: { enabled: true, delay: 150 }
    }
  },
  dataLabels: { enabled: false },
  stroke: {
    curve: 'smooth',
    width: 2
  },
  xaxis: {
    categories: numbers.value,
    labels: {
      show: true,
      style: {
        colors: '#333',
        fontSize: '14px',
        fontWeight: '400'
      }
    },
    // axisBorder: { show: false },
    // axisTicks: { show: false }
  },
  yaxis: {
    labels: {
      show: true,
      style: {
        colors: '#333',
        fontSize: '14px',
        fontWeight: '400'
      }
    },
  },
  grid: { show: false },
  tooltip: {
    shared: true,
    theme: 'dark'
  },
  legend: {
    show: true,
    position: 'top',
    horizontalAlign: 'right',
    labels: {
      colors: '#333',
      fontSize: '14px'
    }
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 0.5,
      opacityFrom: 0.3,
      opacityTo: 0.1,
      stops: [0, 90, 100]
    }
  },
  responsive: [
    {
      breakpoint: 1024,
      options: {
        chart: { height: 300 },
        xaxis: { labels: { show: false } }
      }
    },
    {
      breakpoint: 1400,
      options: {
        chart: { height: 300 },
        xaxis: { labels: { show: false } }
      }
    },
    {
      breakpoint: 1930,
      options: {
        chart: { height: 400 },
        xaxis: { labels: { show: false } }
      }
    }
  ]
})

// All series are now rendered as an area chart.
const series = ref([
  {
    name: 'Temperatura (°C)',
    type: 'area',
    data: avt.value,
    color: tempColor(avt.value)
  },
  {
    name: "Yog'ingarchilik (mm)",
    type: 'area',
    data: rain.value,
    color: 'rgba(51, 84, 170, 1)'
  },
  {
    name: 'Yer osti suv sathi (m)',
    type: 'area',
    data: gwls.value,
    color: 'rgb(223, 133, 0)'
  }
])

// Update data when the wells prop changes
watch(
  wells,
  (newWells) => {
    if (newWells && newWells.length > 0) {
      gwls.value = newWells.flatMap(well =>
        well?.parameters?.filter(param => param.parameter_name === 1).map(param => param.value)
      )
      rain.value = newWells.flatMap(well =>
        well?.parameters?.filter(param => param.parameter_name === 2).map(param => param.value)
      )
      avt.value = newWells.flatMap(well =>
        well?.parameters?.filter(param => param.parameter_name === 3).map(param => param.value)
      )
      numbers.value = newWells.map(well => well.number)
      series.value = [
        {
          name: 'Temperatura (°C)',
          type: 'area',
          data: avt.value,
          color: tempColor(avt.value)
        },
        {
          name: "Yog'ingarchilik (mm)",
          type: 'area',
          data: rain.value,
          color: 'rgba(51, 84, 170, 1)'
        },
        {
          name: 'Yer osti suv sathi (m)',
          type: 'area',
          data: gwls.value,
          color: 'rgb(223, 133, 0)'
        }
      ]
      chartOptions.value.xaxis.categories = numbers.value
    }
  },
  { immediate: true }
)
</script>

<template>
  <ApexChart
    ref="chart"
    :options="chartOptions"
    :series="series"
    height="300"
  />
</template>
