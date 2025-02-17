import { createRouter, createWebHistory } from "vue-router";
import { getMe } from "@/api/auth";
import { store } from "@/store";
import Login from "@/views/LoginView.vue";
import HomeView from "@/views/HomeView.vue";
import PageNotFound from "@/layout/PageNotFound.vue";
import ServerError from "@/layout/ServerError.vue";

const routes = [
  { path: "/", name: "HomeView", component: HomeView, meta: { auth: true, layout: 'main' } },
  { path: "/login", name: "Login", component: Login, meta: { auth: false, layout: 'empty' } },
  { path: "/geo", name: "Geo", component: () => import("../views/GeoView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/geo/:number(\\d+)", name: "GeoSingle", component: () => import("../views/GeoSingleView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/melio/:number(\\d+)", name: "MelioSingle", component: () => import("../views/MelioSingleView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/melio", name: "Melio", component: () => import("../views/MelioView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/meteo", name: "Meteo", component: () => import("../views/MeteoView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/500", component: ServerError },
  { path: "/lithology", component: () => import("../views/LithologyView.vue"), meta: { auth: true, layout: 'main' } },
  { path: "/:pathMatch(.*)*", component: PageNotFound }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.meta.auth) {
    try {
      // If user is already in the store, you may want to skip the API call
      if (!store.user.name) {
        const response = await getMe();
        store.user.name = response.full_name;
      }
      next();
    } catch (error) {
      // Redirect if unauthorized or any other error occurs
      if (error.response && error.response.status === 401) {
        if (to.path !== '/login') {
          return next('/login');
        }
      }
      return next('/500');
    }
  } else {
    next();
  }
});

export default router;
