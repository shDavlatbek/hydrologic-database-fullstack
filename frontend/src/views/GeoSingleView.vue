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
          </div>
          <DataTable :data="params" :columns="param_names" />
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
import { getWell, getParameterNames, getParameter, getPredictions, getNewWellForm, editWell, uploadFile, sendExcelData, sendConfirmedExcelData } from '@/api/geo';
import { getRegions, getDistricts } from '@/api/common';
import { ref } from 'vue';
import { format } from 'date-fns';
import { IconPencil, IconPlus, IconX, IconCheck, IconUpload } from '@tabler/icons-vue'
import ModalForm from '@/components/ModalFormComponent.vue';
import ModalAlert from '@/components/ModalAlert.vue';
import DataTable from '@/components/DataTable.vue';
import DeleteParameterButton from '@/components/DeleteParameterButton.vue';
import RemoveRowButton from '@/components/RemoveRowButton.vue';
const uz = require('../plugins/apexchartUzLocale.json')

export default {
  components: {
    // eslint-disable-next-line
    DeleteParameterButton,
    IconPencil, IconPlus, IconX, IconCheck, IconUpload, ModalForm, DataTable, ModalAlert, RemoveRowButton
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
    }
  },

  async mounted() {
    this.wellNumber = this.$route?.params?.number;
    if (this.wellNumber) {
      try {
        this.well = await getWell(this.wellNumber);
        this.parameter_names = await getParameterNames();
        this.addEmptyRow();
        this.parameters = await getParameter(this.wellNumber);
        this.regions = await getRegions();
        const response = await getNewWellForm();
        this.wellTypes = response.well_types;
        this.organizations = response.organizations;
        this.locations = response.locations;
        this.stations = response.stations;
        this.setGwlOptionsSeries(this.parameters);
        this.setGwlForecastOptionsSeries(await getPredictions(this.wellNumber));
        this.setWellForm(this.well);
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