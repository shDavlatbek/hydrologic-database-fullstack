<template>
  <div class="page-body" v-if="well">
    <div class="container-xl">
      <div class="card mb-4">
        <div class="card-header">
          <h3 class="card-title">Quduq ma'lumotlari</h3>
          <div class="card-actions">
            <a href="#" data-bs-toggle="modal" data-bs-target="">
              Tahrirlash
              <IconPencil class="icon" stroke="2" />
            </a>
          </div>
        </div>
        <div class="card-body">
          <div class="datagrid">
            <div class="datagrid-item">
              <div class="datagrid-title">Quduq raqami</div>
              <div class="datagrid-content">{{ well?.number ? well?.number : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Stansiya nomi</div>
              <div class="datagrid-content">{{ well?.station ? well?.station?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Viloyat</div>
              <div class="datagrid-content">{{ well?.region ? well?.region?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Tuman</div>
              <div class="datagrid-content">{{ well?.district ? well?.district?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Joylashuv o'rni</div>
              <div class="datagrid-content">{{ well?.location ? well?.location?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Quduq turi</div>
              <div class="datagrid-content">{{ well?.well_type ? well?.well_type?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Mo'ljal</div>
              <div class="datagrid-content">{{ well?.address?.name ? well?.address?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Tashkilot</div>
              <div class="datagrid-content">{{ well?.organization ?  well?.organization?.name : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">[X, Y]</div>
              <div class="datagrid-content">{{ well?.x ? well?.x : noInfoMes }}, {{ well?.y ? well?.y : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Qo'shilgan vaqti</div>
              <div class="datagrid-content">{{ well?.created_at ? format(new Date(well?.created_at), 'dd.MM.yyyy HH:mm:ss') : noInfoMes }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cards">
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
        <div class="col">
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
            <div class="table-responsive">
              <table class="table table-vcenter card-table table-bordered">
                <thead>
                  <tr>
                    <th>Sana</th>
                    <th v-for="pn in parameter_names" :key="pn.id">{{ pn.name }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(params, date) in dataByDate" :key="date">
                    <td>{{ date }}</td>
                    <td v-for="pn in parameter_names" :key="pn.id">
                      {{ params[pn.id] !== undefined ? params[pn.id] : '' }}
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
    <ModalForm :modal-id="addParameterModalId" modal-title="Parameterlar qo'shish" :modal-form-confirm="newParameterSubmit" ref="addParameterForm">
      <template #modal-body>
        <div class="modal-body">
          <div class="row">
          </div>
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
import { getWell, getParameterNames, getParameter, getPredictions } from '@/api/geo';
import { ref } from 'vue';
import { format } from 'date-fns';
import { IconPencil, IconPlus } from '@tabler/icons-vue'
import ModalForm from '@/components/ModalFormComponent.vue';
const uz = require('../plugins/apexchartUzLocale.json')

export default {
  data: () => ({
    well: null,
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
    addParameterModalId: 'add-parameter'
  }),

  components: {
    IconPencil, IconPlus, ModalForm
  },

  setup() {
    const modalAlert = ref();
    return {
      modalAlert
    }
  },
  computed: {
    format() {
      return format;
    },
    dataByDate() {
      const grouped = {};
      for (const param of this.parameters) {
        const date = param.date.split("T")[0]; 
        if (!grouped[date]) {
          grouped[date] = {};
        }
        grouped[date][param.parameter_name] = param.value;
      }
      return grouped;
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

  },

  methods:{
    setGwlOptionsSeries(parameters){
      const dates = [];
      const params = [];
      for (const param of parameters) {
        const date = param.date.split("T")[0]; 
        if (!dates.includes(date)) {
          dates.push(date);
        }
        if (param.parameter_name == 1) {
          params.push(param.value)
        }
      }
      console.log(dates);
      console.log(params);
      this.gwlChartSeries.push({
        name: 'GWL (M)',
        data: params
      })
      this.gwlChartDates = dates
      console.log(this.gwlChartSeries[0].data);
      console.log(this.gwlChartOptions.xaxis.categories);
    },
    setGwlForecastOptionsSeries(predictions){
      const params = [];
      predictions.predictions.forEach((prediction) => {
        // округляем до 2 знаков после запятой
        params.push(Math.round(prediction * 100) / 100)
      })
      this.gwlChartSeriesForecast.push({
        name: 'GWL (M)',
        data: params
      })
      this.gwlChartSeriesForecastDates = predictions.dates
    }
  },

  async mounted() {
    const wellNumber = this.$route?.params?.number;
    if (wellNumber) {
      try {
        this.well = await getWell(wellNumber);
        this.parameter_names = await getParameterNames();
        this.parameters = await getParameter(wellNumber);
        this.setGwlOptionsSeries(this.parameters);
        const predictions = await getPredictions(wellNumber);
        this.setGwlForecastOptionsSeries(predictions);
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
