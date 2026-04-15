import { createRouter, createWebHistory } from 'vue-router'
import TaskList from '../views/TaskList.vue'
import TaskSubmit from '../views/TaskSubmit.vue'
import TaskDetail from '../views/TaskDetail.vue'
import DatasetList from '../views/DatasetList.vue'

const routes = [
  {
    path: '/',
    name: 'TaskList',
    component: TaskList
  },
  {
    path: '/submit',
    name: 'TaskSubmit',
    component: TaskSubmit
  },
  {
    path: '/task/:id',
    name: 'TaskDetail',
    component: TaskDetail
  },
  {
    path: '/datasets',
    name: 'DatasetList',
    component: DatasetList
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
