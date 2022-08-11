/* 
 * @Author: hjj 
 * @Date: 2021-08-25 10:50:22 
 * @Last Modified by: wangyang
 * @Last Modified time: 2021-11-02 20:57:10
 */

<template>
  <el-container>
    <el-header>
      <el-input placeholder="请输入内容" v-model="input">
        <el-button slot="append" type="primary" icon="el-icon-search"></el-button>
      </el-input>
      <el-button-group>
        <el-button type="primary" icon="el-icon-s-operation" @click="changeGrid()"></el-button>
        <el-button type="primary" icon="el-icon-menu" @click="changeRow()"></el-button>
      </el-button-group>
    </el-header>
    <el-main>
      <el-row
        v-show="gridShow"
        v-for="(r, count) in parseInt(resList.length / 3) * 3 === resList.length ? resList.length / 3 : parseInt(resList.length / 3) + 1"
        :key="r"
      >
        <el-col
          :span="6"
          v-for="(o, index) in resList.length - 3 * count > 2 ? 3 : resList.length - 3 * count"
          :key="o"
          :offset="index > 0 ? 2 : 0"
        >
          <div class="cards">
            <div v-bind:class="getOClass(count * 3 + index)" id="overview">
              <div class="card-content">
                <div class="row">
                  <div class="left col">
                    <h1 style="font-size: 2em;">{{ resList[count * 3 + index].username }}</h1>
                    <el-tag size="small"
                      >{{
                        resList[count * 3 + index].field == 0
                          ? "数学"
                          : resList[count * 3 + index].field == 1
                          ? "英语"
                          : resList[count * 3 + index].field == 2
                          ? "社会人文"
                          : resList[count * 3 + index].field == 3
                          ? "物理"
                          : resList[count * 3 + index].field == 4
                          ? "化学"
                          : "体育"
                      }}
                    </el-tag>
                  </div>
                  <div class="right col">
                    <div class="buttonGroup">
                      <h2>¥{{ resList[count * 3 + index].price }}</h2>
                      <div class="button" @click="showChat(resList[count * 3 + index].username)">聊天</div>
                      <div class="button" @click="showAsk(resList[count * 3 + index].username, resList[count * 3 + index].price)">提问</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-bind:class="getDClass(count * 3 + index)" id="dribbble">
              <a class="card-toggle" @click="classToggle(count * 3 + index)"><i class="el-icon-user"></i></a>
              <div class="card-content">
                <div class="row">
                  <div class="left col">
                    <h2>
                      <strong>{{ resList[count * 3 + index].resume }}</strong>
                    </h2>
                  </div>
                  <div class="right col">
                    <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" alt="" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row v-show="rowShow" v-for="(r, count) in resList.length" :key="r + '-only'">
        <el-card :body-style="{ padding: '0px' }" shadow="hover">
          <div style="padding: 14px;">
            <div class="clearfix">
              <el-descriptions title="用户信息">
                <template slot="extra">
                  <el-button type="text" @click="showAsk(resList[count].username, resList[count].price)">向他提问</el-button>
                  <el-button type="text" @click="showChat(resList[count].username)">和他聊天</el-button>
                </template>
                <el-descriptions-item label="用户名">{{ resList[count].username }}</el-descriptions-item>
                <el-descriptions-item label="个人简介">{{ resList[count].resume }}</el-descriptions-item>
                <el-descriptions-item label="回答领域">
                  <el-tag size="small"
                    >{{
                      resList[count].field == 0
                        ? "数学"
                        : resList[count].field == 1
                        ? "英语"
                        : resList[count].field == 2
                        ? "社会人文"
                        : resList[count].field == 3
                        ? "物理"
                        : resList[count].field == 4
                        ? "化学"
                        : "体育"
                    }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="提问单价">{{ resList[count].price }}元</el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-card>
      </el-row>
    </el-main>
    <Ask :askVisible="askDialog.askVisible" :answer="answer" :price="price" @update_askVisible="update_askVisible" />
  </el-container>
</template>

<script>
import Ask from "@/components/AskDialog.vue";
export default {
  name: "Question",
  props: {
    resList: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      askDialog: {
        askVisible: false,
      },
      select: "",
      input: "",
      gridShow: true,
      rowShow: false,
      isActive: [true, true, true, true, true, true, true, true],
      answer: "",
      price: 0,
    };
  },
  methods: {
    changeGrid: function() {
      if (this.gridShow == true) {
        this.gridShow = false;
        this.rowShow = true;
      }
    },
    changeRow: function() {
      if (this.rowShow == true) {
        this.gridShow = true;
        this.rowShow = false;
      }
    },
    handleQue(index, row) {
      console.log(index, row);
    },
    handleChat(index, row) {
      console.log(index, row);
    },
    classToggle: function(val) {
      let tempArr = [...this.isActive];
      tempArr[val] = !this.isActive[val];
      this.isActive = tempArr;
    },
    getOClass(val) {
      return { card: true, active: this.isActive[val] };
    },
    getDClass(val) {
      return { card: true, active: !this.isActive[val] };
    },
    showAsk(val, price) {
      this.answer = val;
      this.askDialog.askVisible = true;
      this.price = price;
    },
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
              //const nextReqMessageID = imResponse.data.nextReqMessageID; // 用于续拉，分页续拉时需传入该字段。
              const isCompleted = imResponse.data.isCompleted; // 表示是否已经拉完所有消息。
              console.log("messageList: ", messageList);
              //console.log("nextReqMessageID: ",nextReqMessageID);
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
                  console.log("val: ", val);
                  $isActive = i;
                  console.log("isActive: ", i);
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
    update_askVisible(val) {
      this.askDialog.askVisible = val;
    },
  },
  components: {
    Ask,
  },
};
</script>

<style lang="scss" scoped>
.contact {
  position: absolute;
  top: 22.5px;
  left: 37.5px;
  z-index: 6;
  color: rgba(0, 0, 0, 0.5);
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 12px;
  font-weight: 700;
  padding: 3.75px 9.75px;
  border-radius: 20px;
  background: rgba(0, 0, 0, 0.1);
  line-height: 1;
  cursor: pointer;
  text-shadow: 0 1px 0px rgba(255, 255, 255, 0.1);
}

.cards {
  margin: auto;
  background: #fefefe;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1), 3px 5px 20px rgba(0, 0, 0, 0.2);
  width: 288px;
  height: 206.25px;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 11.25px;

  .card {
    display: inline-block;
    margin-right: 7.5px;
  }

  .card-toggle {
    z-index: 4;
    position: relative;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: block;
    text-align: center;
    line-height: 1.8;
    font-size: 24px;
    cursor: pointer;
    border: 2px solid transparent;
    transition: 0.3s ease;

    &.active {
      color: white;
      border-color: white;
    }
  }
  .card-content {
    position: absolute;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    transition: -webkit-clip-path 1s ease;
    padding: 37.5px 0 0;
    overflow: hidden;
    border-radius: 5px;

    .row {
      display: table;
      width: 100%;
      height: 100%;
    }

    .col {
      width: 50%;
      height: 100%;
      display: table-cell;
      transition: 0.3s ease 0.3s;
      transform: translate3d(0, 0, 0);
      vertical-align: top;

      h1 {
        color: #6a78ca;
      }

      h2 {
        font-weight: 300;
        font-size: 3em;
        line-height: 1;
        margin: 0 0 7.5px;
        color: #90baf8;
        strong {
          font-weight: 300;
          font-size: 0.3em;
          display: block;
          color: #e5ecf8;
        }
      }

      img {
        max-width: 90%;
        width: 100%;
      }

      &.left {
        transform: translate3d(0, 0, 0);
        opacity: 0;
        padding-left: 12.5px;
      }
      &.right {
        transform: translate3d(100px, 0, 0);
        opacity: 0;
        padding-left: 11.25px;
      }
    }
  }
  .card.active .col {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
  #overview {
    .card-toggle {
      position: absolute;
      top: 11.25px;
      right: 11.25px;
      opacity: 1;
      color: white;
    }
    .card-content {
      background-color: #ffffff;
      -webkit-clip-path: circle(0% at 91.5% 25px);
    }
    &.active {
      .card-toggle {
        opacity: 0;
      }
      .card-content {
        -webkit-clip-path: circle(270% at 91.5% 25px);
      }
    }

    .right {
      //background: url(https://dl.dropboxusercontent.com/u/26808427/cdn/james.png) no-repeat bottom right;
      background-size: contain;
    }
  }

  #dribbble {
    .card-content {
      color: white;

      p {
        color: rgba(255, 255, 255, 0.8);
      }
    }
  }
  #dribbble {
    .card-content {
      background-color: #6ca3f7;
      -webkit-clip-path: circle(0% at 76px 88%);
      clip-path: circle(0% at 50px 88%);
    }
    &.active .card-content {
      -webkit-clip-path: circle(270% at 76px 88%);
      clip-path: circle(270% at 50px 88%);
    }
  }
}

.buttonGroup {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  align-content: center;
  text-align: center;
}

.button {
  width: 100px;
  height: 30px;
  line-height: 30px;
  background: #a9d4f7;
  font-weight: bold;
  color: white;
  border: 0 none;
  border-radius: 1px;
  cursor: pointer;
  padding: 10px 5px;
  margin: 10px 5px;
  &:hover,
  &:focus {
    box-shadow: 0 0 0 2px white, 0 0 0 3px #6de0fd;
  }
}

.el-input {
  height: 5vh;
  width: 70vw;
}

.el-header {
  line-height: 6vh;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.el-main {
  text-align: center;
  line-height: 20px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.bottom {
  margin-top: 3px;
  line-height: 12px;
}

.clearfix {
  padding-left: 2.5vw;
  padding-right: 2.5vw;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.el-row {
  margin-bottom: 50px;
}

.el-raw:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}
</style>
