<template>
  <div class="task-detail-container">
    <el-card class="task-detail-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-button type="primary" link @click="handleBack">
              <el-icon>
                <ArrowLeft />
              </el-icon>
              返回
            </el-button>
            <span style="margin-left: 10px;">任务详情</span>
            <el-tag v-if="taskInfo.status" :type="getStatusType(taskInfo.status)" style="margin-left: 10px;">
              {{ getStatusText(taskInfo.status) }}
            </el-tag>
          </div>
        </div>
      </template>

      <div v-loading="loading">
        <el-descriptions title="基本信息" :column="3" border>
          <el-descriptions-item label="任务ID">{{ taskInfo.id }}</el-descriptions-item>
          <el-descriptions-item label="模型">{{ taskInfo.resource }}</el-descriptions-item>
          <el-descriptions-item label="模型ID">{{ taskInfo.model }}</el-descriptions-item>
          <el-descriptions-item label="数据集">{{ taskInfo.dataset }}</el-descriptions-item>
          <el-descriptions-item label="并发数">{{ taskInfo.parallel }}</el-descriptions-item>
          <el-descriptions-item label="请求数">{{ taskInfo.number }}</el-descriptions-item>
          <el-descriptions-item label="服务URL">{{ taskInfo.url }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ taskInfo.created_at }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ taskInfo.completed_at || '-' }}</el-descriptions-item>
          <el-descriptions-item label="最大Token">{{ taskInfo.max_tokens }}</el-descriptions-item>
          <el-descriptions-item label="其他参数">{{ taskInfo.extra_args || '-' }}</el-descriptions-item>
        </el-descriptions>

        <el-tabs v-model="activeTab" style="margin-top: 20px;">
          <el-tab-pane label="性能报告" name="summaryLog">
            <div v-if="summaryLogContent" class="log-content">{{ summaryLogContent }}</div>
            <el-empty v-else description="暂无统计数据" />
          </el-tab-pane>

          <el-tab-pane label="任务日志" name="log">
            <div v-if="logContent" class="log-content">{{ logContent }}</div>
            <el-empty v-else description="暂无日志" />
          </el-tab-pane>

          <el-tab-pane label="数据统计" name="stats">
            <iframe v-if="statsHtml" ref="statsIframe" class="stats-iframe" frameborder="0" scrolling="auto"></iframe>
            <el-empty v-else description="暂无统计数据" />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const activeTab = ref('log')
const taskInfo = ref({})
const logContent = ref('')
const summaryLogContent = ref('')
const statsHtml = ref('')
const statsIframe = ref(null)

const updateIframeContent = () => {
  if (statsIframe.value && statsHtml.value) {
    const iframe = statsIframe.value
    const doc = iframe.contentDocument || iframe.contentWindow.document
    doc.open()
    doc.write(statsHtml.value)
    doc.close()

    iframe.onload = () => {
      try {
        const body = iframe.contentDocument.body
        const html = iframe.contentDocument.documentElement
        const height = Math.max(
          body.scrollHeight,
          body.offsetHeight,
          html.clientHeight,
          html.scrollHeight,
          html.offsetHeight
        )
        iframe.style.height = height + 'px'
      } catch (e) {
        iframe.style.height = '600px'
      }
    }
  }
}

watch(statsHtml, () => {
  nextTick(() => {
    updateIframeContent()
  })
})

const loadTaskDetail = async () => {
  loading.value = true
  const taskId = route.params.id

  try {
    const [detailResponse, logResponse, statsResponse, summaryLogResponse] = await Promise.all([
      api.getTaskDetail(taskId),
      api.getTaskLog(taskId).catch(() => ({ data: '' })),
      api.getTaskStats(taskId).catch(() => ({ data: '' })),
      api.getTaskSummaryLog(taskId).catch(() => ({ data: '' }))
    ])

    taskInfo.value = detailResponse || {}
    logContent.value = logResponse.data || logResponse || ''
    statsHtml.value = statsResponse.data || statsResponse || ''
    summaryLogContent.value = summaryLogResponse.data || summaryLogResponse || ''

    nextTick(() => {
      updateIframeContent()
    })
  } catch (error) {
    ElMessage.error('加载任务详情失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleBack = () => {
  router.push('/')
}

const getStatusType = (status) => {
  const statusMap = {
    'pending': 'info',
    'running': 'warning',
    'completed': 'success',
    'failed': 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待执行',
    'running': '运行中',
    'completed': '已完成',
    'failed': '失败'
  }
  return statusMap[status] || status
}

onMounted(() => {
  loadTaskDetail()
})
</script>

<style scoped>
.task-detail-container {
  width: 100%;
  min-height: calc(100vh - 120px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
}

.task-detail-card {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.stats-iframe {
  width: 100%;
  min-height: 600px;
  border: none;
  background: white;
}
</style>
