<template>
    <div class="page">
        <HeaderComponent />
        <div class="page-wrapper">
            <keep-alive>
                <router-view />
            </keep-alive>
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