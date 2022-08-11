/* 
 * @Author: hjj 
 * @Date: 2021-08-25 17:12:34 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-04 13:55:25
 */

<template>
  <el-container>
    <el-empty v-show="haveOrder" description="您还没有订单"></el-empty>
    <el-header v-show="!haveOrder">
      <div>
        <el-button-group>
          <el-button type="primary" icon="el-icon-question" @click="changeQuestion()">提问订单</el-button>
          <el-button type="primary" @click="changeAnswer()">回答订单<i class="el-icon-reading el-icon--right"></i></el-button>
        </el-button-group>
        <el-button-group>
          <el-button type="primary" icon="el-icon-check" @click="changeOrdered()">已完成</el-button>
          <el-button type="primary" @click="changeOrdering()">未完成<i class="el-icon-close el-icon--right"></i></el-button>
        </el-button-group>
      </div>
      <div>
        <el-tag v-show="!haveOrder && showOrdered && showQuestion" effect="dark">已完成提问订单</el-tag>
        <el-tag v-show="!haveOrder && showOrdering && showQuestion" effect="dark">未完成提问订单</el-tag>
        <el-tag v-show="!haveOrder && showOrdered && showAnswer" effect="dark">已完成回答订单</el-tag>
        <el-tag v-show="!haveOrder && showOrdering && showAnswer" effect="dark">未完成回答订单</el-tag>
      </div>
    </el-header>
    <!-- 已完成提问订单 -->
    <el-empty v-show="!haveOrder && showOrdered && showQuestion && !orderedQuestion.length"></el-empty>
    <el-row v-show="!haveOrder && showOrdered && showQuestion" v-for="item in orderedQuestion" :key="item.title">
      <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <div style="padding: 14px;">
          <div class="clearfix">
            <div>
              <el-avatar icon="el-icon-user-solid"></el-avatar>
            </div>
            <span>{{ item.title }}</span>
            <div>
              <el-button type="text" @click="showDetails(item.order_id)">详情</el-button>
              <el-button type="text" @click="showChat(item.answerer)">聊天</el-button>
              <el-button type="text">申请退款</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </el-row>
    <!-- 已完成回答订单 -->
    <el-empty v-show="!haveOrder && showOrdered && showAnswer && !orderedAnswer.length"></el-empty>
    <el-row v-show="!haveOrder && showOrdered && showAnswer" v-for="item in orderedAnswer" :key="item.title + '-only'">
      <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <div style="padding: 14px;">
          <div class="clearfix">
            <div>
              <el-avatar icon="el-icon-user-solid"></el-avatar>
            </div>
            <span>{{ item.title }}</span>
            <div>
              <el-button type="text" @click="showDetails(item.order_id)">详情</el-button>
              <el-button type="text" @click="showChat(item.questioner)">聊天</el-button>
              <el-button type="text">查看反馈</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </el-row>
    <!-- 未完成提问订单 -->
    <el-empty v-show="!haveOrder && showOrdering && showQuestion && !orderingQuestion.length"></el-empty>
    <el-row v-show="!haveOrder && showOrdering && showQuestion" v-for="item in orderingQuestion" :key="item.title + '--only'">
      <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <div style="padding: 14px;">
          <div class="clearfix">
            <div>
              <el-avatar icon="el-icon-user-solid"></el-avatar>
            </div>
            <span>{{ item.title }}</span>
            <div>
              <el-button type="text" @click="showDetails(item.order_id)">详情</el-button>
              <el-button type="text" @click="showChat(item.answerer)">聊天</el-button>
              <el-button type="text" v-if="cancelButton[item.order_id]" disabled>取消提问</el-button>
              <el-button type="text" v-else @click="cancelOrder(item.order_id)">取消提问</el-button>
            </div>
          </div>
        </div>
      </el-card>
    </el-row>
    <!-- 未完成回答订单 -->
    <el-empty v-show="!haveOrder && showOrdering && showAnswer && !orderingAnswer.length"></el-empty>
    <el-row v-show="!haveOrder && showOrdering && showAnswer" v-for="item in orderingAnswer" :key="item.title + '---only'"> 
      <el-card :body-style="{ padding: '0px' }" shadow="hover">
        <div style="padding: 14px;">
          <div class="clearfix">
            <div>
              <el-avatar icon="el-icon-user-solid"></el-avatar>
            </div>
            <span>{{ item.title }}</span>
            <div>
              <el-button type="text" @click="showDetails(item.order_id)">详情</el-button>
              <el-button type="text" @click="showChat(item.questioner)">聊天</el-button>
              <el-button type="text" @click="finishOrder(item.order_id)">完成</el-button>
              <el-button type="text" @click="showRefuse(item.order_id)" :disabled="refuseButton[item.order_id] || item.end_mark == 5"
                >取消回答</el-button
              >
            </div>
          </div>
        </div>
      </el-card>
    </el-row>
    <Details :detailsVisible="detailsVisible" :orderDetails="orderDetails" @update_detailsVisible="update_detailsVisible"></Details>
    <ToRefuse
      :refuseVisible="refuseVisible"
      :orderDetails="orderDetails"
      @update_refuseVisible="update_refuseVisible"
      @update_refuseOrder="update_refuseOrder"
      @update_refuseButton="update_refuseButton"
    />
  </el-container>
</template>

<script>
import Details from "@/components/Details.vue";
import ToRefuse from "@/components/ToRefuse.vue";

export default {
  name: "Order",
  data() {
    return {
      haveOrder: false,
      orderedQuestion: [],  // 已完成提问订单
      orderedAnswer: [],    // 已完成回答订单
      orderingQuestion: [], // 未完成提问订单
      orderingAnswer: [],   // 未完成回答订单
      showOrdered: true,
      showOrdering: false,
      showQuestion: true,
      showAnswer: false,
      detailsVisible: false,
      refuseVisible: false,
      refuseButton: [],
      cancelButton: [],
      orderDetails: {},
      allAnsOrder: [],  // 所有回答者订单
      allAskOrder: [],  // 所有提问者订单
    };
  },
  methods: {
    // 订单的四种状态
    changeOrdered: function() {
      if (this.showOrdering == true) {
        this.showOrdering = false;
        this.showOrdered = true;
      }
    },
    changeOrdering: function() {
      if (this.showOrdered == true) {
        this.showOrdering = true;
        this.showOrdered = false;
      }
    },
    changeQuestion: function() {
      if (this.showAnswer == true) {
        this.showAnswer = false;
        this.showQuestion = true;
      }
    },
    changeAnswer: function() {
      if (this.showQuestion == true) {
        this.showAnswer = true;
        this.showQuestion = false;
      }
    },
    // 显示订单详情
    showDetails(val) {
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
      this.detailsVisible = true;
    },
    // 显示聊天界面
    showChat(val) {
      this.$http({
        url: this.$url + "api/senduserlist",
        method: "get",
        params: {username: this.$userMsg.username},
      })
      .then((res) => {
          var List = [];
          var resList = [];
          List = res.data.userList;
          var listCount = [];
          List.forEach(async (item,index)=>{
            let promise = this.$tim.getMessageList({conversationID: 'C2C' + item, count: 10});
            var M = [];
            await promise.then(function(imResponse) {
              const messageList = imResponse.data.messageList; // 消息列表。
              const isCompleted = imResponse.data.isCompleted; // 表示是否已经拉完所有消息。
              console.log("messageList: ",messageList);
              console.log("isCompleted: ",isCompleted);
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
              username: item,
              status: "online",
              src: "https://i.loli.net/2021/10/23/nMylftNjSchxr8A.jpg",
              message: M,
            };
            resList[index] = obj;
            listCount.push(index);
            if(listCount.length == List.length){
              $List = resList;
              for (let i = 0;i < $List.length;i++){
                if($List[i].username == val){
                  $isActive = i;
                  break;
                }
              }
              this.$router.push({ path: "/chat" });
            }
          })
      })
      .catch((error) => {
          alter(error);
      });
    },
    update_detailsVisible(val) {
      this.detailsVisible = val;
    },
    // 任何一方完成订单 #TODO
    finishOrder(val) {
      this.$http({
        url: this.$url + "api/finish",
        method: "get",
        params: { order_id: val },
      }).then(() => {
        
      })
    },
    // 取消提问界面
    cancelOrder(val) {
      let _this = this;
      this.$confirm("此操作将取消该提问，是否继续？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        const qs = require("qs");
        this.$http({
          url: this.$url + "api/cancelquestion",
          method: "post",
          data: qs.stringify({
            order_id: val,
          })
        }).then(() => {
          this.$message({
            type: "success",
            message: "取消提问成功！"
          });
          var tmp = _this.cancelButton;
          tmp[val] = true;
          _this.cancelButton = tmp;
          console.log(_this.cancelButton);
        })
      }).catch(() => {})
    },
    // 显示拒绝界面
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
  },
  components: {
    Details,
    ToRefuse,
  },
  mounted() {
    // 获取回答者订单信息
    this.$http({
      url: this.$url + "api/selectorderbyanswerer",
      method: "get",
      params: { answerer: this.$userMsg.username },
    }).then((res) => {
      this.allAnsOrder = res.data.orders;
      console.log("allAnsOrder", this.allAnsOrder);
    }).then(() => {
      for (let i of this.allAnsOrder) {
        // end_mark: 
        // 1: 未接单
        // 2: 已接单未完成
        // 3: 已接单已完成
        // 4: 隐藏订单
        // 5: 已拒绝订单
        if (i.end_mark == 1 || i.end_mark == 2) {
          this.orderingAnswer.push(i);
        }
        else if (i.end_mark == 3 || i.end_mark == 5) {
          this.orderedAnswer.push(i);
        }
      }
    })
    // 获取提问者订单信息
    this.$http({
      url: this.$url + "api/selectorderbyquestioner",
      method: "get",
      params: { questioner: this.$userMsg.username },
    }).then((res) => {
      this.allAskOrder = res.data.orders;
      console.log("allAskOrder:", this.allAskOrder)
    }).then(() => {
      for (let i of this.allAskOrder) {
        if (i.end_mark == 1 || i.end_mark == 2 && i.check_mark != 3) {
          this.orderingQuestion.push(i);
        }
        else if (i.end_mark == 3 || i.end_mark == 5 || i.check_mark == 3) {
          this.orderedQuestion.push(i);
        }
      }
    })
  },
};
</script>

<style scoped>
.el-container {
  text-align: center;
  line-height: 20px;
  display: inline-block;
}

.el-header {
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}

.clearfix {
  padding-left: 2.5vw;
  padding-right: 2.5vw;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.el-row {
  margin-bottom: 20px;
  width: 85vw;
}

.button {
  padding: 0;
  float: right;
}
</style>
