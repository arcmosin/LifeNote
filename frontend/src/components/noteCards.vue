<template>
  <div class="card-container">
    <el-card 
      v-for="(card, index) in cards" 
      :key="card.id"
      class="card-item"
      @click="openDialog(card)"
    >
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div class="card-header">
            <span>{{ card.title || getContentPreview(card.content) }}</span>
          </div>
          <el-icon class="delete-icon" @click.stop="handleDelete(card.id)">
            <Delete />
          </el-icon>
        </div>
      </template>
      <!-- 内容区域 -->
      <div class="content-wrapper">
        <p class="card-content">
          {{ card.content }}
        </p>
      </div>

      <template #footer>
        <div class="card-footer">
          <div>    
            <!-- <el-input
              v-if="inputVisible"
              ref="InputRef"
              v-model="inputValue"
              class="w-20"
              size="small"
              @keyup.enter="handleInputConfirm"
              @blur="handleInputConfirm"
            /> -->
            <el-select v-model="selectValue" 
              placeholder="标签" 
              style="width: 240px"
              v-if="selectVisible"
              @keyup.enter="handleTagSelectConfirm"
              @blur="handleTagSelectConfirm"
              >
              <el-option
                v-for="item in tagOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-button v-else class="button-new-tag" size="small" @click.stop="handleSideToggle(card.id)">
              <img src="@/assets/addTag.svg" alt="New Tag" width="16" height="16">
            </el-button>
          </div>
          <div class="updated-at">{{ formattedDate(dayjs_now,card.updated_at) }}</div>
        </div>

      </template>
    </el-card>

    <!-- 弹窗组件 -->
    <el-dialog
      v-model="dialogVisible"
      width="50%"
      @closed="handleClosed"
    >    

      <template #header>
        <div class="dialog-header">
          <div v-if="!isEditing" class="title-container">
            <span>{{ dialogTitle }}</span>
            <el-icon class="edit-icon" @click="startEditing">
              <Edit />
            </el-icon>
          </div>
          <el-input
            v-else
            ref="titleInput"
            v-model="editingTitle"
            size="small"
            @blur="submitEdit"
            @keyup.enter="submitEdit"
          />
        </div>
      </template>

      <div>
        <el-input
          v-model="textarea"
          style="width: 100%"
          :autosize="{ minRows: 18, maxRows: 18 }"
          type="textarea"
          placeholder="Please input"
        />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleSave">保存</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, nextTick,getCurrentInstance, watch } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import { dayjs_now,formattedDate } from '@/components/DateShow/dataShow.js'
import { useStore } from '@/utils/store'
import bus from 'vue3-eventbus'

// 获取全局 $config
// const { $config } = getCurrentInstance().appContext.config.globalProperties;
import { getApiBaseUrl } from '@/utils/config';

const cards = ref([])
const dialogVisible = ref(false)
const selectedCard = ref({
  id: '',
  title: '',
  content: '',
  created_at: '',
  updated_at: ''
})
const textarea = ref('')
const dialogTitle = ref('')
const isEditing = ref(false)
const editingTitle = ref('')
const titleInput = ref(null)

const store = useStore()

const clear = () => {
  selectedCard.value = {
    id: '',
    title: '',
    content: '',
    created_at: '',
    updated_at: ''
  }
  textarea.value = '',
  dialogTitle.value = ''
}

const handleClosed = () => {
  clear()
}

// 获取所有卡片
const fetchCards = async () => {
  try {
    if(store.tagBarValue != null){
      const response = await axios.get(`${getApiBaseUrl()}/tags/${store.tagBarValue}/items/`)
      cards.value = response.data
    }else{
      const response = await axios.get(`${getApiBaseUrl()}/items/`)
      cards.value = response.data
    }

  } catch (error) {
    console.error('获取卡片失败:', error)
  }
}

watch(() => store.tagBarValue, fetchCards,{deep: true})



const openDialog = (card) => {
  selectedCard.value = { ...card }//解开再赋值，避免绑定原对象
  textarea.value = card.content
  dialogTitle.value = card.title
  dialogVisible.value = true
}

const handleSave = async () => {
  if (selectedCard.value.id) {
    try {
      await axios.put(`${getApiBaseUrl()}/items/${selectedCard.value.id}`, {
        title: dialogTitle.value,
        content: textarea.value
      })
      // 更新本地数据
      const index = cards.value.findIndex(c => c.id === selectedCard.value.id)
      if (index !== -1) {
        cards.value[index].content = textarea.value
      }
      dialogVisible.value = false
    } catch (error) {
      console.error('保存失败:', error)
    }
  }else{
    createNewCardPush()
  }
  fetchCards()
}

const getContentPreview = (content) => {
  if (!content) return '';
  const maxLength = 7;
  return content.length > maxLength 
    ? `${content.substring(0, maxLength)}...` 
    : content;
};

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确认要删除所选的1条笔记吗?',
      '删除确认',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    
    // 用户确认删除后执行的操作
    await axios.delete(`${getApiBaseUrl()}/items/${id}`);
    
    // 删除本地数据
    cards.value = cards.value.filter(card => card.id !== id);
    
    // 如果需要重新获取数据
    await fetchCards();
  } catch (error) {
    if (error === 'cancel') {
    } else {
      // 删除请求失败
      console.error('删除失败:', error);
      ElMessage({
        type: 'error',
        message: '删除失败',
      });
    }
  }
};

const createNewCard = () => {
    selectedCard.value = {
      id: '',
      title: '',
      content: '',
      created_at: '',
      updated_at: ''
    }
  dialogVisible.value = true
}

// 添加创建新卡片的功能
const createNewCardPush = async () => {

  try {
    const response = await axios.post(`${getApiBaseUrl()}/items/`, {
      title: dialogTitle.value,
      content: textarea.value,
      // created_at: new Date().toISOString().split('T')[0]
    })
    cards.value.push(response.data)
  } catch (error) {
    console.error('创建卡片失败:', error)
  } finally {
    dialogVisible.value = false
    fetchCards()
  }

}

const startEditing = () => {
  isEditing.value = true
  editingTitle.value = dialogTitle.value
  nextTick(() => {
    titleInput.value?.focus()
  })
}

const submitEdit = () => {
  // if (editingTitle.value.trim()) {
  //   dialogTitle.value = editingTitle.value.trim()
  // }
    // 无论是否为空都提交，但会trim掉两端的空白
  dialogTitle.value = editingTitle.value.trim()
  isEditing.value = false
}


const selectVisible = ref(false)
const selectValue = ref('')

const tagOptions = ref([])

const fetchTagsByItem = async (value) => {
  try {
    const response = await axios.get(`${getApiBaseUrl()}/items/${value}/tags/`)
    store.updateTagList(response.data)
    bus.emit('itemTags', { id: value, tags: response.data });
    editTagCardID.value = value;
    store.updateSideAction(false)
  } catch (error) {
    console.error('获取卡片的标签失败:', error)
  }finally {
  }
}

const editTagCardID = ref(null)

const handleSideToggle = (value) => {
  fetchTagsByItem(value)
};

watch(() => store.isCollapse, (newVal) => {
  if (newVal) {
    editTagCardID.value = null;
    store.updateTagList([])
  }
});

watch(editTagCardID, (newVal) => {
  store.updateWaitTagID(newVal);
});



// 暴露方法给父组件
defineExpose({
  createNewCard
});

// 初始化加载数据
onMounted(() => {
  fetchCards()
})

</script>
<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px; /* 卡片间距 */
}

.card-item {
  flex: 1 1 calc(20% - 20px); /* 每行4个，减去间距 */
  min-width: 200px; /* 最小宽度防止过小时变形 */
  max-width: calc(20% - 20px); /* 最大宽度限制 */
}

/* 响应式调整 - 在小屏幕上显示2个 */
@media (max-width: 768px) {
  .card-item {
    flex: 1 1 calc(50% - 20px);
    max-width: calc(50% - 20px);
  }
}

/* 在更小的屏幕上显示1个 */
@media (max-width: 480px) {
  .card-item {
    flex: 1 1 100%;
    max-width: 100%;
  }
}

.delete-icon {
  cursor: pointer;
  padding: 0px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.delete-icon:hover {
  background-color: #FEE;
  color: #F56C6C;
}

.delete-icon:active {
  background-color: #FDD;
  transform: scale(0.9);
}

.title-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-icon {
  cursor: pointer;
  transition: color 0.2s;
}

/* 新增内容容器，确保固定高度 */
.content-wrapper {
  min-height: calc(1.5em * 7); /* 固定7行高度 */
  position: relative; /* 为绝对定位的伪元素提供定位上下文 */
}

.card-content {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 7;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
  line-height: 1.5; /* 与min-height计算保持一致 */
  margin: 0; /* 移除默认外边距 */
}

/* 可选：添加淡出效果增强视觉提示 */
.content-wrapper::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1.5em; /* 与行高一致 */
  background: linear-gradient(to bottom, 
             rgba(255,255,255,0), 
             rgba(255,255,255,1) 80%);
  pointer-events: none;
  display: var(--show-fade, block); /* 可以通过变量控制是否显示 */
}

.footer-container { 
  display: flex;
}

.updated-at {
  display: flex;
  justify-content: flex-end; 
  font-size: 0.8rem;
}



</style>

<style>
.el-card__footer{
  padding: 8px !important;
}
</style>