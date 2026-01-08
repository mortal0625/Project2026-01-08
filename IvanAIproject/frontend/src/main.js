import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import VCalendar from 'v-calendar';
import 'v-calendar/dist/style.css';
import './style.css'
import App from './App.vue'
import BoardView from './views/BoardView.vue'
import CalendarView from './views/CalendarView.vue'

const routes = [
  { path: '/', component: BoardView },
  { path: '/calendar', component: CalendarView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.use(VCalendar, {})
app.mount('#app')
