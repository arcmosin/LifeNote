<template>
  <div class="tags-container">
    <div class="tag-scrollbar">
        <el-check-tag
          class="tag-item"
          round
          :checked="selectedTag===null"
          @change="toggleTag(null)"
        >全部</el-check-tag>
      <template v-for="(tag, index) in tags" :key="tag.id">
        <el-input
          v-if="editingTagId === tag.id"
          :ref="(el) => setEditInputRef(el, index)"
          v-model="editValue"
          class="w-20"
          size="small"
          style="width: 100px;"
          @keyup.enter="handleEditConfirm(tag.id)"
          @blur="handleEditConfirm(tag.id)"
        />
        <el-check-tag
          v-else
          class="tag-item"
          round
          :key="tag.id"
          :checked="tag.id===selectedTag"
          @change="toggleTag(tag.id)"
          type="primary"
        >
        <img 
          v-if="isEditing"
          src="@/assets/editTag.svg"  width="10" height="10"
          @click="handleDoubleClick(tag)"
          style="margin-right: 5px;"
        />
          {{ tag.name }}
        <img 
          v-if="isEditing"
          src="@/assets/fork.svg"  width="10" height="10"
          @click="handleClose(tag.id)"
          style="margin-left: 5px;"
        />
        </el-check-tag> 
      </template>
      <el-input
        v-if="inputVisible && isEditing"
        ref="InputRef"
        v-model="inputValue"
        class="w-20"
        size="small"
        style="width: 100px;"
        @keyup.enter="handleInputConfirm"
        @blur="handleInputConfirm"
      />
      <el-button v-if="!inputVisible && isEditing" style="width: 100px;" size="small" @click="showInput">
        + New Tag
      </el-button>
    </div>
    
    <div class="new-tag-button">

      <el-button  size="small" class="button-new-tag" :class="{ 'editing-button': isEditing }" @click="EditToggle">
        <img src="@/assets/editTags.svg" alt="Edit Tag" width="16" height="16"></img>
      </el-button>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, nextTick,getCurrentInstance,computed, watch } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from '@/utils/store'

// 获取全局 $config
const { $config } = getCurrentInstance().appContext.config.globalProperties;

const tags=ref([])
const inputVisible = ref(false)
const InputRef = ref();
const editInputRef = ref()
const inputValue = ref('')

const isEditing=ref(false)

const store = useStore()

const selectedTag = ref(null)


const editInputRefs = ref([]); // 存储所有编辑输入框的 ref
const editingTagId = ref(null)
const editValue = ref('')

// 设置编辑输入框的 ref
const setEditInputRef = (el, index) => {
  editInputRefs.value[index] = el;
};

// 获取所有标签
const fetchTags = async () => {
  try {
    const response = await axios.get(`${$config.API_BASE_URL}/tags/`)
    console.log('response',response)
    tags.value = response.data
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}

const showInput = () => {
  inputVisible.value = true;
  nextTick(() => {
    InputRef.value.input.focus()
  })
};

const handleClose = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确认要删除所选的标签吗?',
      '删除确认',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    await axios.delete(`${$config.API_BASE_URL}/tags/${id}`);
    tags.value = tags.value.filter(tag => tag.id !== id);
    await fetchTags();
  } catch (error){
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
}

const handleInputConfirm = async () => {
  if (inputValue.value) {
    try {
      await axios.post(`${$config.API_BASE_URL}/tags/`,{

        name: inputValue.value
      })
    } catch (error) {
      console.error('创建标签失败:', error)
      if (error.response && error.response.status === 400) {
        ElMessage({
          type: 'error',
          message: '标签已存在',
        });
      } else {
        ElMessage({
          type: 'error',
          message: '创建标签失败，请稍后再试',
        });
      }
    } finally {
      inputVisible.value = false
      inputValue.value = ''
      fetchTags()
    }
  }else{
      inputVisible.value = false
      inputValue.value = ''
  }
}


const handleDoubleClick=(tag)=> {
  editingTagId.value = tag.id;
  editValue.value = tag.name;
  nextTick(() => {
    const index = tags.value.findIndex(t => t.id === tag.id);
    if (editInputRefs.value[index]) {
      editInputRefs.value[index].focus();
    }
  });
}

const handleEditConfirm = async (id) => {
  try {
    await axios.put(`${$config.API_BASE_URL}/tags/${id}`,{
      name: editValue.value
    })
    const index = tags.value.findIndex(tag => tag.id === id)
      if (index !== -1) {
        tags.value[index].name = editValue.value
      }
  } catch (error) {
      ElMessage({
        type: 'error',
        message: '标签名更改失败',
      }); 
  }finally{
    editingTagId.value = null
    editValue.value = ''
    fetchTags()
  }
}

const EditToggle=()=>{ 
  isEditing.value = !isEditing.value
}



const toggleTag = (value) => {
  if(isEditing.value)return
  selectedTag.value=value
  store.updateTagBarValue(value)
}

// const handleShowAllTags=() =>{
//   if(isEditing.value)return
//   if(store.tagBarValue!=null){
//     store.tagBarValue=null
//     }
// }

onMounted(() => {
  fetchTags()
})

</script>

<style scoped>
.tags-container {
  display: flex;
  gap: 8px;  /* 可选：添加间距使标签之间有空隙 */
  margin-bottom: 20px;
  width: 100%;
  overflow: hidden;
}

.tag-scrollbar {
  display: flex;
  overflow-x: auto;
  flex: 1;
  gap: 8px; /* 添加标签间距 */
  padding: 4px 0; /* 添加一些内边距 */
}

.new-tag-button {
  flex-shrink: 0;
  margin-left: 8px;
  margin-right: 20px;
}
.button-new-tag{
  background-color: #409EFF;
  color: white;
  border: 1px;
  /* padding: 8px 16px; */
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.1s ease;
  box-shadow: 
      0 2px 4px rgba(0, 0, 0, 0.12), /* 外阴影（浮起感） */
      inset 0 1px 1px rgba(255, 255, 255, 0.2); /* 内阴影（轻微立体感） */
}

.button-new-tag.editing-button {
  /* 编辑状态下的样式 */
  transform: translateY(1px);
  box-shadow: 
    0 0 2px rgba(0, 0, 0, 0.1), /* 外阴影变小 */
    inset 0 2px 4px rgba(0, 0, 0, 0.2); /* 内阴影加深（凹陷感） */
  background-color: #3a8ee6;

}

/* 可选：自定义滚动条样式 */
.tag-scrollbar::-webkit-scrollbar {
  height: 6px;
}

.tag-scrollbar::-webkit-scrollbar-thumb {
  background-color: #c1c1c1;
  border-radius: 3px;
}

.tag-scrollbar::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

.tag-item{
  width: 100px;
}



</style>