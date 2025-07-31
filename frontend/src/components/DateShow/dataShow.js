import dayjs from 'dayjs'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
import weekday from 'dayjs/plugin/weekday'

// 初始化dayjs插件
dayjs.extend(isSameOrBefore)
dayjs.extend(isSameOrAfter)
dayjs.extend(weekday)

// 星期映射表
const weekdayMap = {
  0: '周日',
  1: '周一',
  2: '周二',
  3: '周三',
  4: '周四',
  5: '周五',
  6: '周六'
}

// 假设这是从后端获取的数据
export const dayjs_now = dayjs()

export function formattedDate(now, backendDate) {
  const date = dayjs(backendDate)
  
  // 如果是同一天
  if (date.isSame(now, 'day')) {
    return date.format('HH:mm')
  }
  
  // 如果是同一周
  if (date.isSame(now, 'week')) {
    return weekdayMap[date.day()] // 使用映射表返回中文星期
  }
  
  // 如果是同一年
  if (date.isSame(now, 'year')) {
    return date.format('M月D日') // 显示"7月5日"
  }
  
  // 其他情况
  return date.format('YYYY年M月D日') // 显示"2025年7月5日"
}