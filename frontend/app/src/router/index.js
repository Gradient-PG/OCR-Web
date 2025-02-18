import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import InstructionView from '../views/InstructionView.vue'
import AgreementView from '../views/AgreementView.vue'
import MarkView from '../views/MarkView.vue'
import ThanksView from '../views/ThanksView.vue'
import Error404 from '../views/Error404View.vue'
import AdminPanel from '../views/AdminPanel.vue'
import CardsPanel from "@/views/CardsPanel.vue";
import CardView from "@/views/CardView.vue";
import WelcomeView from '@/views/WelcomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: WelcomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/instruction',
      name: 'instruction',
      component: InstructionView,
    },
    {
      path: '/agreement',
      name: 'agreement',
      component: AgreementView,
    },
    {
      path: '/marking',
      name: 'marking',
      component: MarkView,
    },
    {
      path: '/thanks',
      name: 'thanks',
      component: ThanksView,
    },
    {
      path: '/404',
      name: '404',
      component: Error404,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel,
    },
    {
      path: '/cards-panel',
      name: 'cards',
      component: CardsPanel,
    },
    {
      path: '/card/:imageCode',
      name: 'card',
      component: CardView,
      props: true
    }
  ],
})

export default router
