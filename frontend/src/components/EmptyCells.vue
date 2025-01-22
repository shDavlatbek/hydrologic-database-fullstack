<script setup>
import RemoveRowButton from '@/components/RemoveRowButton.vue';
import { defineProps } from 'vue';

defineProps({
  param_names: {
    type: Array,
    required: true
  }
});
</script>

<template>
  <tr>
        <td v-for="one in param_names.slice(0, -1)" :key="one.key">
          <input type="text" class="form-control form-control-sm" />
        </td>
        <RemoveRowButton />
      </tr>
</template>