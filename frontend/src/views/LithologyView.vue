<template>  
  
    <div class="page-body">
      <div class="container-xl">
  
        <div class="row">
          <div class="col-12 col-lg-6" style="height: 88vh">
            <div class="card rounded-2 h-100 mb-0 overflow-hidden">
              <div class="card-body" style="display: flex; flex-direction: column">
                <div class="row mb-3">
                  <label for="id_well" class="col-sm-6 col-form-label">Kuzatuv-burg'u qudug'i raqami</label>
                  <div class="col-sm-6 d-flex align-items-center">
                    <select class="form-control well_select" id="id_well" name="well" required>
                      <option value="-1">---------</option>
                      <option v-for="well in wellsData" :value="well.number" :key="well.number">{{ well.number }}</option>
                    </select>
                  </div>
                </div>

                <div class="mb-3 w-100 d-flex">
                  <input type="number" id="well-height" name="well-height" min="0" value="100" hidden />
                  <button class="btn btn-primary" id="download-png" @click="captureSVG">Yuklab olish</button>
                  <button class="btn btn-primary ms-auto" id="add-interval">Add</button>
                  <canvas id="canvas" style="display: none"></canvas>
                </div>
                <div id="lithology-inputs">
                  <div class="lithology-row input-group mb-3">
                      <label for="depth-start-0" class="input-group-text">Dan (m):</label>
                      <input type="number" class="form-control" id="depth-start-0" name="depth-start" min="0" max="100" value="0" />
                      <label class="input-group-text" for="depth-end-0">Gacha (m):</label>
                      <input type="number" class="form-control" id="depth-end-0" name="depth-end" min="0" max="100" value="0" />
                      <label class="input-group-text" for="pattern-0">Element:</label>
                      <select class="form-control" id="pattern-0" name="pattern">
                        <option value="loam">Loam</option>
                        <option value="sandy-loam">Sandy Loam</option>
                        <option value="clay">Clay</option>
                        <option value="sandy-gravel">Sandy Gravel</option>
                        <option value="pebble-and-gravel">Pebble and Gravel</option>
                        <option value="pebbly">Pebbly</option>
                        <option value="boulder-pebble">Boulder-Pebble</option>
                        <option value="sand">Sand</option>
                        <option value="gravel-with-gravel-and-sand">Gravel with Gravel and Sand</option>
                        <option value="sand-with-gravel">Sand with Gravel</option>
                        <option value="loam-with-clay">Loam with Clay</option>
                        <option value="loamy-sand">Loamy Sand</option>
                        <option value="gravel-with-sand-and-pebbles">Gravel with Sand and Pebbles</option>
                        <option value="loam-with-gravel">Loam with Gravel</option>
                        <option value="clay-with-gravel">Clay with Gravel</option>
                        <option value="gravel-with-pebbles">Gravel with Pebbles</option>
                        <option value="pebbles-with-boulders-included">Pebbles with Boulders Included</option>
                        <option value="conglomerate">Conglomerate</option>
                        <option value="coarse-gravel">Coarse Gravel</option>
                        <option value="sandy-loam-2">Sandy Loam</option>
                        <option value="sand-with-sandy-loam-and-clay">Sand with Sandy Loam and Clay</option>
                        <option value="sand-including-gravel-and-loam">Sand Including Gravel and Loam</option>
                        <option value="loam-with-sandy-loam">Loam with Sandy Loam</option>
                        <option value="sand-with-sandy-loam">Sand with Sandy Loam</option>
                        <option value="loam-including-pebbles">Loam Including Pebbles</option>
                        <option value="limestone-with-gypsum-interlayer">Limestone with Gypsum Interlayer</option>
                        <option value="sand-with-loam-and-clay">Sand with Loam and Clay</option>
                        <option value="sandstone-with-siltstone">Sandstone with Siltstone</option>
                        <option value="sandstone">Sandstone</option>
                        <option value="siltstone">Siltstone</option>
                        <option value="limestone">Limestone</option>
                        <option value="gravel">Gravel</option>
                      </select>
                      <button class="btn btn-outline-danger deleteRow" type="button">
                        Del
                      </button>
                  </div>
                </div>
                
              </div>
            </div>
          </div>
          <div class="col-12 col-lg-6" style="height: 88vh">
            <div class="card rounded-2 h-100 mb-0" id="captureZone">
              <div class="card-body">
                <div class="row my-3 text-center blue"><h1>Litologik Kesma</h1></div>
                <div class="row d-flex justify-content-center">
                  <div class="d-flex" >
                    <svg id="well-svg" class="well-container overflow-visible mx-auto p-5" xmlns="http://www.w3.org/2000/svg" width="250" height="500">
                      <!-- SVG patterns and well visualization will go here -->

                    </svg>
                  </div>
                </div>
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
  import ModalAlert from '@/components/ModalAlert.vue';
  import { getDistricts, getRegions } from '@/api/common';
  import { addNewWell, getNewWellForm, getWells } from '@/api/geo';
  import { ref } from 'vue';
  import domtoimg from '@/assets/js/dom-to-img.js';
  
  
  export default {
    components: {
      ModalAlert
    },
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
          x: null,
          y: null
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
      wellsData() {
        return this.wells.length > 0 ? this.wells.map(well => ({ 
          number: well.number, 
          station: well?.station ? well?.station.name : this.noInfoMessage, 
          region: well?.region ? well?.region.name : this.noInfoMessage,
          district: well?.district ? well?.district.name : this.noInfoMessage,
          progress: 30
        })) : [];
      }
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
      captureSVG() {
        domtoimg.toPng(document.getElementById('captureZone'))
          .then(dataUrl => {
            const downloadLink = document.createElement('a');
            downloadLink.href = dataUrl;
            downloadLink.download = 'well-lithology.png';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

          })
          .catch(error => {
            console.error('Error capturing element:', error);
          });
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
            this.modalAlert.openModal();
            this.modalDesc = `Xato xabari: ${error.message}<br>Url: ${error.config.url}`;
            this.modalType = 'danger';
            this.modalOnCloseFunc = () => {};
          }
        }
      },
      navigateToGeoSingle(item) {
        this.$router.push({ name: "GeoSingle", params: { number: item.number } });
      },
    },
    
    async mounted() {
      const wellHeightInput = document.getElementById('well-height');
      const addIntervalButton = document.getElementById('add-interval');
      const lithologyInputs = document.getElementById('lithology-inputs');
      let deleteRowButton = document.querySelectorAll('.deleteRow');
      const wellSvg = document.getElementById('well-svg');

      let intervalCount = 1;

      function addInterval() {
          const newRow = document.createElement('div');
          newRow.className = 'lithology-row input-group mb-3';
          newRow.innerHTML = `

              <label for="depth-start-${intervalCount}" class="input-group-text">Dan (m):</label>
              <input type="number" class="form-control" id="depth-start-${intervalCount}" name="depth-start" min="0" max="100" value="0" />
              <label class="input-group-text" for="depth-end-${intervalCount}">Gacha (m):</label>
              <input type="number" class="form-control" id="depth-end-${intervalCount}" name="depth-end" min="0" max="100" value="0" />
              <label class="input-group-text" for="pattern-${intervalCount}">Element:</label>
              <select class="form-control" id="pattern-${intervalCount}" name="pattern">
                  <option value="loam">Loam</option>
                  <option value="sandy-loam">Sandy Loam</option>
                  <option value="clay">Clay</option>
                  <option value="sandy-gravel">Sandy Gravel</option>
                  <option value="pebble-and-gravel">Pebble and Gravel</option>
                  <option value="pebbly">Pebbly</option>
                  <option value="boulder-pebble">Boulder-Pebble</option>
                  <option value="sand">Sand</option>
                  <option value="gravel-with-gravel-and-sand">Gravel with Gravel and Sand</option>
                  <option value="sand-with-gravel">Sand with Gravel</option>
                  <option value="loam-with-clay">Loam with Clay</option>
                  <option value="loamy-sand">Loamy Sand</option>
                  <option value="gravel-with-sand-and-pebbles">Gravel with Sand and Pebbles</option>
                  <option value="loam-with-gravel">Loam with Gravel</option>
                  <option value="clay-with-gravel">Clay with Gravel</option>
                  <option value="gravel-with-pebbles">Gravel with Pebbles</option>
                  <option value="pebbles-with-boulders-included">Pebbles with Boulders Included</option>
                  <option value="conglomerate">Conglomerate</option>
                  <option value="coarse-gravel">Coarse Gravel</option>
                  <option value="sandy-loam-2">Sandy Loam</option>
                  <option value="sand-with-sandy-loam-and-clay">Sand with Sandy Loam and Clay</option>
                  <option value="sand-including-gravel-and-loam">Sand Including Gravel and Loam</option>
                  <option value="loam-with-sandy-loam">Loam with Sandy Loam</option>
                  <option value="sand-with-sandy-loam">Sand with Sandy Loam</option>
                  <option value="loam-including-pebbles">Loam Including Pebbles</option>
                  <option value="limestone-with-gypsum-interlayer">Limestone with Gypsum Interlayer</option>
                  <option value="sand-with-loam-and-clay">Sand with Loam and Clay</option>
                  <option value="sandstone-with-siltstone">Sandstone with Siltstone</option>
                  <option value="sandstone">Sandstone</option>
                  <option value="siltstone">Siltstone</option>
                  <option value="limestone">Limestone</option>
                  <option value="gravel">Gravel</option>
              </select>
              <button class="btn btn-outline-danger deleteRow" type="button">Del</button>
          `;
          lithologyInputs.appendChild(newRow);
          deleteRowButton = document.querySelectorAll('.deleteRow')
          intervalCount++;
      }

      function removeLithologyRow(button) {
          // Find the parent element with class 'lithology-row' and remove it
          const row = button.closest('.lithology-row');
          if (row) {
              // row.remove();
              lithologyInputs.removeChild(row)
          }
      }

      function enforceMinMax(el) {
          if (el.value != "") {
            if (parseInt(el.value) < parseInt(el.min)) {
              el.value = el.min;
            }
            if (parseInt(el.value) > parseInt(el.max)) {
              el.value = el.max;
            }
          }
        }

      function drawWell() {
          const wellHeight = parseFloat(wellHeightInput.value);
          wellSvg.setAttribute('height', wellHeight*5);

          // Clear the existing SVG elements
          wellSvg.innerHTML = `
          
          <rect x="0" y="0" width="100" height="500" fill="none" stroke="black" stroke-width="1"></rect>
          <g font-size="10" fill="black">
              <!-- Labels and lines for scale -->
              <!-- Scale from 0 to 100 in steps of 10 -->
              <line x1="0" y1="0" x2="-20" y2="0" stroke="black" stroke-width="1"></line>
              <text x="-25" y="4" text-anchor="middle">0</text>

              <line x1="0" y1="25" x2="-10" y2="25" stroke="black" stroke-width="1"></line>
              
              <line x1="0" y1="50" x2="-20" y2="50" stroke="black" stroke-width="1"></line>
              <text x="-27" y="54" text-anchor="middle">10</text>

              <line x1="0" y1="75" x2="-10" y2="75" stroke="black" stroke-width="1"></line>
              
              <line x1="0" y1="100" x2="-20" y2="100" stroke="black" stroke-width="1"></line>
              <text x="-27" y="104" text-anchor="middle">20</text>

              <line x1="0" y1="125" x2="-10" y2="125" stroke="black" stroke-width="1"></line>
              
              <line x1="0" y1="150" x2="-20" y2="150" stroke="black" stroke-width="1"></line>
              <text x="-27" y="154" text-anchor="middle">30</text>

              <line x1="0" y1="175" x2="-10" y2="175" stroke="black" stroke-width="1"></line>
              
              <line x1="0" y1="200" x2="-20" y2="200" stroke="black" stroke-width="1"></line>
              <text x="-27" y="204" text-anchor="middle">40</text>

              <line x1="0" y1="225" x2="-10" y2="225" stroke="black" stroke-width="1"></line>

              <line x1="0" y1="250" x2="-20" y2="250" stroke="black" stroke-width="1"></line>
              <text x="-27" y="254" text-anchor="middle">50</text>

              <line x1="0" y1="275" x2="-10" y2="275" stroke="black" stroke-width="1"></line>

              <line x1="0" y1="300" x2="-20" y2="300" stroke="black" stroke-width="1"></line>
              <text x="-27" y="304" text-anchor="middle">60</text>

              <line x1="0" y1="325" x2="-10" y2="325" stroke="black" stroke-width="1"></line>

              <line x1="0" y1="350" x2="-20" y2="350" stroke="black" stroke-width="1"></line>
              <text x="-27" y="354" text-anchor="middle">70</text>

              <line x1="0" y1="375" x2="-10" y2="375" stroke="black" stroke-width="1"></line>

              <line x1="0" y1="400" x2="-20" y2="400" stroke="black" stroke-width="1"></line>
              <text x="-27" y="404" text-anchor="middle">80</text>

              <line x1="0" y1="425" x2="-10" y2="425" stroke="black" stroke-width="1"></line>

              <line x1="0" y1="450" x2="-20" y2="450" stroke="black" stroke-width="1"></line>
              <text x="-27" y="454" text-anchor="middle">90</text>

              <line x1="0" y1="475" x2="-10" y2="475" stroke="black" stroke-width="1"></line>            

              <line x1="0" y1="500" x2="-20" y2="500" stroke="black" stroke-width="1"></line>
              <text x="-30" y="504" text-anchor="middle">100</text>

          </g>
          `;
                    
          


          const intervals = document.querySelectorAll('.lithology-row');
          intervals.forEach(row => {
              
              const depthStart = parseFloat(row.querySelector('input[name="depth-start"]').value);
              const depthEnd = parseFloat(row.querySelector('input[name="depth-end"]').value);
              const pattern = row.querySelector('select[name="pattern"]').value;
              const pattern_name = row.querySelector('select[name="pattern"]').options[row.querySelector('select[name="pattern"]').selectedIndex].text;

              const lithologyColors = {
                "loam": "hsl(0,70%,60%)",
                "sandy-loam": "hsl(11,70%,60%)",
                "clay": "hsl(23,70%,60%)",
                "sandy-gravel": "hsl(34,70%,60%)",
                "pebble-and-gravel": "hsl(45,70%,60%)",
                "pebbly": "hsl(56,70%,60%)",
                "boulder-pebble": "hsl(68,70%,60%)",
                "sand": "hsl(79,70%,60%)",
                "gravel-with-gravel-and-sand": "hsl(90,70%,60%)",
                "sand-with-gravel": "hsl(101,70%,60%)",
                "loam-with-clay": "hsl(112,70%,60%)",
                "loamy-sand": "hsl(124,70%,60%)",
                "gravel-with-sand-and-pebbles": "hsl(135,70%,60%)",
                "loam-with-gravel": "hsl(146,70%,60%)",
                "clay-with-gravel": "hsl(158,70%,60%)",
                "gravel-with-pebbles": "hsl(169,70%,60%)",
                "pebbles-with-boulders-included": "hsl(180,70%,60%)",
                "conglomerate": "hsl(191,70%,60%)",
                "coarse-gravel": "hsl(203,70%,60%)",
                "sandy-loam-2": "hsl(214,70%,60%)",
                "sand-with-sandy-loam-and-clay": "hsl(225,70%,60%)",
                "sand-including-gravel-and-loam": "hsl(236,70%,60%)",
                "loam-with-sandy-loam": "hsl(247,70%,60%)",
                "sand-with-sandy-loam": "hsl(259,70%,60%)",
                "loam-including-pebbles": "hsl(270,70%,60%)",
                "limestone-with-gypsum-interlayer": "hsl(281,70%,60%)",
                "sand-with-loam-and-clay": "hsl(292,70%,60%)",
                "sandstone-with-siltstone": "hsl(304,70%,60%)",
                "sandstone": "hsl(315,70%,60%)",
                "siltstone": "hsl(327,70%,60%)",
                "limestone": "hsl(338,70%,60%)",
                "gravel": "hsl(349,70%,60%)"
              };
              
              const rectHeight = ((depthEnd - depthStart) / wellHeight) * wellSvg.clientHeight;

              // Create the SVG pattern
              const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
              const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
              const text_val = document.createElementNS('http://www.w3.org/2000/svg', 'text');
              const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                  // eslint-disable-next-line
                  if (isNaN(depthStart) || isNaN(wellHeight) || isNaN(rectHeight)) {
                      
                  } else {
                      rect.setAttribute('x', 0);
                      rect.setAttribute('y', (depthStart / wellHeight) * wellSvg.clientHeight);
                      rect.setAttribute('width', 100);
                      rect.setAttribute('height', rectHeight);
                      rect.setAttribute('fill', lithologyColors[pattern]);
                      console.log(rect);
                      
                      wellSvg.appendChild(rect);
                  
                      line.setAttribute('x1', 0);
                      line.setAttribute('y1', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight);
                      line.setAttribute('x2', wellSvg.clientWidth - 60);
                      line.setAttribute('y2', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight);
                      line.setAttribute('stroke', 'black');
                      line.setAttribute('stroke-width', 1);
                      wellSvg.appendChild(line);
                  
                      text_val.setAttribute('x', 210);
                      text_val.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight + 5);
                      text_val.setAttribute('text-anchor', 'middle');
                      text_val.textContent = depthEnd; // Replace with dynamic name if needed
                      wellSvg.appendChild(text_val);
                  
                      // Add the well name at the bottom
                      text.setAttribute('x', 150);
                      text.setAttribute('y', rectHeight + (depthStart / wellHeight) * wellSvg.clientHeight - 5);
                      text.setAttribute('text-anchor', 'middle');
                      text.textContent = pattern_name; // Replace with dynamic name if needed
                      wellSvg.appendChild(text);
                  }
              
                  
              
              
          });
      }

      wellHeightInput.addEventListener('input', drawWell);
      lithologyInputs.addEventListener('input', e => {
          drawWell();
          console.log(e);
          
          enforceMinMax(e);
      });
      // eslint-disable-next-line
      deleteRowButton.forEach(el => el.addEventListener('click', event => {
          drawWell();
          removeLithologyRow(el);
      }));
      // eslint-disable-next-line
      addIntervalButton.addEventListener('click', event => {
          addInterval();
          // eslint-disable-next-line
          deleteRowButton.forEach(el => el.addEventListener('click', event => {
              drawWell();
              removeLithologyRow(el);
          }));
      });

      drawWell();  // Initial draw

      try {
        this.wells = await getWells();
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