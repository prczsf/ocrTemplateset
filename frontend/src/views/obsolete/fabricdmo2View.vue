<template>
  <div class="container">
    <div class="image-area" ref="canvasContainer">
      <canvas id="canvas"></canvas>
    </div>
    <div class="rect-list">
      <button @click="addRect">添加新的矩形框</button>
      <table>
        <thead>
          <tr>
            <th>Seq</th>
            <th>RectVarName</th>
            <th>RectArea</th>
            <th>Type</th>
            <th>Language</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rect, index) in rects" :key="index" @click="selectRect(index)" :class="{highlight: selectedRect === index}">
            <td>{{ rect.seq }}</td>
            <td><input v-model="rect.rectVarName" /></td>
            <td>{{ rect.rectArea }}</td>
            <td>
              <select v-model="rect.type">
                <option value="letter">字母</option>
                <option value="number">数字</option>
                <option value="character">字符</option>
                <option value="mixed">混合</option>
              </select>
            </td>
            <td>
              <select v-model="rect.language">
                <option value="zh">中文</option>
                <option value="en">英文</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="saveRects">保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { fabric } from 'fabric';


const canvasContainer = ref(null);
const rects = reactive([]);
let canvas;
let selectedRect = ref(null);

onMounted(() => {
  canvas = new fabric.Canvas('canvas', {
    width: 1080,
    height: 720,
    backgroundColor: 'white',
  });

  fabric.Image.fromURL('page_1.png', (img) => {
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
      scaleX: canvas.width / img.width,
      scaleY: canvas.height / img.height,
    });
  });
});

const addRect = () => {
  const rect = new fabric.Rect({
    left: 100,
    top: 100,
    width: 60,
    height: 70,
    fill: 'rgba(255, 0, 0, 0.5)',
    selectable: true,
  });
  canvas.add(rect);
  const seq = rects.length + 1;
  rects.push({
    seq,
    rectVarName: `rect${seq}`,
    rectArea: `${rect.left},${rect.top},${rect.width},${rect.height}`,
    type: 'mixed',
    language: 'zh',
  });
  rect.on('selected', () => {
    selectedRect.value = seq - 1;
  });
};

const selectRect = (index) => {
  selectedRect.value = index;
  const rect = canvas.getObjects()[index];
  canvas.setActiveObject(rect);
};

const saveRects = () => {
  const json = JSON.stringify(rects);
  // 发送到后台
  console.log(json);
};
</script>

<style scoped>
.container {
  display: flex;
}
.image-area {
  width: 1080px;
  border: 1px solid #ccc;
}
.rect-list {
  margin-left: 20px;
}
.highlight {
  background-color: yellow;
}
</style>
