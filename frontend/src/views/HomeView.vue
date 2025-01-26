<template>
  <div class="page-body">
    <div class="container-xl">
      <div class="row">
        <div class="col-8">
          <div class="card mb-4">
            
            <div class="card-header">
              <h3 class="card-title">
                Quduqlarning yer osti suvi sathi | Oy bo'yicha
              </h3>
              <div class="card-actions">
                <DatePicker v-model:model-value="selectedDate" :min-date="startDate" :max-date="endDate" @update:modelValue="updateWells" size="small" placeholder="Oyni tanlash" showIcon iconDisplay="input"
                  view="month" dateFormat="MM yy" />
              </div>
            </div>
            <!-- <div class="card-body">
              <div class="row">
                <div class="col-12 col-lg-6">
                  <label class="form-label d-flex">Vaqt bo'yicha <span class="ms-auto">{{ formattedTime }}</span></label>
                  <input type="range" class="form-range mb-2" v-model.number="selectedHour" value="1" min="0" max="23" step="1">
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-end align-items-center">

                </div>
              </div>
            </div> -->
            <AQIMap :wells="wells" :selected-date="selectedDate" :view-coordinates="mapView" :view-zoom="mapZoom" />
          </div>
        </div>
        <div class="col-12 col-lg-4">
          <div class="card mb-4">
            <div class="card-header">
              <h3 class="card-title">Quduqlar bo‘yicha</h3>
            </div>
            <DataTable :columns="[
              { key: 'number', label: 'Raqam' },
              { key: 'gwl', label: 'Yer osti suv sathi (m)' },
            ]"
            :data="wellsData"
            :on-row-click="zoomMap"
            :local-text="localText"
            :compact="true"
            ></DataTable>
          </div>

        </div>
        <!-- <div class="col-12 col-lg-8">
          <div class="card mb-4">
            <div class="card-body">
              <div class="badges-list">
                <span class="badge text-white ms-lg-auto" style="background-color: #00e400;">Yaxshi</span>
                <span class="badge text-white" style="background-color: #f7D543;">O‘rtacha</span>
                <span class="badge text-white" style="background-color: #ff7e00;">Nozik guruhlar uchun zararli</span>
                <span class="badge text-white" style="background-color: #E95F5E;">Zararli</span>
                <span class="badge text-white" style="background-color: #9168A1;">Juda zararli</span>
              </div>
            </div>
            
          </div>
        </div> -->
        <div class="col-12">
          <div class="card mb-4">
            <div class="card-body pt-5">
              <HomePageChart :wells="wells" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {  getWellsWithParameters, getParameterDates } from '@/api/geo';
import DatePicker from 'primevue/datepicker';
import AQIMap from '@/components/AQIMap.vue';
import { dateWithoutTimezone, dateToISOString } from '@/helpers';
import DataTable from '@/components/DataTable.vue';
import HomePageChart from '@/components/HomePageChart.vue';
export default {
  data() {
    return {
      wells: [],
      selectedDate: null,
      startDate: null,
      endDate: null,
      mapView: [38.0005, 67.5724],
      mapZoom: 8
    };
  },
  components: {
    AQIMap, DatePicker, DataTable, HomePageChart
  },
  methods: {
    async updateWells(date) {
      this.wells = await getWellsWithParameters(dateWithoutTimezone(date));
    },
    async updateDates() {
      const dates = await getParameterDates();
      this.startDate = dateToISOString(dates.start_date);
      this.endDate = dateToISOString(dates.end_date);
    },
    zoomMap(wellInfo) {
      const well = this.wells.find(w => wellInfo.number === w.number);
      this.mapView = [well.y, well.x];
      this.mapZoom = 15;
    }
  },
  computed: {
    wellsData() {
      return this.wells.map(well => ({
        number: well.number,
        gwl: well.parameters?.find(p => p.parameter_name === 1)?.value ?? '--',
      }));
    },
    localText() {
      return {
        previous: 'Oldingi',
        next: 'Keyingi',
      }
    }
  },
  async mounted() {
    await this.updateDates();
    this.selectedDate = this.endDate;
    this.wells = await getWellsWithParameters(dateWithoutTimezone(this.selectedDate));
  },
};
</script>
