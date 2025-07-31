<template>
  <div style="position: relative;height: 100%;">  
    <div class="side-container">
      <div style="margin-left: auto;margin-right: 10px;" >
        <!-- <el-button size="small" @click="handleClose">关闭</el-button> -->
          <button class="arrow-button" @click="handleClose">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M15 18l-6-6 6-6" />
            </svg>
        </button>
      </div>
      <div class="radius">
        <el-check-tag
          v-for="tag in tags"
          :key="tag.id"
          class="tag-item"
          :checked="isTagSelected(tag)"
          @change="val => toggleTag(tag, val)"
        >
          {{ tag.name }}
        </el-check-tag>
      </div>
    </div>
    <div class="confirm-btn">
      <el-button type="primary" size="small" @click="handleSubmit">确认</el-button>
    </div>

  </div>

</template>


<script setup>
import { ref, onMounted, nextTick,getCurrentInstance,computed, watch } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from '@/utils/store'
import bus from 'vue3-eventbus'

// 获取全局 $config
const { $config } = getCurrentInstance().appContext.config.globalProperties;

const tags=ref([])



const store = useStore()
const handleClose=()=>{
  store.updateSideAction(true)
}

const isTagSelected = (tag) => {
  // return selectedTags.value.some(t => t.id === tag.id)
  return store.tagList.some(t => t.id === tag.id)
}

const toggleTag = (tag, checked) => {
  if (checked) {
    // 只加一次
    if (!isTagSelected(tag)) {
      store.pushTagList(tag)
    }
  }else{
    // 删除
    store.removeTagList(tag)

  }
}



// 获取所有标签
const fetchTags = async () => {
  try {
    const response = await axios.get(`${$config.API_BASE_URL}/tags/`)
    tags.value = response.data
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}


bus.on('itemTags', (data) => { 
    for(let i = 0; i < tags.value.length; i++){
    const isExist = data.tags.some(item => item.id === tags.value[i].id);
    if(isExist){  
      toggleTag(tags.value[i], true)
    }else{
      toggleTag(tags.value[i], false)
    }
  }
});

const handleSubmit = async () => {
  const sendIDs = store.tagList.map(item => item.id)
  try {
    await axios.put(`${$config.API_BASE_URL}/items/${store.waitTagID}/tags`, 
      sendIDs,
    )
    ElMessage({
      type: 'success',
      message: '修改成功',
    });
    store.updateSideAction(true)
  } catch (error) {
    console.error('保存失败:', error)
  }
}


onMounted(() => {
  fetchTags()
})

</script>

<style scoped>
.side-container {
  display: flex;
  flex-direction: column;  /* 改为 column 使元素垂直排列 */
  gap: 8px;  /* 可选：添加间距使标签之间有空隙 */
  margin-top: 10px;
  align-items: center;
}

.tag-item{
  margin: 4px;
}

.arrow-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #333; /* 可以修改颜色 */
  transition: color 0.2s ease;
}

.arrow-button:hover {
  color: #007bff; /* 悬停颜色 */
}

.arrow-button:focus {
  outline: none; /* 移除焦点轮廓 */
}

.radius {
  height: 400px;
  width: 95%;
  border: 1px solid var(--el-border-color);
  border-radius: 2px;
  background-color:rgb(252, 252, 252);
  margin: 0 10px;
}

.confirm-btn {
  position: absolute;
  right: 10px;
  bottom: 20px;
}
</style>