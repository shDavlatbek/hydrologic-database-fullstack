<template>
    <div class="page">
        <HeaderComponent />
        <div class="page-wrapper">
            <router-view v-slot="{ Component, route }">
                <keep-alive>
                    <component :is="Component" :key="route.path" />
                </keep-alive>
            </router-view>
        </div>
    </div>
</template>

<script>
import HeaderComponent from '@/components/HeaderComponent.vue';

export default {
    name: 'MainLayout',
    components: {
        HeaderComponent
    },
}
</script>