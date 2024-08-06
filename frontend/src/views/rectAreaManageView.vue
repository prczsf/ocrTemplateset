<template>
  <div>
    <div style="width: 100%; height: 30px;">
      <select v-model="imagePath">
        <option value="moban1.png">moban1.png</option>
        <option value="andan.png">andan.png</option>       
        <option value="fenguanghuifafen1.png">fenguanghuifafen1.png</option>
        <option value="fenguanghuifafen2.png">fenguanghuifafen2.png</option>
        <option value="fenguanghuifafen3.png">fenguanghuifafen3.png</option>
        <option value="fenguanghuifafen4.png">fenguanghuifafen4.png</option>   
        <option value="fenguangliuhuawu.png">fenguangliuhuawu.png</option>           
        <option value="fenuangqinghua.png">fenuangqinghua.png</option>             
        <option value="huaxuexuyang828.png">huaxuexuyang828.png</option>    
        <option value="huaxuexuyang3991.png">huaxuexuyang3991.png</option>
        <option value="huaxuexuyang3992.png">huaxuexuyang3992.png</option>
        <option value="wurishenghua.png">wurishenghua.png</option>
        <option value="xuanfuwu.png">xuanfuwu.png</option>            
        <option value="moban2.png">moban2.png</option>
        <option value="moban3.png">moban3.png</option>
        <option value="moban4.png">moban4.png</option>
        <option value="moban5.png">moban5.png</option>
      </select>
      <button @click="setBackgroundImage">选择模板图片开始设置</button>
    </div>
    <div class="rect-area-manage-view">
      <div id="canvas-container">
        <canvas id="canvas" width="1080" height="1528"></canvas>
      </div>
      <div>
        <div class="operationButton">
          <button @click="addRect">添加识别区域</button>
          <button @click="saveRects">保存到后台</button>
          <button @click="exportConfig">导出配置</button>
        </div>

        <table>
          <thead>
            <tr>
              <th>序号</th>
              <th>表单变量名</th>
              <th>坐标区域</th>
              <th>类型</th>
              <th>语言</th>
              <th>校正规则</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rect in rects" :key="rect.seq" :class="{ highlighted: rect.seq === selectedRectSeq }">
              <td>{{ rect.seq }}</td>
              <td><input v-model="rect.rectVarName" /></td>
              <td>{{ rect.rectArea }}</td>
              <td>
                <select v-model="rect.type">
                  <option value="header">表头</option>
                  <option value="body">主体</option>
                  <option value="footer">表尾</option>
                </select>
              </td>
              <td>
                <select v-model="rect.language">
                  <option value="zh">中文</option>
                  <option value="en">英文</option>
                  <!-- 其他语言选项 -->
                </select>
              </td>
              <td>
                <select v-model="rect.correctRule">
                  <option value="rule1">规则1</option>
                  <option value="rule2">规则2</option>
                  <option value="rule3">规则3</option>
                  <option value="rule4">规则4</option>
                </select>
              </td>
              <td><button @click="deleteRect(rect.seq)">删除</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { fabric } from 'fabric';

const rects = ref([]);
const imagePath = ref('moban1.png');
const selectedRectSeq = ref(null);
let canvas;

const addRect = () => {
  const seq = rects.value.length + 1;
  const rect = new fabric.Rect({
    left: 50,
    top: 50,
    width: 100,
    height: 50,
    fill: 'rgba(255, 0, 0, 0.5)',
    hasControls: true,
    hasBorders: true,
    selectable: true
  });
  rect.seq = seq; // Add sequence number to the rectangle object
  canvas.add(rect);
  rects.value.push({
    seq,
    rectVarName: '',
    rectArea: `(${rect.left}, ${rect.top}, ${rect.width}, ${rect.height})`,
    type: '',
    language: '',
    correctRule: ''
  });

  rect.on('selected', () => {
    selectedRectSeq.value = seq;
  });

  rect.on('deselected', () => {
    selectedRectSeq.value = null;
  });

  const updateRectArea = () => {
    const index = rects.value.findIndex(r => r.seq === seq);
    const width = rect.width * rect.scaleX;
    const height = rect.height * rect.scaleY;
    rects.value[index].rectArea = `(${rect.left}, ${rect.top}, ${width}, ${height})`;
  };

  rect.on('modified', updateRectArea);
  rect.on('scaling', updateRectArea);
  rect.on('scaled', updateRectArea);
};

const deleteRect = (seq) => {
  const index = rects.value.findIndex(r => r.seq === seq);
  if (index !== -1) {
    const rect = canvas.getObjects().find(obj => obj.seq === seq);
    if (rect) {
      canvas.remove(rect);
      canvas.renderAll(); // Refresh the canvas
    }
    rects.value.splice(index, 1);
  }
};

const saveRects = () => {
  const jsonData = JSON.stringify(rects.value);
  console.log(jsonData);
  // 使用Axios发送jsonData到后端
};

const exportConfig = () => {
  const jsonData = JSON.stringify(rects.value, null, 2);
  const blob = new Blob([jsonData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'config.json';
  a.click();
  URL.revokeObjectURL(url);
};

const importConfig = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const json = JSON.parse(e.target.result);
      rects.value = json;
      canvas.clear();
      json.forEach((rectData) => {
        const rect = new fabric.Rect({
          left: rectData.rectArea[0],
          top: rectData.rectArea[1],
          width: rectData.rectArea[2],
          height: rectData.rectArea[3],
          fill: 'rgba(255, 0, 0, 0.5)',
          hasControls: true,
          hasBorders: true,
          selectable: true
        });
        rect.seq = rectData.seq;
        canvas.add(rect);

        rect.on('selected', () => {
          selectedRectSeq.value = rect.seq;
        });

        rect.on('deselected', () => {
          selectedRectSeq.value = null;
        });

        const updateRectArea = () => {
          const index = rects.value.findIndex(r => r.seq === rect.seq);
          rects.value[index].rectArea = `(${rect.left}, ${rect.top}, ${rect.width}, ${rect.height})`;
        };

        rect.on('modified', updateRectArea);
        rect.on('scaling', updateRectArea);
        rect.on('scaled', updateRectArea);
      });
      canvas.renderAll();
    };
    reader.readAsText(file);
  }
};

const setBackgroundImage = () => {
  canvas.clear();
  rects.value = [];
  fabric.Image.fromURL(imagePath.value, (img) => {
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
      scaleX: canvas.width / img.width,
      scaleY: canvas.height / img.height
    });
  });
};

onMounted(() => {
  canvas = new fabric.Canvas('canvas');
  setBackgroundImage();
});
</script>

<style scoped>
.rect-area-manage-view {
  width: 100%;
  display: flex;
}

.highlighted {
  background-color: yellow;
}

#canvas-container {
  width: 1080px;
  height: 1528px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.operationButton button {
  /* padding: 20px; */
  margin: 10px;
  font-size: medium;
}
</style>
