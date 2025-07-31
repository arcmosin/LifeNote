<template>
<div>
  <div class="submit-container">
    <el-button type="warning"  round @click="GreatCard">&nbsp;&nbsp;+&nbsp;&nbsp;</el-button>
  </div>
  <tagScrollbar/>
  <noteCards ref="noteCardsRef"/>
</div>
</template>

<script setup>
import { ref } from 'vue'
import noteCards from './noteCards.vue'
import tagScrollbar from './tagScrollbar.vue';

const textarea2 = ref('')
const noteCardsRef = ref(null);

const GreatCard = () => {
  if (noteCardsRef.value) {
    noteCardsRef.value.createNewCard();
  }
};

</script>

<style scoped>

.submit-container{
  position: fixed;
  right: 20px;  /* 距离右边界的距离 */
  bottom: 20px; /* 距离下边界的距离 */
  z-index: 999; /* 确保按钮在其他内容之上 */
}

</style>