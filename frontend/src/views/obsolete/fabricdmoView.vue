<template>
  <div class="container">
    <div class="image-area">
      <v-stage :config="stageConfig">
        <v-layer>
          <v-image :config="imageConfig" />
          <v-rect
            v-for="(rect, index) in rectangles"
            :key="rect.seq"
            :config="rect.config"
            @click="selectRect(index)"
            @dragend="updateRect(index, $event)"
            @transformend="updateRect(index, $event)"
            :draggable="true"
          />
          <v-transformer
            v-if="selectedRect !== null"
            :config="transformerConfig"
            :nodes="[rectangles[selectedRect].config]"
          />
        </v-layer>
      </v-stage>
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
          <tr
            v-for="(rect, index) in rectangles"
            :key="rect.seq"
            :class="{ selected: selectedRect === index }"
            @click="selectRect(index)"
          >
            <td>{{ rect.seq }}</td>
            <td><input v-model="rect.rectVarName" /></td>
            <td>{{ rect.config.x }}, {{ rect.config.y }}, {{ rect.config.width }}, {{ rect.config.height }}</td>
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
import { Stage, Layer, Rect, Transformer, Image as KonvaImage } from 'vue-konva';


const stageConfig = reactive({
  width: 1080,
  height: 720,
});

const imageConfig = reactive({
  image: null,
  width: 1080,
  height: 720,
});

const rectangles = ref([]);
const selectedRect = ref(null);

const loadImage = () => {
  const img = new Image();
  img.src = 'page_1.png';
  img.onload = () => {
    imageConfig.image = img;
  };
};

onMounted(() => {
  loadImage();
});

const addRect = () => {
  const seq = rectangles.value.length + 1;
  rectangles.value.push({
    seq,
    rectVarName: '',
    config: {
      x: 50,
      y: 50,
      width: 100,
      height: 100,
      fill: 'rgba(0,0,255,0.5)',
      draggable: true,
      transform: {
        rotate: 0,
      },
    },
    type: 'letter',
    language: 'zh',
  });
};

const selectRect = (index) => {
  selectedRect.value = index;
};

const updateRect = (index, event) => {
  const shape = event.target;
  rectangles.value[index].config = {
    ...rectangles.value[index].config,
    x: shape.x(),
    y: shape.y(),
    width: shape.width() * shape.scaleX(),
    height: shape.height() * shape.scaleY(),
    scaleX: 1,
    scaleY: 1,
  };
};

const saveRects = () => {
  const data = rectangles.value.map((rect) => ({
    seq: rect.seq,
    rectVarName: rect.rectVarName,
    rectArea: `${rect.config.x},${rect.config.y},${rect.config.width},${rect.config.height}`,
    type: rect.type,
    language: rect.language,
  }));
  console.log(JSON.stringify(data));
};

const transformerConfig = reactive({
  rotateEnabled: false,
  boundBoxFunc: (oldBox, newBox) => {
    // limit resize
    if (newBox.width < 20 || newBox.height < 20) {
      return oldBox;
    }
    return newBox;
  },
});
</script>

<style scoped>
.container {
  display: flex;
}
.image-area {
  width: 1080px;
}
.rect-list {
  margin-left: 20px;
}
.selected {
  background-color: yellow;
}
</style>
