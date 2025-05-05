import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MainLayout from '../layouts/Main.vue' // layout with sidebar/topbar

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('../views/LogoutView.vue')
    },

    // ✅ Routes wrapped in Main layout
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: 'user-page',
          name: 'user-page',
          component: () => import('../views/UserPage.vue'),
          props: true
        },
        {
          path: 'users/:user_id',
          name: 'user-profile',
          component: () => import('../views/UserProfileView.vue'),
          props: true
        },
        {
          path: 'profiles/new',
          name: 'new-profile',
          component: () => import('../views/NewProfileView.vue')
        },
        {
          path: 'profiles/:profile_id',
          name: 'profile-details',
          component: () => import('../views/ProfileDetailView.vue'),
          props: true
        },
        {
          path: 'profiles/favourites',
          name: 'favourites',
          component: () => import('../views/FavouritesView.vue')
        }
      ]
    }
  ]
})

export default router
