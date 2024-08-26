<template>
    <div>
      <!-- 顶部横条 -->
      <el-row class="top-bar">
        <el-col :span="24">
          <span>D202401688</span>
          <span>新建</span>
          <el-button-group>
            <el-button type="warning">转换格式</el-button>
            <el-button>保存</el-button>
            <el-button type="warning">导出</el-button>
            <el-button>导入</el-button>
            <el-button type="warning">完成并提交</el-button>
            <el-button>打印原始记录</el-button>
            <el-button type="warning">导出到仪器</el-button>
            <el-button>仪器导入</el-button>
            <el-button type="warning">打印样品序列</el-button>
            <el-button>查看限值</el-button>
          </el-button-group>
        </el-col>
      </el-row>
  
      <!-- 中间部分 -->
      <el-row class="middle-section" :gutter="20">
        <el-col :span="8">
          <el-form-item label="工作单号" >
            <el-input id="workOrder" v-model="formData.workOrder" />
          </el-form-item>
          <el-form-item label="测试项目" id="testProject">
            <el-input v-model="formData.testProject" />
          </el-form-item>
          <el-form-item label="测试方法" id="testMethod">
            <el-input v-model="formData.testMethod" />
          </el-form-item>
          <el-form-item label="测试人">
            <el-input v-model="formData.tester" />
          </el-form-item>
          <el-form-item label="校核人">
            <el-input v-model="formData.checker" />
          </el-form-item>
          <el-form-item label="审核人">
            <el-input v-model="formData.reviewer" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="测试日期">
            <el-date-picker v-model="formData.testDate" type="daterange" />
          </el-form-item>
          <el-form-item label="校核日期">
            <el-date-picker v-model="formData.checkDate" type="daterange" />
          </el-form-item>
          <el-form-item label="审核日期">
            <el-date-picker v-model="formData.reviewDate" type="daterange" />
          </el-form-item>
          <el-form-item label="前处理日期">
            <el-date-picker v-model="formData.preprocessDate" type="daterange" />
          </el-form-item>
          <el-form-item label="地点">
            <el-input v-model="formData.location" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="温度(℃)">
            <el-input v-model="formData.temperature"  id="temperature" />
          </el-form-item>
          <el-form-item label="湿度(%RH)" >
            <el-input v-model="formData.humidity" id="humidity" />
          </el-form-item>
          <el-form-item label="仪器名称/仪器编号">
            <el-input v-model="formData.instrument" />
          </el-form-item>
        </el-col>
      </el-row>
  
      <!-- 多tab页面 -->
      <el-tabs v-model="activeTab">
        <el-tab-pane label="完整数据录入" name="completeData">
          <!-- 完整数据录入内容 -->
          <el-row class="complete-data-entry">
            <el-col :span="24">
              <el-form-item label="请选择质控类型">
                <el-select v-model="formData.qcType" placeholder="请选择">
                  <el-option label="质控类型A" value="qcA" />
                  <el-option label="质控类型B" value="qcB" />
                  <el-option label="质控类型C" value="qcC" />
                </el-select>
                <el-button-group>
                  <el-button type="warning">添加</el-button>
                  <el-button>批量添加质控样</el-button>
                  <el-button type="warning">添加试样</el-button>
                  <el-button>标准溶液</el-button>
                  <el-button type="warning">标准曲线</el-button>
                  <el-button>调高检出限</el-button>
                  <el-button type="warning">复测报出</el-button>
                  <el-button>复测</el-button>
                  <el-button type="warning">平行报平均</el-button>
                  <el-button>分组求平均</el-button>
                </el-button-group>
              </el-form-item>
            </el-col>
          </el-row>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="sampleId" label="样品编号" />
            <el-table-column prop="samplingPoint" label="采样点位" />
            <el-table-column prop="sampleType" label="样品类型" />
            <el-table-column prop="qc" label="质控" />
            <el-table-column prop="location" label="位置" />
            <el-table-column prop="samplingDate" label="采样日期" />
            <el-table-column prop="samplingTime" label="采样时间" />
            <el-table-column prop="dilutionFactor" label="稀释倍数">
              <template #default="scope">
                <el-input v-model="scope.row.dilutionFactor" />
              </template>
            </el-table-column>
            <el-table-column prop="dbfmStandardConcentration" label="二溴氟甲烷标准浓度 (Hg/L)">
              <template #default="scope">
                <el-input v-model="scope.row.dbfmStandardConcentration" />
              </template>
            </el-table-column>
            <el-table-column prop="bfbStandardConcentration" label="4-溴氟苯标准浓度 (Hg/L)">
              <template #default="scope">
                <el-input v-model="scope.row.bfbStandardConcentration" />
              </template>
            </el-table-column>
            <el-table-column prop="tolueneD8StandardConcentration" label="甲苯-d8标准浓度 (μg/L)">
              <template #default="scope">
                <el-input v-model="scope.row.tolueneD8StandardConcentration" />
              </template>
            </el-table-column>
            <el-table-column prop="dbfmTestConcentration" label="二溴氟甲烷测试浓度 (g/L)">
              <template #default="scope">
                <el-input v-model="scope.row.dbfmTestConcentration" />
              </template>
            </el-table-column>
            <el-table-column prop="bfbTestConcentration" label="4-溴氟苯测试浓度 (Hg/L)">
              <template #default="scope">
                <el-input v-model="scope.row.bfbTestConcentration" />
              </template>
            </el-table-column>
            <el-table-column prop="tolueneD8TestConcentration" label="甲苯-d8测试浓度 (μg/L)">
              <template #default="scope">
                <el-input v-model="scope.row.tolueneD8TestConcentration" />
              </template>
            </el-table-column>
          </el-table>
          <el-row>
        <el-button type="primary">保存提交</el-button>
    </el-row>
        </el-tab-pane>
        <el-tab-pane label="相关文档" name="relatedDocs">
            <el-label>相关文档</el-label>
        </el-tab-pane>
        <el-tab-pane label="修约后结果" name="roundedResults">
            <el-label>修约后结果</el-label>
        </el-tab-pane>
        <el-tab-pane label="调整检出限" name="adjustDetectionLimits">
            <el-label>调整检出限</el-label>
        </el-tab-pane>
        <el-tab-pane label="消息/留言" name="messages">
            <el-label>消息/留言</el-label>
        </el-tab-pane>
      </el-tabs>

    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { ElMessageBox } from 'element-plus';
  
  const formData = ref({
    workOrder: '2024080048-O-1',
    testProject: '挥发性有机物(苯、甲苯、乙苯、间,对-二甲苯、苯乙烯、邻-二甲苯、异...',
    testMethod: 'HJ 639-2012《水质 挥发性有机物的测定 吹扫捕集/气相色谱·质谱法》',
    tester: '周良',
    checker: '左世峰',
    reviewer: '方爱国',
    testDate: [],
    checkDate: [],
    reviewDate: [],
    preprocessDate: [],
    location: '上海',
    temperature: '22.5',
    humidity: '67.4',
    instrument: '7466554',
    qcType: '',
  });
  
  const tableData = ref([
    { sampleId: '2024080048_001', samplingPoint: 'DWO1', sampleType: '测试样', qc: '质控1', location: '', samplingDate: '2024-08-09', samplingTime: '09:09-09:16', dilutionFactor: '', dbfmStandardConcentration: '', bfbStandardConcentration: '', tolueneD8StandardConcentration: '', dbfmTestConcentration: '', bfbTestConcentration: '', tolueneD8TestConcentration: '' },
    { sampleId: '2024080048_002', samplingPoint: 'DWO1', sampleType: 'SREP', qc: '质控2', location: '', samplingDate: '2024-08-09', samplingTime: '17:09-17:15', dilutionFactor: '', dbfmStandardConcentration: '', bfbStandardConcentration: '', tolueneD8StandardConcentration: '', dbfmTestConcentration: '', bfbTestConcentration: '', tolueneD8TestConcentration: '' },
    { sampleId: '2024080048_003', samplingPoint: 'DWO1', sampleType: 'SHTEBLK', qc: '质控3', location: '', samplingDate: '2024-08-10', samplingTime: '09:09-09:16', dilutionFactor: '', dbfmStandardConcentration: '', bfbStandardConcentration: '', tolueneD8StandardConcentration: '', dbfmTestConcentration: '', bfbTestConcentration: '', tolueneD8TestConcentration: '' },

    // 其他默认数据
  ]);
  
  const activeTab = ref('completeData');
  </script>
  
  <style scoped>
  .top-bar {
    background-color: #f5f5f5;
    padding: 10px;
  }
  
  .middle-section {
    margin-top: 20px;
  }
  
  .complete-data-entry {
    margin-top: 20px;
  }
  </style>
  