<script setup>
import { onMounted, ref, watch, defineProps, computed } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../assets/js/leaflet-idw.js'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import 'leaflet.markercluster'
import * as maptiler from '@maptiler/leaflet-maptilersdk'

const mapContainer = ref(null);
let map;

const props = defineProps({
  stations: {
    type: Array,
    required: true,
    default: () => []
  },
  selectedHour: {
    type: Number,
    required: false,
    default: () => {
      const now = new Date();
      now.setMinutes(0);
      now.setSeconds(0);
      now.setMilliseconds(0);
      return now.getHours(); // Returns the current hour (0-23)
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

// const getAqiColor = (aqi) => {
//   if (aqi <= 50) return '#00e400';
//   if (aqi <= 100) return '#f7D543';
//   if (aqi <= 150) return '#ff7e00';
//   if (aqi <= 200) return '#E95F5E';
//   if (aqi <= 300) return '#9168A1';

//   return '#9D6878';
// };

const utcRoundedTime = computed(() => {
  const now = new Date();
  return new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    props.selectedHour, // Keep hours
    0,                 // Set minutes to 0
    0,                 // Set seconds to 0
    0                  // Set milliseconds to 0
  );
})

function getCurTimeParameter(parameters) {
  // Вычисляем текущее округленное время
  if(typeof parameters !== 'object') return null;
  const curTime = utcRoundedTime.value; // Если utcRoundedTime - это computed, нужно использовать .value

  // Ищем параметр с совпадающим временем
  const curTimeParameter = parameters.find((param) => {
    const paramTime = new Date(param.datetime);
    return paramTime.getTime() === curTime.getTime();
  });

  return curTimeParameter;
}

const updateMarkers = () => {
  const markers = L.markerClusterGroup();
  if (map) {
    // Clear existing layers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker || layer instanceof L.Circle || layer instanceof L.markerClusterGroup) {
        map.removeLayer(layer);
      }
    });
    // Add station markers and circles
    props.stations.forEach(station => {
      // getAqiColor(station?.parameter[0]?.aqi)
      // station?.parameter[0]?.aqi
      const markerHtml = `
          <div class="station-marker">
            <span class="station-text">${station.number}</span>
            <svg class="station-icon" xmlns="http://www.w3.org/2000/svg"  width="24"  height="24"  viewBox="0 0 24 24"  fill="currentColor"  class="icon icon-tabler icons-tabler-filled icon-tabler-map-pin"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M18.364 4.636a9 9 0 0 1 .203 12.519l-.203 .21l-4.243 4.242a3 3 0 0 1 -4.097 .135l-.144 -.135l-4.244 -4.243a9 9 0 0 1 12.728 -12.728zm-6.364 3.364a3 3 0 1 0 0 6a3 3 0 0 0 0 -6z" /></svg>
          </div>
        `;

      const icon = L.divIcon({
        html: markerHtml,
        className: 'custom-div-icon',
        iconSize: [20, 20],
        iconAnchor: [10, 40],
      });

      // Add circle with opacity


      const marker = L.marker([station.y, station.x], { icon })
        .bindPopup(`
          <strong>${station?.number}</strong><br>
          GWL (m): ${getCurTimeParameter(station?.parameters)?.aqi}
        `)
        // .addTo(map);
        markers.addLayer(marker);


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

watch([() => props.stations, () => props.selectedHour], updateMarkers, { deep: true });
// watch([() => props.stations], updateInterpolation, { deep: true });
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

:deep(.station-marker) {
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

:deep(.station-text) {
  text-shadow: 1px 1px 2px black;
}

:deep(.station-icon) {
  -webkit-filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, .7));
  filter: drop-shadow(3px 3px 2px rgba(0, 0, 0, .7));
}

:deep(.custom-div-icon) {
  background: none;
  border: none;
}
</style>
