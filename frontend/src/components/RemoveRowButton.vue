
<script setup>
import { IconX, IconTrash } from '@tabler/icons-vue'
import { defineEmits } from 'vue'

const emit = defineEmits(['click'])
</script>

<template>
  <td class="text-center p-0 align-middle dropdown">
    <button class="btn btn-sm btn-danger btn-icon rounded-2 p-2" data-bs-toggle="dropdown">
      <IconX class="icon" stroke="2" />
    </button>
    <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
      <div class="card w-100">
        <div class="card-body p-2 m-0 w-100">
          <h3 class="card-title m-0 w-100 d-flex flex-row">Tasdiqlash
            <button class="btn btn-sm btn-danger btn-icon rounded-2 p-2 ms-auto" type="button">
              <IconX class="icon" stroke="2" />
            </button>
            <button class="btn btn-sm btn-secondary btn-icon rounded-2 p-2 ms-1" type="button" @click="emit('click')">
              <IconTrash class="icon" stroke="2" />
            </button>
          </h3>
        </div>
      </div>
    </div>
  </td>
</template>