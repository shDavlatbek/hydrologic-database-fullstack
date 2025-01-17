<template>
  <div class="page-body">
    <div class="container-xl">
      <div class="row">
        <div class="col-8">
          <div class="card mb-4">
            <div class="card-header">
              <h3 class="card-title">Quduqlarning yer osti suvi sathi | Oy bo'yicha</h3>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-12 col-lg-6">
                  <!-- <label class="form-label d-flex">Vaqt bo'yicha <span class="ms-auto">{{ formattedTime }}</span></label> -->
                  <!-- <input type="range" class="form-range mb-2" v-model.number="selectedHour" value="1" min="0" max="23" step="1"> -->
                </div>
                <div class="col-12 col-lg-6 d-flex justify-content-end align-items-center">
                  <h1 class="m-0"><div class="input-icon">
                              <span class="input-icon-addon"><!-- Download SVG icon from http://tabler-icons.io/i/calendar -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12z"></path><path d="M16 3v4"></path><path d="M8 3v4"></path><path d="M4 11h16"></path><path d="M11 15h1"></path><path d="M12 15v3"></path></svg>
                              </span>
                              <input class="form-control" placeholder="Select a date" id="datepicker-icon-prepend" value="2020-06-20">
                            </div></h1>
                </div>
              </div>
            </div>
            <AQIMap :stations="wells" :selected-hour="selectedHour" />
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
import { getWells } from '@/api/geo';
import AQIMap from '@/components/AQIMap.vue';
import Litepicker from '@tabler/core/dist/libs/litepicker/dist/litepicker.js';
export default {
  data() {
    return {
      wells: []
    };
  },
  setup(){
    document.addEventListener("DOMContentLoaded", function () {
      new Litepicker({
        element: document.getElementById('datepicker-icon-prepend'),
        buttonText: {
          previousMonth: `<!-- Download SVG icon from http://tabler-icons.io/i/chevron-left -->
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M15 6l-6 6l6 6" /></svg>`,
          nextMonth: `<!-- Download SVG icon from http://tabler-icons.io/i/chevron-right -->
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 6l6 6l-6 6" /></svg>`,
        },
      });
    });
  },
  components: {
    AQIMap
  },
  async mounted(){
    this.wells = await getWells();
    
    
  
  }
};
</script>
