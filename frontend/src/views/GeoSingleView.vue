<template>
  <div class="page-body" v-if="well">
    <div class="container-xl">
      <div class="card mb-4">
        <form @submit.prevent="wellEditSubmit">
          <div class="card-header">
            <h3 class="card-title">Quduq ma'lumotlari</h3>
            <div class="card-actions">
              <button class="btn btn-sm btn-primary rounded-2 px-2 py-1" href="#" v-if="!editMode" @click="editMode = true">
                <IconPencil class="icon" stroke="2" />
                Tahrirlash
              </button>
            </div>
          </div>
          <div class="card-body">
              <div class="datagrid">
                <div class="datagrid-item">
                  <div class="datagrid-title">
                    <span :class="{'required': editMode}">Quduq raqami</span>
                  </div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <input type="text" required class="form-control form-control-sm" v-model="wellForm.number" />
                    </template>
                    <template v-else>{{ well?.number ? well?.number : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Stansiya nomi</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <select class="form-select form-select-sm" v-model="wellForm.station">
                        <option value="-1">---------</option>
                        <option v-for="one in stations" :key="one.id" :value="one.id">{{ one.name }}</option>
                      </select>
                    </template>
                    <template v-else>{{ well?.station ? well?.station?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Viloyat</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <select class="form-select form-select-sm" v-model="wellForm.region" @change="changeDistricts">
                        <option value="-1">---------</option>
                        <option v-for="one in regions" :key="one.id" :value="one.id">{{ one.name }}</option>
                      </select>
                    </template>
                    <template v-else>{{ well?.region ? well?.region?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Tuman</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <select class="form-select form-select-sm" v-model="wellForm.district">
                        <option value="-1">---------</option>
                        <option v-for="one in districts" :key="one.id" :value="one.id">{{ one.name }}</option>
                      </select>
                    </template>
                    <template v-else>{{ well?.district ? well?.district?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Joylashuv o'rni</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <select class="form-select form-select-sm" v-model="wellForm.location">
                        <option value="-1">---------</option>
                        <option v-for="one in locations" :key="one.id" :value="one.id">{{ one.name }}</option>
                      </select>
                    </template>
                    <template v-else>{{ well?.location ? well?.location?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Quduq turi</div>
                  <template v-if="editMode">
                    <select class="form-select form-select-sm" v-model="wellForm.well_type">
                      <option value="-1">---------</option>
                      <option v-for="one in wellTypes" :key="one.id" :value="one.id">{{ one.name }}</option>
                    </select>
                  </template>
                  <template v-else>{{ well?.well_type ? well?.well_type?.name : noInfoMes }}</template>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Mo'ljal</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <input type="text" class="form-control form-control-sm" v-model="wellForm.address" />
                    </template>
                    <template v-else>{{ well?.address?.name ? well?.address?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Tashkilot</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <select class="form-select form-select-sm" v-model="wellForm.organization">
                        <option value="-1">---------</option>
                        <option v-for="one in organizations" :key="one.id" :value="one.id">{{ one.name }}</option>
                      </select>
                    </template>
                    <template v-else>{{ well?.organization ?  well?.organization?.name : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">[X, Y]</div>
                  <div class="datagrid-content">
                    <template v-if="editMode">
                      <div class="row">
                        <div class="col-6">
                        <input type="text" class="form-control form-control-sm" v-model="wellForm.x" />
                      </div>
                      <div class="col-6">
                        <input type="text" class="form-control form-control-sm" v-model="wellForm.y" />
                      </div>
                      </div>
                    </template>
                    <template v-else>{{ well?.x ? well?.x : noInfoMes }}, {{ well?.y ? well?.y : noInfoMes }}</template>
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Qo'shilgan vaqti</div>
                  <div class="datagrid-content">{{ well?.created_at ? format(new Date(well?.created_at), 'dd.MM.yyyy HH:mm:ss') : noInfoMes }}</div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">O'zgartirilgan vaqti</div>
                  <div class="datagrid-content">{{ well?.updated_at ? format(new Date(well?.updated_at), 'dd.MM.yyyy HH:mm:ss') : noInfoMes }}</div>
                </div>
              </div>
          </div>
          <div class="card-footer d-flex" v-if="editMode">
            <button class="btn btn-sm btn-danger rounded-2 me-2 ms-auto px-2 py-1" @click="editMode = false; setWellForm(well)">
              <IconX class="icon" stroke="2" />
              Bekor qilish
            </button>
            <button class="btn btn-sm btn-success rounded-2 px-2 py-1" type="submit">
              <IconCheck class="icon" stroke="2" />
              Saqlash
            </button>
          </div>
        </form>
      </div>
      <div class="row row-cards">
        <!-- GRAPHS -->
        <div class="col-12 col-md-6">
          <div class="card">
            <div class="card-body">
              <div class="d-flex">
                <h3 class="card-title">Yer osti suvi sathi</h3>
                <!-- <div class="ms-auto">
                  <div class="dropdown">
                    <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Last 7 days</a>
                    <div class="dropdown-menu dropdown-menu-end">
                      <a class="dropdown-item active" href="#">Last 7 days</a>
                      <a class="dropdown-item" href="#">Last 30 days</a>
                      <a class="dropdown-item" href="#">Last 3 months</a>
                    </div>
                  </div>
                </div> -->
              </div>
              <apexchart height="350" type="area" 
                :options="gwlChartOptions" 
                :series="gwlChartSeries"
              ></apexchart>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-6">
          <div class="card">
            <div class="card-body">
              <div class="d-flex">
                <h3 class="card-title">Bashorat</h3>
                <!-- <div class="ms-auto">
                  <div class="dropdown">
                    <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Last 7 days</a>
                    <div class="dropdown-menu dropdown-menu-end">
                      <a class="dropdown-item active" href="#">Last 7 days</a>
                      <a class="dropdown-item" href="#">Last 30 days</a>
                      <a class="dropdown-item" href="#">Last 3 months</a>
                    </div>
                  </div>
                </div> -->
              </div>
              <apexchart height="350" type="area" 
                :options="gwlChartForecastOptions" 
                :series="gwlChartSeriesForecast"
              ></apexchart>
            </div>
          </div>
        </div>
        
        <!-- PARAMETERS -->
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Parameterlar</h3>
              <div class="ms-auto">
                <button class="btn btn-primary d-none d-sm-inline-block" data-bs-toggle="modal"
                  :data-bs-target="'#'+addParameterModalId"
                  @click="onModalOpen">
                  <IconPlus class="icon" stroke="2" />
                  Qo'shish
                </button>
                <button class="btn btn-primary d-sm-none btn-icon" data-bs-toggle="modal" 
                  :data-bs-target="'#'+addParameterModalId"
                  aria-label="Qo'shish"
                  @click="onModalOpen">
                  <IconPlus class="icon" stroke="2" />
                </button>
              </div>
            </div>
          </div>
          <DataTable :data="params" :columns="param_names" />
        </div>
        
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Mann Kendall</h3>
              <div class="ms-auto d-flex align-items-center gap-2">
                
                
                <DatePicker v-model:model-value="calculationStartDate" :min-date="paramStartDate" :max-date="paramEndDate" size="small" placeholder="Oyni tanlash" showIcon iconDisplay="input"
                  view="month" dateFormat="MM yy" />
                  —
                <DatePicker v-model:model-value="calculationEndDate" :min-date="paramStartDate" :max-date="paramEndDate" size="small" placeholder="Oyni tanlash" showIcon iconDisplay="input"
                  view="month" dateFormat="MM yy" />
                <button class="btn btn-primary d-none d-sm-inline-block" 
                  aria-label="Hisoblash"
                  @click="calculateUpdate">
                  <IconCalculator class="icon" stroke="2" />
                  Hisoblash
                </button>
                <button class="btn btn-primary d-sm-none btn-icon" 
                  aria-label="Hisoblash"
                  @click="calculateUpdate">
                  <IconCalculator class="icon" stroke="2" />
                </button>
              </div>
            </div>
            <div class="row">
              <div class="col-6 border-end">
                <apexchart
              height="350"
              :options="yearlyAvgOptions"
              :series="yearlyAvgSeries"
            ></apexchart>

            <!-- Amplitude Chart -->
            
              </div>
              <div class="col-6">
                <apexchart
              height="350"
              :options="amplitudeOptions"
              :series="amplitudeSeries"
            ></apexchart>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <div class="card">
                  <div class="card-body">
                    <h3 class="card-title">Heatmap</h3>
                    <div class="d-flex w-100 justify-content-center">
                      <img :src="heatmapImage" alt="Heatmap" class="img-fluid" style="max-height: 500px;">
                    </div>
                    <div class="d-flex w-100 justify-content-end">
                      <a :href="heatmapImage" download="heatmap.png">
                        <button class="btn btn-primary">Yuklash</button>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-header">
              <h3 class="card-title">Butun davr uchun hisobot</h3>
            </div>
            <div class="card-body my-3">
              <!-- all_time_avg
: 
3.41
all_time_cv
: 
"3.03%"
all_time_max
: 
6.15
all_time_min
: 
1.64
all_time_std_dev
: 
0.1
all_time_variance
: 
0.03 -->
              <div class="datagrid">
                <div class="datagrid-item">
                  <div class="datagrid-title">
                    <span>Maximum sathi</span>
                  </div>
                  <div class="datagrid-content">
                    {{ calculations?.all_time_max ? calculations?.all_time_max : noInfoMes }}
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">
                    <span>Minimum sathi</span>
                  </div>
                  <div class="datagrid-content">
                    {{ calculations?.all_time_min ? calculations?.all_time_min : noInfoMes }}
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">O'rtacha Dispersiya</div>
                  <div class="datagrid-content">
                    {{ calculations?.all_time_std_dev ? calculations?.all_time_std_dev : noInfoMes }}
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">O'zgarish koeffitsienti</div>
                  <div class="datagrid-content">
                    {{ calculations?.all_time_variance ? calculations?.all_time_variance : noInfoMes }}
                  </div>
                </div>
                <div class="datagrid-item">
                  <div class="datagrid-title">Standart og'ish</div>
                  <div class="datagrid-content">
                    {{ calculations?.all_time_cv ? calculations?.all_time_cv : noInfoMes }}
                  </div>
                </div>
              </div>
            </div>
            <div class="table-responsive">
              <table class="table card-table table-vcenter text-nowrap datatable">
                <!-- Sticky Header -->
                <thead class="sticky-top">
                  <tr>
                    <th v-for="stat in [{year: 'Oy'},...mannKendall]" :key="stat.year">
                      {{ stat.year }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="month in months" :key="month.key">
                    <td>{{ month.name }}</td>
                    <!-- Loop through each mannKendall statistic to display the value for that month -->
                    <td v-for="stat in mannKendall" :key="stat.year">
                      {{ stat[month.key] }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
          </div>
        </div>
      </div>
    </div>
    
  </div>

  <teleport to="body">
    <ModalForm 
      :modal-id="addParameterModalId" scrollable 
      modal-title="Parameterlar qo'shish" 
      :modal-form-confirm="collectData" 
      :reset-button-function="resetExcelData"
      ref="addParameterForm"
    >
      <template #modal-body>
        <div class="modal-status bg-danger" v-if="excelError"></div>
        <div class="modal-body p-0 m-0" v-if="excelError">
          <div class="alert alert-danger mb-0 rounded-0 border-start-0"  role="alert">
            <div class="d-flex">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0"></path><path d="M12 8v4"></path><path d="M12 16h.01"></path></svg>
              </div>
              <div>
                {{ excelErrorMsg }}
              </div>
            </div>
          </div>
        </div>
        <div class="modal-status bg-warning" v-if="dublicateExist"></div>
        <div class="modal-body p-0 m-0" v-if="dublicateExist">
          <div class="alert alert-warning mb-0 rounded-0 border-start-0"  role="alert">
            <div class="d-flex">
              <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon alert-icon"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 9v4"></path><path d="M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0z"></path><path d="M12 16h.01"></path></svg>
              </div>
              <div>
                {{ dublicateExistMsg }}
              </div>
            </div>
          </div>
        </div>
        <div class="modal-body p-0 px-2">
          <div class="row">
            <table class="table table-responsive table-bordered mb-0 pb-0" id="new-parameters-table">
              <thead class="sticky-top">
                <tr>
                  <th v-for="one in param_names.slice(0, -1)" :key="one.key">{{ one.label }}</th>
                  <th>O'chirish</th>
                </tr>
              </thead>
              <tbody v-if="!loading">
                <tr v-for="(one, index) in excelData" :key="index">
                  <td v-for="(key, idx) in Object.keys(one)" :key="key">
                    <input type="text" class="form-control form-control-sm" :value="one[key]" @input="updateCellValue(one, key, $event.target.value)" />
                    <div class="invalid-feedback" v-if="idx != 0 && validationError">To'g'ri qiymat kiriting</div>
                    <div class="invalid-feedback" v-if="idx === 0 && validationError">'YYYY/MM' formatida kiriting</div>
                    <div class="invalid-feedback" v-if="dublicateExist">Mavjud</div>
                  </td>
                  <RemoveRowButton @click="removeRow(index)" />
                </tr>
              </tbody>
            </table>
            <div class="d-flex justify-content-end align-items-center py-2" v-if="!loading">
              <button class="btn btn-sm btn-primary rounded-2 px-2 py-1" type="button" @click="addEmptyRow">
                <IconPlus class="icon" stroke="2" />
                Bo'sh katak qo'shish
              </button>
            </div>
            <div class="d-flex justify-content-center align-items-center py-5" v-if="loading">
              <div class="loader-custom"></div>
            </div>
          </div>
        </div>
      </template>
      <template #modal-footer-buttons>
        
        <div class="nav-item dropdown d-md-flex me-3">
          <label for="import-file-input" class="btn btn-outline-success" type="button">
            <IconUpload class="icon" stroke="2" />
            Excel yuklash
          </label>
          <input type="file"  class="form-control" id="import-file-input" hidden accept="application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" @change="excelUpload" />
        </div>
      </template>
    </ModalForm>
  </teleport>

  <teleport to="body">
    <ModalAlert :title="modalTitle" :description="modalDesc" ref="modalAlert" :type="modalType">
      <template #buttons>
        <div class="col">
          <button class="btn w-100" @click="modalOnCloseFunc" data-bs-dismiss="modal" data-bs-target="#modal-alert">
            Tushinarli
          </button>
        </div>
      </template>
    </ModalAlert>
  </teleport>
</template>

<script>
import { getWell, getParameterNames, getParameter, getPredictions, 
  getNewWellForm, editWell, calculateParameters, uploadFile, sendExcelData, sendConfirmedExcelData, getHeatmap } from '@/api/geo';
import { getRegions, getDistricts } from '@/api/common';
import { ref } from 'vue';
import { format } from 'date-fns';
import { IconPencil, IconPlus, IconX, IconCheck, IconUpload, IconCalculator } from '@tabler/icons-vue'
import ModalForm from '@/components/ModalFormComponent.vue';
import ModalAlert from '@/components/ModalAlert.vue';
import DataTable from '@/components/DataTable.vue';
import DeleteParameterButton from '@/components/DeleteParameterButton.vue';
import RemoveRowButton from '@/components/RemoveRowButton.vue';
import DatePicker from 'primevue/datepicker';
import { dateWithoutTimezone, dateToISOString } from '@/helpers';
const uz = require('../plugins/apexchartUzLocale.json')

export default {
  components: {
    // eslint-disable-next-line
    DeleteParameterButton,
    IconPencil, IconPlus, IconX, IconCheck, IconUpload, IconCalculator, ModalForm, DataTable, ModalAlert, RemoveRowButton, DatePicker
  },
  data: () => ({
    well: null,
    wellForm: {
      number: null,
      station: null,
      region: null,
      district: null,
      location: null,
      well_type: null,
      address: null,
      organization: null,
      x: null,
      y: null,
    },
    wellNumber: null,
    editMode: false,
    modalTitle: '',
    modalDesc: '',
    modalType: '',
    noInfoMes: '-',
    modalOnCloseFunc: () => { },
    parameter_names: [],
    parameters: [],
    gwlChartDates: [],
    gwlChartSeries: [],
    gwlChartSeriesForecast: [],
    gwlChartSeriesForecastDates: [],
    addParameterModalId: 'add-parameter',
    wellTypes: [],
    organizations: [],
    locations: [],
    stations: [],
    regions: [],
    districts: [],
    excelData: [],
    loading: false,
    excelError: false,
    excelErrorMsg: '',
    dublicateExist: false,
    dublicateExistMsg: '',
    confirmOverwrite: false,
    validationError: false,
    calculations: [],
    paramStartDate: null,
    paramEndDate: null,
    calcData: [],
    mannKendall: [],
    heatmapImage: null,
    months: [
        { key: "I", name: "Yan" },
        { key: "II", name: "Fev" },
        { key: "III", name: "Mart" },
        { key: "IV", name: "Aprel" },
        { key: "V", name: "May" },
        { key: "VI", name: "Iyun" },
        { key: "VII", name: "Iyul" },
        { key: "VIII", name: "Avgust" },
        { key: "IX", name: "Sent" },
        { key: "X", name: "Okt" },
        { key: "XI", name: "Noy" },
        { key: "XII", name: "Dek" }
      ],
  }),


  setup() {
    const modalAlert = ref();
    const addParameterForm = ref();
    return {
      modalAlert,
      addParameterForm
    }
  },
  computed: {
    format() {
      return format;
    },
    param_names() {
      let names = this.parameter_names.map(pn => ({
        key: pn.id,
        label: pn.name
      }));
      names.unshift({
        key: 'date',
        label: 'Sana'
      });
      names.push({
        key: 'delete',
        label: '',
        type: 'custom',
        render: DeleteParameterButton
      });
      return names;
    },
    params() {
      const grouped = {};
      for (const param of this.parameters) {
        const dateParts = param.date.split("T")[0].split("-");
        const date = `${dateParts[0]}/${dateParts[1]}`; // YYYY/MM format
        if (!grouped[date]) {
          grouped[date] = {};
        }
        grouped[date][param.parameter_name] = param.value;
      }

      const params = [];
      for (const date in grouped) {
        params.push({
          date: date,
          ...grouped[date],
          delete: date
        });
      }
      return params;
    },
    gwlChartOptions() {
      return {
        chart: {
          type: "area",
          locales: [uz],
          defaultLocale: 'uz'
        },
        stroke: {
          curve: 'straight'
        },
        legend: {
          horizontalAlign: 'left'
        },
        dataLabels: {
          enabled: false,
        },
        markers: {
          size: 0,
          style: "hollow",
        },
        xaxis: {
          type: "datetime",
          // min: new Date("01 Mar 2012").getTime(),
          categories: this.gwlChartDates, // Reactive data for x-axis
        },
        tooltip: {
          x: {
            format: "dd MMM yyyy",
          },
        },
      };
    },
    gwlChartForecastOptions() {
      return {
        chart: {
          type: "area",
          locales: [uz],
          defaultLocale: 'uz'
        },
        stroke: {
          curve: 'straight'
        },
        legend: {
          horizontalAlign: 'left'
        },
        dataLabels: {
          enabled: false,
        },
        markers: {
          size: 0,
          style: "hollow",
        },
        xaxis: {
          type: "datetime",
          // min: new Date("01 Mar 2012").getTime(),
          categories: this.gwlChartSeriesForecastDates, // Reactive data for x-axis
        },
        tooltip: {
          x: {
            format: "yyyy/MM",
          },
        },
      };
    },

    yearlyAvgSeries() {
      return [
        {
          name: `Yillik o’rtacha ${this.well.number}`,
          data: this.calcData.map((item) => item.yearly_avg),
        },
      ];
    },
    yearlyAvgOptions() {
      return {
        chart: {
          id: 'yearlyAvgChart',
          type: 'area',
        },
        xaxis: {
          categories: this.calcData.map((item) => item.year),
          title: {
            text: 'Yil',
          },
        },
        title: {
          text: 'Yillik o’rtacha',
          align: 'center',
        },
        dataLabels: {
          enabled: false
        },
      };
    },
    // Series and options for the amplitude chart
    amplitudeSeries() {
      return [
        {
          name: `Amplituda ${this.well.number}`,
          data: this.calcData.map((item) => item.amplitude),
        },
      ];
    },
    amplitudeOptions() {
      return {
        chart: {
          id: 'amplitudeChart',
          type: 'area',
        },
        xaxis: {
          categories: this.calcData.map((item) => item.year),
          title: {
            text: 'Yil',
          },
        },
        title: {
          text: 'Amplituda',
          align: 'center',
        },
        dataLabels: {
          enabled: false
        },
      };
    },
  },

  methods:{
    setGwlOptionsSeries(parameters){
      const dates = [];
      const params = [];
      this.gwlChartSeries = [];
      for (const param of parameters) {
        const date = param.date.split("T")[0]; 
        if (!dates.includes(date)) {
          dates.push(date);
        }
        if (param.parameter_name == 1) {
          params.push(param.value)
        }
      }
      this.gwlChartSeries.push({
        name: 'GWL (M)',
        data: params
      })
      this.gwlChartDates = dates
    },
    setGwlForecastOptionsSeries(predictions){
      const params = [];
      this.gwlChartSeriesForecast = [];
      predictions.predictions.forEach((prediction) => {
        params.push(Math.round(prediction * 100) / 100)
      })
      this.gwlChartSeriesForecast.push({
        name: 'GWL (M)',
        data: params
      })
      this.gwlChartSeriesForecastDates = predictions.dates
    },
    async changeDistricts(event) {
      try {
        this.districts = await getDistricts(event.target.value);
      } catch (error) {
        this.modalAlert.openModal();
        this.modalTitle = "Tumanlarni yuklashda xatolik yuzaga keldi";
        this.modalDesc = `Xato xabari: ${error.message}`;
        this.modalType = 'danger';
      }
    },
    setWellForm(well) {
      for (const key in this.wellForm) {
        if (['location', 'organization', 'well_type', 'station', 'region', 'district'].includes(key)) {
          if (well[key]?.id) {
            this.wellForm[key] = well[key].id;
          }
          else {
            this.wellForm[key] = null;
          }
        }
        else if (well[key]) {
          this.wellForm[key] = well[key];
        }
      }
    },
    async wellEditSubmit() {
      try{
        await editWell(this.well.number, this.wellForm);
        this.well = await getWell(this.wellNumber);
        this.setWellForm(this.well);
        this.editMode = false;
      }
      catch(error){
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlarni tahrirlashda xatolik yuzaga keldi";
        this.modalDesc = `Xato xabari: ${error?.message}`;
        this.modalType = 'danger';
      }
      console.log(this.wellForm);
    },
    async excelUpload(event) {
      this.loading = true;
      this.excelError = false;
      this.excelErrorMsg = '';
      try{
        const response = await uploadFile(this.wellNumber, event.target.files[0]);
        this.excelData.push(...JSON.parse(response.data.df));
      }
      catch(error){
        this.excelError = true;
        this.excelErrorMsg = 'Excel faylni yuklashda xatolik yuzaga keldi, iltimos ';
      }
      this.loading = false;
    },
    addEmptyRow(){
      this.dublicateExist = false;
      this.excelData.push({
        ...Array(this.param_names.length - 1).fill('')
      });
    },
    async collectData() {
      let dataToSend = [];
      let error = false;
      const dateRegex = /^\d{4}\/\d{2}$/;
      const param_length = this.param_names.length - 1;
      // Collect data for empty rows
      document.querySelectorAll('#new-parameters-table input[type=text]').forEach((input, index) => {
        // Only process inputs from empty rows
        const inputValue = input.value;
        let rowIndex = Math.floor(index / param_length);
        let columnIndex = index % param_length;
        this.validationError = false;
        if (!dataToSend[rowIndex]) {
          dataToSend[rowIndex] = {};
        }
        if (columnIndex == 0 && !dateRegex.test(inputValue)) {
          input.classList.add('is-invalid');
          error = true;
          this.validationError = true;
        } else if (
          columnIndex != 0 && inputValue.trim() !== '' && !/^-?\d+(\.\d+)?$/.test(inputValue)
        ) {
          input.classList.add('is-invalid');
          error = true;
          this.validationError = true;
        } else {
          input.classList.remove('is-invalid');
        }
        dataToSend[rowIndex][columnIndex] = inputValue;
      });
      if (error) {
        return;
      }
      try{
        this.loading = true;
        const response = await sendExcelData(this.wellNumber, dataToSend);
        if (response.existing_parameters.length > 0) {
          if (this.confirmOverwrite) {
            this.confirmOverwrite = false;
            try{
              await sendConfirmedExcelData(this.wellNumber, dataToSend);
              this.parameters = await getParameter(this.wellNumber);
              this.setGwlOptionsSeries(this.parameters);
              this.setGwlForecastOptionsSeries(await getPredictions(this.wellNumber));
              this.excelData = [];
              this.addEmptyRow();
              this.addParameterForm.closeModal();
              this.modalAlert.openModal();
              this.modalTitle = "Ma'lumotlar yuklandi";
              this.modalType = 'success';
              this.loading = false;
            }
            catch(error){
              this.loading = false;
              this.addParameterForm.closeModal();
              this.modalAlert.openModal();
              this.modalTitle = "Ma'lumotlar yuklashda xatolik yuzaga keldi, iltimos qaytadan urinib ko'ring";
              this.modalDesc = `Xato xabari: ${error?.message}`;
              this.modalType = 'danger';
            }
          } else {
            this.dublicateExist = true;
            this.confirmOverwrite = true;
            this.dublicateExistMsg = "Bazi sanada ma'lumotlar mavjud, mavjud sanadagi ma'lumotlarni o'zgartirishni istasangiz, qo'shish tugmasini yana bosing";
            let exist_rows_idx = -1;
            this.loading = false;
            await this.$nextTick();
            document.querySelectorAll('#new-parameters-table input[type=text]').forEach((input, index) => {
              
              let rowIndex = Math.floor(index / param_length);
              let columnIndex = index % param_length;
              response.existing_parameters.forEach(param => {
                let dateParts = param.date.split("T")[0].split("-");
                if (columnIndex == 0 && `${dateParts[0]}/${dateParts[1]}` == input.value) {
                  input.classList.add('is-invalid');
                  exist_rows_idx = rowIndex;
                } else if (columnIndex != 0 && param.parameter_name == columnIndex && exist_rows_idx == rowIndex) {
                  input.classList.add('is-invalid');
                }
              })
            });
            this.existing_parameters = response.existing_parameters;
          }
        } else {

          try{
              await sendConfirmedExcelData(this.wellNumber, dataToSend);
              this.parameters = await getParameter(this.wellNumber);
              this.setGwlOptionsSeries(this.parameters);
              this.setGwlForecastOptionsSeries(await getPredictions(this.wellNumber));
              this.excelData = [];
              this.addEmptyRow();
              this.addParameterForm.closeModal();
              this.modalAlert.openModal();
              this.modalTitle = "Ma'lumotlar yuklandi";
              this.modalType = 'success';
              this.loading = false;
            }
            catch(error){
              this.loading = false;
              this.addParameterForm.closeModal();
              this.modalAlert.openModal();
              this.modalTitle = "Ma'lumotlar yuklashda xatolik yuzaga keldi, iltimos qaytadan urinib ko'ring";
              this.modalDesc = `Xato xabari: ${error?.message}`;
              this.modalType = 'danger';
            }
        }
      }
      catch(error){
        this.loading = false;
        this.addParameterForm.closeModal();
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlar yuklashda xatolik yuzaga keldi, iltimos qaytadan urinib ko'ring";
        this.modalDesc = `Xato xabari: ${error?.message}`;
        this.modalType = 'danger';
        console.log(error);
      }
      return dataToSend;
    },
    resetExcelData(){
      this.excelData = [];
      this.addEmptyRow();
      this.confirmOverwrite = false;
    },
    updateCellValue(row, key, value) {
      row[key] = value;
      this.confirmOverwrite = false;
    },
    removeRow(row){
      this.excelData.splice(row, 1);
      this.confirmOverwrite = false;
    },
    async calculateUpdate(){
      try{
        this.calculations = await calculateParameters(Number(this.wellNumber), 1, dateWithoutTimezone(this.calculationStartDate), dateWithoutTimezone(this.calculationEndDate));
        this.calcData = this.calculations.data.filter(item => typeof item.year === 'number');
        this.mannKendall = this.calculations.data.filter(item => typeof item.year !== 'number'); 
        this.heatmapImage = await getHeatmap(this.wellNumber, 1, dateWithoutTimezone(this.calculationStartDate), dateWithoutTimezone(this.calculationEndDate));
      }
      catch(error){
        this.modalAlert.openModal();
        this.modalTitle = "Hisoblash uchun 1 yildan ortiq intervalda ma'lumot kerak";
        this.modalDesc = ``;
        this.modalType = 'danger';
      }
    }
  },

  async mounted() {
    this.wellNumber = this.$route?.params?.number;
    if (this.wellNumber) {
      try {
        this.well = await getWell(this.wellNumber);
        this.parameter_names = await getParameterNames();
        
        this.parameters = await getParameter(this.wellNumber);
        this.regions = await getRegions();
        const response = await getNewWellForm();
        this.calculations = await calculateParameters(Number(this.wellNumber), 1, this.parameters[0].date, this.parameters[this.parameters.length - 1].date);
        this.setGwlForecastOptionsSeries(await getPredictions(this.wellNumber));
        this.heatmapImage = await getHeatmap(this.wellNumber, 1, this.parameters[0].date, this.parameters[this.parameters.length - 1].date);

        await this.$nextTick();

        this.addEmptyRow();
        this.wellTypes = response.well_types;
        this.organizations = response.organizations;
        this.locations = response.locations;
        this.stations = response.stations;
        this.calcData = this.calculations.data.filter(item => typeof item.year === 'number');
        this.mannKendall = this.calculations.data.filter(item => typeof item.year !== 'number'); 
        this.setGwlOptionsSeries(this.parameters);
        this.setWellForm(this.well);
        this.paramStartDate = dateToISOString(this.parameters[0].date);
        this.paramEndDate = dateToISOString(this.parameters[this.parameters.length - 1].date);
        this.calculationStartDate = dateToISOString(this.parameters[0].date);
        this.calculationEndDate = dateToISOString(this.parameters[this.parameters.length - 1].date);
      } catch (error) {
        console.error('Error fetching well data:', error);
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlarni yuklashda xatolik yuzaga keldi";
        this.modalDesc = `Xato xabari: ${error?.message}`;
        this.modalType = 'danger';
      }
    } else {
      console.error('No wellId found in route parameters.');
    }
  },
};
</script>

<style>
.required:after {
    content: "*";
    margin-left: .25rem;
    color: #d63939;
}
.dropdown-menu{
  -webkit-user-select: auto;
  user-select: auto;
}
</style>