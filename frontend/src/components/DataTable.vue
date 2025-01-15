<template>
  
  <div class="card"> 
    <!-- Search Filter -->
    <div class="card-body border-bottom py-3">
        <div class="d-flex">
          <div class="text-secondary">
            <div class="mx-2 d-inline-block">
              <select v-model="perPage" class="form-control form-control-sm">
                <option :value="5">{{ text.perPageText.replace('$perPage', 5) }}</option>
                <option :value="10">{{ text.perPageText.replace('$perPage', 10) }}</option>
                <option :value="20">{{ text.perPageText.replace('$perPage', 20) }}</option>
              </select>
            </div>
            {{ text.perPageOptionText.replace('$perPage', perPage) }}
          </div>
          <div class="ms-auto text-secondary">
            {{ text.search }}
            <div class="ms-2 d-inline-block">
              <input
                v-model="searchQuery"
                class="form-control form-control-sm"
                @input="handleSearch"
              />
            </div>
          </div>
        </div>
      </div>

    <!-- Table -->
    <div class="table-responsive">
      <table class="table card-table table-vcenter text-nowrap datatable">
        <!-- Sticky Header -->
        <thead class="sticky-top">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              @click="sortBy(column.key)"
            >
              <button class="table-sort" :class="{asc: sortDirection === 'asc' && sortColumn === column.key, desc: sortDirection === 'desc' && sortColumn === column.key}">
                {{ column.label }}
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="paginatedData.length">
            <tr v-for="(item, index) in paginatedData" :key="index" :class="{'table-row': onRowClick}" @click="onRowClick && onRowClick(item)">
              <td
                v-for="column in columns"
              :key="column.key"
            >
              {{ item[column.key] }}
              </td>
            </tr>
          </template>
          <template v-else>
            <tr>
              <td :colspan="columns.length" class="text-center">
                <template v-if="searchQuery">
                  {{ noSearchResultsText }}
                </template>
                <template v-else>
                  {{ noDataText }}
                </template>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div class="card-footer d-flex align-items-center">
      <p class="m-0 text-secondary">
        {{ 
          text.dataPerPage
            .replace('$data', filteredData.length)
            .replace('$from', (currentPage - 1) * perPage + 1)
            .replace('$to', (currentPage - 1) * perPage + paginatedData.length) 
        }}
      </p>
      <ul class="pagination m-0 ms-auto">
        <li class="page-item me-2" :class="{disabled: currentPage === 1}">
          <span class="page-link" tabindex="-1" aria-disabled="true" @click="changePage(currentPage - 1)">
            <!-- Left Arrow -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon">
              <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M15 6l-6 6l6 6" />
            </svg>
            {{ text.previous }}
          </span>
        </li>

        <!-- First Page -->
        <li class="page-item" v-if="paginationRange.includes(1) && paginationRange[0] !== 1">
          <span class="page-link" @click="changePage(1)">1</span>
        </li>
        <li class="page-item disabled" v-if="paginationRange[0] > 2">
          <span class="page-link">...</span>
        </li>

        <!-- Dynamic Page Numbers -->
        <li class="page-item" 
            :class="{active: currentPage === page}" 
            v-for="page in paginationRange" 
            :key="page">
          <span class="page-link" @click="changePage(page)">{{ page }}</span>
        </li>

        <!-- Last Page -->
        <li class="page-item disabled" v-if="paginationRange[paginationRange.length - 1] < totalPages - 1">
          <span class="page-link">...</span>
        </li>
        <li class="page-item" v-if="!paginationRange.includes(totalPages)">
          <span class="page-link" @click="changePage(totalPages)">{{ totalPages }}</span>
        </li>

        <li class="page-item ms-2" :class="{disabled: currentPage === totalPages || totalPages === 0}">
          <span class="page-link" tabindex="-1" aria-disabled="true" @click="changePage(currentPage + 1)">
            {{ text.next }}
            <!-- Right Arrow -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon">
              <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 6l6 6l-6 6" />
            </svg>
          </span>
        </li>
      </ul>

      </div>
  </div>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    // Data array to display in the table
    data: {
      type: Array,
      required: true
    },
    // Column configuration
    columns: {
      type: Array,
      required: true,
      // Example: [{ key: 'name', label: 'Name' }, { key: 'age', label: 'Age' }]
    },
    onRowClick: {
      type: Function,
      required: false,
    },
    noDataText: {
      type: String,
      required: false,
      default: 'Ma\'lumotlar topilmadi'
    },
    noSearchResultsText: {
      type: String,
      required: false,
      default: 'Bunday ma\'lumotlar topilmadi'
    },
  },
  data() {
    return {
      searchQuery: '',
      sortColumn: '',
      sortDirection: null,
      currentPage: 1,
      perPage: 10,
      filteredData: [],
      text: {
        first: 'chi bo\'lib',
        second: 'chidan',
        previous: 'Oldingi',
        next: 'Keyingi',
        perPageOptionText: '$perPage ma\'lumotlar sahifasida',
        perPageText: '$perPage ta',
        search: 'Qidiruv:',
        noData: 'Ma\'lumotlar topilmadi',
        noSearchResults: 'Bunday ma\'lumotlar topilmadi',
        dataPerPage: '$data ta ma\'lumotdan $from dan $to gacha ko\'rsatilmoqda',
      }
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredData.length / this.perPage)
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.perPage
      const end = start + this.perPage
      return this.filteredData.slice(start, end)
    },
    paginationRange() {
      const totalNumbers = 5; // Total numbers to display excluding first/last and ellipses
      const sideNumbers = 2; // Numbers to show before and after the current page
      const range = [];

      if (this.totalPages <= totalNumbers) {
        // If total pages are less than or equal to totalNumbers, show all pages
        for (let i = 1; i <= this.totalPages; i++) {
          range.push(i);
        }
      } else {
        // Calculate the range dynamically
        let start = Math.max(this.currentPage - sideNumbers, 2);
        let end = Math.min(this.currentPage + sideNumbers, this.totalPages - 1);

        // Adjust the range if close to the edges
        if (this.currentPage - sideNumbers <= 1) {
          start = 2;
          end = totalNumbers - 1;
        } else if (this.currentPage + sideNumbers >= this.totalPages) {
          start = this.totalPages - totalNumbers + 2;
          end = this.totalPages - 1;
        }

        range.push(1); // Always include the first page

        if (start > 2) {
          range.push('...'); // Ellipsis before the range
        }

        for (let i = start; i <= end; i++) {
          range.push(i);
        }

        if (end < this.totalPages - 1) {
          range.push('...'); // Ellipsis after the range
        }

        range.push(this.totalPages); // Always include the last page
      }

      return range;
    }
  },
  methods: {
    handleSearch() {
      this.currentPage = 1
      this.filterData()
    },
    filterData() {
      if (!Array.isArray(this.data)) {
        this.filteredData = []
        return
      }

      if (!this.searchQuery) {
        this.filteredData = [...this.data]
      } else {
        const query = this.searchQuery.toLowerCase()
        this.filteredData = this.data.filter(item =>
          Object.values(item).some(
            value =>
              value &&
              value.toString().toLowerCase().includes(query)
          )
        )
      }
      this.sortData()
    },
    sortBy(column) {
      if (this.sortColumn === column) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortColumn = column
        this.sortDirection = 'asc'
      }
      this.sortData()
    },
    sortData() {
      if (!this.sortColumn) {
        return
      }
      
      this.filteredData.sort((a, b) => {
        const aValue = a[this.sortColumn]
        const bValue = b[this.sortColumn]
        
        if (this.sortDirection === 'asc') {
          return aValue > bValue ? 1 : -1
        }
        return aValue < bValue ? 1 : -1
      })
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    }
  },
  created() {
    this.filterData()
  },
  watch: {
    data: {
      handler() {
        this.filterData();
      },
      immediate: true
    },
    perPage: {
      handler() {
        this.currentPage = 1;
      },
      immediate: true
    }
  }
}
</script>

<style>
.page-item:not(.disabled) .page-link {
  cursor: pointer;
}
</style>