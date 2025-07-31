<template>
  <div class="app">
    <div class="common-layout">
      <el-container>
        <el-aside 
          :style="{ 
            width: isCollapse ? '0' : '400px',
            transition: 'width 0.3s',
            overflow: 'hidden'
          }"
        >
          <sideApp />
        </el-aside>
        <el-main>
          <!-- 添加遮罩层 -->
          <div 
            v-if="!isCollapse"
            class="main-overlay"
            @click="handleMainClick"
          ></div>
          <mainApp />
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script setup>
import mainApp from '@/components/mainApp.vue'
import sideApp from '@/components/sideApp.vue'
import { useStore } from '@/utils/store'
import { ref, computed } from 'vue';

const store = useStore()
const isCollapse = computed(() => store.isCollapse);

const handleMainClick = () => {
  store.isCollapse = true;
};
</script>

<style scoped>
.common-layout {   
  position:absolute;
  top:0;
  right:0;
  bottom:0;
  left:0;
}

.el-container {   
  height: 100%;    
}

.el-aside {
  background-color: #f0f0f0;
}

.el-main {
  background-color: #ffffff;
  position: relative; /* 为遮罩层定位做准备 */
}

.main-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1; /* 确保遮罩层在内容之上 */
  background-color: transparent; /* 透明背景 */
  cursor: pointer;
}
</style>