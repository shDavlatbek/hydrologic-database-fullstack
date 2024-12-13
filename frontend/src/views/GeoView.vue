<template>
  <HeaderText :title="title" :modal-id="modalId" :on-modal-open="loadForm" />

  <div class="page-body">
    <div class="container-xl">
      <div class="card">
        <div class="card-body border-bottom py-3">
          <div class="d-flex">
            <div class="ms-auto row">
              <div class="col-auto">
                <label for="geo-search" class="col-form-label p-0">Qidiruv</label>
              </div>
              <div class="col-auto">
                <input type="text" v-model="searchQuery" @input="updateSearch" id="geo-search" class="form-control form-control-sm">
              </div>
            </div>
          </div>
        </div>
        <div id="table-geo" class="table-responsive">
            <table class="table">
              <thead>
                <tr>
                  <th><button class="table-sort" data-sort="sort-number">Raqam</button></th>
                  <th><button class="table-sort" data-sort="sort-station">Stansiya</button></th>
                  <th><button class="table-sort" data-sort="sort-region">Viloyat</button></th>
                  <th><button class="table-sort" data-sort="sort-district">Tuman</button></th>
                  <th><button class="table-sort" data-sort="sort-progress">Malumotlar mavjudligi</button></th>
                </tr>
              </thead>
              <tbody class="table-tbody">
                <tr class="table-row" v-for="(well, index) in wells" :key="index" @click="navigateToGeoSingle(well.id)">
                  <td class="sort-number">{{ well?.number }}</td>
                  <td class="sort-station">{{ well?.station ? well?.station.name : noInfoMessage }}</td>
                  <td class="sort-region">{{ well?.region ? well?.region.name : noInfoMessage }}</td>
                  <td class="sort-district">{{ well?.district ? well?.district.name : noInfoMessage }}</td>
                  <td class="sort-progress" data-progress="30">
                    <div class="row align-items-center">
                      <div class="col-12 col-lg-auto">30%</div>
                      <div class="col">
                        <div class="progress" style="width: 5rem">
                          <div class="progress-bar" style="width: 30%" role="progressbar" aria-valuenow="30"
                            aria-valuemin="0" aria-valuemax="100" aria-label="30% Complete">
                            <span class="visually-hidden">30% Complete</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
      </div>
    </div>
  </div>

  <teleport to="body">
    <ModalForm :modal-id="modalId" :modal-title="title" :modal-form-confirm="formHandler" ref="modalForm">
      <template #modal-body>
        <div class="modal-body">
          <div class="row">
            <div class="col-lg-6 col-md-12">
              <SelectField label="Qaysi davlat tashkilotiga mansubligi" v-model="addWellForm.organization">
                <option v-for="one in organizations" :key="one.id" :value="one.id">{{ one.name }}</option>
              </SelectField>
            </div>
            <div class="col-lg-6 col-md-12">
              <InputField label="Kuzatuv qudug'i raqami" :required="true" v-model.number="addWellForm.number"
                type="number" />
            </div>
            <div class="col-lg-6 col-md-12">
              <SelectField label="Kuzatuv burg'u qudug'ining turi" v-model="addWellForm.well_type">
                <option v-for="one in wellTypes" :key="one.id" :value="one.id">{{ one.name }}</option>
              </SelectField>
            </div>
            <div class="col-lg-6 col-md-12">
              <SelectField label="Qaysi stansiya" v-model="addWellForm.station">
                <option v-for="one in stations" :key="one.id" :value="one.id">{{ one.name }}</option>
              </SelectField>
            </div>
          </div>
        </div>

        <div class="modal-body">
          <div class="row">
            <div class="col-lg-6">
              <div class="row">
                <div class="col-12">
                  <SelectField label="Viloyat nomi" empty-value="0" @change="changeDistricts"
                    v-model="addWellForm.region">
                    <option v-for="region in regions" :key="region.id" :value="region.id">
                      {{ region.name }}
                    </option>
                  </SelectField>
                </div>
                <div class="col-12">
                  <SelectField label="Tuman nomi" empty-value="0" v-model="addWellForm.district">
                    <option v-for="district in districts" :key="district.id" :value="district.id">
                      {{ district.name }}
                    </option>
                  </SelectField>
                </div>
                <div class="col-12">
                  <InputField label="Mo'ljal" v-model="addWellForm.address" />
                </div>
                <div class="col-12">
                  <SelectField label="Joylashuv o'rni" v-model="addWellForm.location">
                    <option v-for="one in locations" :key="one.id" :value="one.id">{{ one.name }}</option>
                  </SelectField>
                </div>
              </div>
            </div>
            <div class="col-lg-6">
              <div class="mb-3">
                <label class="form-label">*</label>
                <div class="form-control-plaintext">Kuzatuv burg'u qudug'ining koordinatasi</div>
              </div>
              <label class="form-label">Shimoliy kenglik</label>
              <div class="row">
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.latitude_degree">
                    <template #after>
                      <span class="input-group-text">°</span>
                    </template>
                  </InputField>
                </div>
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.latitude_minute">
                    <template #after>
                      <span class="input-group-text">'</span>
                    </template>
                  </InputField>
                </div>
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.latitude_second">
                    <template #after>
                      <span class="input-group-text">"</span>
                    </template>
                  </InputField>
                </div>
              </div>
              <label class="form-label">Sharqiy uzunlik</label>
              <div class="row">
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.longitude_degree">
                    <template #after>
                      <span class="input-group-text">°</span>
                    </template>
                  </InputField>
                </div>
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.longitude_minute">
                    <template #after>
                      <span class="input-group-text">'</span>
                    </template>
                  </InputField>
                </div>
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.longitude_second">
                    <template #after>
                      <span class="input-group-text">"</span>
                    </template>
                  </InputField>
                </div>
              </div>
              <label class="form-label">[x; y]</label>
              <div class="row">
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.x">
                    <template #after>
                      <span class="input-group-text">x</span>
                    </template>
                  </InputField>
                </div>
                <div class="col-4">
                  <InputField class="input-group" type="number" v-model="addWellForm.coordinate.y">
                    <template #after>
                      <span class="input-group-text">y</span>
                    </template>
                  </InputField>
                </div>
              </div>
            </div>
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
import HeaderText from '@/components/HeaderTextComponent.vue';
import ModalForm from '@/components/ModalFormComponent.vue';
import InputField from '@/components/InputField.vue';
import SelectField from '@/components/SelectField.vue';
import ModalAlert from '@/components/ModalAlert.vue';
import List from 'list.js';
import { getDistricts, getRegions } from '@/api/common';
import { addNewWell, getNewWellForm, getWells } from '@/api/geo';
import { ref } from 'vue';

export default {
  data() {
    return {
      title: "Gidrogeologik ma'lumotlar",
      modalId: "hydrogeologic-modal",
      addWellForm: {
        number: null,
        region: null,
        district: null,
        address: null,
        well_type: null,
        organization: null,
        location: null,
        station: null,
        coordinate: {
          latitude_degree: null,
          latitude_minute: null,
          latitude_second: null,
          longitude_degree: null,
          longitude_minute: null,
          longitude_second: null,
          x: null,
          y: null
        }
      },
      formLoaded: false,
      wellTypes: {},
      organizations: {},
      locations: {},
      stations: {},
      regions: {},
      districts: {},
      wells: {},
      modalOnCloseFunc: null,
      list: null,
      searchQuery: '',
      modalType: null,
      modalDesc: '',
      modalTitle: '',
      noInfoMessage: '------'
    }
  },
  computed: {
  },
  setup() {
    const modalAlert = ref();
    const modalForm = ref();
    return {
      modalAlert, modalForm
    }
  },
  methods: {
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
    async formHandler() {
      console.log("Form submitted");
      try {
        await addNewWell(JSON.stringify(this.addWellForm));
        this.modalForm.resetForm();
        this.modalForm.closeModal();
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlar muvaffaqiyatli qo'shildi";
        this.modalDesc = ""
        this.modalType = 'success';
        setTimeout(() => {
          this.$router.go();
        }, 2000);
        this.modalOnCloseFunc = () => {this.$router.go();};
      } catch (error) {
        console.log(error);
        this.modalForm.resetForm();
        this.modalForm.closeModal();
        this.modalAlert.openModal();
        this.modalTitle = "Ma'lumotlarni saqlashda xatolik yuzaga keldi";
        this.modalDesc = `Xato xabari: ${error?.message}<br>Url: ${error?.config?.url}`;
        this.modalType = 'danger'; 
        this.modalOnCloseFunc = () => {};
      }
    },
    async loadForm() {
      if (this.formLoaded) {
        return;
      } else {
        try {
          this.regions = await getRegions();
          const response = await getNewWellForm();
          this.wellTypes = response.well_types;
          this.organizations = response.organizations;
          this.locations = response.locations;
          this.stations = response.stations;
        } catch (error) {
          console.log(error);
          this.modalTitle = "Ma'lumotlarni yuklashda xatolik yuzaga keldi";
          this.dangerModal.openModal();
          this.modalDesc = `Xato xabari: ${error.message}<br>Url: ${error.config.url}`;
          this.modalType = 'danger';
          this.modalOnCloseFunc = () => {};
        }
      }
    },
    initializeList() {
      const tableGeo = document.getElementById('table-geo');
      if (tableGeo) {
        if (!this.list) {
          this.list = new List('table-geo', {
            sortClass: 'table-sort',
            listClass: 'table-tbody',
            valueNames: ['sort-number', 'sort-station', 'sort-region', 'sort-district'],
          });
        } else {
          this.list.reIndex();
        }
      } else {
        console.error("Element #table-geo not found!");
      }
    },
    updateSearch() {
      if (this.list) {
        this.list.search(this.searchQuery);
      }
    },
    navigateToGeoSingle(id) {
      this.$router.push({ name: "GeoSingle", params: { id } });
    },
  },
  components: {
    HeaderText, ModalForm, InputField, SelectField, ModalAlert
  },
  async mounted() {
    try {
      this.wells = await getWells();
      await this.$nextTick();
      this.initializeList();
    } catch (error) {
      console.log(error);
      this.modalAlert.openModal();
      this.modalTitle = "Ma'lumotlarni yuklashda xatolik yuzaga keldi";
      if( error.message && error.config ){
        this.modalDesc = `Xato xabari: ${error.message}<br>Url: ${error?.config?.url}`;
      } else {
        this.modalDesc = `Xato xabari: ${error}`;
      }
      this.modalType = 'danger';
      this.modalOnCloseFunc = () => {};
    }
  },
}

</script>