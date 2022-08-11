/*
 * @Author: hjj 
 * @Date: 2021-10-30 09:37:28 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-14 11:47:24
 */

<template>
<div class="mainbody">
    <div class="app-container">
        <div class="sidebar">
            <ul class="sidebar-list">
                <li class="sidebar-list-item" :class="{active: sideBar == 0}" @click="changeSideBar(0)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-shopping-bag"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                    <span>订单审核</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 1}" @click="changeSideBar(1)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-inbox"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>
                    <span>管理人员</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 3}" @click="changeSideBar(3)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-pie-chart"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>
            
                    <span>参数调整</span>
                    </a>
                </li>
                <li class="sidebar-list-item" :class="{active: sideBar == 2}" @click="changeSideBar(2)">
                    <a>
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            
                    <span>个人中心</span>
                    </a>
                </li>
            </ul>
        </div>
        <div class="app-content" v-show="sideBar == 0">
            <div class="app-content-header">
                <h1 class="app-content-headerText">订单审核</h1>
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
                        订单状态
                    </div>
                    <div class="product-cell status-cell">
                        订单类型
                    </div>
                    <div class="product-cell price">
                        操作
                    </div> 
                </div>
                <div class="products-row" v-for="(item,Index) in checkorderList" :key="Index">
                    <div class="product-cell image">
                        <span>{{item.questioner}}</span>
                    </div>
                    <div class="product-cell image">
                        <span>{{item.answerer}}</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="status" :class="
                       item.check_mark == 1 ? 'disabled' :
                      (item.check_mark == 2 ? 'math' : 'refused')">
                        {{item.check_mark == 1 ? "未处理" : 
                        (item.check_mark == 2 ? "通过" : "不通过")}}
                      </span>
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
                        {{item.field == 1 ? "英语" : 
                        (item.field == 2 ? "社会人文" : 
                        (item.field == 3 ? "物理" : 
                        (item.field == 4 ? "化学" : 
                        (item.field == 5 ? "体育" : "数学"
                        ))))}}
                      </span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="showDetail(item.title,item.content)">详情</el-button>
                        <el-button v-if="item.check_mark == 1" type="text" @click="pass(item.order_id, 2)">
                          通过
                        </el-button>
                        <el-button v-else type="text" disabled>
                          通过
                        </el-button>
                        <el-button v-if="item.check_mark == 1" type="text" @click="pass(item.order_id, 3)">
                          不通过
                        </el-button>
                        <el-button v-else type="text" disabled>
                          不通过
                        </el-button>
                        <el-button v-if="item.check_mark == 1" type="text" disabled>
                          删除
                        </el-button>
                        <el-button v-else type="text" @click="del(item.order_id)">
                          删除
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 1">
            <div class="app-content-header">
                <h1 class="app-content-headerText">管理人员</h1>
                <button class="app-content-headerButton" @click="addAdmin">添加管理员</button>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                    <div class="product-cell image">
                        用户名
                    </div>
                    <div class="product-cell category">
                        账号类型
                    </div>
                    <div class="product-cell status-cell">
                        审核类型
                    </div>
                    <div class="product-cell stock">
                        创建时间
                    </div> 
                    <div class="product-cell price">
                        操作
                    </div> 
                </div>
                <div class="products-row" v-for="(item,index) in manageList" :key="index">
                    <div class="product-cell image">
                        <span>{{item.username}}</span>
                    </div>
                    <div class="product-cell status-cell">
                        <span class="userstatus" :class="item.management > 0 ? 'auditor' : 'manage'">{{item.management > 0 ? "审核员" : "管理员"}}</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="status" :class="
                       item.management == 0 ? 'disabled' :
                      (item.management == 1 ? 'math' :
                      (item.management == 2 ? 'eng' :
                      (item.management == 3 ? 'human' :
                      (item.management == 4 ? 'phy' :
                      (item.management == 5 ? 'che' : 'pe'
                      )))))
                      ">
                        {{item.management == 1 ? "数学" : 
                        (item.management == 2 ? "英语" : 
                        (item.management == 3 ? "社会人文" : 
                        (item.management == 4 ? "物理" : 
                        (item.management == 5 ? "化学" : 
                        (item.management == 6 ? "体育" : "无"
                        )))))}}
                      </span>
                    </div>
                    <div class="product-cell stock">{{item.confirmed_at}}</div>
                    <div class="product-cell price">
                        <el-button v-if="item.management" :key="index + '_ONLY'" type="text" disabled>升级</el-button>
                        <el-button v-else type="text" @click="upGrade(item.username,index)">升级</el-button>
                        <el-button v-if="item.management" :key="index+'_only'" type="text" @click="upDate(item.username,index)">更新</el-button>
                        <el-button v-else type="text" disabled>更新</el-button>
                        <el-button type="text" @click="delAdmin(item.username)">删除</el-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 2">
            <div class="app-content-header">
                <h1 class="app-content-headerText">个人中心</h1>
                <button class="app-content-headerButton" @click="changePassword">
                  修改密码
                </button>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                    <div class="product-cell image">
                        信息展示
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>用户名</span>
                    </div>
                    <div class="product-cell status-cell">
                        <span class="userstatus user">
                          {{manageMsg.username}}
                        </span>
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>账号类型</span>
                    </div>
                    <div class="product-cell status-cell">
                        <span class="userstatus"
                        :class="manageMsg.username == 'root' ? 'admin' :
                        (manageMsg.management > 0 ? 'auditor' : 'manage')">
                          {{manageMsg.username == 'root' ? "admin" :
                          (manageMsg.management > 0 ? "审核员" : "管理员")}}
                        </span>
                    </div>
                </div>
                <div class="products-row" v-show="manageMsg.username != 'root'">
                    <div class="product-cell image">
                        <span>审核类型</span>
                    </div>
                    <div class="product-cell status-cell">
                      <span class="status" :class="
                       manageMsg.management == 0 ? 'disabled' :
                      (manageMsg.management == 1 ? 'math' :
                      (manageMsg.management == 2 ? 'eng' :
                      (manageMsg.management == 3 ? 'human' :
                      (manageMsg.management == 4 ? 'phy' :
                      (manageMsg.management == 5 ? 'che' : 'pe'
                      )))))
                      ">
                        {{manageMsg.management == 1 ? "数学" : 
                        (manageMsg.management == 2 ? "英语" : 
                        (manageMsg.management == 3 ? "社会人文" : 
                        (manageMsg.management == 4 ? "物理" : 
                        (manageMsg.management == 5 ? "化学" : 
                        (manageMsg.management == 6 ? "体育" : "无"
                        )))))}}
                      </span>
                    </div>
                </div>
            </div>
        </div>
        <div class="app-content" v-show="sideBar == 3">
            <div class="app-content-header">
                <h1 class="app-content-headerText">参数调整</h1>
            </div>
            <div class="products-area-wrapper tableView">
                <div class="products-header">
                    <div class="product-cell image">
                        参数名称
                    </div>
                    <div class="product-cell image">
                        当前值
                    </div>
                    <div class="product-cell price">
                        操作
                    </div> 
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>问题定价区间</span>
                    </div>
                    <div class="product-cell image">
                        <span class="paramstatus num">{{minDollar}}</span> &nbsp;
                        <span class="paramstatus dollor">$</span> &nbsp;&nbsp;
                        <span> ~ </span> &nbsp;&nbsp;
                        <span class="paramstatus num">{{maxDollar}}</span> &nbsp;
                        <span class="paramstatus dollor">$</span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="downmindollar">下限减少</el-button>
                        <el-button type="text" @click="upmindollar">下限增加</el-button>
                        <el-button type="text" @click="downmaxdollar">上限减少</el-button>
                        <el-button type="text" @click="upmaxdollar">上限增加</el-button>
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>接单等待时间</span>
                    </div>
                    <div class="product-cell image">
                        <span class="paramstatus num">{{orderWait}}</span> &nbsp;
                        <span class="paramstatus hour">min</span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="downorderwait">减少</el-button>
                        <el-button type="text" @click="uporderwait">增加</el-button>
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>首次作答等待时间</span>
                    </div>
                    <div class="product-cell image">
                        <span class="paramstatus num">{{answerWait}}</span> &nbsp;
                        <span class="paramstatus hour">min</span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="downanswerwait">减少</el-button>
                        <el-button type="text" @click="upanswerwait">增加</el-button>
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>最大回答次数</span>
                    </div>
                    <div class="product-cell image">
                        <span class="paramstatus num">{{maxTimes}}</span> &nbsp;
                        <span class="paramstatus times">times</span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="downmaxtimes">减少</el-button>
                        <el-button type="text" @click="upmaxtimes">增加</el-button>
                    </div>
                </div>
                <div class="products-row">
                    <div class="product-cell image">
                        <span>最长回答时间</span>
                    </div>
                    <div class="product-cell image">
                        <span class="paramstatus num">{{maxTime}}</span> &nbsp;
                        <span class="paramstatus hour">min</span>
                    </div>
                    <div class="product-cell price">
                        <el-button type="text" @click="downmaxtime">减少</el-button>
                        <el-button type="text" @click="upmaxtime">增加</el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <el-dialog title="详情" :visible.sync="dialogTableVisible">
      <el-table :data="gridData">
        <el-table-column property="title" label="标题" width="200"></el-table-column>
        <el-table-column property="content" label="内容" width="500"></el-table-column>
      </el-table>
    </el-dialog>
</div>
</template>

<script>
export default {
  name: "ExamineMainPage",
  data() {
    return {
        sideBar: 1,
        manageList: [],
        manageMsg: {},
        checkorderList: [],
        gridData: [
          {
            title: "",
            content: "",
          }
        ],
        dialogTableVisible: false,
        minDollar: 0,
        maxDollar: 100,
        orderWait: 24,
        answerWait: 24,
        maxTimes: 10,
        maxTime: 48,
    };
  },
  methods: {
    changeSideBar(val) {
      if(this.sideBar != val)
        this.sideBar = val;
    },
    upDate(v, i) {
      if(this.manageMsg.username == "root"){
        this.$prompt('1～6代表[数学、英语、社会人文、物理、化学、体育]', '更新', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /[1-6]{1,1}/,
          inputPlaceholder: '请输入1～6的整数',
          inputErrorMessage: '输入格式错误'
        })
        .then(({ value }) => {
          var val = this.manageList[i].management;
          if(val == parseInt(value)){
            this.$message({
              showClose: true,
              message: "与原设定一致",
              type: "error",
            });
          }
          else{
            if(value == "1")
              val = "数学";
            else if(value == "2")
              val = "英语";
            else if(value == "3")
              val = "社会人文";
            else if(value == "4")
              val = "物理";
            else if(value == "5")
              val = "化学";
            else
              val = "体育";
            const qs = require("qs");
            this.$http({
              url: this.$url + "api/admin/adminpermission",
              method: "post",
              data: qs.stringify({
                field: parseInt(value),
                username: v,
              }),
            })
            .then((res) => {
              let tmp = this.manageList;
              tmp[i].management = parseInt(value);
              this.manageList = tmp;
              this.$message({
                type: 'success',
                message: '设置审核领域为: ' + val
              });
            })
            .catch((error) => {
              if (error.response.status == 401) {
                this.$message({
                  showClose: true,
                  message: "用户名不存在",
                  type: "error",
                });
              }
            })
          }
        })
        .catch(() => {    
        });
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upGrade(v, i) {
      if(this.manageMsg.username == "root"){
        this.$prompt('1～6代表[数学、英语、社会人文、物理、化学、体育]', '升级', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /[1-6]{1,1}/,
          inputPlaceholder: '请输入1～6的整数',
          inputErrorMessage: '输入格式错误'
        })
        .then(({ value }) => {
          var val = "";
          if(value == "1")
            val = "数学";
          else if(value == "2")
            val = "英语";
          else if(value == "3")
            val = "社会人文";
          else if(value == "4")
            val = "物理";
          else if(value == "5")
            val = "化学";
          else
            val = "体育";
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/adminpermission",
            method: "post",
            data: qs.stringify({
              field: parseInt(value),
              username: v,
            }),
          })
          .then((res) => {
            let tmp = this.manageList;
            tmp[i].management = parseInt(value);
            this.manageList = tmp;
            this.$message({
              type: 'success',
              message: '设置审核领域为: ' + val
            });
          })
          .catch((error) => {
            if (error.response.status == 401) {
              this.$message({
                showClose: true,
                message: "用户名不存在",
                type: "error",
              });
            }
          })
        })
        .catch(() => {    
        });
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    addAdmin() {
      if(this.manageMsg.username == "root"){
        this.$prompt('输入用户名', '添加', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^[a-zA-Z]([-_a-zA-Z0-9]{2,8})$/,
          inputPlaceholder: '请输入2-8位长度并以字母开头的用户名',
          inputErrorMessage: '输入格式错误'
        })
        .then(({ value }) => {
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/addadmin",
            method: "post",
            data: qs.stringify({
              username: value,
            }),
          })
          .then((res) => {
            var standardDate = new Date();
            var year = standardDate.getFullYear();
            var month= standardDate.getMonth()+1;
            if(month < 10)
                month = '0' + month;
            var day = standardDate.getDate();
            if(day < 10)
                day = '0' + day;
            var hour = standardDate.getHours();
            if(hour < 10)
                hour = '0' + hour;
            var minute = standardDate.getMinutes();
            if(minute < 10)
                minute = '0' + minute;
            var second = standardDate.getSeconds();
            if(second < 10)
                second = '0' + second;
            var formatting = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second;
            let tmp = this.manageList;
            let obj = {
              management: 0,
              username: value,
              confirmed_at: formatting
            };
            tmp.push(obj);
            this.manageList = tmp;
            sessionStorage.removeItem('manageList');
            sessionStorage.setItem('manageList', JSON.stringify(this.manageList));
            this.$message({
              type: 'success',
              message: '初始密码为: ' + res.data.password,
              time: 5000
            });
          })
          .catch((error) => {
            if (error.response.status == 403) {
              this.$message({
                showClose: true,
                message: "用户名已存在",
                type: "error",
              });
            }
          })
        })
        .catch(() => {    
        });
      }
      else {
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    delAdmin(val) {
      if(this.manageMsg.username == "root"){
        this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$http({
            url: this.$url + "api/admin/deleteadmin",
            method: "get",
            params: { username: val },
          })
          .then(() => {
            let tmp = this.manageList;
            tmp.forEach(function(item, index, arr) {
                if(item.username == val) {
                    arr.splice(index, 1);
                }
            });
            this.manageList = tmp;
            sessionStorage.removeItem('manageList');
            sessionStorage.setItem('manageList', JSON.stringify(this.manageList));
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          })
          .catch((error) => {
            if (error.response.status == 401) {
              this.$message({
                message: "用户不存在",
                type: "error",
              });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
      }
      else {
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    changePassword() {
      var that = this;
      var V = "";
      var v = "";
      this.$prompt('原密码', '修改密码', {
        inputPlaceholder: '请输入原密码',
        confirmButtonText: '下一步',
        cancelButtonText: '取消',
        inputErrorMessage: '输入不能为空',
        inputValidator: (value) => {
            if(!value) {
                return '输入不能为空';
            }else{
              V = value;
            }
        },
        callback: function (action, instance) {
            if(action === 'confirm') {       
              that.$prompt('新密码', '修改密码', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputErrorMessage: '输入不能为空',
                inputValidator: (val) => {
                    if(!val) {
                        return '输入不能为空';
                    }else{
                      v = val;
                    }
                },
              })
              .then(({ val }) => {
                const qs = require("qs");
                that.$http({
                  url: that.$url + "api/admin/changepassword",
                  method: "post",
                  data: qs.stringify({
                    newpassword: v,
                    originalpassword: V,
                    username: that.manageMsg.username,
                  }),
                })
                .then((res) => {
                  that.$message({
                    type: 'success',
                    message: '修改成功',
                    time: 1000
                  });
                })
                .catch((error) => {
                  if (error.response.status == 401) {
                    that.$message({
                      showClose: true,
                      message: "验证错误",
                      type: "error",
                    });
                  }
                })
              })
              .catch((error) => {});
            }else {
                that.$message({
                    type: 'info',
                    message: '取消修改'
                });
            }
        }
     })
    },
    pass(id, val) {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/checkorder",
        method: "post",
        data: qs.stringify({
          order_id: id,
          check_mark: val,
        }),
      })
      .then(() => {
        if (val == 2){
          let tmp = this.checkorderList;
          for(let i = 0;i < tmp.length;i++){
            if(tmp[i].order_id == id)
              tmp[i].check_mark = val;
          }
          this.checkorderList = tmp;
          this.checkorderList = this.checkorderList.slice();
          sessionStorage.removeItem('checkorderList');
          sessionStorage.setItem('checkorderList',JSON.stringify(this.checkorderList));
          this.$message({
              type: 'success',
              message: '订单审核结果为:通过'
          });
        }
        else{
          let tmp = this.checkorderList;
          for(let i = 0;i < tmp.length;i++){
            if(tmp[i].order_id == id){
              tmp[i].check_mark = val;
              this.$http({
                url: this.$url + "api/walletmanagement",
                method: 'post',
                data: qs.stringify({
                    "username": tmp[i].questioner,
                    "money": tmp[i].price,
                })
              })
            }
          }
          this.checkorderList = tmp;
          this.checkorderList = this.checkorderList.slice();
          sessionStorage.removeItem('checkorderList');
          sessionStorage.setItem('checkorderList',JSON.stringify(this.checkorderList));
          this.$message({
              type: 'info',
              message: '订单审核结果为:不通过'
          });
        }
      })
      .catch(() => {});
    },
    del(id) {
      const qs = require("qs");
      this.$http({
        url: this.$url + "api/hiddencheckorder",
        method: "post",
        data: qs.stringify({
          order_id: id,
        }),
      })
      .then(() => {
        let tmp = this.checkorderList;
        tmp.forEach(function(item, index, arr) {
            if(item.order_id == id) {
                arr.splice(index, 1);
            }
        });
        this.checkorderList = tmp;
        this.checkorderList = this.checkorderList.slice();
        sessionStorage.removeItem('checkorderList');
        sessionStorage.setItem('checkorderList',JSON.stringify(this.checkorderList));
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      })
      .catch(() => {})
    },
    showDetail(title,content) {
      let obj = [
        {
          title: title,
          content: content,
        }
      ];
      this.gridData = obj;
      this.dialogTableVisible = true;
    },
    downmindollar() {
      if(this.manageMsg.username == "root"){
        if(this.minDollar < 1)
          this.$message({
            type: 'warning',
            message: '设定值不能为负数!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              lowest_prices: this.minDollar - 1,
            }),
          })
          .then(() => {
            this.minDollar = this.minDollar - 1;
            sessionStorage.removeItem('sysparam_lowest_prices');
            sessionStorage.setItem('sysparam_lowest_prices', this.minDollar);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upmindollar() {
      if(this.manageMsg.username == "root"){
        if(this.minDollar >= this.maxDollar - 1)
          this.$message({
            type: 'warning',
            message: '设定值不能超过最大值!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              lowest_prices: this.minDollar + 1,
            }),
          })
          .then(() => {
            this.minDollar = this.minDollar + 1;
            sessionStorage.removeItem('sysparam_lowest_prices');
            sessionStorage.setItem('sysparam_lowest_prices', this.minDollar);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    downmaxdollar() {
      if(this.manageMsg.username == "root"){
        if(this.maxDollar - 1 <= this.minDollar)
          this.$message({
            type: 'warning',
            message: '设定值不能小于最大值!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              top_prices: this.maxDollar - 1,
            }),
          })
          .then(() => {
            this.maxDollar = this.maxDollar - 1;
            sessionStorage.removeItem('sysparam_top_prices');
            sessionStorage.setItem('sysparam_top_prices', this.maxDollar);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upmaxdollar() {
      if(this.manageMsg.username == "root"){
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/admin/systemconfig",
          method: "post",
          data: qs.stringify({
            top_prices: this.maxDollar + 1,
          }),
        })
        .then(() => {
          this.maxDollar = this.maxDollar + 1;
          sessionStorage.removeItem('sysparam_top_prices');
          sessionStorage.setItem('sysparam_top_prices', this.maxDollar);
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '设定失败!'
          });
        })
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    downorderwait() {
      if(this.manageMsg.username == "root"){
        if(this.orderWait < 1)
          this.$message({
            type: 'warning',
            message: '设定值不能为负数!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              wait_receive: this.orderWait - 1,
            }),
          })
          .then(() => {
            this.orderWait = this.orderWait - 1;
            sessionStorage.removeItem('sysparam_wait_receive');
            sessionStorage.setItem('sysparam_wait_receive', this.orderWait);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    uporderwait() {
      if(this.manageMsg.username == "root"){
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/admin/systemconfig",
          method: "post",
          data: qs.stringify({
            wait_receive: this.orderWait + 1,
          }),
        })
        .then(() => {
          this.orderWait = this.orderWait + 1;
          sessionStorage.removeItem('sysparam_wait_receive');
          sessionStorage.setItem('sysparam_wait_receive', this.orderWait);
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '设定失败!'
          });
        })
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    downanswerwait() {
      if(this.manageMsg.username == "root"){
        if(this.answerWait < 1)
          this.$message({
            type: 'warning',
            message: '设定值不能为负数!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              wait_answer: this.answerWait - 1,
            }),
          })
          .then(() => {
            this.answerWait = this.answerWait - 1;
            sessionStorage.removeItem('sysparam_wait_answer');
            sessionStorage.setItem('sysparam_wait_answer', this.answerWait);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upanswerwait() {
      if(this.manageMsg.username == "root"){
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/admin/systemconfig",
          method: "post",
          data: qs.stringify({
            wait_answer: this.answerWait + 1,
          }),
        })
        .then(() => {
          this.answerWait = this.answerWait + 1;
          sessionStorage.removeItem('sysparam_wait_answer');
          sessionStorage.setItem('sysparam_wait_answer', this.answerWait);
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '设定失败!'
          });
        })
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    downmaxtimes() {
      if(this.manageMsg.username == "root"){
        if(this.maxTimes < 1)
          this.$message({
            type: 'warning',
            message: '设定值不能为负数!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              times_AQ: this.maxTimes - 1,
            }),
          })
          .then(() => {
            this.maxTimes = this.maxTimes - 1;
            sessionStorage.removeItem('sysparam_times_AQ');
            sessionStorage.setItem('sysparam_times_AQ', this.maxTimes);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upmaxtimes() {
      if(this.manageMsg.username == "root"){
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/admin/systemconfig",
          method: "post",
          data: qs.stringify({
            times_AQ: this.maxTimes + 1,
          }),
        })
        .then(() => {
          this.maxTimes = this.maxTimes + 1;
          sessionStorage.removeItem('sysparam_times_AQ');
          sessionStorage.setItem('sysparam_times_AQ', this.maxTimes);
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '设定失败!'
          });
        })
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    downmaxtime() {
      if(this.manageMsg.username == "root"){
        if(this.maxTime < 1)
          this.$message({
            type: 'warning',
            message: '设定值不能为负数!'
          });
        else{
          const qs = require("qs");
          this.$http({
            url: this.$url + "api/admin/systemconfig",
            method: "post",
            data: qs.stringify({
              time_service: this.maxTime - 1,
            }),
          })
          .then(() => {
            this.maxTime = this.maxTime - 1;
            sessionStorage.removeItem('sysparam_time_service');
            sessionStorage.setItem('sysparam_time_service', this.maxTime);
          })
          .catch(() => {
            this.$message({
              type: 'error',
              message: '设定失败!'
            });
          })
        }
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    upmaxtime() {
      if(this.manageMsg.username == "root"){
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/admin/systemconfig",
          method: "post",
          data: qs.stringify({
            time_service: this.maxTime + 1,
          }),
        })
        .then(() => {
          this.maxTime = this.maxTime + 1;
          sessionStorage.removeItem('sysparam_time_service');
          sessionStorage.setItem('sysparam_time_service', this.maxTime);
        })
        .catch(() => {
          this.$message({
            type: 'error',
            message: '设定失败!'
          });
        })
      }
      else{
        this.$message({
          showClose: true,
          message: "您不可进行此操作",
          type: "error",
        });
      }
    },
    fetchResData() {
      if(sessionStorage.getItem('manageList')){
        let storage_manageList = sessionStorage.getItem('manageList');
        this.manageList = JSON.parse(storage_manageList);
      }
      else{
        this.manageList = this.$manageList;
      }

      if(sessionStorage.getItem('manageMsg')){
        let storage_manageMsg = sessionStorage.getItem('manageMsg');
        this.manageMsg = JSON.parse(storage_manageMsg);
      }
      else{
        this.manageMsg = this.$manageMsg;
      }

      let myfield = 100;
      if(this.manageMsg.username != "root"){
          myfield = this.manageMsg.management;
      }
      this.$http({
          url: this.$url + "api/checkorderlist",
          method: "get",
          params: { field: myfield },
      })
      .then((RES) => {
          this.checkorderList = RES.data.userList;
      })
      .catch((error) => {
          console.log(error);
      })

      if(sessionStorage.getItem('sysparam_lowest_prices')){
        let sysparam_lowest_prices = sessionStorage.getItem('sysparam_lowest_prices');
        let sysparam_top_prices = sessionStorage.getItem('sysparam_top_prices');
        let sysparam_wait_answer = sessionStorage.getItem('sysparam_wait_answer');
        let sysparam_wait_receive = sessionStorage.getItem('sysparam_wait_receive');
        let sysparam_times_AQ = sessionStorage.getItem('sysparam_times_AQ');
        let sysparam_time_service = sessionStorage.getItem('sysparam_time_service');
        this.minDollar = parseInt(sysparam_lowest_prices);
        this.maxDollar = parseInt(sysparam_top_prices);
        this.answerWait = parseInt(sysparam_wait_answer);
        this.orderWait = parseInt(sysparam_wait_receive);
        this.maxTimes = parseInt(sysparam_times_AQ);
        this.maxTime = parseInt(sysparam_time_service);
      }
      else{
        this.minDollar = this.$sysparam.lowest_prices;
        this.maxDollar = this.$sysparam.top_prices;
        this.answerWait = this.$sysparam.wait_answer;
        this.orderWait = this.$sysparam.wait_receive;
        this.maxTimes = this.$sysparam.times_AQ;
        this.maxTime = this.$sysparam.time_service;
      }
    }
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
  @include searchIcon('fff');
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

.filter-button-wrapper {
  position: relative;
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
    @include arrowDown('fff');
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
    
    .light & {
      @include arrowDown('1f1c2e');
    }
    
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
    }
    
    .cell-more-button {
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
    margin-bottom: 8px;
    
    &:not(.image) {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    
    &.image  span {
      font-size: 18px;
      line-height: 24px;
    }

    img {
      width: 100%;
      height: 140px;
      object-fit: cover;
      border-radius: 4px;
      margin-bottom: 16px;
    }
  }
  
  .cell-label { opacity: 0.6; }
}
</style>
