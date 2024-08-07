<template>
  <div>
      <el-container>
        <el-header>
          <el-card>说明</el-card>
          
        </el-header>

        <p style="margin: 5%;">
          这只是一个demo程序，用于探索当前的OCR识别技术达到的业务过程和离线识别的参考效果。
        </p>
        <div class="stepsarea">
          <el-steps :space="300" active="4">
            <el-step title="步骤一：设置识别模板"> </el-step>
            <el-step title="步骤二：保存并下载识别模板"> </el-step>
            <el-step title="步骤三：基于识别模板，基于已经上传在后台的图片，发起识别请求"> </el-step>
            <el-step title="步骤四：识别结果展示"> </el-step>
            <el-step title="步骤五：审核并手工调整结果"> </el-step>
          </el-steps>
        
        </div>

        

      </el-container>
  </div>
</template>

<script setup>

</script>

<style scoped>

.stepsarea{
  margin: 5%;
  width: 80%;
  align-items: center;
}

</style>