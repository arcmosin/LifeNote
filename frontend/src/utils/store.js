// stores/counter.js
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => ({
    isCollapse: true,//'expand',
    waitTagID: null, // 用于记录当前编辑的标签ID
    tagList: [], // 用于存储标签列表
    tagBarValue: null,
  }),
  actions: {
    updateSideAction(value) {
      this.isCollapse=value
    },
    toggleSideAction() {
      this.isCollapse = !this.isCollapse;
    },
    updateWaitTagID(value) {
      this.waitTagID = value
    },
    clearWaitTagID() {
      this.waitTagID = null
    },
    updateTagList(newTagList) {
      this.tagList = newTagList
    },
    pushTagList(value) {
      this.tagList.push(value)
    },
    removeTagList(value) {
      this.tagList = this.tagList.filter(item => item.id !== value.id);
    },

    updateTagBarValue(value) {
      this.tagBarValue = value
    }
  },
})
