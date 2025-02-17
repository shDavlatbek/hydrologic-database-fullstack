<template>
  <component :is="currentLayout">
    <router-view />
  </component>
</template>

<script>
import MainLayout from './layout/MainLayout.vue';
import EmptyLayout from './layout/EmptyLayout.vue';

export default {
  name: 'App',
  computed: {
    currentLayout() {
      const layoutType = this.$route.meta.layout || 'empty';
      // Map layout names to components
      const layouts = {
        main: MainLayout,
        empty: EmptyLayout,
      };
      return layouts[layoutType] || EmptyLayout;
    },
  },
};
</script>

<style>
#app {
  position: relative;
  z-index: 1;
}
</style>
