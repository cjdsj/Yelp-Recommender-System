import { createRouter, createWebHistory } from "vue-router";
const Home = () => import("../views/home.vue");
const showRestaurant = () => import("../views/showRestaurant.vue");
const foodType = () => import("../views/foodType.vue");

const routes = [
  { path: "/", name: "home", component: Home },
  { path: "/home", redirect: "/" },
  { path: "/index", redirect: "/" },
  { path: "/show", name: "show", component: showRestaurant },
  { path: "/food", name: "foodType", component: foodType },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
