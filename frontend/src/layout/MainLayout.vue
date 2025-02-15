<template>
    <div class="page">
        <HeaderComponent />
        <div class="page-wrapper">
            <router-view v-slot="{ Component, route }">
                <keep-alive>
                    <component :is="Component" :key="route.path" />
                </keep-alive>
            </router-view>
            <FooterMain />
        </div>
    </div>
</template>

<script>
import HeaderComponent from '@/components/HeaderComponent.vue';
import FooterMain from '@/components/FooterMain.vue';

export default {
    name: 'MainLayout',
    components: {
        HeaderComponent,
        FooterMain
    },
}

</script>