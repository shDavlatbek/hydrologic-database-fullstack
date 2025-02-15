<script setup>
import { onMounted, ref, watch, defineProps, 
  // computed
 } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../assets/js/leaflet-idw.js'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import 'leaflet.markercluster'
import * as maptiler from '@maptiler/leaflet-maptilersdk'
import { useRouter } from 'vue-router'

// Get router instance
const router = useRouter()

const mapContainer = ref(null);
let map;

const props = defineProps({
  wells: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedDate: {
    type: Date,
    required: false,
    default: () => {
      const now = new Date();
      now.setMinutes(0);
      now.setSeconds(0);
      now.setMilliseconds(0);
      return now; // Returns the current hour (0-23)
    }
  },
  viewCoordinates: {
    type: Array,
    required: false,
    default: () => [38.0005, 67.5724]
  },
  viewZoom: {
    type: Number,
    required: false,
    default: () => 8
  }
});

const getColor = (val) => {
  if (val === null || val === undefined) return '#808080'; // серый
  if (val <= 1) return '#E3F2FD'; // светло-голубой
  if (val <= 2) return '#BBDEFB';
  if (val <= 3) return '#90CAF9';
  if (val <= 4) return '#64B5F6';
  if (val <= 5) return '#42A5F5';
  if (val <= 6) return '#2196F3'; // базовый синий
  if (val <= 7) return '#1E88E5';
  if (val <= 8) return '#1976D2';
  if (val <= 9) return '#1565C0';
  return '#0D47A1'; // насыщенно-синий
};

const markers = L.markerClusterGroup();

// const utcRoundedTime = computed(() => {
//   const now = new Date();
//   return new Date(
//     now.getFullYear(),
//     now.getMonth(),
//     now.getDate(),
//     props.selectedDate, // Keep hours
//     0,                 // Set minutes to 0
//     0,                 // Set seconds to 0
//     0                  // Set milliseconds to 0
//   );
// })

// function getCurTimeParameter(parameters) {
//   // Вычисляем текущее округленное время
//   if(typeof parameters !== 'object') return null;
//   const curTime = utcRoundedTime.value; // Если utcRoundedTime - это computed, нужно использовать .value

//   // Ищем параметр с совпадающим временем
//   const curTimeParameter = parameters.find((param) => {
//     const paramTime = new Date(param.datetime);
//     return paramTime.getTime() === curTime.getTime();
//   });

//   return curTimeParameter;
// }

const updateMapView = () => {
  if (map) {
    map.flyTo(props.viewCoordinates, props.viewZoom, {
      duration: 1.5,
    });
  }
}

const updateMarkers = () => {
  
  if (map) {

    markers.clearLayers();
    props.wells.forEach(well => {
      const gwl = well?.parameters?.find(param => param.parameter_name === 1).value
      const markerHtml = `
          <div class="well-marker">
            <span class="well-text" style="background: ${getColor(gwl)}; color: white;">
              ${gwl ? gwl : 
              `<svg  xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-question-mark">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                <path d="M8 8a3.5 3 0 0 1 3.5 -3h1a3.5 3 0 0 1 3.5 3a3 3 0 0 1 -2 3a3 4 0 0 0 -2 4" /><path d="M12 19l0 .01" />
              </svg>`
              }
            </span>
            <svg class="well-icon" xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-map-pin"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M18.364 4.636a9 9 0 0 1 .203 12.519l-.203 .21l-4.243 4.242a3 3 0 0 1 -4.097 .135l-.144 -.135l-4.244 -4.243a9 9 0 0 1 12.728 -12.728zm-6.364 3.364a3 3 0 1 0 0 6a3 3 0 0 0 0 -6z" /></svg>
          </div>
        `;

      const icon = L.divIcon({
        html: markerHtml,
        className: 'custom-div-icon',
        iconSize: [20, 20],
        iconAnchor: [10, 40],
      });

      // Add circle with opacity

      if(well.x && well.y) {
        const marker = L.marker([well.y, well.x], { icon })
          .bindPopup(`
            <strong>${well?.number}</strong><br>
            GWL (m): ${gwl ? gwl : '?'}<br>
            <a href="javascript:void(0)" class="well-link" data-well-number="${well.number}">Batafsil</a>
          `);

        // Add click handler after popup is created
        marker.on('popupopen', () => {
          const link = marker.getPopup().getElement().querySelector('.well-link');
          if (link) {
            link.addEventListener('click', (e) => {
              e.preventDefault();
              router.push({ name: 'GeoSingle', params: { number: link.dataset.wellNumber } });
            });
          }
        });

        markers.addLayer(marker);
      }
    });
    map.addLayer(markers);
  }
};

onMounted(() => {
  if (mapContainer.value) {
    // Initialize map
    map = L.map(mapContainer.value, {
      maxZoom: 20,
      minZoom: 1,
    }).setView(props.viewCoordinates, props.viewZoom);

    // Add OpenStreetMap tiles
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //   attribution: '© OpenStreetMap contributors',
    //   // maxZoom: 10,
    //   // minZoom: 6
    // }).addTo(map);
    new maptiler.maptilerLayer({
      // Get your free API key at https://cloud.maptiler.com
      apiKey: "XcL6b3Sx0AnqO90X2oUF",
    }).addTo(map);
    // Initial marker load
    updateMarkers(); 
  }
});

watch([() => props.wells, () => props.selectedDate], updateMarkers, { deep: true });
watch([() => props.viewCoordinates, () => props.viewZoom], updateMapView, { deep: true });
// watch([() => props.wells], updateInterpolation, { deep: true });
</script>

<template>
  <div class="map-container">
    <div ref="mapContainer" class="map"></div>
    <div class="time-tracker">
      {{ new Date().toLocaleTimeString() }}
    </div>
    <div id="u" title="Change units to “km/h”" class="ws">
      <span class="xo" style="">bft</span>
      <span class="tt" style="background: rgba(153, 25, 81, 0.93); color: rgb(255, 255, 255);">12</span>
      <span class="tt" style="background: rgba(157, 25, 83, 0.93); color: rgb(255, 255, 255);">11</span>
      <span class="tt" style="background: rgba(206, 59, 109, 0.85); color: rgb(255, 255, 255);">10</span>
      <span class="tt" style="background: rgba(233, 131, 70, 0.85); color: rgb(0, 0, 0);">9</span>
      <span class="tt" style="background: rgba(234, 189, 56, 0.85); color: rgb(0, 0, 0);">8</span>
      <span class="tt" style="background: rgba(223, 232, 55, 0.85); color: rgb(0, 0, 0);">7</span>
      <span class="tt" style="background: rgba(141, 217, 72, 0.85); color: rgb(0, 0, 0);">6</span>
      <span class="tt" style="background: rgba(73, 201, 79, 0.85); color: rgb(0, 0, 0);">5</span>
      <span class="tt" style="background: rgba(71, 173, 163, 0.85); color: rgb(255, 255, 255);">4</span>
      <span class="tt" style="background: rgba(59, 130, 198, 0.85); color: rgb(255, 255, 255);">3</span>
      <span class="tt" style="background: rgba(77, 91, 186, 0.85); color: rgb(255, 255, 255);">2</span>
      <span class="tt" style="background: rgba(85, 78, 177, 0.57); color: rgb(255, 255, 255);">1</span>
      <span class="tt" style="background: rgba(83, 72, 148, 0.45); color: rgb(255, 255, 255);">0</span>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 500px;
}

.map {
  width: 100%;
  height: 100%;
}

.time-tracker {
  position: absolute;
  top: 90%;
  right: 1%;
  background: white;
  padding: 5px 10px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

#u {
  position: absolute;
  right: 1em;
  z-index: 1000;
  line-height: 1.5em;
  font-size: 80%;
  bottom: 7.5em;
  display: table-cell;
  background: #777;
  background: linear-gradient(90deg, #555, #999, #555)
}

:deep(.well-marker) {
  /* width: 10px;
  height: 10px; */
  /* border-radius: 50%; */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  

  color: white;
  font-weight: bold;
  /* box-shadow: 0 2px 4px rgba(0,0,0,0.3); */
}

:deep(.well-text) {
  text-shadow: 1px 1px 2px black;
  padding: 2px 5px;
  border-radius: 5px;
}

:deep(.well-icon) {
  -webkit-filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, .7));
  filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, .7));
}

:deep(.custom-div-icon) {
  background: none;
  border: none;
}
</style>
