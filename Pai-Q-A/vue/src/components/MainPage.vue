/* 
 * @Author: hjj 
 * @Date: 2021-08-24 11:14:47 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-16 11:21:43
 */

<template>
<div class="mainbody">
    <div class="app-container">
        <div class="sidebar">
            <ul class="sidebar-list">
                <li class="sidebar-list-item" :class="{active: sideBar == 0}" @click="changeSideBar(0)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-shopping-bag"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                    <span>提问</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 1}" @click="changeSideBar(1)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-inbox"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>
                    <span>回答</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 3}" @click="changeSideBar(3)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bell"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    <span>订单</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 2}" @click="changeSideBar(2)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-filter"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
                    <span>设置</span>
                    </a>
                </li>
            </ul>
            <div class="account-info">
                <div class="account-info-picture">
                  <img :src="userphoto" alt="Account">
                </div>
                <div class="account-info-name">{{userMsg.username}}</div>
                <button class="account-info-more">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-horizontal"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
                </button>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 0">
            <div class="app-content-header">
                <h1 class="app-content-headerText">回答者列表</h1>
                <div>
                  <button class="app-content-headerButton" @click="toChat">
                    <i class="el-icon-chat-square"></i>
                    聊天
                  </button>
                  <button class="app-content-headerButton" @click="reDialog.rechargeVisible = true">
                    <i class="el-icon-bank-card"></i>
                    余额
                  </button>
                </div>
            </div>
            <div class="app-content-actions">
              <input class="search-bar" placeholder="Search..." type="text" v-model="searchName" @keyup.enter="changeAnswererSearch">
              <div class="app-content-actions-wrapper">
                <div class="filter-button-wrapper">
                  <button class="action-button filter jsFilter" @click="showAnswererFilter"><span>筛选</span><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-filter"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg></button>
                  <div class="filter-menu" :class="{active: isShowAnswererFilter}">
                    <label>回答类型</label>
                    <select v-model="answererScreen">
                      <option>所有类型</option>
                      <option>数学</option>
                      <option>英语</option>
                      <option>社会人文</option>
                      <option>物理</option>
                      <option>化学</option>
                      <option>体育</option>
                    </select>
                    <div class="filter-menu-buttons">
                      <button class="filter-button reset" @click="showAnswererFilter">
                        Close
                      </button>
                      <button class="filter-button apply" @click="changeAnswererFilter">
                        Apply
                      </button>
                    </div>
                  </div>
                </div>
                <button class="action-button list" :class="{active: showMethod == 0}" title="List View" @click="changeShowMethod(0)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-list"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                </button>
                <button class="action-button grid" :class="{active: showMethod == 1}" title="Grid View" @click="changeShowMethod(1)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-grid"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                </button>
              </div>
            </div>
            <div class="products-area-wrapper" :class="{tableView: showMethod == 0, gridView: showMethod == 1}">
                <div class="products-header">
                    <div class="product-cell image">
                        回答者
                    </div>
                    <div class="product-cell status-cell">
                        回答类型
                    </div>
                    <div class="product-cell price">
                        单价
                        <button class="sort-button" @click="changeAnswererList">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 512 512"><path fill="currentColor" d="M496.1 138.3L375.7 17.9c-7.9-7.9-20.6-7.9-28.5 0L226.9 138.3c-7.9 7.9-7.9 20.6 0 28.5 7.9 7.9 20.6 7.9 28.5 0l85.7-85.7v352.8c0 11.3 9.1 20.4 20.4 20.4 11.3 0 20.4-9.1 20.4-20.4V81.1l85.7 85.7c7.9 7.9 20.6 7.9 28.5 0 7.9-7.8 7.9-20.6 0-28.5zM287.1 347.2c-7.9-7.9-20.6-7.9-28.5 0l-85.7 85.7V80.1c0-11.3-9.1-20.4-20.4-20.4-11.3 0-20.4 9.1-20.4 20.4v352.8l-85.7-85.7c-7.9-7.9-20.6-7.9-28.5 0-7.9 7.9-7.9 20.6 0 28.5l120.4 120.4c7.9 7.9 20.6 7.9 28.5 0l120.4-120.4c7.8-7.9 7.8-20.7-.1-28.5z"/></svg>
                        </button>
                    </div> 
                    <div class="product-cell price">
                        操作
                    </div>
                    <div class="product-cell status-cell">
                        简介
                    </div>
                </div>
                <div class="products-row" v-for="(item,Index) in resList" :key="Index">
                    <el-popover
                        placement="left"
                        width="160"
                        trigger="click"
                        :content="item.resume">
                        <el-button slot="reference" class="cell-more-button">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-vertical"><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>
                        </el-button>
                    </el-popover>
                    
                    <div class="product-cell image">
                        <img :src="'data:image/jpeg;base64,' + item.photo.slice(2).substr(0, item.photo.length - 3)" alt="product">
                        <span>{{item.username}}</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="cell-label">类型:</span>
                      <span class="status" :class="
                       item.field == 5 ? 'pe' :
                      (item.field == 0 ? 'math' :
                      (item.field == 1 ? 'eng' :
                      (item.field == 2 ? 'human' :
                      (item.field == 3 ? 'phy' : 'che'
                      ))))
                      ">
                        {{item.field == 0 ? "数学" : 
                        (item.field == 1 ? "英语" : 
                        (item.field == 2 ? "社会人文" : 
                        (item.field == 3 ? "物理" : 
                        (item.field == 4 ? "化学" : "体育"
                        ))))}}
                      </span>
                    </div>
                    <div class="product-cell price">
                        <span class="cell-label">单价:</span>
                        <span class="paramstatus dollor">{{item.price}} $</span>
                    </div>
                    <div class="product-cell price">
                        <span class="cell-label">操作:</span>
                        <div class="btngroup">
                            <el-button type="text" @click="showAsk(item.username, item.price)">
                                提问
                            </el-button>
                            <el-button type="text" @click="showChat(item.username)">
                                聊天
                            </el-button>
                        </div>
                    </div>
                    <div class="product-cell status-cell">
                        <el-popover
                            placement="top-start"
                            width="160"
                            trigger="click"
                            :content="item.resume">
                            <el-button slot="reference" class="more-button">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-horizontal"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
                            </el-button>
                        </el-popover>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 1">
            <div class="app-content-header">
                <h1 class="app-content-headerText"></h1>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                    <div class="product-cell image">
                        提问者
                    </div>
                    <div class="product-cell price">
                        提问名称
                    </div>
                    <div class="product-cell status-cell">
                        订单类型
                    </div>
                    <div class="product-cell status-cell">
                        订单状态
                    </div>
                    <div class="product-cell price">
                        操作
                    </div>
                </div>
                <div class="products-row" v-for="(item,index) in allQuestions" :key="index" v-show="!(item.check_mark == 1 || item.check_mark == 3)">
                    <div class="product-cell image">
                      <img :src="'data:image/jpeg;base64,' + item.questioner_photo.slice(2).substr(0, item.questioner_photo.length - 3)" alt="product">
                      <span>{{item.questioner}}</span>
                    </div>
                    <div class="product-cell price">
                      <span>{{item.title}}</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="status" :class="
                       item.field == 0 ? 'math' :
                      (item.field == 1 ? 'eng' :
                      (item.field == 2 ? 'human' :
                      (item.field == 3 ? 'phy' :
                      (item.field == 4 ? 'che' : 'pe'
                      ))))
                      ">
                        {{item.field == 0 ? "数学" : 
                        (item.field == 1 ? "英语" : 
                        (item.field == 2 ? "社会人文" : 
                        (item.field == 3 ? "物理" : 
                        (item.field == 4 ? "化学" : "体育"
                        ))))}}
                      </span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="orderstatus" :class="
                       item.end_mark == 0 ? 'cancel' :
                      (item.end_mark == 1 ? 'miss' :
                      (item.end_mark == 2 ? 'incomplete' :
                      (item.end_mark == 3 || item.end_mark == 6 ? 'complete' :
                      (item.end_mark == 5 ? 'refuse' : 'none'
                      ))))
                      ">
                        {{item.end_mark == 0 ? "已取消" : 
                        (item.end_mark == 1 ? "未接单" : 
                        (item.end_mark == 2 ? "未完成" : 
                        (item.end_mark == 3 || item.end_mark == 6 ? "已完成" : 
                        (item.end_mark == 5 ? "已拒绝" : "无状态"
                        ))))}}
                      </span>&nbsp;&nbsp;
                      <span v-show="item.end_mark == 1">{{allQuestionsCount[index]}}</span>
                      <span v-show="item.end_mark == 2 && !allAnswersC[index]">{{allAnswersCount[index]}}</span>
                    </div>
                    <div class="product-cell price">
                      <el-popover
                          placement="top-start"
                          width="160"
                          trigger="click"
                          :content="item.content">
                          <el-button slot="reference" type="text">
                            内容
                          </el-button>
                      </el-popover>&nbsp;&nbsp;&nbsp;
                      <el-button type="text" @click="showChat(item.questioner, item.order_id)">
                        聊天
                      </el-button>
                      <el-button type="text" @click="finishOrder(item.order_id, index, 1)" :disabled="item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 5">
                        完成
                      </el-button>
                      <el-button type="text" @click="refuseOrder(item.order_id, index, 1)" :disabled="!item.end_mark == 1 || item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 5 || item.end_mark == 2">
                        拒单
                      </el-button>
                      <el-button type="text" @click="acceptOrder(item.order_id, index)" :disabled="!item.end_mark == 1 || item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 5 || item.end_mark == 2">
                        接单
                      </el-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 3">
            <div class="app-content-header">
              <div>
                <div class="app-content-actions-wrapper">
                  <div class="filter-button-wrapper">
                    <button class="action-button filter jsFilter" @click="showFilter"><span>筛选</span><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-filter"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg></button>
                    <div class="filter-menu" :class="{active: isShowFilter}">
                      <label>订单类型</label>
                      <select v-model="orderScreen1">
                        <option>所有类型</option>
                        <option>提问订单</option>
                        <option>回答订单</option>
                      </select>
                      <label>订单状态</label>
                      <select v-model="orderScreen2">
                        <option>所有状态</option>
                        <option>未接单</option>
                        <option>未完成</option>
                        <option>已完成</option>
                        <option>已拒绝</option>
                        <option>已取消</option>
                      </select>
                      <div class="filter-menu-buttons">
                        <button class="filter-button reset" @click="showFilter">
                          Close
                        </button>
                        <button class="filter-button apply" @click="changeOrderFilter">
                          Apply
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                    <div class="product-cell image">
                        提问者
                    </div>
                    <div class="product-cell image">
                        回答者
                    </div>
                    <div class="product-cell status-cell">
                        订单类型
                    </div>
                    <div class="product-cell status-cell">
                        订单状态
                    </div>
                    <div class="product-cell price">
                        单价
                        <button class="sort-button" @click="changeOrderList">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 512 512"><path fill="currentColor" d="M496.1 138.3L375.7 17.9c-7.9-7.9-20.6-7.9-28.5 0L226.9 138.3c-7.9 7.9-7.9 20.6 0 28.5 7.9 7.9 20.6 7.9 28.5 0l85.7-85.7v352.8c0 11.3 9.1 20.4 20.4 20.4 11.3 0 20.4-9.1 20.4-20.4V81.1l85.7 85.7c7.9 7.9 20.6 7.9 28.5 0 7.9-7.8 7.9-20.6 0-28.5zM287.1 347.2c-7.9-7.9-20.6-7.9-28.5 0l-85.7 85.7V80.1c0-11.3-9.1-20.4-20.4-20.4-11.3 0-20.4 9.1-20.4 20.4v352.8l-85.7-85.7c-7.9-7.9-20.6-7.9-28.5 0-7.9 7.9-7.9 20.6 0 28.5l120.4 120.4c7.9 7.9 20.6 7.9 28.5 0l120.4-120.4c7.8-7.9 7.8-20.7-.1-28.5z"/></svg>
                        </button>
                    </div>
                    <div class="product-cell price">
                        提问名称
                    </div>
                    <div class="product-cell price">
                        操作
                    </div>
                </div>
                <div class="products-row" v-for="(item,INDEX) in showOrder" :key="INDEX" v-show="!(item.check_mark == 1 || item.check_mark == 3)">
                    <div class="product-cell image">
                      <img v-if="item.questioner == userMsg.username" :src="questioner_photo" alt="product">
                      <img v-else :src="'data:image/jpeg;base64,' + item.questioner_photo.slice(2).substr(0, item.questioner_photo.length - 3)" alt="product">
                      <span>{{item.questioner}}</span>
                    </div>
                    <div class="product-cell image">
                      <img v-if="item.answerer == userMsg.username" :src="answerer_photo" alt="product">
                      <img v-else :src="'data:image/jpeg;base64,' + item.answerer_photo.slice(2).substr(0, item.answerer_photo.length - 3)" alt="product">
                      <span>{{item.answerer}}</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="status" :class="
                       item.field == 0 ? 'math' :
                      (item.field == 1 ? 'eng' :
                      (item.field == 2 ? 'human' :
                      (item.field == 3 ? 'phy' :
                      (item.field == 4 ? 'che' : 'pe'
                      ))))
                      ">
                        {{item.field == 0 ? "数学" : 
                        (item.field == 1 ? "英语" : 
                        (item.field == 2 ? "社会人文" : 
                        (item.field == 3 ? "物理" : 
                        (item.field == 4 ? "化学" : "体育"
                        ))))}}
                      </span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="orderstatus" :class="
                       item.end_mark == 0 ? 'cancel' :
                      (item.end_mark == 1 ? 'miss' :
                      (item.end_mark == 2 ? 'incomplete' :
                      (item.end_mark == 3 || item.end_mark == 6 ? 'complete' :
                      (item.end_mark == 5 ? 'refuse' : 'none'
                      ))))
                      ">
                        {{item.end_mark == 0 ? "已取消" : 
                        (item.end_mark == 1 ? "未接单" : 
                        (item.end_mark == 2 ? "未完成" : 
                        (item.end_mark == 3 || item.end_mark == 6 ? "已完成" : 
                        (item.end_mark == 5 ? "已拒绝" : "无状态"
                        ))))}}
                      </span>
                    </div>
                    <div class="product-cell price">
                        <span class="paramstatus dollor">
                          {{item.price}} $
                        </span>
                    </div>
                    <div class="product-cell price">
                      <span>{{item.title}}</span>
                    </div> 
                    <div class="product-cell price">
                      <el-popover
                          placement="top-start"
                          width="160"
                          trigger="click"
                          :content="item.content">
                          <el-button slot="reference" type="text">
                            内容
                          </el-button>
                      </el-popover>&nbsp;&nbsp;&nbsp;
                      <el-button type="text" @click="showChat(item.questioner, item.order_id)">
                        聊天
                      </el-button>
                      <el-button type="text" @click="finishOrder(item.order_id, INDEX, 2)" :disabled="item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 0 || item.end_mark == 5">
                        完成
                      </el-button>
                      <el-button v-if="item.questioner == userMsg.username" type="text" @click="cancelOrder(item.order_id,INDEX)" :disabled="item.end_mark == 0 || item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 5">
                        取消
                      </el-button>
                      <el-button v-else type="text" @click="refuseOrder(item.order_id, INDEX, 2)" :disabled="item.end_mark == 5 || item.end_mark == 3 || item.end_mark == 6 || item.end_mark == 2">
                        拒单
                      </el-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 2">
            <div class="app-content-header">
                <h1 class="app-content-headerText">个人中心</h1>
                <div>
                  <button v-show="JSON.stringify(userAnswererMsg) === '{}'" class="app-content-headerButton" @click="upDialog.dialogVisible = true">
                      用户升级
                  </button>
                  <button class="app-content-headerButton" @click="update_password">
                    修改密码
                  </button>
                </div>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                  <div class="product-cell image">
                      基础信息展示
                  </div>
                </div>
                <div class="products-row">
                  <div class="product-cell image">
                      <span>用户名</span>
                  </div>
                  <div class="product-cell status-cell">
                      <span class="userstatus user">
                        {{ userMsg.username }}
                      </span>
                  </div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </div>
                <div class="products-row">
                  <div class="product-cell image">
                      <span>账户余额</span>
                  </div>
                  <div class="product-cell status-cell">
                      <span class="paramstatus dollor">
                        {{ userMsg.balance }} $
                      </span>
                  </div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                </div>
                <div class="products-row">
                  <div class="product-cell image">
                      <span>邮箱</span>
                  </div>
                  <div class="product-cell status-cell">
                      <span class="paramstatus num">
                        {{ userMsg.email }}
                      </span>
                  </div>
                  <button class="app-content-headerButton" @click="update_email">
                    更新邮箱
                  </button>
                </div>
                <div class="products-row">
                  <div class="product-cell image">
                      <span>头像</span>
                  </div>
                  <div class="product-cell status-cell">
                      <el-avatar style="width: 100px; height: 100px" :src="userphoto"></el-avatar>
                  </div>
                  <el-upload
                    class="upload avatar-image upload_img"
                    action=""
                    accept="image/jpeg,image/png"
                    :before-upload="beforeUpload"
                    :show-file-list="false"
                    :http-request="httpRequest"
                  >
                    <button class="app-content-headerButton">
                      更换头像
                    </button>
                  </el-upload>
                </div>
                <div v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="products-header">
                  <div class="product-cell image">
                    回答者信息展示
                  </div>
                  <button v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="app-content-headerButton" @click="upDialog.dialogVisible = true">
                    更新
                  </button>
                </div>
                <div v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="products-row">
                  <div class="product-cell image">
                      <span>简介</span>
                  </div>
                  <div class="product-cell status-cell">
                      {{ userAnswererMsg.resume }}
                  </div>
                </div>
                <div v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="products-row">
                  <div class="product-cell image">
                      <span>领域</span>
                  </div>
                  <div class="product-cell status-cell">
                    <span class="status" :class="
                       userAnswererMsg.field == 0 ? 'math' :
                      (userAnswererMsg.field == 1 ? 'eng' :
                      (userAnswererMsg.field == 2 ? 'human' :
                      (userAnswererMsg.field == 3 ? 'phy' :
                      (userAnswererMsg.field == 4 ? 'che' : 'pe'
                      ))))
                      ">
                        {{userAnswererMsg.field == 0 ? "数学" : 
                        (userAnswererMsg.field == 1 ? "英语" : 
                        (userAnswererMsg.field == 2 ? "社会人文" : 
                        (userAnswererMsg.field == 3 ? "物理" : 
                        (userAnswererMsg.field == 4 ? "化学" : "体育"
                        ))))}}
                    </span>
                  </div>
                </div>
                <div v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="products-row">
                  <div class="product-cell image">
                      <span>定价</span>
                  </div>
                  <div class="product-cell status-cell">
                    <span class="paramstatus dollor">
                      {{ userAnswererMsg.price }} $
                    </span>
                  </div>
                </div>
                <div v-show="JSON.stringify(userAnswererMsg) !== '{}'" class="products-header">
                  <div class="product-cell image">
                    收入统计
                  </div>
                </div>
                <Chart v-show="JSON.stringify(userAnswererMsg) !== '{}'"/>
            </div>
        </div>
    </div>
    <Dia :dialogVisible="upDialog.dialogVisible" @update_dialogVisible="updateDialog"/>
    <Rec :rechargeVisible="reDialog.rechargeVisible" @update_rechargeVisible="rechargeDialog"/>
    <Ask :askVisible="askDialog.askVisible" :answer="answer" :price="price" @update_askVisible="update_askVisible" />
    <ToRefuse
      :refuseVisible="refuseVisible"
      :orderDetails="orderDetails"
      @update_refuseVisible="update_refuseVisible"
      @update_refuseOrder="update_refuseOrder"
      @update_refuseButton="update_refuseButton"
    />
    <UdPwd :updatePwdVisible="updatePwdVisible" @update_updatePwdVisible="update_updatePwdVisible"></UdPwd>
</div>
</template>

<script>
import Ask from "@/components/AskDialog.vue";
import Dia from "@/components/UpDialog.vue";
import Rec from "@/components/RechargeDialog.vue";
import ToRefuse from "@/components/ToRefuse.vue";
import UdPwd from "@/components/UpdatePassword.vue";
import Chart from "@/components/Chart.vue";

export default {
  name: "MainPage",
  data() {
    return {
      askDialog: {
        askVisible: false,
      },
      upDialog: {
        dialogVisible: false,
      },
      reDialog: {
        rechargeVisible: false,
      },
      refuseVisible: false,
      updatePwdVisible: false,
      refuseButton: [],
      orderDetails: {},
      isQuestion: true,
      isAnswer: false,
      isSettings: false,
      isOrder: false,
      sideBar: 0,
      showMethod: 0,
      allAnswerer: [],
      resList: [],
      allUnread: 0,
      answer: "",
      price: 0,
      //所有回答订单
      allQuestions: [],
      //所有与用户相关订单
      allQrder: [],
      //当前展示订单
      showOrder: [],
      //显示回答者列表筛选
      isShowAnswererFilter: false,
      //显示订单列表筛选
      isShowFilter: false,
      //回答者列表排序计数(0表示顺序，1表示逆序)
      answererListNum: 0,
      //回答者列表筛选结果
      answererScreen: "所有类型",
      //订单列表排序计数(0表示顺序，1表示逆序)
      orderListNum: 0,
      //订单列表筛选结果
      orderScreen1: "提问订单",
      orderScreen2: "所有状态",

      //登录人信息
      userphoto: "",
      userMsg: {},
      userAnswererMsg: {},
      questioner_photo: "",
      answerer_photo: "",

      //系统参数
      sysparam_lowest_prices: 0,
      sysparam_top_prices: 0,
      sysparam_wait_answer: 0,
      sysparam_wait_receive: 0,
      sysparam_times_AQ: 0,
      sysparam_time_service: 0,

      //接单倒计时数组
      allQuestionsCount: [],
      seconds: [],

      //首次回答倒计时数组
      allAnswersCount: [],
      allAnswersC: [],
      Aseconds: [],

      //搜索框
      searchName: "",
    };
  },
  created() {
    this.fetchResData();
  },
  mounted() {
    this.Time()
    this.Time2()
  },
  methods: {
    // 天 时 分 秒 格式化函数
    countDown(i) {
      if(this.seconds[i] == 0)
        this.allQuestionsCount[i] = "none";
      else{
        let d = parseInt(this.seconds[i] / (24 * 60 * 60))
        d = d < 10 ? "0" + d : d
        let h = parseInt(this.seconds[i] / (60 * 60) % 24);
        h = h < 10 ? "0" + h : h
        let m = parseInt(this.seconds[i] / 60 % 60);
        m = m < 10 ? "0" + m : m
        let s = parseInt(this.seconds[i] % 60);
        s = s < 10 ? "0" + s : s
        //let tmp = this.allQuestionsCount;
        //tmp[i] = d + '天' + h + '时' + m + '分' + s + '秒';
        //this.allQuestionsCount = tmp;
        this.allQuestionsCount[i] = d + '天' + h + '时' + m + '分' + s + '秒';
      }
    },
    countDown2(i) {
      if(this.Aseconds[i] == 0)
        this.allAnswersCount[i] = "none";
      else{
        let d = parseInt(this.Aseconds[i] / (24 * 60 * 60))
        d = d < 10 ? "0" + d : d
        let h = parseInt(this.Aseconds[i] / (60 * 60) % 24);
        h = h < 10 ? "0" + h : h
        let m = parseInt(this.Aseconds[i] / 60 % 60);
        m = m < 10 ? "0" + m : m
        let s = parseInt(this.Aseconds[i] % 60);
        s = s < 10 ? "0" + s : s
        this.allAnswersCount[i] = d + '天' + h + '时' + m + '分' + s + '秒';
      }
    },
    //定时器每过1秒参数减1
    Time() {
      setInterval(() => {
        for(var i = 0;i < this.allQuestions.length;i++){
          if(this.seconds[i] != 0){
            this.seconds[i] -= 1;
            this.countDown(i);
          }
        }
        this.allQuestionsCount = this.allQuestionsCount.slice();
      }, 1000)
    },
    Time2() {
      setInterval(() => {
        for(var i = 0;i < this.allQuestions.length;i++){
          if(this.Aseconds[i] != 0){
            this.Aseconds[i] -= 1;
            this.countDown2(i);
          }
        }
        this.allAnswersCount = this.allAnswersCount.slice();
      }, 1000)
    },
    changeSideBar(val) {
      if(this.sideBar != val)
        this.sideBar = val;
    },
    changeShowMethod(val) {
      if(this.showMethod != val)
          this.showMethod = val;
    },
    showAsk(val, price) {
      this.answer = val;
      this.askDialog.askVisible = true;
      this.price = price;
    },
    showChat(val, id) {
      if(sessionStorage.getItem('now_order_id')){
        sessionStorage.removeItem('now_order_id');
        sessionStorage.setItem('now_order_id', id);
      }else{
        sessionStorage.setItem('now_order_id', id);
      }
      let sig = sessionStorage.getItem('userSig');
      let promise = this.$tim.login({userID: this.userMsg.username, userSig: sig});
      var that = this;
      promise.then(function(imResponse) {
        if (imResponse.data.repeatLogin === true) {
          that.$http({
            url: that.$url + "api/senduserlist",
            method: "get",
            params: { username: that.userMsg.username },
          })
            .then((res) => {
              var List = [];
              var resList = [];
              List = res.data.userList;
              var listCount = [];
              List.forEach(async (item, index) => {
                let promise = that.$tim.getMessageList({ conversationID: "C2C" + item.username, count: 10 });
                var M = [];
                await promise.then(function(imResponse) {
                  const messageList = imResponse.data.messageList; // 消息列表。
                  for (var k = 0; k < messageList.length; k++) {
                    let obj = {
                      id: messageList[k].from,
                      content: messageList[k].payload.text,
                      time: messageList[k].time,
                    };
                    M.push(obj);
                  }
                });
                let obj = {
                  username: item.username,
                  status: "online",
                  src: "data:image/jpeg;base64," + item.photo.slice(2).substr(0, item.photo.length - 3),
                  message: M,
                };
                resList[index] = obj;
                listCount.push(index);
                if (listCount.length == List.length) {
                  $List = resList;
                  sessionStorage.setItem('$List',JSON.stringify(resList));
                  for (let i = 0; i < $List.length; i++) {
                    if ($List[i].username == val) {
                      $isActive = i;
                      break;
                    }
                  }
                  that.$router.push({ path: "/chat" });
                }
              });
            })
            .catch((error) => {
              alter(error);
            });
          }
          else{
            setTimeout(function(){
              that.$http({
                url: that.$url + "api/senduserlist",
                method: "get",
                params: { username: that.userMsg.username },
              })
                .then((res) => {
                  var List = [];
                  var resList = [];
                  List = res.data.userList;
                  var listCount = [];
                  List.forEach(async (item, index) => {
                    let promise = that.$tim.getMessageList({ conversationID: "C2C" + item.username, count: 10 });
                    var M = [];
                    await promise.then(function(imResponse) {
                      const messageList = imResponse.data.messageList; // 消息列表。
                      for (var k = 0; k < messageList.length; k++) {
                        let obj = {
                          id: messageList[k].from,
                          content: messageList[k].payload.text,
                          time: messageList[k].time,
                        };
                        M.push(obj);
                      }
                    });
                    let obj = {
                      username: item.username,
                      status: "online",
                      src: "data:image/jpeg;base64," + item.photo.slice(2).substr(0, item.photo.length - 3),
                      message: M,
                    };
                    resList[index] = obj;
                    listCount.push(index);
                    if (listCount.length == List.length) {
                      $List = resList;
                      sessionStorage.setItem('$List',JSON.stringify(resList));
                      for (let i = 0; i < $List.length; i++) {
                        if ($List[i].username == val) {
                          $isActive = i;
                          break;
                        }
                      }
                      that.$router.push({ path: "/chat" });
                    }
                  });
                })
                .catch((error) => {
                  alter(error);
                });
            },1000);
          }
        })
    },
    showRefuse(val) {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/selectorderbyid",
        method: "get",
        params: { order_id: val },
      }).then((res) => {
        this.orderDetails = res.data.orders[0];
        switch (this.orderDetails["end_mark"]) {
          case 0:
            this.orderDetails["end_mark"] = "已取消";
            break;
          case 1:
            this.orderDetails["end_mark"] = "未接单";
            break;
          case 2:
            this.orderDetails["end_mark"] = "未完成";
            break;
          case 3:
            this.orderDetails["end_mark"] = "已完成";
            break;
          case 5:
            this.orderDetails["end_mark"] = "已拒绝";
            break;
          default:
            this.orderDetails["end_mark"] = "无状态";
            break;
        }
      });
      this.refuseVisible = true;
    },
    // 上传文件之前检查文件格式
    beforeUpload(file) {
      const isJPGorPNG = file.type === "image/jpeg" || "image/png";
      const isLt1M = file.size / 1024 / 64 < 1;
      if (!isJPGorPNG) {
        this.$message.error("上传的头像文件只能是 jpg 或者 png 图片格式！");
      }
      if (!isLt1M) {
        this.$message.error("上传的头像文件大小不能超过 64 KB！");
      }
      return isJPGorPNG && isLt1M;
    },
    // 不使用默认的 action 上传
    httpRequest(data) {
      const qs = require("qs");
      let formData = new FormData();
      formData.append("username", this.userMsg.username);
      formData.append("photo", data.file);
      this.$http({
        url: this.$url + "api/modifyuserinfo",
        method: "post",
        data: formData,
      });
      let _this = this;
      let reader = new FileReader();
      let file = data.file;
      reader.readAsDataURL(file);
      reader.onloadend = function(e) {
        _this.userphoto = this.result;
        _this.userMsg.photo = this.result;
        sessionStorage.removeItem('userMsg');
        sessionStorage.setItem('userMsg',JSON.stringify(_this.userMsg));
      };
    },
    // 更新邮箱的弹窗
    update_email() {
      var _this = this;
      const qs = require("qs");
      this.$prompt("请输入新的邮箱", "更新邮箱", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: "邮箱格式不正确",
      }).then(({ value }) => {
        _this.userMsg.email = value;
        sessionStorage.removeItem('userMsg');
        sessionStorage.setItem('userMsg',JSON.stringify(_this.userMsg));
        _this.$http({
          url: _this.$url + "api/modifyuserinfo",
          method: "post",
          data: qs.stringify({
            username: _this.userMsg.username,
            email: value,
          }),
        });
        this.$message({
          type: "success",
          message: "更新成功，新邮箱为: " + value,
        });
      }).catch(() => {});
    },
    update_askVisible(val) {
      this.askDialog.askVisible = val;
    },
    updateDialog(val) {
      this.upDialog.dialogVisible = val;
    },
    rechargeDialog(val) {
      this.reDialog.rechargeVisible = val;
    },
    update_askVisible(val) {
      this.askDialog.askVisible = val;
    },
    update_refuseVisible(val) {
      this.refuseVisible = val;
    },
    update_refuseOrder(val) {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/refuseask",
        method: "post",
        data: qs.stringify({
          order_id: val,
        }),
      });
    },
    update_refuseButton(val) {
      this.refuseButton[val] = true;
    },
    update_password() {
      this.updatePwdVisible = true;
    },
    update_updatePwdVisible(val) {
      this.updatePwdVisible = val;
    },
    fetchResData() {
      var _this = this;

      //从缓存中获取userMsg
      if(sessionStorage.getItem('userMsg')){
        let userMsg = sessionStorage.getItem('userMsg');
        this.userMsg = JSON.parse(userMsg);
      }
      else{
        this.userMsg = this.$userMsg;
      }

      //拉取个人最新信息
      this.$http({
        url: this.$url + "api/getusermsg",
        method: "get",
        params: {
          username: this.userMsg.username,
        },
      })
      .then((res) => {
        const userMsg = {
          photo: res.data.doc.photo,
          username: res.data.doc.username,
          email: res.data.doc.email,
          photo: "data:image/jpeg;base64," + res.data.doc.photo.slice(2).substr(0, res.data.doc.photo.length - 3),
          permission: res.data.doc.permission,
          balance: res.data.doc.balance,
        };
        this.userMsg = userMsg;
        sessionStorage.removeItem('userMsg');
        sessionStorage.setItem('userMsg', JSON.stringify(userMsg));
      })

      //获取userphoto
      this.userphoto = this.userMsg.photo;

      //获取全局参数
      if(sessionStorage.getItem('sysparam_lowest_prices')){
        let sysparam_lowest_prices = sessionStorage.getItem('sysparam_lowest_prices');
        let sysparam_top_prices = sessionStorage.getItem('sysparam_top_prices');
        let sysparam_wait_answer = sessionStorage.getItem('sysparam_wait_answer');
        let sysparam_wait_receive = sessionStorage.getItem('sysparam_wait_receive');
        let sysparam_times_AQ = sessionStorage.getItem('sysparam_times_AQ');
        let sysparam_time_service = sessionStorage.getItem('sysparam_time_service');
        this.sysparam_lowest_prices = parseInt(sysparam_lowest_prices);
        this.sysparam_top_prices = parseInt(sysparam_top_prices);
        this.sysparam_wait_answer = parseInt(sysparam_wait_answer);
        this.sysparam_wait_receive = parseInt(sysparam_wait_receive);
        this.sysparam_times_AQ = parseInt(sysparam_times_AQ);
        this.sysparam_time_service = parseInt(sysparam_time_service);
      }
      else{
        this.sysparam_lowest_prices = this.$Usersysparam.sysparam_lowest_prices;
        this.sysparam_top_prices = this.$Usersysparam.sysparam_top_prices;
        this.sysparam_wait_answer = this.$Usersysparam.sysparam_wait_answer;
        this.sysparam_wait_receive = this.$Usersysparam.sysparam_wait_receive;
        this.sysparam_times_AQ = this.$Usersysparam.sysparam_times_AQ;
        this.sysparam_time_service = this.$Usersysparam.sysparam_time_service;
      }

      //获取个人回答者信息
      if(this.userMsg.permission == 2){
        this.$http({
          url: this.$url + "api/sendansinfo",
          method: "get",
        })
        .then((res) => {
          for(var i = 0;i < res.data.res.length;i++){
            if(res.data.res[i].username == this.userMsg.username){
              this.userAnswererMsg = res.data.res[i];
            }
          }
        })
        .catch((error) => {
            console.log(error);
        });
      }

      //获取回答者订单
      this.$http({
        url: this.$url + "api/selectorderbyanswerer",
        method: "get",
        params: { answerer: this.userMsg.username },
      }).then((Res) => {
        var ttmp = Res.data.orders;
        var ttmpphoto = ttmp.pop().answerer_photo;
        ttmpphoto = "data:image/jpeg;base64," + ttmpphoto.slice(2).substr(0, ttmpphoto.length - 3);
        this.answerer_photo = ttmpphoto;
        this.allQuestions = ttmp;

        //获取倒计时
        for(let k = 0;k < ttmp.length;k++){
          //未接单
          if(ttmp[k].end_mark == 1){
            //服务器时间
            let time = new Date().getTime() - 8 * 60 * 60 * 1000;
            //本地时间
            //let time = new Date().getTime();
            let V =  Date.parse(new Date(ttmp[k].confirmed_at));
            this.seconds[k] = parseInt(this.sysparam_wait_receive*60 - (time-V)/1000);
            if(this.seconds[k] < 0)
              this.seconds[k] = 0;
          }else{
            this.seconds[k] = 0;
          }

          //已接单未第一次回答
          if(ttmp[k].end_mark == 2){
            this.allAnswersC[k] = ttmp[k].first_answer;
            //服务器时间
            let time = new Date().getTime() - 8 * 60 * 60 * 1000;
            //本地时间
            //let time = new Date().getTime();
            let V =  Date.parse(new Date(ttmp[k].receive_at));
            this.Aseconds[k] = parseInt(this.sysparam_wait_answer*60 - (time-V)/1000);
            if(this.Aseconds[k] < 0)
              this.Aseconds[k] = 0;
          }else{
            //let time = new Date().getTime();
            //let V =  Date.parse(new Date(ttmp[k].receive_at));
            //this.Aseconds[k] = parseInt(this.sysparam_wait_answer*60 - (time-V)/1000);
            //this.allAnswersC[k] = ttmp[k].first_answer;
            this.Aseconds[k] = 9;
          }
        }
        
        //获取提问者订单
        this.$http({
          url: this.$url + "api/selectorderbyquestioner",
          method: "get",
          params: { questioner: this.userMsg.username },
        }).then((res) => {
          var tmp = res.data.orders;
          var tmpphoto = tmp.pop().questioner_photo;
          tmpphoto = "data:image/jpeg;base64," + tmpphoto.slice(2).substr(0, tmpphoto.length - 3);
          this.questioner_photo = tmpphoto;
          this.showOrder = tmp;
          this.allOrder = this.allQuestions;
          this.allOrder = this.allQuestions.concat(tmp);
        })
      });
      //then(() => {
        /*
        for (let i of this.allOrder) {
          if (i.end_mark == 1 || i.end_mark == 2 && i.check_mark != 3) {
            this.orderingQuestion.push(i);
          }
          else if (i.end_mark == 3 || i.end_mark == 5 || i.check_mark == 3) {
            this.orderedQuestion.push(i);
          }
        }
        */
      //})

      //获取答主信息
      this.$http({
        url: this.$url + "api/sendansinfo",
        method: "get",
        params: {username: this.userMsg.username},
      })
      .then((res) => {
        this.allAnswerer = res.data.res;
        _this.resList = res.data.res;
      })
      .catch((error) => {
        console.log(error);
      });

      //获取用户列表
      this.$http({
          url: this.$url + "api/senduserlist",
          method: "get",
          params: {username: this.userMsg.username},
      })
      .then((res) => {
          var List = [];
          List = res.data.userList;
          this.$http({
              url: this.$url + "api/genusersig",
              method: "get",
              params: { username: "ad" },
          })
          .then((Res)=>{
            if(List.length <= 10){
              this.$http({
                  url: "https://console.tim.qq.com/v4/openim/get_c2c_unread_msg_num",
                  method: "post",
                  params: {
                      sdkappid: 1400581926,
                      identifier: "ad",
                      usersig: Res.data.sig,
                      random: 89999999,
                      contenttype: "json",
                  },
                  headers: {
                      "Content-Type": "application/json"
                  },
                  data: {
                      "To_Account":this.userMsg.username,
                      "Peer_Account":List
                  }
              })
              .then((RES=>{
                let num = 0;
                let unreadList = [];
                for(let k = 0;k < List.length;k++){
                  let obj = {
                    username: RES.data.C2CUnreadMsgNumList[k].Peer_Account,
                    num: RES.data.C2CUnreadMsgNumList[k].C2CUnreadMsgNum
                  }
                  unreadList.push(obj);
                  num += RES.data.C2CUnreadMsgNumList[k].C2CUnreadMsgNum;
                }
                _this.allUnread = num;
                $unreadList = unreadList;
                sessionStorage.setItem('$unreadList',JSON.stringify(unreadList));
              }))
              .catch((error) => {
                console.log(error);
              });
            }else{
              split_array=(arr,len)=>{
                let arr_length = arr.length;
                let newArr = [];
                for(let i=0;i<arr_length;i+=len){
                  newArr.push(arr.slice(i,i+len));
                }
                return newArr;
              }
              let num = 0;
              let unreadList = [];
              let result = split_array(List, 10);
              var listCount = [];
              result.forEach(async (item, index)=>{
                await _this.$http({
                  url: "https://console.tim.qq.com/v4/openim/get_c2c_unread_msg_num",
                  method: "post",
                  params: {
                      sdkappid: 1400581926,
                      identifier: "ad",
                      usersig: Res.data.sig,
                      random: 89999999,
                      contenttype: "json",
                  },
                  headers: {
                      "Content-Type": "application/json"
                  },
                  data: {
                      "To_Account":_this.userMsg.username,
                      "Peer_Account":item.username
                  }
                })
                .then((RES=>{
                  for(let k = 0;k < item.length;k++){
                    let obj = {
                      username: RES.data.C2CUnreadMsgNumList[k].Peer_Account,
                      num: RES.data.C2CUnreadMsgNumList[k].C2CUnreadMsgNum
                    }
                    unreadList.push(obj);
                    num += RES.data.C2CUnreadMsgNumList[k].C2CUnreadMsgNum;
                  }
                  listCount.push(index);
                }))
                .catch((error) => {
                  console.log(error);
                });
                if(listCount.length == result.length){
                  _this.allUnread = num;
                  $unreadList = unreadList;
                  sessionStorage.setItem('$unreadList',JSON.stringify(unreadList));
                }
              })
            }
          })
          .catch((error) => {
              console.log(error);
          });
      })
      .catch((error) => {
          console.log(error);
      });
    },
    toChat() {
      let sig = sessionStorage.getItem('userSig');
      let promise = this.$tim.login({userID: this.userMsg.username, userSig: sig});
      var that = this;
      promise.then(function(imResponse) {
        if (imResponse.data.repeatLogin === true) {
          that.$http({
            url: that.$url + "api/senduserlist",
            method: "get",
            params: {username: that.userMsg.username},
          })
          .then((res) => {
              var List = [];
              var resList = [];
              List = res.data.userList;
              var listCount = [];
              List.forEach(async (item,index)=>{
                let promise = that.$tim.getMessageList({conversationID: 'C2C' + item.username, count: 10});
                var M = [];
                await promise.then(function(imResponse) {
                  const messageList = imResponse.data.messageList; // 消息列表。
                  for(var k = 0;k < messageList.length;k++){
                    let obj = {
                      id: messageList[k].from,
                      content: messageList[k].payload.text,
                      time: messageList[k].time,
                    };
                    M.push(obj);
                  }
                });
                let obj = {
                  username: item.username,
                  status: "online",
                  src: "data:image/jpeg;base64," + item.photo.slice(2).substr(0, item.photo.length - 3),
                  message: M,
                };
                resList[index] = obj;
                listCount.push(index);
                if(listCount.length == List.length){
                  $List = resList;
                  sessionStorage.setItem('$List',JSON.stringify(resList));
                  that.$router.push({ path: "/chat" });
                }
              })
          })
          .catch((error) => {
              console.log(error);
          });
        }
        else{
        setTimeout(function(){
          that.$http({
            url: that.$url + "api/senduserlist",
            method: "get",
            params: {username: that.userMsg.username},
          })
          .then((res) => {
              var List = [];
              var resList = [];
              List = res.data.userList;
              var listCount = [];
              List.forEach(async (item,index)=>{
                let promise = that.$tim.getMessageList({conversationID: 'C2C' + item.username, count: 10});
                var M = [];
                await promise.then(function(imResponse) {
                  const messageList = imResponse.data.messageList; // 消息列表。
                  for(var k = 0;k < messageList.length;k++){
                    let obj = {
                      id: messageList[k].from,
                      content: messageList[k].payload.text,
                      time: messageList[k].time,
                    };
                    M.push(obj);
                  }
                });
                let obj = {
                  username: item.username,
                  status: "online",
                  src: "data:image/jpeg;base64," + item.photo.slice(2).substr(0, item.photo.length - 3),
                  message: M,
                };
                resList[index] = obj;
                listCount.push(index);
                if(listCount.length == List.length){
                  $List = resList;
                  that.$router.push({ path: "/chat" });
                }
              })
          })
          .catch((error) => {
              console.log(error);
          });
        },1000);
        }
      }).catch(function(imError) {
        console.warn('login error:', imError); // 登录失败的相关信息
      });
    },
    showFilter() {
      this.isShowFilter = !this.isShowFilter;
    },
    showAnswererFilter() {
      this.isShowAnswererFilter = !this.isShowAnswererFilter;
    },

    //按照单价排列回答者列表
    changeAnswererList() {
      if(this.answererListNum == 0){
        this.answererListNum = 1;
        function sortRule(a,b) {
          return a.price- b.price;
        }
        this.resList.sort(sortRule);
      }else{
        this.answererListNum = 0;
        function sortRule(a,b) {
          return b.price- a.price;
        }
        this.resList.sort(sortRule);
      }
    },

    //按照筛选结果排列回答者列表
    changeAnswererFilter() {
      if(this.answererScreen == "所有类型"){
        this.resList = this.allAnswerer;
      }
      else if(this.answererScreen == "数学"){
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 0)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      else if(this.answererScreen == "英语"){
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 1)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      else if(this.answererScreen == "社会人文"){
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 2)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      else if(this.answererScreen == "物理"){
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 3)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      else if(this.answererScreen == "化学"){
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 4)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      else{
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.field == 5)
            tmp.push(i);
        }
        this.resList = tmp;
      }
      this.isShowAnswererFilter = !this.isShowAnswererFilter;
    },

    //按照搜索内容排列回答者列表
    changeAnswererSearch() {
      if(this.searchName == ""){
        this.resList = this.allAnswerer;
      }else{
        let tmp = [];
        for(var i of this.allAnswerer){
          if(i.username == this.searchName)
            tmp.push(i);
        }
        this.resList = tmp;
      }
    },

    //按照单价排列订单列表
    changeOrderList() {
      if(this.orderListNum == 0){
        this.orderListNum = 1;
        function sortRule(a,b) {
          return a.price- b.price;
        }
        this.showOrder.sort(sortRule);
      }else{
        this.orderListNum = 0;
        function sortRule(a,b) {
          return b.price- a.price;
        }
        this.showOrder.sort(sortRule);
      }
    },

    //根据筛选结果排列订单列表
    changeOrderFilter() {
      if(this.orderScreen1 == "所有类型"){
        this.showOrder = this.allOrder;
      }
      else if(this.orderScreen1 == "提问订单"){
        let tmp = [];
        for(var i of this.allOrder){
          if(i.questioner == this.userMsg.username)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }
      else{
        let tmp = [];
        for(var i of this.allOrder){
          if(i.answerer == this.userMsg.username)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }

      if(this.orderScreen2 == "所有状态"){}
      else if(this.orderScreen2 == "未接单"){
        let tmp = [];
        for(var i of this.showOrder){
          if(i.end_mark == 1)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }
      else if(this.orderScreen2 == "未完成"){
        let tmp = [];
        for(var i of this.showOrder){
          if(i.end_mark == 2)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }
      else if(this.orderScreen2 == "已拒绝"){
        let tmp = [];
        for(var i of this.showOrder){
          if(i.end_mark == 5)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }
      else if(this.orderScreen2 == "已取消"){
        let tmp = [];
        for(var i of this.showOrder){
          if(i.end_mark == 0)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }
      else{
        let tmp = [];
        for(var i of this.showOrder){
          if(i.end_mark == 3 || i.end_mark == 6)
            tmp.push(i);
        }
        this.showOrder = tmp;
      }

      this.isShowFilter = !this.isShowFilter;
    },

    //完成
    finishOrder(val, i, num) {
      this.$confirm('是否确定结束订单?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http({
          url: this.$url + "api/completeorder",
          method: "get",
          params: { 
            order_id: val,
          },
        }).then(()=>{
          if(num == 1){
            let tmp = this.allQuestions;
            tmp[i].end_mark = 3;
            this.allQuestions = tmp;
          }
          else{
            let tmp = this.showOrder;
            tmp[i].end_mark = 3;
            this.showOrder = tmp;
          }
          this.$message({
            type: 'success',
            message: '结束订单成功!'
          });
        }).catch((error)=>{
          console.log("error: ",error)
          this.$message({
            type: 'info',
            message: '订单结束失败！'
          });
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消操作'
        });          
      });
    },

    //接单
    acceptOrder(val,i) {
      this.$confirm('是否确定接单?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http({
          url: this.$url + "api/modifyorderstate",
          method: "get",
          params: { 
            order_id: val,
            end_mark: 2,
          },
        }).then(()=>{
          let tmp = this.allQuestions;
          tmp[i].end_mark = 2;
          this.allQuestions = tmp;
          this.$message({
            type: 'success',
            message: '接单成功!',
            onClose: () => {
              this.$router.go(0);
            }
          });
        }).catch(()=>{
          this.$message({
            type: 'info',
            message: '接单失败！'
          });
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消操作'
        });          
      });
    },

    //拒单
    refuseOrder(val, i, num) {
      this.$confirm('是否确定拒绝订单?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http({
          url: this.$url + "api/modifyorderstate",
          method: "get",
          params: { 
            order_id: val,
            end_mark: 5,
          },
        }).then(()=>{
          const qs = require("qs");
          if(num == 1){
            let tmp = this.allQuestions;
            tmp[i].end_mark = 5;
            this.allQuestions = tmp;
            this.$http({
              url: this.$url + "api/walletmanagement",
              method: 'post',
              data: qs.stringify({
                  "username": tmp[i].questioner,
                  "money": tmp[i].price,
              })
            })
          }else{
            let tmp = this.showOrder;
            tmp[i].end_mark = 5;
            this.showOrder = tmp;
            this.$http({
              url: this.$url + "api/walletmanagement",
              method: 'post',
              data: qs.stringify({
                  "username": tmp[i].questioner,
                  "money": tmp[i].price,
              })
            })
          }
          this.$message({
            type: 'success',
            message: '拒单成功!'
          });
        }).catch(()=>{
          this.$message({
            type: 'info',
            message: '拒单失败！'
          });
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消操作'
        });          
      });
    },

    //取消
    cancelOrder(val,i) {
      this.$confirm('是否确定取消订单?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http({
          url: this.$url + "api/modifyorderstate",
          method: "get",
          params: { 
            order_id: val,
            end_mark: 0,
          },
        }).then(()=>{
          let tmp = this.allQuestions;
          tmp[i].end_mark = 0;
          this.allQuestions = tmp;
          this.$http({
            url: this.$url + "api/walletmanagement",
            method: 'post',
            data: qs.stringify({
                "username": tmp[i].questioner,
                "money": tmp[i].price,
            })
          })
          this.userMsg.balance += tmp[i].price;
          sessionStorage.removeItem('userMsg');
          sessionStorage.setItem('userMsg',JSON.stringify(this.userMsg));
          this.$message({
            type: 'success',
            message: '取消订单成功!'
          });
        }).catch(()=>{
          this.$message({
            type: 'info',
            message: '取消订单失败！'
          });
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消操作'
        });          
      });
    },

    //获取剩余时间
    getRestTime(val) {
      var time = new Date().getTime();
      var V =  Date.parse(new Date(val));
      return parseInt((time-V)/1000);
    },
  },
  watch: {
    allQuestionsCount: {
      handler(newName, oldName){
        for(let i = 0;i < this.allQuestions.length;i++){
          if(this.seconds[i] == 0 && this.allQuestions[i].end_mark == 1){
            this.allQuestions[i].end_mark = 5;
            this.allQuestions = this.allQuestions.slice();
            /*
            const qs = require("qs");
            this.$http({
              url: this.$url + "api/modifyorderstate",
              method: "get",
              params: { 
                order_id: this.allQuestions[i].order_id,
                end_mark: 5,
              },
            }).then(()=>{
            }).catch((error)=>{
              console.log(error);
            })*/
          }
        }
      },
      deep:true
    },
    allAnswersCount: {
      handler(newName, oldName){
        for(let i = 0;i < this.allQuestions.length;i++){
          if(this.Aseconds[i] == 0 && this.allQuestions[i].end_mark == 2 && !this.allAnswersC[i]){
            this.allQuestions[i].end_mark = 5;
            this.allAnswersC[i] = 1;
            this.allQuestions = this.allQuestions.slice();
            this.allAnswersC = this.allAnswersC.slice();
            /*
            const qs = require("qs");
            this.$http({
              url: this.$url + "api/modifyorderstate",
              method: "get",
              params: { 
                order_id: this.allQuestions[i].order_id,
                end_mark: 5,
              },
            }).then(()=>{
              
            }).catch((error)=>{
              console.log(error);
            })*/
          }
        }
      },
      deep:true
    }
  },
  components: {
    Dia,
    Rec,
    Ask,
    ToRefuse,
    UdPwd,
    Chart,
  },
};
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap');
* { box-sizing: border-box; }

$font-small: 14px;
$font-medium: 16px;
$font-large: 24px;

.mainbody {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  font-family: 'Poppins', sans-serif;
  background-color: #101827;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  border-radius: 4px;
  width: 100%;
  height: 100%;
  max-height: 100%;
  max-width: 1280px;
  display: flex;
  overflow: hidden;
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
  max-width: 2000px;
  margin: 0 auto;
}

.sidebar {
  flex-basis: 200px;
  max-width: 200px;
  flex-shrink: 0;
  background-color: #f3f6fd;
  display: flex;
  flex-direction: column;
  
  &-list {
    list-style-type: none;
    padding: 0;
    
    &-item {
      position: relative;
      margin-bottom: 4px;
      
      a {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 10px 16px;
        color: #1f1c2e;
        text-decoration: none;
        font-size: $font-small;
        line-height: 24px;
      }
      
      svg { margin-right: 8px; }
      
      &:hover { background-color: rgba(195, 207, 244, 0.5); }
      
      &.active {
        background-color: rgba(195, 207, 244, 1);
        
        &:before {
          content: '';
          position: absolute;
          right: 0;
          background-color: #2869ff;
          height: 100%;
          width: 4px;
        }
      }
    }
  }
  
  @media screen and (max-width: 1024px) {&{
      display: none;
  }}
}

.mode-switch {
  background-color: transparent;
  border: none;
  padding: 0;
  color: #1f1c2e;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: auto;
  margin-right: 8px;
  cursor: pointer;
  
  .moon {
    fill: #1f1c2e;
  }
}

.mode-switch.active .moon {
  fill: none;
}

.account-info {
  display: flex;
  align-items: center;
  padding: 16px;
  margin-top: auto;
  
  &-picture {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  
  &-name {
    font-size: $font-small;
    color: #1f1c2e;
    margin: 0 8px;
    overflow: hidden;
    max-width: 100%;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  &-more {
    color: #1f1c2e;
    padding: 0;
    border: none;
    background-color: transparent;
    margin-left: auto;
  }
}

.app-icon {
  color: #1f1c2e;
  
  svg {
    width: 24px;
    height: 24px;
  }
}

.app-content {
  padding: 16px;
  background-color: #fff;
  height: 100%;
  flex: 1;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  
  &-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4px;
    margin-bottom: 15px;
  }
  
  &-headerText {
    color: #1f1c2e;
    font-size: $font-large;
    line-height: 32px;
    margin: 0;
  }
  
  &-headerButton {
    background-color: #2869ff;
    color: #fff;
    font-size: $font-small;
    line-height: 24px;
    border: none;
    border-radius: 4px;
    height: 32px;
    padding: 0 16px;
    transition: .2s;
    cursor: pointer;
    
    &:hover {
      background-color: #6291fd;
    }
  }
  
  &-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 4px;
    
    &-wrapper {
      display: flex;
      align-items: center;
      margin-left: auto;
    }
    
    @media screen and (max-width: 520px) {&{
      flex-direction: column;
      
      .search-bar { max-width: 100%; order: 2; }
      .app-content-actions-wrapper { padding-bottom: 16px; order: 1; }
    }}
  }
}

.filter-button-wrapper {
  position: relative;
}

@mixin searchIcon($color) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23#{$color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-search'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'/%3E%3C/svg%3E");
}

.search-bar {
  background-color: #f3f6fd;
  border: 1px solid #f3f6fd;
  color: #1f1c2e;
  font-size: $font-small;
  line-height: 24px;
  border-radius: 4px;
  padding: 0px 10px 0px 32px;
  height: 32px;
  @include searchIcon('1f1c2e');
  background-size: 16px;
  background-repeat: no-repeat;
  background-position: left 10px center;
  width: 100%;
  max-width: 320px;
  transition: .2s;
  
  .light & { @include searchIcon('1f1c2e'); }
  
  &:placeholder { color: #1f1c2e; }
  
  &:hover {
    border-color: #6291fd;
    @include searchIcon('6291fd');
  }
  
  &:focus {
    outline: none;
    border-color: #2869ff;
    @include searchIcon('2869ff');
  }
}

.action-button {
  border-radius: 4px;
  height: 32px;
  background-color: #f3f6fd;
  border: 1px solid #f3f6fd;
  display: flex;
  align-items: center;
  color: #1f1c2e;
  font-size: $font-small;
  margin-left: 8px;
  cursor: pointer;
  
  span { margin-right: 4px; }
  
   &:hover {
    border-color: #6291fd;
  }
  
  &:focus, &.active {
    outline: none;
    color: #2869ff;
    border-color: #2869ff;
  }
}

@mixin arrowDown($color) {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23#{$color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-chevron-down'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
}

.filter-menu {
  background-color: #f3f6fd;
  position: absolute;
  top: calc(100% + 16px);
  right: -74px;
  border-radius: 4px;
  padding: 8px;
  width: 220px;
  z-index: 2;
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
  
  visibility: hidden;
  opacity: 0;
  transition: .2s;
  
  &:before {
    content: '';
    position: absolute;
    width: 0; 
    height: 0; 
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;

    border-bottom: 5px solid #f3f6fd;
    bottom: 100%;
    left: 50%;
    transform: translatex(-50%);
  }
  
  &.active {
    visibility: visible;
    opacity: 1;
    top: calc(100% + 8px);
  }
  
  label {
    display: block;
    font-size: $font-small;
    color: #1f1c2e;
    margin-bottom: 8px;
  }
  
  select {
    appearance: none;
    @include arrowDown('1f1c2e');
    background-repeat: no-repeat;
    padding: 8px 24px 8px 8px;
    background-position: right 4px center;
    border: 1px solid #1f1c2e;
    border-radius: 4px;
    color: #1f1c2e;
    font-size: 12px;
    background-color: transparent;
    margin-bottom: 16px;
    width: 100%;
    option { font-size: 14px; }
    
    &:hover {
      border-color: #6291fd;
    }

    &:focus, &.active {
      outline: none;
      color: #2869ff;
      border-color: #2869ff;
      @include arrowDown('2869ff');
    }
  }
}

.filter-menu-buttons {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filter-button {
  border-radius: 2px;
  font-size: 12px;
  padding: 4px 8px;
  cursor: pointer;
  border: none;
  color: #fff;
  
  &.apply {
    background-color: #2869ff;
  }
  
  &.reset {
    background-color: #2c394f;
  }
}

.products-area-wrapper {
  width: 100%;
  max-height: 100%;
  overflow: auto;
  padding: 0 4px;
}

.tableView {
  .products-header {
    display: flex;
    align-items: center;
    border-radius: 4px;
    background-color: #f3f6fd;
    position: sticky;
    top: 0;
  }
  
  .products-row {
    display: flex;
    align-items: center;
    border-radius: 4px;
    
    &:hover {
      box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
      background-color: #f3f6fd;
      
      .cell-more-button {
        display: none;
      }

      .more-button {
        display: flex;
      }
    }

    .cell-more-button {
      display: none;
    }

    .more-button {
      border: none;
      padding: 0;
      border-radius: 4px;
      z-index: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width:24px;
      height: 24px;
      background-color: rgba(151, 183, 243, 0.7);
      color: #fff;
      cursor: pointer;
      display: none;
    }
    
  }
  
  .product-cell {
    flex: 1;
    padding: 8px 16px;
    color: #1f1c2e;
    font-size: $font-small;
    display: flex;
    align-items: center;
        
    img {
      width: 32px;
      height: 32px;
      border-radius: 6px;
      margin-right: 6px;
    }
    
    @media screen and (max-width: 780px) {&{
      font-size: 12px;
      &.image span { display: none; }
      &.image { flex: 0.2; }
    }}
      
    @media screen and (max-width: 520px) {&{      
      &.category, &.sales {
        display: none;
      }
      &.status-cell { flex: 0.4; }
      &.stock, &.price { flex: 0.2; }
    }}
    
    @media screen and (max-width: 480px) {&{
      &.stock { display: none; }
      &.price { flex: 0.4; }
    }}
  }
  
  .sort-button {
    padding: 0;
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #1f1c2e;
    margin-left: 4px;
    display: flex;
    align-items: center;
    
    &:hover { color: #2869ff; }
    svg { width: 12px; }
  }
  
  .cell-label {
    display: none;
  }
}

.userstatus {
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  font-size: 13px;

  &:before {
    content: '';
    width: 4px;
    height: 4px;
    border-radius: 50%;
    margin-right: 4px;
  }

  &.user {
    color: #22c57e;
    background-color: #b3f5d8;
    
    &:before {
      background-color: #22c57e;
    }
  }

  &.manage {
    color: #224ec5;
    background-color: #b3bdf5;
    
    &:before {
      background-color: #224ec5;
    }
  }

  &.auditor {
    color: #5322c5;
    background-color: #c1b3f5;
    
    &:before {
      background-color: #5322c5;
    }
  }

  &.admin {
    color: #c54322;
    background-color: #f5c0b3;
    
    &:before {
      background-color: #c54322;
    }
  }
}

.paramstatus {
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  font-size: 12px;

  &.num {
    color: #c52294;
    background-color: #f5b3d7;
  }

  &.hour {
    color: #229fc5;
    background-color: #b3e2f5;
  }

  &.dollor {
    color: #22bac5;
    background-color: #b3f5f2;
  }

  &.times {
    color: #2240c5;
    background-color: #b3bff5;
  }
}

.orderstatus {
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  font-size: 12px;

  &:before {
    content: '';
    width: 4px;
    height: 4px;
    border-radius: 50%;
    margin-right: 4px;
  }

  //已取消
  &.cancel {
    color: #2b2929;
    background-color: rgba(59, 59, 59, 0.2);
    
    &:before {
      background-color: #2b2929;
    }
  }

  //未接单
  &.miss {
    color: #345b5e;
    background-color: rgba(51, 107, 81, 0.2);
    
    &:before {
      background-color: #345b5e;
    }
  }

  //未完成
  &.incomplete {
    color: #63643c;
    background-color: rgba(141, 140, 63, 0.2);
    
    &:before {
      background-color: #63643c;
    }
  }

  //已完成
  &.complete {
    color: #3ee755;
    background-color: rgba(165, 223, 141, 0.2);
    
    &:before {
      background-color: #3ee755;
    }
  }

  //已拒绝
  &.refuse {
    color: #2b2929;
    background-color: rgba(59, 59, 59, 0.2);
    
    &:before {
      background-color: #2b2929;
    }
  }

  //无状态
  &.none {
    color: #59719d;
    background-color: rgba(89, 113, 157, 0.2);
    
    &:before {
      background-color: #59719d;
    }
  }
}

.status {
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding: 4px 8px;
  font-size: 12px;
  
  &:before {
    content: '';
    width: 4px;
    height: 4px;
    border-radius: 50%;
    margin-right: 4px;
  }
  
  &.math {
    color: #2ba972;
    background-color: rgba(43, 169, 114, 0.2);
    
    &:before {
      background-color: #2ba972;
    }
  }
  
  &.pe {
    color: #9f2ba9;
    background-color: rgba(169, 43, 169, 0.2);
    
    &:before {
      background-color: #9f2ba9;
    }
  }

  &.eng {
    color: #a96e2b;
    background-color: rgba(169, 156, 43, 0.2);
    
    &:before {
      background-color: #a96e2b;
    }
  }

  &.phy {
    color: #2b9aa9;
    background-color: rgba(43, 169, 148, 0.2);
    
    &:before {
      background-color: #2b9aa9;
    }
  }

  &.human {
    color: #a92b51;
    background-color: rgba(169, 43, 81, 0.2);
    
    &:before {
      background-color: #a92b51;
    }
  }

  &.che {
    color: #a9a72b;
    background-color: rgba(161, 169, 43, 0.2);
    
    &:before {
      background-color: #a9a72b;
    }
  }

  &.disabled {
    color: #59719d;
    background-color: rgba(89, 113, 157, 0.2);
    
    &:before {
      background-color: #59719d;
    }
  }

  &.refused {
    color: #2b2929;
    background-color: rgba(59, 59, 59, 0.2);
    
    &:before {
      background-color: #2b2929;
    }
  }
}

.gridView {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -8px;
  
  @media screen and (max-width: 520px) {&{
    margin: 0;
  }}
  
  .products-header {
    display: none;
  }
  
  .products-row {
    margin: 8px;
    width: calc(25% - 16px);
    background-color: #f3f6fd;
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    transition: transform .2s;
    position: relative;
    
    &:hover {
      transform: scale(1.01);
      box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
      
      .cell-more-button {
        display: flex;
      }
    }

    .more-button {
      display: none;
    }
    
    @media screen and (max-width: 1024px) {&{
      width: calc(33.3% - 16px);
    }}
    
    @media screen and (max-width: 820px) {&{
      width: calc(50% - 16px);
    }}
    
    @media screen and (max-width: 520px) {&{
      width: 100%;
      margin: 8px 0;
      
      &:hover {
        transform: none;
      }
    }}
    
    .cell-more-button {
      border: none;
      padding: 0;
      border-radius: 4px;
      position: absolute;
      top: 16px;
      right: 16px;
      z-index: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width:24px;
      height: 24px;
      background-color: rgba(16, 24, 39, 0.7);
      color: #fff;
      cursor: pointer;
      display: none;
    }
  }
  
  .product-cell {
    color: #1f1c2e;
    font-size: $font-small;
    
    &:not(.image) {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    &:not(.price) {
        margin-bottom: 8px;
    }
    
    &.image  span {
      font-size: 18px;
      line-height: 24px;
    }

    img {
      width: 100%;
      height: 200px;
      object-fit: cover;
      border-radius: 4px;
      margin-bottom: 16px;
    }
  }
  
  .cell-label { opacity: 0.6; }
}

.btngroup {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
</style>
