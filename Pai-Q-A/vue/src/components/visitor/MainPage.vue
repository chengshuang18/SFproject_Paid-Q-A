/*
 * @Author: hjj 
 * @Date: 2021-11-03 12:24:53 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-14 16:58:40
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
                    <img src="https://i.loli.net/2021/10/23/nMylftNjSchxr8A.jpg?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTE2fHx3b21hbnxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=900&q=60" alt="Account">
                </div>
                <div class="account-info-name">Visitor</div>
                <button class="account-info-more">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-horizontal"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
                </button>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 0">
            <div class="app-content-header">
                <h1 class="app-content-headerText"></h1>
                <button class="app-content-headerButton" @click="toLogin">登录</button>
            </div>
            <div class="app-content-actions">
              <input class="search-bar" placeholder="Search..." type="text" v-model="searchName" @keyup.enter="changeAnswererSearch">
              <div class="app-content-actions-wrapper">
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
                            <el-button type="text" disabled>
                                提问
                            </el-button>
                            <el-button type="text" disabled>
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
                <h1 class="app-content-headerText">登录查看回答信息</h1>
                <button class="app-content-headerButton" @click="toLogin">登录</button>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 2">
            <div class="app-content-header">
                <h1 class="app-content-headerText">登录查看订单信息</h1>
                <button class="app-content-headerButton" @click="toLogin">登录</button>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 3">
            <div class="app-content-header">
                <h1 class="app-content-headerText">登录查看设置信息</h1>
                <button class="app-content-headerButton" @click="toLogin">登录</button>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
  name: "VisitorMainPage",
  data() {
    return {
        sideBar: 0,
        showMethod: 0,
        resList: [],
        allAnswerer: [],
        searchName: "",
    };
  },
  methods: {
    changeSideBar(val) {
      if(this.sideBar != val)
        this.sideBar = val;
    },
    toLogin() {
      this.$router.push({ path: "/" });
    },
    changeShowMethod(val) {
        if(this.showMethod != val)
            this.showMethod = val;
    },
    fetchResData() {
      if (sessionStorage.getItem('ansList')){
        var List = sessionStorage.getItem('ansList');
        this.resList = JSON.parse(List);
        this.allAnswerer = this.resList;
      }
      else{
        this.resList = this.$ansList;
        this.allAnswerer = this.$ansList;
      }
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
  },
  created() {
    this.fetchResData();
  },
  components: {},
  watch: {},
}
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
      //position: absolute;
      //top: 16px;
      //right: 16px;
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
