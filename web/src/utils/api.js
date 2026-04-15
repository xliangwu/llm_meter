import axios from 'axios'

const API_BASE_URL = '/api'

const api = {
  async getTaskList(params = {}) {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks`, { params })
      return response.data
    } catch (error) {
      console.error('获取任务列表失败:', error)
      throw error
    }
  },

  async getTaskDetail(taskId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}`)
      return response.data
    } catch (error) {
      console.error('获取任务详情失败:', error)
      throw error
    }
  },

  async getTaskLog(taskId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}/log`)
      return response.data
    } catch (error) {
      console.error('获取任务日志失败:', error)
      throw error
    }
  },

  async getTaskSummaryLog(taskId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}/summaryLog`)
      return response.data
    } catch (error) {
      console.error('获取任务总结日志失败:', error)
      throw error
    }
  },

  async getTaskStats(taskId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${taskId}/stats`)
      return response.data
    } catch (error) {
      console.error('获取任务统计失败:', error)
      throw error
    }
  },

  async submitTask(taskData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/tasks`, taskData)
      return response.data
    } catch (error) {
      console.error('提交任务失败:', error)
      throw error
    }
  },

  async deleteTask(taskId) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/tasks/${taskId}`)
      return response.data
    } catch (error) {
      console.error('删除任务失败:', error)
      throw error
    }
  },

  async getDatasetList(params = {}) {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets`, { params })
      return response.data
    } catch (error) {
      console.error('获取数据集列表失败:', error)
      throw error
    }
  },

  async uploadDataset(formData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/datasets/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      console.error('上传数据集失败:', error)
      throw error
    }
  },

  async deleteDataset(datasetId) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/datasets/${datasetId}`)
      return response.data
    } catch (error) {
      console.error('删除数据集失败:', error)
      throw error
    }
  }
}

export default api
