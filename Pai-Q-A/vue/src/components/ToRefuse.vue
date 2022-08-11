/* 
 * @Author: wangyang 
 * @Date: 2021-10-12 10:19:32 
 * @Last Modified by: wangyang
 * @Last Modified time: 2021-10-18 23:06:15
 */

<template>
  <el-dialog
    title="订单详情"
    :visible.sync="refuseVisible"
    width="30%"
    :show-close="false"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
  >
    <el-descriptions :column="1" border>
      <el-descriptions-item label="提问者">{{ orderDetails["questioner"] }}</el-descriptions-item>
      <el-descriptions-item label="回答者">{{ orderDetails["answerer"] }}</el-descriptions-item>
      <el-descriptions-item label="订单状态">
        <el-tag size="small">{{ orderDetails["end_mark"] }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="提问名称">{{ orderDetails["title"] }}</el-descriptions-item>
      <el-descriptions-item label="提问内容">{{ orderDetails["content"] }}</el-descriptions-item>
    </el-descriptions>
    <span slot="footer" class="dialog-footer">
      <el-button @click="close()">取 消</el-button>
      <el-button type="danger" @click="refuse(orderDetails['order_id'])">拒 绝</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  props: {
    refuseVisible: {
      type: Boolean,
      default: () => false,
    },
    orderDetails: {
      type: Object,
      default: () => {},
    },
  },
  methods: {
    close() {
      this.$emit("update_refuseVisible", false);
    },
    refuse(val) {
      this.$confirm("此操作将拒绝回答该提问, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        center: true,
      })
        .then(() => {
          this.$message({
            type: "success",
            message: "拒绝订单成功!",
          });
          this.$emit("update_refuseOrder", val)
          this.$emit("update_refuseButton", val)
        })
        .then(() => {
          this.$emit("update_refuseVisible", false);
        });
    },
  },
};
</script>
