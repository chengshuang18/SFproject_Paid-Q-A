/* 
 * @Author: hjj 
 * @Date: 2021-08-25 17:08:19 
 * @Last Modified by: wangyang
 * @Last Modified time: 2021-11-04 11:23:34
 */

<template>
  <el-container>
    <el-empty v-show="isTeacher" description="您还不是老师"></el-empty>
    <el-row v-show="!isTeacher" v-for="item in allQuestions" :key="item.title">
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
    <Details :detailsVisible="detailsVisible" :orderDetails="orderDetails" @update_detailsVisible="update_detailsVisible" />
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
  name: "Answer",
  data() {
    return {
      isTeacher: false,
      allQuestions: [],
      detailsVisible: false,
      refuseVisible: false,
      refuseButton: [],
      orderDetails: {},
    };
  },
  methods: {
    // 显示详情界面
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
    update_detailsVisible(val) {
      this.detailsVisible = val;
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
    // 显示聊天界面
    showChat(val) {
      this.$http({
        url: this.$url + "api/senduserlist",
        method: "get",
        params: { username: this.$userMsg.username },
      })
        .then((res) => {
          var List = [];
          var resList = [];
          List = res.data.userList;
          var listCount = [];
          List.forEach(async (item, index) => {
            let promise = this.$tim.getMessageList({ conversationID: "C2C" + item, count: 10 });
            var M = [];
            await promise.then(function(imResponse) {
              const messageList = imResponse.data.messageList; // 消息列表。
              const isCompleted = imResponse.data.isCompleted; // 表示是否已经拉完所有消息。
              console.log("messageList: ", messageList);
              console.log("isCompleted: ", isCompleted);
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
              username: item,
              status: "online",
              src: "https://i.loli.net/2021/10/23/nMylftNjSchxr8A.jpg",
              message: M,
            };
            resList[index] = obj;
            listCount.push(index);
            if (listCount.length == List.length) {
              $List = resList;
              for (let i = 0; i < $List.length; i++) {
                if ($List[i].username == val) {
                  $isActive = i;
                  break;
                }
              }
              this.$router.push({ path: "/chat" });
            }
          });
        })
        .catch((error) => {
          alter(error);
        });
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
  // 获取回答者的所有订单
  mounted() {
    this.$http({
      url: this.$url + "api/selectorderbyanswerer",
      method: "get",
      params: { answerer: this.$userMsg.username },
    }).then((res) => {
      this.allQuestions = res.data.orders;
    });
  },
};
</script>

<style scoped>
.el-container {
  text-align: center;
  line-height: 20px;
  display: inline-block;
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
