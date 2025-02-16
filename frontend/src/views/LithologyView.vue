<template>  
  
    <div class="page-body">
      <div class="container-xl">
  
        <div class="row">
          <!-- Left panel: controls and lithology inputs -->
          <div class="col-12 col-lg-6" style="height: 88vh">
            <div class="card rounded-2 h-100 mb-0 overflow-hidden">
              <div class="card-body d-flex flex-column">
                <!-- Well selection -->
                <div class="row mb-3">
                  <label for="id_well" class="col-sm-6 col-form-label">
                    Kuzatuv-burg'u qudug'i raqami
                  </label>
                  <div class="col-sm-6 d-flex align-items-center">
                    <select class="form-control well_select" id="id_well" name="well" required>
                      <option value="-1">---------</option>
                      <option
                        v-for="well in wellsData"
                        :value="well.number"
                        :key="well.number"
                      >
                        {{ well.number }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- Buttons and well height (hidden) -->
                <div class="mb-3 w-100 d-flex">
                  <!-- Note: wellHeight is bound via v-model -->
                  <input
                    type="number"
                    id="well-height"
                    name="well-height"
                    min="0"
                    v-model.number="wellHeight"
                    hidden
                  />
                  <button class="btn btn-primary" id="download-png" @click="captureSVG">
                    Yuklab olish
                  </button>
                  <button class="btn btn-primary ms-auto btn-icon" id="add-interval" @click="addInterval">
                    <IconPlus />
                  </button>
                </div>

                <!-- Lithology inputs -->
                <div id="lithology-inputs">
                  <div
                    class="lithology-row input-group mb-3"
                    v-for="(interval, index) in intervals"
                    :key="interval.id"
                  >
                    <label
                      :for="`depth-start-${interval.id}`"
                      class="input-group-text"
                    >
                      Dan (m):
                    </label>
                    <input
                      type="number"
                      class="form-control"
                      :id="`depth-start-${interval.id}`"
                      name="depth-start"
                      min="0"
                      max="100"
                      v-model.number="interval.depthStart"
                      @input="drawWell"
                    />

                    <label
                      class="input-group-text"
                      :for="`depth-end-${interval.id}`"
                    >
                      Gacha (m):
                    </label>
                    <input
                      type="number"
                      class="form-control"
                      :id="`depth-end-${interval.id}`"
                      name="depth-end"
                      min="0"
                      max="100"
                      v-model.number="interval.depthEnd"
                      @input="drawWell"
                    />

                    <label
                      class="input-group-text"
                      :for="`pattern-${interval.id}`"
                    >
                      Element:
                    </label>
                    <select
                      class="form-control"
                      :id="`pattern-${interval.id}`"
                      name="pattern"
                      v-model="interval.pattern"
                      @change="drawWell"
                    >
                      <option
                        v-for="element in lithologyElements"
                        :value="element.id"
                        :key="element.id"
                      >
                        {{ element.name }}
                      </option>
                    </select>

                    <button
                      class="btn btn-outline-danger btn-icon"
                      type="button"
                      @click="removeInterval(index)"
                    >
                      <IconTrash stroke="1" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right panel: SVG drawing -->
          <div class="col-12 col-lg-6" style="height: 88vh">
            <div class="card rounded-2 h-100 mb-0" id="captureZone">
              <div class="card-body">
                <div class="row my-3 text-center blue">
                  <h1>Litologik Kesma</h1>
                </div>
                <div class="row d-flex justify-content-center">
                  <div class="d-flex">
                    <!-- Use ref to get the SVG element in the script -->
                    <svg
                      ref="wellSvg"
                      id="well-svg"
                      class="well-container overflow-visible mx-auto p-5"
                      xmlns="http://www.w3.org/2000/svg"
                      width="250"
                      :height="wellHeight * 5"
                    >
                      <!-- SVG drawing is handled dynamically in drawWell() -->
                    </svg>
                  </div>
                  <!-- Include additional component for lithology SVG elements if needed -->
                  <LithologyElementsSVG />
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
  import LithologyElementsSVG from '@/lithology/LithologyElementsSVG.vue';
  import { lithologyElements } from '@/lithology/elements';
  import { IconTrash, IconPlus } from '@tabler/icons-vue';

  export default {
    components: {
      ModalAlert,
      LithologyElementsSVG,
      IconTrash,
      IconPlus
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
        noInfoMessage: '------',
        lithologyElements: lithologyElements,


        // LITHOLOGY DRAW
        wellHeight: 100,
        // Array of lithology intervals; each interval has a unique id, start/end depths, and a pattern
        intervals: [
          {
            id: 0,
            depthStart: 0,
            depthEnd: 0,
            pattern: "loam", // default pattern (should match one of the lithologyElements id values)
          },
        ],
        // This counter is used to give each new interval a unique id
        nextIntervalId: 1,
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


      // LITHOLOGY DRAW
      addInterval() {
        this.intervals.push({
          id: this.nextIntervalId,
          depthStart: this.intervals[this.intervals.length - 1]?.depthEnd || 0,
          depthEnd: 0,
          pattern: this.lithologyElements[0].id,
        });
        this.nextIntervalId++;
        this.drawWell();
      },
      // Removes the interval at the given index
      removeInterval(index) {
        this.intervals.splice(index, 1);
        this.drawWell();
      },
      // Draws (or redraws) the well SVG based on the well height and current intervals
      drawWell() {
        const wellSvg = this.$refs.wellSvg;
        if (!wellSvg) return;

        // Calculate the SVG height (we use a 5× scale of the wellHeight)
        const svgHeight = this.wellHeight * 5;
        wellSvg.setAttribute("height", svgHeight);

        // Clear any previous content
        while (wellSvg.firstChild) {
          wellSvg.removeChild(wellSvg.firstChild);
        }

        // --- Background Rectangle ---
        const bgRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        bgRect.setAttribute("x", "0");
        bgRect.setAttribute("y", "0");
        bgRect.setAttribute("width", "100");
        bgRect.setAttribute("height", svgHeight);
        bgRect.setAttribute("fill", "none");
        bgRect.setAttribute("stroke", "black");
        bgRect.setAttribute("stroke-width", "1");
        wellSvg.appendChild(bgRect);

        // --- Dynamically Generated Scale ---
        // We'll divide the SVG into 20 equal segments (minor ticks).
        // Every even tick (i=0,2,4,...) will be a major tick with a longer line and a label.
        const scaleGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
        scaleGroup.setAttribute("font-size", "10");
        scaleGroup.setAttribute("fill", "black");

        const numMinorTicks = 20;
        const step = svgHeight / numMinorTicks;
        for (let i = 0; i <= numMinorTicks; i++) {
          const y = i * step;
          const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
          line.setAttribute("x1", "0");
          line.setAttribute("y1", y);
          line.setAttribute("y2", y);
          // Even ticks (major) get a longer line (x2 = -20)
          // Odd ticks (minor) get a shorter line (x2 = -10)
          line.setAttribute("x2", i % 2 === 0 ? "-20" : "-10");
          line.setAttribute("stroke", "black");
          line.setAttribute("stroke-width", "1");
          scaleGroup.appendChild(line);

          // On every major tick, add a text label.
          if (i % 2 === 0) {
            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            // Calculate label value (e.g., if wellHeight = 100, then i=2 => (2/20)*100 = 10)
            const labelValue = (i / numMinorTicks) * this.wellHeight;
            text.textContent = labelValue;
            // Position the label slightly to the left (x) and a few units down from the tick (y)
            text.setAttribute("x", "-30");
            text.setAttribute("y", y + 4);
            text.setAttribute("text-anchor", "middle");
            scaleGroup.appendChild(text);
          }
        }
        wellSvg.appendChild(scaleGroup);
        // Draw each lithology interval on the SVG
        this.intervals.forEach((interval) => {
          const { depthStart, depthEnd, pattern } = interval;
          // Skip drawing if any value is not a valid number
          if (
            isNaN(depthStart) ||
            isNaN(depthEnd) ||
            isNaN(this.wellHeight)
          ) {
            return;
          }
          const svgHeight = wellSvg.clientHeight;
          // Calculate rectangle height and y-position based on well height and input depths
          const rectHeight = ((depthEnd - depthStart) / this.wellHeight) * svgHeight;
          const rectY = (depthStart / this.wellHeight) * svgHeight;

          // Look up the lithology name from the list based on the selected pattern
          const selectedElement = this.lithologyElements.find(
            (el) => el.id === pattern
          );
          const patternName = selectedElement ? selectedElement.name : "";

          // Create a rectangle to represent the lithology interval
          const rect = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "rect"
          );
          rect.setAttribute("x", 0);
          rect.setAttribute("y", rectY);
          rect.setAttribute("width", 100);
          rect.setAttribute("height", rectHeight);
          // Assume an SVG pattern with id equal to the pattern string exists
          rect.setAttribute("fill", `url(#${pattern})`);
          wellSvg.appendChild(rect);

          // Add text for the lithology element name
          const textElem = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
          );
          textElem.textContent = patternName;
          wellSvg.appendChild(textElem);
          const width = textElem.getBBox().width;
          textElem.setAttribute("x", 105 + width);
          textElem.setAttribute("y", rectY + rectHeight - 5);
          textElem.setAttribute("text-anchor", "end");

          // Add text showing the depthEnd value
          const textVal = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
          );
          textVal.textContent = depthEnd;
          wellSvg.appendChild(textVal);
          const widthVal = textVal.getBBox().width;
          textVal.setAttribute("x", 115 + width + widthVal);
          textVal.setAttribute("y", rectY + rectHeight + 5);
          textVal.setAttribute("text-anchor", "end");

          
          const line = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "line"
          );
          line.setAttribute("x1", 0);
          line.setAttribute("x2", 110 + width);
          line.setAttribute("y1", rectY + rectHeight);
          line.setAttribute("y2", rectY + rectHeight);
          line.setAttribute("stroke", "black");
          line.setAttribute("stroke-width", 1);
          wellSvg.appendChild(line);
        });
      },
    },
    
    async mounted() {
      this.drawWell();

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
    watch: {
    // Redraw whenever wellHeight changes.
      wellHeight() {
        this.drawWell();
      },
      // Use a deep watch to catch changes inside each interval.
      intervals: {
        handler() {
          this.drawWell();
        },
        deep: true,
      },
    },
  }
  
  </script>