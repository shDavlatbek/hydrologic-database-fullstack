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
              <div class="datagrid-title">Shimoliy kenglik</div>
              <div class="datagrid-content">{{ latitude }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Sharqiy kenglik</div>
              <div class="datagrid-content">{{ longitude }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">[X, Y]</div>
              <div class="datagrid-content">{{ well?.coordinate?.x ? well?.coordinate?.x : noInfoMes }}:{{ well?.coordinate?.y ? well?.coordinate?.y : noInfoMes }}</div>
            </div>
            <div class="datagrid-item">
              <div class="datagrid-title">Qo'shilgan vaqti</div>
              <div class="datagrid-content">{{ well?.created_at ? format(new Date(well?.created_at), 'dd.MM.yyyy HH:mm:ss') : noInfoMes }}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cards">
        <div class="col-12 col-lg-6">
          <div class="card">
            <div class="card-body">
              <div class="d-flex">
                <h3 class="card-title">Social referrals</h3>
                <div class="ms-auto">
                  <div class="dropdown">
                    <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Last 7 days</a>
                    <div class="dropdown-menu dropdown-menu-end">
                      <a class="dropdown-item active" href="#">Last 7 days</a>
                      <a class="dropdown-item" href="#">Last 30 days</a>
                      <a class="dropdown-item" href="#">Last 3 months</a>
                    </div>
                  </div>
                </div>
              </div>
              <apexchart height="350" type="line" 
                :options="gwlChartOptions" 
                :series="gwlChartSeries"
              ></apexchart>
            </div>
          </div>
        </div>
        <div class="col-12 col-lg-6">
          <div class="card">
            <div class="card-body">
              <div class="d-flex">
                <h3 class="card-title">Social referrals</h3>
                <div class="ms-auto">
                  <div class="dropdown">
                    <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Last 7 days</a>
                    <div class="dropdown-menu dropdown-menu-end">
                      <a class="dropdown-item active" href="#">Last 7 days</a>
                      <a class="dropdown-item" href="#">Last 30 days</a>
                      <a class="dropdown-item" href="#">Last 3 months</a>
                    </div>
                  </div>
                </div>
              </div>
              <apexchart height="350" type="line" 
                :options="gwlChartOptions" 
                :series="gwlChartSeries"
              ></apexchart>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card">
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
import { getWell, getParameterNames, getParameter } from '@/api/geo';
import { ref } from 'vue';
import { format } from 'date-fns';
import { IconPencil } from '@tabler/icons-vue'

// let table = new DataTable('#datatable', {
//     perPageSelect: [5, 10, 15, ["All", -1]],
//     language: {
//       "decimal":        "",
//       "emptyTable":     "Mavjud emas",
//       "info":           "_TOTAL_ ta yozuvdan _START_ dan _END_ gacha koʻrsatilmoqda",
//       "infoFiltered":   "(filtered from _MAX_ total entries)",
//       "infoPostFix":    "",
//       "thousands":      ",",
//       "lengthMenu":     "_MENU_ mehmon har bir sahifada",
//       "loadingRecords": "Yuklanmoqda...",
//       "processing":     "",
//       "search":         "Qidiruv:",
//       "zeroRecords":    "Mehmon topilmadi",

//     }
//   });

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
    gwlChartOptions: {
      chart: {
        type: 'line'
      },
      xaxis: {
        categories: ['1991-01-01', 1992, 1993, 1994, 1995, 1996, 1997, 1998],
        type: 'datetime',
      }
    },
    gwlChartSeries: [{
      name: 'series-1',
      data: [30, 40, 45, 50, 49, 60, 70, 91]
    }]
  }),

  components: {
    IconPencil
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
    longitude(){
      const { longitude_degree, longitude_minute, longitude_second } = this.well?.coordinate ?? {};
      return `${longitude_degree ?? ''}°${longitude_minute ?? ''}"${longitude_second ?? ''}'`;
    },
    latitude() {
      const { latitude_degree, latitude_minute, latitude_second } = this.well?.coordinate ?? {};
      return `${latitude_degree ?? ''}°${latitude_minute ?? ''}"${latitude_second ?? ''}'`;
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
    }
  },

  methods:{
    setGwlOptionsSeries(parameters){
      const grouped = {};
      for (const param of parameters) {
        const date = param.date.split("T")[0]; 
        if (!grouped[date]) {
          grouped[date] = {};
        }
        grouped[date][param.parameter_name] = param.value;
      }
      return grouped;
    }
  },

  async mounted() {
    const wellId = this.$route?.params?.id;
    if (wellId) {
      try {
        this.well = await getWell(wellId);
        this.parameter_names = await getParameterNames();
        this.parameters = await getParameter(wellId);
        this.setGwlOptionsSeries(this.parameters);
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
