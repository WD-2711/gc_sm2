import { createRouter, createWebHashHistory } from "vue-router";

import DashboardLayout from "@/layout/DashboardLayout";
import AuthLayout from "@/layout/AuthLayout";

import Login from "../views/Login.vue";
import Basic from "../views/Basic.vue";

const routes = [
    {
        path: "/",
        redirect: "/login",
        component: AuthLayout,
        children: [
          {
            path: "/login",
            name: "login",
            components: { default: Login },
          }
        ],
    },
    {
      path: "/",
      redirect: "dashboard",
      component: DashboardLayout,
      children: [
        {
          path: "/dashboard",
          name: "dashboard",
          components: { default: Basic },
        },
      ],
    },

  ];
  
const router = createRouter({
    history: createWebHashHistory(),
    linkActiveClass: "active",
    routes,
  });
  
  export default router;