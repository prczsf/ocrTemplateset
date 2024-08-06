<template>
    <div class="whole-container">
        <h1>OCR 演示</h1>
        <div class="file-setting">
            <input type="file" @change="handleFileUpload" accept=".json">
            <input type="text" v-model="imageName" placeholder="输入已经保存在后台的图片名称（不含扩展名）">
            <select v-model="imageName">
                <option value="moban">moban.png</option>
                <option value="andan">andan.png</option>
                <option value="fenguanghuifafen1">fenguanghuifafen1.png</option>
                <option value="fenguanghuifafen2">fenguanghuifafen2.png</option>
                <option value="fenguanghuifafen3">fenguanghuifafen3.png</option>
                <option value="fenguanghuifafen4">fenguanghuifafen4.png</option>
                <option value="fenguangliuhuawu">fenguangliuhuawu.png</option>
                <option value="fenuangqinghua">fenuangqinghua.png</option>
                <option value="huaxuexuyang828">huaxuexuyang828.png</option>
                <option value="huaxuexuyang3991">huaxuexuyang3991.png</option>
                <option value="huaxuexuyang3992">huaxuexuyang3992.png</option>
                <option value="wurishenghua">wurishenghua.png</option>
                <option value="xuanfuwu">xuanfuwu.png</option>
            </select>

            <button @click="startRecognition">开始识别</button>
        </div>

        <div class="return-container">
            <div v-if="imageSrc" class="image-container">
                <h2>图片预览</h2>
                <img :src="imageSrc" alt="图片预览" style="max-width: 100%;">
            </div>
            <div class="result-container">
                <div v-if="bodyResults.length">
                    <h2>表格数据</h2>
                    <div v-for="item in bodyResults" :key="item.seq">
                        <div v-html="item.rectVarValue" border="1px"></div>
                    </div>
                </div>
                <div v-if="otherResults.length">
                    <h2>其他数据</h2>
                    <table border="1px">
                        <thead>
                            <tr>
                                <th>序号</th>
                                <th>变量名称</th>
                                <th>矩形区域</th>
                                <th>类型</th>
                                <th>设置检测语言</th>
                                <th>校正规则</th>
                                <th>矩形变量值</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in otherResults" :key="item.seq">
                                <td>{{ item.seq }}</td>
                                <td>{{ item.rectVarName }}</td>
                                <td>{{ item.rectArea }}</td>
                                <td>{{ item.type }}</td>
                                <td>{{ item.language }}</td>
                                <td>{{ item.correctRule }}</td>
                                <td>{{ item.rectVarValue }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>

        </div>


    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const jsonFile = ref(null);
const imageName = ref('');
const bodyResults = ref([]);
const otherResults = ref([]);
const imageSrc = ref('');

const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        jsonFile.value = JSON.parse(e.target.result);
    };
    reader.readAsText(file);
};

const startRecognition = async () => {
    bodyResults.value = "";
    otherResults.vale = "";
    if (!jsonFile.value || !imageName.value) {
        alert('请上传 JSON 文件并输入图片名称。');
        return;
    }

    const formData = new FormData();
    formData.append('json', JSON.stringify(jsonFile.value));
    formData.append('image_name', imageName.value);

    try {
        const response = await axios.post('api/paddleoffline', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        // 分离数据
        bodyResults.value = response.data.filter(item => item.type === 'body');
        otherResults.value = response.data.filter(item => item.type !== 'body');

        // 获取并显示图片
        imageSrc.value = `api/filesPic/${imageName.value}/page_1.png`;
    } catch (error) {
        console.error(error);
        alert('处理请求时发生错误。');
    }
}
</script>


<style scoped>
/* 在这里添加任何需要的样式 */

.whole-container {
    display: flex;
    flex-direction: column;
}

.return-container {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: row;
}

.image-container {
    width: 100%;
}
</style>
