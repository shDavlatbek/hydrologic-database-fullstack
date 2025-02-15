import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/LoginView.vue";
import HomeView from "../views/HomeView.vue";
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

export default router;
