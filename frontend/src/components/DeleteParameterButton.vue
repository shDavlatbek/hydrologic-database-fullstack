<template>
  <button class="btn btn-danger p-0" @click="deleteRow">
    <IconTrash class="icon m-0" stroke="2" />
    {{ props.value }}
  </button>
</template>

<script setup>
import { IconTrash } from '@tabler/icons-vue';
import { defineProps } from 'vue';

const props = defineProps({
  value: {
    type: String,
    required: true
  },
  row: {
    type: Object,
    required: true
  }
});

const deleteRow = () => {
  console.log(props.row);
};
</script>