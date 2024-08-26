<template>
  <div class="home">
    <div style="display: flex; padding: 16px;">
      <a-upload :disabled="hide !== null" :showUploadList="false" name="file" action="/api/ocrimage" @change="handleChange" :multiple="true">
        <a-button>
          <upload-outlined></upload-outlined>
          点击上传识别图片（后台服务）
        </a-button>
       
      </a-upload>
      <a-button type="primary" style="margin-left: 16px;" @click="showExample">
          快速展示（无后端）
        </a-button>
        <!-- <a-button type="primary" style="margin-left: 16px;" @click="handleTest">
          测试
        </a-button> -->
    </div>
    <!--  <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <div style="display: flex; padding: 0 16px;">
      <div>
      <div style="padding: 10px 0px; text-align: left; display: flex;">
        <a-button @click="handleShowAllBox"> 展示所有的边框 </a-button>
        <div v-if="activateIndex" style="flex: 1; display: flex; flex-wrap: nowrap; justify-content: flex-end; align-items: center;">
          <div>
            <span style="color: rgba(0, 0, 0, 0.65);font-weight: bold;">
              类型:
            </span> 
            <span style="font-weight: bold;">
              {{ ocrRes[activateIndex].type }}
            </span>
          </div>
          <div v-if="ocrRes[activateIndex].type != 'table'" style="margin-left: 16px;">
            <span style="color: rgba(0, 0, 0, 0.65);font-weight: bold;">
              置信度:
            </span> 
            <span :style="getMinConfidence !== null && getMinConfidence > 0.9 ?   { color: '#52c41a'} : { color: '#faad14'}">
              {{ getMinConfidence }}
            </span>
          </div>
        </div>
      </div>
      <div @wheel.prevent="() => { }" style=" border: 1px solid #ccc; padding: 10px;">
        <canvas id="fabric" :width="Math.ceil((clientWidth - 50) / 2)" :height="clientHeight - 200" style=""></canvas>
      </div></div>
      <div style="flex: 1; width: 0; min-width: 600px;text-align: left; margin-left: 16px;">
        <div style="padding: 10px 0px; text-align: left;">
          <a-button @click="handlePreviewHTML"> 预览 </a-button>
          <!-- <a-button style="margin-left: 16px;" @click="handlePreviewCode"> 代码预览 </a-button> -->
        </div>
        <div
        style=" border: 1px solid #ccc; padding: 10px; max-height: calc(100vh - 180px); height: 100%; overflow-y: auto;">
        <div style="position: relative; margin: 30px; background: #fff;padding: 16px;">
          <div v-for="(layout, layoutIndex) in layoutList" :key="layoutIndex">
            <div v-if="layout.type === 'single'">
              <div v-for="(editor, editorIndex) in layout.children" class="editor-ctn" @click="handleClick(editor.index)"
                :key="editorIndex">
                <ckeditor type="inline" v-model="layoutList[layoutIndex].children[editorIndex].html"></ckeditor>
              </div>
            </div>
            <div v-if="layout.type === 'double'">
              <div v-if="layout.children.length > 0" style="display: inline-block; width: 48%; margin-left: 1%; vertical-align: top;">
                <div v-for="(editor, editorIndex) in layout.children[0].children" class="editor-ctn"
                  @click="handleClick(editor.index)" :key="editorIndex">
                  <ckeditor type="inline" v-model="layoutList[layoutIndex].children[0].children[editorIndex].html">
                  </ckeditor>
                </div>
              </div>
              <div v-if="layout.children.length > 1" style="display: inline-block; width: 48%; margin-left: 1%; vertical-align: top;">
                <div v-for="(editor, editorIndex) in layout.children[1].children" class="editor-ctn"
                  @click="handleClick(editor.index)" :key="editorIndex">
                  <ckeditor type="inline" v-model="layoutList[layoutIndex].children[1].children[editorIndex].html">
                  </ckeditor>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      
    </div>
    <a-modal :width="800" v-model:open="htmlModalShow" :footer="null">
      <div class="html-ctn">
        <div v-html="htmlText">

        </div>
      </div>
      
    </a-modal>
    <a-modal :width="800" v-model:open="codeModalShow" :footer="null">
      <div class="code-ctn">
        <!-- <highlightjs autodetect :code="htmlText" /> -->
      </div>
    </a-modal>
  </div>
</template>

<style lang="less" scoped>
.html-ctn {
  :deep(img)  {
    max-width: 100%;
  }
  div {
    vertical-align: top;
  }
  :deep(table) {
        border-spacing: 0px !important;
        width: 100%;
        border-right: 1px solid #eee;
    }

  :deep(table>thead>tr>th) {
        border-left: 1px solid #eee;
        border-bottom: 1px solid #eee;
        border-top: 1px solid #eee;
        word-break: break-all;
        padding: 5px;
        background: #F0F5FF;
        font-weight: 400;
        color: rgba(0, 0, 0, 0.85);
    }

  :deep(table>tbody>tr>td) {
        border-left: 1px solid #eee;
        border-bottom: 1px solid #eee;
        border-top: 1px solid #eee;
        word-break: break-all;
        padding: 5px;
        color: rgba(0, 0, 0, 0.65);
    }
}
.home {
  :deep(table) {
        border-spacing: 0px !important;
        width: 100%;
        border-right: 1px solid #eee;
    }

  :deep(table>thead>tr>th) {
        border-left: 1px solid #eee;
        border-bottom: 1px solid #eee;
        border-top: 1px solid #eee;
        word-break: break-all;
        padding: 5px;
        background: #F0F5FF;
        font-weight: 400;
        color: rgba(0, 0, 0, 0.85);
    }

  :deep(table>tbody>tr>td) {
        border-left: 1px solid #eee;
        border-bottom: 1px solid #eee;
        border-top: 1px solid #eee;
        word-break: break-all;
        padding: 5px;
        color: rgba(0, 0, 0, 0.65);
    }
}
</style>

<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'
import { message } from 'ant-design-vue';
import { fabric } from 'fabric'
import { computed, nextTick, onMounted, ref } from 'vue';
const clientWidth = document.documentElement.clientWidth;
const clientHeight = document.documentElement.clientHeight;
import exampleData from '../example/example';
import axios from 'axios';
export default {
  name: 'tablercaliexample',
  components: {
    // HelloWorld
  },
  props: {

  },
  setup() {
    const canvas = ref();   // fabric画布示例

    // 初始化fabric画布实例
    const initCanvas = () => {
      // 初始化
      canvas.value = new fabric.Canvas('fabric', {
        allowTouchScrolling: true,
        hoverCursor: 'pointer',
        selection: false,
      });
      // 画布随滚轮转动在鼠标位置进行缩/放
      // 监听鼠标滚轮缩放事件
      canvas.value.on('mouse:wheel', opt => {
        const delta = opt.e.deltaY // 滚轮，向上滚一下是 -100，向下滚一下是 100
        let zoom = canvas.value.getZoom() // 获取画布当前缩放值
        zoom *= 0.999 ** delta
        if (zoom > 20) zoom = 20 // 限制最大缩放级别
        if (zoom < 0.01) zoom = 0.01 // 限制最小缩放级别

        // 以鼠标所在位置为原点缩放
        canvas.value.zoomToPoint(
          { // 关键点
            x: opt.e.offsetX,
            y: opt.e.offsetY
          },
          zoom // 传入修改后的缩放级别
        )
      })

      // 设置鼠标点击进行画布拖动事件
      // 监听鼠标按下事件
      canvas.value.on('mouse:down', function (opt) {
        var evt = opt.e;
        /* 
        // 按下alt键再开启拖动
        if (evt.altKey === true) { */
        // 记录位移参数
        canvas.value.isDragging = true
        canvas.value.selection = false
        canvas.value.lastPosX = evt.clientX
        canvas.value.lastPosY = evt.clientY
        /*  } */
      })

      // 监听鼠标拖动事件
      canvas.value.on('mouse:move', function (opt) {
        if (canvas.value.isDragging) {
          // 计算偏移值
          var e = opt.e;
          var vpt = canvas.value.viewportTransform;
          vpt[4] += e.clientX - canvas.value.lastPosX
          vpt[5] += e.clientY - canvas.value.lastPosY
          canvas.value.requestRenderAll()
          canvas.value.lastPosX = e.clientX
          canvas.value.lastPosY = e.clientY
        }
      })

      // 监听鼠标释放事件
      canvas.value.on('mouse:up', function () {
        // on mouse up we want to recalculate new interaction
        // for all objects, so we call setViewportTransform
        // 根据偏移值进行更改
        canvas.value.setViewportTransform(canvas.value.viewportTransform)
        canvas.value.isDragging = false
        canvas.value.selection = true
      })
    }

    onMounted(() => {
      // 初始化画布
      initCanvas();
    })

    const href = ref(''); // 上传图片的浏览器路径

    const ocrRes = ref([]); // OCR结果数组

    const layoutList = ref([]); // 根据OCR结果，计算出的布局列表

    // 根据传入参数，获取裁剪指定区域的图片， 用于OCR结果为figure（图片）时， 根据bbox对图片进行裁剪
    const getClipPicUrl = (area, drawCanvasCtx) => {
      const canvas = document.createElement('canvas')
      const context = canvas.getContext('2d')
      const data = drawCanvasCtx.getImageData(area.x, area.y, area.w, area.h)
      canvas.width = area.w
      canvas.height = area.h
      context.putImageData(data, 0, 0)
      return canvas.toDataURL('image/png', 1)
    }

    const canvasContext = ref(null);  // 裁剪图片的canvas

    // 获取htmlList的结果
    const getHTMLList = (imgShape) => {
      // 创建HTML元素
      const html = document.createElement('div');  // 用于记录直接生成的HTML元素 
      //let flag = 1;
      let currentDiv = null;    // 当前布局的div元素
      let currentDoubleLeft = null; // 记录当前双列布局当前布局的left值
      let currentElement = null;  // 当前布局结构的对象；
      let doubleElement = null; // 用于记录当前的双层布局结构对象；
      const list = [];  // 输出结构对象数组
      // 循环遍历OCR结果
      for (let i = 0; i < ocrRes.value.length; ++i) {
        // 获取区域元素
        const region = ocrRes.value[i];
        // 如果区域元素为图片识别结果，则跳过。
        if (region['type'].toLowerCase() === 'figure_caption') {
          continue
        }
        // 元素布局判断
        // 如果布局是单列
        if (region['layout'] == 'single') {
          // 创建新的HTML元素
          const newDiv = document.createElement('div')
          newDiv.classList = `single-layout ck-editor-ctn`  // 单列类
          newDiv.id = `editor${i}`   
          html.appendChild(newDiv); // 添加布局元素
          currentDiv = newDiv;  // 设置当前布局元素为
          currentDoubleLeft = null; // 重置 用于标记双列布局当前布局的left值为null
          // 创建单列布局元素
          currentElement = {
            type: 'single',
            children: []
          }
          // 添加布局元素
          list.push(currentElement)
        }
        // 如果布局时双列
        else if (region['layout'] == 'double') {
          // 如果双列布局当前布局的left值为空，则当前是新的双列元素布局
          if (currentDoubleLeft === null) {
            // 创建双列布局HTML元素
            const doubleDivCtn = document.createElement('div')
            doubleDivCtn.classList = 'double-div-ctn' // 类
            html.appendChild(doubleDivCtn)  // 添加元素
            currentDoubleLeft = region['bbox'][0];  // 设置当前的布局的左值为当前区域元素的左值
            const currentDoubleDiv = document.createElement('div')  // 当前双列布局中的活跃布局元素
            currentDoubleDiv.classList = 'double-div ck-editor-ctn'
            currentDoubleDiv.id = `editor${i}`
            currentDoubleDiv.style.setProperty('display', 'inline-block');
            currentDoubleDiv.style.setProperty('width', '48%')
            currentDoubleDiv.style.setProperty('margin-left', '2%')
            doubleDivCtn.appendChild(currentDoubleDiv); // 添加当前单列布局进入双列布局中
            currentDiv = currentDoubleDiv;
            doubleElement = {
              type: 'double',
              children: []
            }
            currentElement = {
              children: []
            }
            doubleElement.children.push(currentElement);
            list.push(doubleElement)
          }
          else {
            // 这里判断double 布局下是否已经换行
            if (Math.abs(currentDoubleLeft < Math.floor(imgShape.w / 2 - 20) &&  region['bbox'][0] > Math.floor(imgShape.w / 2 - 20))) {
              const currentDoubleDiv = document.createElement('div')
              currentDoubleDiv.classList = 'double-div ck-editor-ctn'
              currentDoubleDiv.id = `editor${i}`
              currentDoubleDiv.style.setProperty('display', 'inline-block');
              currentDoubleDiv.style.setProperty('width', '48%')
              currentDoubleDiv.style.setProperty('margin-left', '2%')
              currentDiv.parentElement.appendChild(currentDoubleDiv);
              currentDiv = currentDoubleDiv;
              currentDoubleLeft = region['bbox'][0]
              currentElement = {
                children: []
              }
              doubleElement.children.push(currentElement)
              // list.push(currentElement)
            }
            else {
              1;
            }
          }
          // flag = 2;
        }
        /******************* */
        // 以下处理是 根据当前元素的类型， 进行处理后直接添加至当前布局元素下
        
        // 如果是图片则直接从原图进行剪裁
        if (region['type'].toLowerCase() == 'figure') {
          const img = document.createElement('img', {
            class: 'img-ctn',
            src: ''
          })
          img.src = getClipPicUrl({
            x: region['bbox'][0],
            y: region['bbox'][1],
            w: region['bbox'][2] - region['bbox'][0],
            h: region['bbox'][3] - region['bbox'][1],
          }, canvasContext.value)
          currentDiv.appendChild(img);
          currentElement.children.push({
            type: region['type'].toLowerCase(),
            index: i,
            html: `
                    <div id="editor${i}">
                        ${img.outerHTML}
                    </div>
                  `
          })
        }
        else if (region['type'].toLowerCase() == 'title') {
          const title = document.createElement('h1', {
            class: 'title'
          })
          for (let j = 0; j < region['res'].length; ++j) {
            title.innerText = `${title.innerText}${region['res'][j].text}`;
            /* title.appendChild(p) */
          }
          currentDiv.appendChild(title);
          currentElement.children.push({
            type: region['type'].toLowerCase(),
            index: i,
            html: `
                    <div id="editor${i}">
                       ${title.outerHTML}
                    </div>
             `
          })
        }
        else if (region['type'].toLowerCase() == 'table') {
          const tableCtn = document.createElement('div', {
            class: 'table-ctn'
          })
          tableCtn.innerHTML = region['res']['html'];
          currentDiv.appendChild(tableCtn)
          currentElement.children.push({
            type: region['type'].toLowerCase(),
            index: i,
            html: `
                    <div id="editor${i}">
                          ${tableCtn.outerHTML}
                    </div>
                  `
          })
        }
        // text类型
        else {
          const textCtn = document.createElement('div', {
            class: 'text-ctn'
          })
          const tab = document.createElement('span');
          tab.innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;`
          textCtn.appendChild(tab);
          let textLength = 0
          for (let j = 0; j < region['res'].length; ++j) {
            const line = region['res'][j];
            const paragrah = document.createElement('span')
            paragrah.innerText = line['text'];
            textLength = textLength + line['text'].length;
            textCtn.appendChild(paragrah);
          }
          if(textLength === 0) {
            continue
          }
          currentDiv.appendChild(textCtn)
          currentElement.children.push({
            type: region['type'].toLowerCase(),
            index: i,
            html: `
                    <div id="editor${i}">
                        ${textCtn.outerHTML}
                     </div>
                 `
          })
        }
      }
      
      console.log(html.outerHTML) // 输出生成的HTML
      layoutList.value = list;  // 生成的HTML结构数组
      console.log(list)
      return list;
    }

    const initCanvas1 = async (url) => {
      return new Promise((resolve, reject) => {
        const image = new Image();
        image.src = url;
        const canvas = document.createElement('canvas')
        const context = canvas.getContext('2d')
        canvasContext.value = context;
        //canvasInstance.value = canvas;
        image.onload = () => {
          canvas.width = image.width;
          canvas.height = image.height;
          context.drawImage(image, 0, 0, image.width, image.height);
          //document.documentElement.appendChild(canvas)
          resolve();
        }
        image.onerror = () => {
          reject();
        }
      })
    }

    const hide = ref(null);


    // 上传状态发生改变
    const handleChange = async (info) => {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }

      if(info.file.status === 'uploading') {
        !hide.value  && (hide.value = message.loading('正在上传中..', 0));
      }
      if (info.file.status === 'done') {
        href.value = window.URL.createObjectURL(info.file.originFileObj);
        if (info.file.response.res && info.file.response.res instanceof Array) {
          ocrRes.value = info.file.response.res;
          /* getHTML(); */
          //await initCanvas(href.value);
          await initCanvas1(href.value)
          insertImage();
          getHTMLList(info.file.response.imgShape);
          hide.value && hide.value() && (hide.value = null)
          message.success('获取OCR结果成功')
        }
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    }

    // 上传图片完成后， 向canvas内插入图片
    const insertImage = () => {
      fabric.Image.fromURL(href.value, img => {
        canvas.value.setBackgroundImage(img)
        const width = canvas.value.getWidth();
        //const height = canvas.value.getHeight();
        canvas.value.setZoom(width / img.width)
        canvas.value.renderAll()
        initBbox()
      })
    }

    const bboxList = ref([]);

    const initBbox = () => {
      for (let i = 0; i < ocrRes.value.length; ++i) {
        //const zoom = canvas.value.getZoom();
        const item = ocrRes.value[i];
        const rect = new fabric.Rect({
          left: 0,
          top: 22,
          width: (item.bbox[2] - item.bbox[0]) + 3,
          height: (item.bbox[3] - item.bbox[1]) + 3,
          backgroundColor: 'transparent',
          fill: 'transparent',
          strokeWidth: 1.5,
          stroke: 'red',
        });
        const label = new fabric.Text(`${item.type}_${i}`, {
          fontSize: 14,
          // padding: 4,
          /*   stroke: 'red',
            strokeWidth: 2, */
          top: 0,
          left: 0,
          backgroundColor: 'red',
          fill: 'white', // 填充色：橙色
        })

        const group = new fabric.Group([rect, label], {
          left: item.bbox[0],
          top: item.bbox[1] - 24,
        })
        group.selectable = false;
        bboxList.value.push(group)
        // canvas.value.add(group)
      }
    }
    const activateIndex = ref(null);

    // 清除所有的bbox
    const removeAllBox = () => {
      bboxList.value.forEach(bbox => {
        // 当前bbox是否存在于画布内
        const isbboxContains = canvas.value.contains(bbox);
        if(isbboxContains) {
          canvas.value.remove(bbox)
        }
      })
    }

    const handleClick = (index) => {
      removeAllBox()
      activateIndex.value = index;
      canvas.value.add(bboxList.value[index])
      console.log(canvas.value.viewportTransform)
      console.log(canvas.value.calcViewportBoundaries())
      const zoom = canvas.value.getZoom()
      const vpt = canvas.value.viewportTransform;
      vpt[4] = (0 - (bboxList.value[index].left - 10)) * zoom
      vpt[5] = (0 - (bboxList.value[index].top - 30)) * zoom
      //canvas.value.setZoom(Math.min(canvas.value.getWidth() / bboxList.value[index].width  , canvas.value.getHeight() / bboxList.value[index].height ))
      canvas.value.setViewportTransform(canvas.value.viewportTransform)
      //const zoom = canvas.value.getZoom();
      
      canvas.value.renderAll()
    }

    // 展示所有的边框
    const handleShowAllBox = () => {
     /*  if(activateIndex.value !== null) {
        canvas.value.remove(bboxList.value[activateIndex.value])
      } */
      removeAllBox();
      activateIndex.value = null;
      for(let i = 0; i < bboxList.value.length; ++i) {
        canvas.value.add(bboxList.value[i])
      }
    }

    const htmlModalShow = ref(false);

    const htmlText = ref('');

    // HTML布局数组转换为HTML
    const handleLayoutListToHTML = () => {
      // 创建最外层HTML元素
      const htmlElement = document.createElement('div');
      // 遍历结构数组
      for(let i = 0; i < layoutList.value.length; ++i) {
        const layout = layoutList.value[i];
        // 如果是单列结构
        if(layout.type === 'single') {
          const singleLayout = document.createElement('div');
          for(let j = 0; j < layout.children.length; ++j) {
            singleLayout.innerHTML = `${singleLayout.innerHTML}${layout.children[j].html}`
          }
          htmlElement.appendChild(singleLayout)
        }
        // 如果是双列结构
        else if(layout.type === 'double') {
          // 创建双列布局元素
          const doubleLayout = document.createElement('div');
          // 创建第一列，并遍历第一列元素
          const leftDiv = document.createElement('div');
          leftDiv.style.setProperty('width', '49%');
          leftDiv.style.setProperty('display', 'inline-block');
          leftDiv.style.setProperty('vertical-align', 'top');
          for(let j  = 0; j < layout.children[0].children.length; ++j) {
            leftDiv.innerHTML =  `${leftDiv.innerHTML}${layout.children[0].children[j].html}`
          }
          doubleLayout.appendChild(leftDiv);
          // 遍历第二列
          const rightDiv = document.createElement('div');
          rightDiv.style.setProperty('width', '49%');
          rightDiv.style.setProperty('display', 'inline-block');
          rightDiv.style.setProperty('vertical-align', 'top');
          rightDiv.style.setProperty('margin-left', '2%');
          for(let j  = 0; j < layout.children[1].children.length; ++j) {
            rightDiv.innerHTML = `${rightDiv.innerHTML}${layout.children[1].children[j].html}`
          }
          doubleLayout.appendChild(rightDiv);
          // 添加双列布局元素进入外层元素
          htmlElement.appendChild(doubleLayout);
        }
      }
      htmlText.value = htmlElement.outerHTML;
      return htmlElement.outerHTML;
    }

    const handlePreviewHTML = () => {
      handleLayoutListToHTML()
      htmlModalShow.value = true
      
    }

    const getMinConfidence = computed(() => {
      if(activateIndex.value === null) {
        return null;
      }
      const activeRes = ocrRes.value[activateIndex.value]
      if( activeRes.type != 'table') {
        return activeRes.res.reduce((pre,current) => {
          return pre < current.confidence ? pre : current.confidence;
        }, 1)
      }
      else {
        return null;
      }
    })

    const codeModalShow = ref(false);

    const handlePreviewCode = () => {
      handleLayoutListToHTML()
      codeModalShow.value = true;
    }

    // 无后端样例展示
    const showExample = async () => {
      href.value = '/1.png';
      await initCanvas1(href.value);
      insertImage();
      nextTick(() => {
        ocrRes.value = exampleData.res;
        getHTMLList(exampleData.imgShape);
      })
    }

    // 测试
    const handleTest = async () => {
     /*  axios.post('http://192.168.2.28:38088/ocr=video', JSON.stringify({
        "ocrflag": "0",
        "savefilepath": "./res.txt",
      })) */
      let data1 = {
        "filepath": "",
        "rotate": "0",
        "cutpage": "0",
        "camidx": "0"
      } 
      axios.post("http://192.168.2.28:38088/video=grabimage", JSON.stringify(data1)).then((res1)=>{
        //add_image(res1.data.photoBase64)
        //mylog("识别中。。。")
        let data2 = {
          "ocrflag": "1",
          "picfilepath": res1.data.filepath,
          "savefilepath": "D://ocr.pdf"
        }
        axios.post("http://192.168.2.28:38088/video=ocr", JSON.stringify(data2)).then((res2)=>{
          if(res2.data.code == '0'){
            console.log('识别成功')
            //mylog("识别成功")
          }else{
            console.log('识别失败')
           // mylog("识别失败")
          }
        })
      })
    }

    return {
      clientHeight,
      clientWidth,
      handleChange,
      activateIndex,
      handleClick,
      layoutList,
      handleShowAllBox,
      handlePreviewHTML,
      hide,
      htmlModalShow,
      htmlText,
      ocrRes,
      getMinConfidence,
      handlePreviewCode,
      codeModalShow,
      showExample,
      handleTest
    }
  }
} 
</script>
