<template>
    <div>
      <el-card>
        <h2>规则编排界面</h2>
        <div class="section">
          <h3>Patterns</h3>
          <el-row :gutter="20" >
            <el-col :span="24" v-for="(pattern, index) in config.Patterns" :key="index" >
              <el-card id="patternParams">
                <el-input v-model="pattern.PropName" placeholder="PropName" />
                <el-input v-model="pattern.HeaderName" placeholder="HeaderName" />
                <el-select v-model="pattern.PropType" placeholder="PropType">
                  <el-option label="String" value="string"></el-option>
                  <el-option label="DateTime" value="DateTime"></el-option>
                  <el-option label="Int" value="int"></el-option>
                  <el-option label="Double" value="double"></el-option>
                  <el-option label="Bool" value="bool"></el-option>
                </el-select>
                <el-input v-model="pattern.CellType" placeholder="CellType" />
                <el-checkbox v-model="pattern.Ignore">Ignore</el-checkbox>
                <el-input-number v-model="pattern.Order" placeholder="Order" />
                <el-input v-model="pattern.CleaningRule" placeholder="清洗规则" />
                <el-input v-model="pattern.CorrectionRule" placeholder="矫正规则" />
                <el-input v-model="pattern.Validation.Target" placeholder="Validation Target" />
                <el-input v-model="pattern.Validation.Description" placeholder="Validation Description" />
                <el-input v-model="pattern.Validation.Convention" placeholder="Validation Convention" />
                <el-input v-model="pattern.Validation.Expression" placeholder="Validation Expression" />
                <el-button type="danger" @click="removePattern(index)">删除</el-button>
              </el-card>
            </el-col>
          </el-row>
          <el-button type="primary" @click="addPattern">添加参数</el-button>
        </div>
        <div class="section">
          <h3>字段间关联关系</h3>
          <el-row :gutter="20">
            <el-col :span="24" v-for="(relation, index) in config.Relations" :key="index">
              <el-card id="paramsRelation">
                <el-input v-model="relation.SourceField" placeholder="Source Field" />
                <el-input v-model="relation.TargetField" placeholder="Target Field" />
                <el-input v-model="relation.Condition" placeholder="Condition" />
                <el-button type="danger" @click="removeRelation(index)">删除</el-button>
              </el-card>
            </el-col>
          </el-row>
          <el-button type="primary" @click="addRelation">添加关联关系</el-button>
        </div>
        <el-button type="success" @click="generateJSON">生成校验配置</el-button>
        <el-card>
          <pre>{{ generatedJSON }}</pre>
        </el-card>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { ElMessage } from 'element-plus';
  
  const config = ref({
    Patterns: [],
    Relations: []
  });
  
  const generatedJSON = ref('');
  const draggableContainer = ref(null);
  
  const addPattern = () => {
    config.value.Patterns.push({
      PropName: '',
      HeaderName: '',
      PropType: 'string',
      CellType: '常规',
      Ignore: false,
      Order: config.value.Patterns.length,
      CleaningRule: '',
      CorrectionRule: '',
      Validation: {
        Target: '单元格公式',
        Description: '需要满足正则表达式',
        Convention: '正则表达式校验器',
        Expression: '^SUM\\(I\\d+,J\\d+\\)$'
      }
    });
  };

  
  const removePattern = (index) => {
    config.value.Patterns.splice(index, 1);
    ElMessage.success('Pattern removed successfully');
  };
  
  const addRelation = () => {
    config.value.Relations.push({
      SourceField: '',
      TargetField: '',
      Condition: ''
    });
  };
  
  const removeRelation = (index) => {
    config.value.Relations.splice(index, 1);
    ElMessage.success('Relation removed successfully');
  };
  
  const generateJSON = () => {
    generatedJSON.value = JSON.stringify(config.value, null, 2);
    ElMessage.success('JSON generated successfully');
  };
  
  onMounted(() => {
  });
  </script>
  
  <style scoped>
  #patternParams, #paramsRelation
  {
    display: flex;
  }
  #patternParams .el-input,.el-select {
    width: 160px;
  }

  #paramsRelation .el-input,.el-select {
    width: 300px;
  }
  .section {
    margin-bottom: 20px;
  }
  </style>
  