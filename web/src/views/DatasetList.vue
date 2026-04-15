<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据集管理</span>
          <el-button type="primary" @click="handleUpload">
            上传数据集
          </el-button>
        </div>
      </template>

      <el-table :data="datasetList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="数据集ID" width="350" />
        <el-table-column prop="dataset_name" label="数据集名称" />
        <el-table-column prop="dataset_desc" label="描述" />
        <el-table-column prop="dataset_path" label="文件路径" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" fixed="right" width="100">
          <template #default="scope">
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

    <el-dialog v-model="uploadDialogVisible" title="上传数据集" width="500px">
      <el-form :model="uploadForm" :rules="uploadRules" ref="uploadFormRef" label-width="100px">
        <el-form-item label="数据集名称" prop="dataset_name">
          <el-input v-model="uploadForm.dataset_name" placeholder="请输入数据集名称" />
        </el-form-item>
        <el-form-item label="数据集描述" prop="dataset_desc">
          <el-input v-model="uploadForm.dataset_desc" type="textarea" :rows="3" placeholder="请输入数据集描述" />
        </el-form-item>
        <el-form-item label="数据集文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            :file-list="fileList"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持上传数据集文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUpload" :loading="uploading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../utils/api'

const loading = ref(false)
const uploading = ref(false)
const datasetList = ref([])
const uploadDialogVisible = ref(false)
const uploadFormRef = ref(null)
const uploadRef = ref(null)
const fileList = ref([])

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0
})

const uploadForm = ref({
  dataset_name: '',
  dataset_desc: '',
  file: null
})

const uploadRules = {
  dataset_name: [
    { required: true, message: '请输入数据集名称', trigger: 'blur' }
  ],
  file: [
    { required: true, message: '请选择文件', trigger: 'change' }
  ]
}

const loadDatasets = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.current,
      page_size: pagination.value.pageSize
    }
    const response = await api.getDatasetList(params)
    datasetList.value = response.data || []
    pagination.value.total = response.total || 0
  } catch (error) {
    ElMessage.error('加载数据集列表失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleUpload = () => {
  uploadForm.value = {
    dataset_name: '',
    dataset_desc: '',
    file: null
  }
  fileList.value = []
  uploadDialogVisible.value = true
}

const handleFileChange = (file) => {
  uploadForm.value.file = file.raw
  fileList.value = [file]
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const submitUpload = async () => {
  if (!uploadFormRef.value) return
  
  await uploadFormRef.value.validate(async (valid) => {
    if (valid) {
      if (!uploadForm.value.file) {
        ElMessage.error('请选择文件')
        return
      }

      uploading.value = true
      try {
        const formData = new FormData()
        formData.append('file', uploadForm.value.file)
        formData.append('dataset_name', uploadForm.value.dataset_name)
        if (uploadForm.value.dataset_desc) {
          formData.append('dataset_desc', uploadForm.value.dataset_desc)
        }

        await api.uploadDataset(formData)
        ElMessage.success('上传成功')
        uploadDialogVisible.value = false
        loadDatasets()
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '上传失败')
        console.error(error)
      } finally {
        uploading.value = false
      }
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据集吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await api.deleteDataset(row.id)
    ElMessage.success('删除成功')
    loadDatasets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const handleSizeChange = (val) => {
  pagination.value.pageSize = val
  loadDatasets()
}

const handleCurrentChange = (val) => {
  pagination.value.current = val
  loadDatasets()
}

onMounted(() => {
  loadDatasets()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>
