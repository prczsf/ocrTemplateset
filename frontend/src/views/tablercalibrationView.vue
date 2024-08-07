<template>
    <div class="container_all">
        <div id="picture" class="picture">图片
            <div class="picture_content">
                <img src="/andan.png" alt="" width="100%">
                </img>
            </div>
        </div>
        <!-- <div id="luckysheet" class="luckysheet-content"></div> -->
    </div>

  </template>
  <script setup >
  // import { onMounted } from 'vue';
  
  // onMounted(() => {
  //   init()
  // })
  // const init = () => {
  //   var options = {
  //     container: 'luckysheet', //luckysheet为容器id
  //     title: "测试Excel", // 表 头名
  //     lang: "zh", // 中文
  //     showtoolbar: true, // 是否显示工具栏
  //     showinfobar: false, // 是否显示顶部信息栏
  //     showsheetbar: true, // 是否显示底部sheet按钮
  //   }
  //   luckysheet.create(options)
  // }
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

  .luckysheet-content {
    margin: 0px;
    padding: 0px;
    /* position: absolute; */
    width: 100%;
    height: 80vh;
    left: 0px;
    top: 40px;
    bottom: 0px;
  }
  </style>