<template>
  <div class="task-submit-container">
    <el-card class="task-submit-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" link @click="handleBack">
            <el-icon>
              <ArrowLeft />
            </el-icon>
            返回
          </el-button>
          <span style="margin-left: 10px;">提交新任务</span>
        </div>
      </template>

      <el-form ref="taskFormRef" :model="taskForm" :rules="rules" label-width="auto">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="任务名称" />
        </el-form-item>

        <el-form-item label="模型名称" prop="model">
          <el-input v-model="taskForm.model" placeholder="请输入模型名称" />
        </el-form-item>

        <el-form-item label="数据集" prop="dataset">
          <el-select v-model="taskForm.dataset" placeholder="请选择数据集" style="width: 100%;">
            <el-option label="random" value="random" />
            <el-option label="line_by_line" value="line_by_line" />
            <el-option label="openqa" value="openqa" />
            <el-option label="longalpaca" value="longalpaca" />
            <el-option label="flickr8k" value="flickr8k" />
            <el-option label="kontext_bench" value="kontext_bench" />
            <el-option label="random_vl" value="random_vl" />
          </el-select>
        </el-form-item>

        <el-form-item label="推理地址" prop="url">
          <el-input v-model="taskForm.url" placeholder="请输入服务URL，例如: http://127.0.0.1:8000/v1/chat/completions" />
        </el-form-item>

        <el-form-item label="API Key">
          <el-input v-model="taskForm.api_key" placeholder="可选，如果服务需要认证" show-password />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="并发数" prop="parallel">
              <el-input v-model="taskForm.parallel" type="text" style="width: 100%;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="请求数量" prop="number">
              <el-input v-model="taskForm.number" type="text" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="最大Token数" prop="max_tokens">
          <el-input v-model="taskForm.max_tokens" :min="1" :max="8192" style="width: 100%;" />
        </el-form-item>

        <div v-if="taskForm.dataset === 'random'">
          <el-divider content-position="left">Prompt 配置</el-divider>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Prompt min">
                <el-input-number v-model="taskForm.min_prompt_length" :min="10" :max="131072" style="width: 100%;" />
                <div class="form-tip">小于该值时，将丢弃prompt</div>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="max">
                <el-input-number v-model="taskForm.max_prompt_length" :min="10" :max="131072" style="width: 100%;" />
                <div class="form-tip">大于该值时，将丢弃prompt</div>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="前缀长度">
            <el-input-number v-model="taskForm.prefix_length" :min="0" :max="131072" style="width: 100%;" />
            <div class="form-tip">仅对于random数据集有效</div>
          </el-form-item>

          <el-form-item label="指定Prompt">
            <el-input v-model="taskForm.prompt" type="textarea" :rows="3" placeholder="字符串或本地文件路径（@/path/to/file）" />
            <div class="form-tip">使用优先级高于dataset，本地文件使用@前缀，例如：@./prompt.txt</div>
          </el-form-item>

          <el-form-item label="查询模板">
            <el-input v-model="taskForm.query_template" type="textarea" :rows="3"
              placeholder="JSON字符串或本地文件路径（@/path/to/file）" />
            <div class="form-tip">本地文件使用@前缀，例如：@./query_template.json</div>
          </el-form-item>
        </div>
        <div v-if="taskForm.dataset === 'line_by_line'">
          <el-form-item label="数据集文件">
            <el-select v-model="taskForm.dataset_path" placeholder="请选择数据集文件" style="width: 100%;" clearable filterable>
              <el-option v-for="dataset in datasetList" :key="dataset.id" :label="dataset.dataset_name"
                :value="dataset.dataset_path">
                <span style="float: left">{{ dataset.dataset_name }}</span>
                <span style="float: right; color: var(--el-text-color-secondary); font-size: 13px">
                  {{ dataset.dataset_path }}
                </span>
              </el-option>
            </el-select>
            <div class="form-tip">从已上传的数据集中选择，或前往<a href="/datasets" style="color: #409EFF;">数据集管理</a>上传新数据集</div>
          </el-form-item>
        </div>

        <div v-if="taskForm.dataset === 'random_vl'">
          <el-divider content-position="left">图像配置</el-divider>
          <el-form-item label="图像宽度">
            <el-input-number v-model="taskForm.image_width" :min="1" :max="4096" style="width: 100%;" />
          </el-form-item>

          <el-form-item label="图像高度">
            <el-input-number v-model="taskForm.image_height" :min="1" :max="4096" style="width: 100%;" />
          </el-form-item>

          <el-form-item label="图像格式">
            <el-select v-model="taskForm.image_format" style="width: 100%;">
              <el-option label="RGB" value="RGB" />
              <el-option label="RGBA" value="RGBA" />
            </el-select>
          </el-form-item>

          <el-form-item label="图像数量">
            <el-input-number v-model="taskForm.image_num" :min="1" :max="10" style="width: 100%;" />
          </el-form-item>
        </div>

        <el-divider content-position="left">其他配置</el-divider>
        <el-form-item label="温度" prop="temperature">
          <el-slider v-model="taskForm.temperature" :min="0" :max="2" :step="0.1" show-input />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">提交任务</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import api from '../utils/api'

const router = useRouter()
const taskFormRef = ref(null)
const submitting = ref(false)
const datasetList = ref([])

const taskForm = ref({
  model: '',
  dataset: 'random',
  url: null,
  parallel: "1 5 10",
  number: "10 10 10",
  max_tokens: 512,
  max_prompt_length: 4096,
  min_prompt_length: 10,
  prefix_length: 0,
  prompt: null,
  query_template: null,
  dataset_path: null,
  image_width: 224,
  image_height: 224,
  image_format: 'RGB',
  image_num: 1,
  stream: true,
  temperature: 0.0,
  api_key: '',
  name: null
})

const rules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' }
  ],
  model: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  dataset: [
    { required: true, message: '请选择数据集', trigger: 'change' }
  ],
  url: [
    { required: true, message: '请输入服务URL', trigger: 'blur' },
    { type: 'url', message: '请输入正确的URL地址', trigger: 'blur' }
  ],
  parallel: [
    { required: true, message: '请输入并发数', trigger: 'blur' }
  ],
  number: [
    { required: true, message: '请输入请求数量', trigger: 'blur' }
  ]
}

const handleBack = () => {
  router.push('/')
}

const handleSubmit = () => {
  taskFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const response = await api.submitTask(taskForm.value)
        ElMessage.success('任务提交成功')
        router.push(`/task/${response.id}`)
      } catch (error) {
        ElMessage.error('任务提交失败: ' + (error.response?.data?.message || error.message))
        console.error(error)
      } finally {
        submitting.value = false
      }
    }
  })
}

const handleReset = () => {
  taskFormRef.value.resetFields()
  taskForm.value = {
    model: '',
    dataset: 'random',
    url: '',
    parallel: 1,
    number: 10,
    max_tokens: 1024,
    prompt_length: 1024,
    max_prompt_length: 131072,
    min_prompt_length: 0,
    prefix_length: 0,
    prompt: '',
    query_template: '',
    image_width: 224,
    image_height: 224,
    image_format: 'RGB',
    image_num: 1,
    stream: true,
    temperature: 0.0,
    api_key: '',
    name: '',
    extraArgs: ''
  }
}

const loadDatasets = async () => {
  try {
    const response = await api.getDatasetList({ page: 1, page_size: 1000 })
    datasetList.value = response.data || []
  } catch (error) {
    console.error('加载数据集列表失败:', error)
  }
}

onMounted(() => {
  loadDatasets()
})
</script>

<style scoped>
.task-submit-container {
  width: 100%;
  min-width: 960px;
  min-height: calc(100vh - 120px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
}

.task-submit-card {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  line-height: 1.4;
}
</style>
