<template>
  <button class="btn btn-danger p-0" @click="deleteRow">
    <IconTrash class="icon m-0" stroke="2" />
  </button>
</template>

<script setup>
import { IconTrash } from '@tabler/icons-vue';
import { defineProps, computed } from 'vue';
import { useRoute } from 'vue-router';
import { deleteParameter } from '@/api/geo';
import { dateWithoutTimezone } from '@/helpers';

const route = useRoute();

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

const deleteRow = async () => {
  // Convert 'YYYY/MM' to datetime
  const dateTime = new Date(`${props.row.date}/01`);
  await deleteParameter(wellNumber.value, dateWithoutTimezone(dateTime));
};


const wellNumber = computed(() => {
  return route.params?.number;
});

</script>