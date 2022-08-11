/*
 * @Author: wangyang 
 * @Date: 2021-10-09 16:55:46 
 * @Last Modified by: wangyang
 * @Last Modified time: 2021-10-19 12:40:46
 */
 
<template>
  <el-dialog 
    title="订单详情" 
    :visible.sync="detailsVisible" 
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
      <el-button type="primary" @click="close()">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  props: {
    detailsVisible: {
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
      this.$emit("update_detailsVisible", false);
    },
  },
};
</script>
