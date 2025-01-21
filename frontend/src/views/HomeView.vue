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
                <DatePicker v-model:model-value="selectedDate" :min-date="startDate"  @update:modelValue="updateWells" size="small" placeholder="Oyni tanlash" showIcon iconDisplay="input"
                  view="month" dateFormat="MM yy" />
              </div>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 col-lg-6">
                  <!-- <label class="form-label d-flex">Vaqt bo'yicha <span class="ms-auto">{{ formattedTime }}</span></label> -->
                  <!-- <input type="range" class="form-range mb-2" v-model.number="selectedHour" value="1" min="0" max="23" step="1"> -->
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-end align-items-center">

                </div>
              </div>
            </div>
            <AQIMap :wells="wells" :selected-date="selectedDate" />
          </div>
        </div>
        <div class="col-12 col-lg-4">
          <div class="card mb-4">
            <div class="card-header">
              <h3 class="card-title">Quduqlar bo‘yicha</h3>
            </div>
            <AQITable :stations="wells" :selected-hour="selectedHour" />
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
        <div class="col-12 col-lg-6">
          <div class="card mb-4">
            <div class="card-body pt-5">
              <AQIChart :stations="wells" :selected-hour="selectedHour" />
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="card mb-4">
            <div class="card-body pt-5">
              <PM25Chart :stations="wells" :selected-hour="selectedHour" />
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
export default {
  data() {
    return {
      wells: [],
      selectedDate: null,
      startDate: null,
      endDate: null
    };
  },
  components: {
    AQIMap, DatePicker
  },
  methods: {
    async updateWells(date) {
      this.wells = await getWellsWithParameters(dateWithoutTimezone(date));
    },
    async updateDates() {
      const dates = await getParameterDates();
      this.startDate = dateToISOString(dates.start_date);
      this.endDate = dateToISOString(dates.end_date);
    }
  },
  async mounted() {
    await this.updateDates();
    this.selectedDate = this.endDate;
    this.wells = await getWellsWithParameters(dateWithoutTimezone(this.selectedDate));
  },
};
</script>
