<template>
  <component :is="currentLayout">
  </component>
</template>

<script>
import { getMe } from './api/auth';
import MainLayout from './layout/MainLayout.vue';
import PreloadDiv from './components/PreloadDiv.vue';
import EmptyLayout from './layout/EmptyLayout.vue';
import { store } from './store';

const layout = {
  main: MainLayout,
  empty: EmptyLayout,
};

export default {
  name: 'App',
  data() {
    return {
      currentLayout: PreloadDiv
    };
  },
  async created() {
    // Handle auth-based layout assignment
    await this.setLayout();
  },
  watch: {
    // Watch for route changes and update layout dynamically
    $route: {
      immediate: true,
      handler() {
        this.setLayout();
      },
    },
  },
  methods: {
    async setLayout() {
      this.currentLayout = PreloadDiv;
      // Handle authentication and layout assignment
      if (this.$route.meta.auth) {
        try {
          const response = await getMe();
          store.user.name = response.full_name;
          this.currentLayout = layout[this.$route.meta.layout] || layout['empty'];
        } catch (error) { 
          if (error.response && error.response.status === 401) {
            if (this.$route.path !== '/login') {
              return this.$router.push('/login');
            }
          } else {
            if (this.$route.path !== '/500') {
              return this.$router.push('/500');
            }
          }
        }
      } else {
        this.currentLayout = layout[this.$route.meta.layout] || layout['empty'];
      }
    },
  },
  components: {
    MainLayout,
    PreloadDiv,
    EmptyLayout
  },
};
</script>

<style>
#app{
  position: relative;
  z-index: 1;
}
</style>
