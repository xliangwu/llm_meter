<template>
  <el-container>
    <el-header class="header">
      <h1>LLM Meter - 性能测试平台</h1>
      <el-menu
        mode="horizontal"
        :default-active="activeMenu"
        class="nav-menu"
        router
        :ellipsis="false"
      >
        <el-menu-item index="/">任务管理</el-menu-item>
        <el-menu-item index="/datasets">数据集管理</el-menu-item>
      </el-menu>
    </el-header>
    
    <el-main class="main-container">
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.header h1 {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
}

.nav-menu {
  background: transparent;
  border-bottom: none;
  height: 60px;
}

.nav-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.85);
  border-bottom: none;
  font-size: 15px;
  font-weight: 500;
  height: 60px;
  line-height: 60px;
  padding: 0 24px;
  transition: all 0.3s ease;
}

.nav-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
}

.nav-menu .el-menu-item.is-active {
  background-color: transparent !important;
  color: white !important;
  border-bottom: 3px solid #ffd700 !important;
  font-weight: 600;
}

.main-container {
  padding: 20px;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.task-card {
  cursor: pointer;
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stats-item {
  margin-bottom: 15px;
}

.stats-label {
  font-weight: 500;
  color: #606266;
  margin-bottom: 5px;
}

.stats-value {
  font-size: 18px;
  color: #409EFF;
  font-weight: 600;
}

.log-content {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
  max-height: 600px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.filter-section {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>
