<template>
  <div>
    <el-card class="filter-section">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="任务名称">
          <el-input v-model="filterForm.name" placeholder="请输入任务名称" clearable />
        </el-form-item>
        <el-form-item label="任务状态">
          <el-select v-model="filterForm.status" placeholder="请选择状态" clearable style="width: 180px">
            <el-option label="待执行" value="pending" />
            <el-option label="运行中" value="running" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-button type="primary" @click="handleCreate">
            提交新任务
          </el-button>
        </div>
      </template>

      <el-table :data="taskList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="任务ID" width="300" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="model" label="模型" />
        <el-table-column prop="dataset" label="数据集" />
        <el-table-column prop="parallel" label="并发数" />
        <el-table-column prop="number" label="请求数" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column prop="completed_at" label="完成时间" width="180" />
        <el-table-column label="操作" fixed="right" width="140">
          <template #default="scope">
            <el-button type="primary" link size="small" @click="handleView(scope.row)">
              查看详情
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
          :current-page="pagination.current" :page-sizes="[10, 20, 50, 100]" :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper" :total="pagination.total" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../utils/api'

const router = useRouter()

const loading = ref(false)
const filterForm = ref({
  name: '',
  status: ''
})
const taskList = ref([])
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const loadTasks = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.current,
      page_size: pagination.value.pageSize,
      ...filterForm.value
    }
    const response = await api.getTaskList(params)
    taskList.value = response.data || []
    pagination.value.total = response.total || 0
  } catch (error) {
    ElMessage.error('加载任务列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.value.current = 1
  loadTasks()
}

const handleReset = () => {
  filterForm.value = {
    name: '',
    status: ''
  }
  pagination.value.current = 1
  loadTasks()
}

const handleCreate = () => {
  router.push('/submit')
}

const handleDataset = () => {
  router.push('/datasets')
}

const handleView = (row) => {
  router.push(`/task/${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteTask(row.id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const handleSizeChange = (val) => {
  pagination.value.pageSize = val
  loadTasks()
}

const handleCurrentChange = (val) => {
  pagination.value.current = val
  loadTasks()
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
  loadTasks()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
