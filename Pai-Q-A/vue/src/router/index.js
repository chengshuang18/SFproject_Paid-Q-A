import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import MainPage from '../components/MainPage'
import Chat from '../components/Chat'
import ExamineLogin from '../components/examine/Login'
import ExamineMainPage from '../components/examine/MainPage'
import VisitorMainPage from '../components/visitor/MainPage'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', component: Login },
    { path: '/visitor', component: VisitorMainPage},
    { path: '/main', component: MainPage, meta: {requireAuth: true}},
    { path: '/chat', component: Chat, meta: {requireAuth: true}},
    { path: '/examine', component: ExamineLogin },
    { path: '/examine/main', component: ExamineMainPage},
  ]
})
