<template>
    <div class="container_all">

        <div id="luckysheet" class="luckysheet-content"></div>
        <div id="picture" class="picture">
            <h3>报告处理</h3>
            <el-button type="primary">生成报告</el-button>   
            <el-button type="infor">下载报告</el-button>   
        </div>
    </div>

  </template>
  <script setup >
  import { onMounted } from 'vue';
  
  onMounted(() => {
    init()
  })
  const init = () => {
    var options = {
      container: 'luckysheet', //luckysheet为容器id
      title: "测试Excel", // 表 头名
      lang: "zh", // 中文
      showtoolbar: true, // 是否显示工具栏
      showinfobar: false, // 是否显示顶部信息栏
      showsheetbar: true, // 是否显示底部sheet按钮
    }
    luckysheet.create(options)
  }
  </script>
  <style>
    .container_all{
        margin: 0px;
        padding: 0px;
        display: flex;
        flex-direction: row;
    }
    .picture_content{
        margin: 0px;
        width: 720px;
        display: flex;
    }
    .picture{
        margin: 0px;
        display: flex;
        flex-direction: column;
        margin: 50px;
    }

  .luckysheet-content {
    margin: 0px;
    padding: 0px;
    /* position: absolute; */
    width: 80%;
    height: 80vh;
    left: 0px;
    top: 40px;
    bottom: 0px;
  }
  </style>