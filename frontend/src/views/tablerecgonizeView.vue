<template>
    <div class="whole-container">
        <h1>OCR 演示</h1>
        <p>工单号码：{{ $route.params.wordorder}}</p>
        <div class="file-setting">
            <span>导入区域识别模板：</span>
            <input type="file" @change="handleFileUpload" accept=".json">
            <span>后台已经存储的待识别图片选择：</span>
            <input type="text" v-model="imageName" placeholder="输入已经保存在后台的图片名称（不含扩展名）">
            <select v-model="imageName" @change="setImage">
                <!-- <option value="calibration1">calibration1.png</option>
                <option value="calibration2">calibration2.png</option>
                <option value="calibration3">calibration3.png</option>
                <option value="calibration4">calibration4.png</option>
                <option value="calibration5">calibration5.png</option>
                <option value="calibration6">calibration6.png</option>-->
                <option value="moban">moban.png</option> 
                <option value="andan">andan.png</option>
                <option value="selfHand0809">selfHand0809.png</option> 
                <option value="selfHandFang01">selfHandFang01.png</option> 
                <option value="selfHandFang02">selfHandFang02.png</option> 
                <option value="selfHandFang03">selfHandFang03.png</option> 
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
                <option value="andan0809">andan0809.png</option>
                <option value="codcr0809">codcr0809.png</option>
                <option value="fenguangguangdu0809">fenguangguangdu0809.png</option>
                <option value="xuanfuwu0809">xuanfuwu0809.png</option>
                <option value="youceding0809">youceding0809.png</option>    
            </select>

            <button @click="startRecognition">开始识别</button>
        </div>

        <div class="return-container">

            <div class="image-container">
                <h2>图片预览</h2>
                <img :src="imageSrc" v-if="imageSrc"  alt="图片预览" width="1080px">
            </div>
            <div class="result-container">


                <div v-if="otherResults.length" class="tableArea">
                    <h2>批次数据</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>序号</th>
                                <th>变量名称</th>
                                <th>矩形区域</th>
                                <th>类型</th>
                                <th>设置检测语言</th>
                                <th>校正规则</th>
                                <th>矩形变量值</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in otherResults" :key="item.seq">
                                <td>{{ item.seq }}</td>
                                <td><input v-model="item.rectVarName"></td>
                                <td><input v-model="item.rectArea"></td>
                                <td><input v-model="item.type"></td>
                                <td><input v-model="item.language"></td>
                                <td><input v-model="item.correctRule"></td>
                                <td><input v-model="item.rectVarValue"></td>
                                <td><button @click="removeOtherResult(index)">删除</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-if="bodyResults.length"  class="tableArea">
                    <h2>样品测试数据</h2>
                    <div v-for="item in bodyResults" :key="item.seq">
                        <div v-html="item.rectVarValue" style="border: 1px solid black;" id="bodyResult"></div>
                    </div>
                    <!-- <div v-for="(item, index) in bodyResults" :key="item.seq">
                        <div contenteditable="true" @input="updateBodyResult(index, $event)">{{ item.rectVarValue }}</div>
                        <button @click="removeBodyResult(index)">删除</button>
                    </div> -->
                </div>
                <div>
                <el-button type="primary">保存提交</el-button>
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


const setImage=()=>{
    console.log(imageName.value);
    imageSrc.value = `api/filesPic/${imageName.value}/page_1.png`;
}
const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        jsonFile.value = JSON.parse(e.target.result);
    };
    reader.readAsText(file);
};

const startRecognition = async () => {
    bodyResults.value = [];
    otherResults.value = [];
    if (!jsonFile.value || !imageName.value) {
        alert('请上传 JSON 文件并输入图片名称。');
        return;
    }

    const formData = new FormData();
    formData.append('json', JSON.stringify(jsonFile.value));
    formData.append('image_name', imageName.value);
    imageSrc.value = `api/filesPic/${imageName.value}/page_1.png`;

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
    } catch (error) {
        console.error(error);
        alert('处理请求时发生错误。');
    }
};

const removeOtherResult = (index) => {
    otherResults.value.splice(index, 1);
};

const removeBodyResult = (index) => {
    bodyResults.value.splice(index, 1);
};

const updateBodyResult = (index, event) => {
    bodyResults.value[index].rectVarValue = event.target.innerText;
};
</script>

<style scoped>
.whole-container {
    display: flex;
    flex-direction: column;
}

.return-container {
    display: flex;
    justify-content: flex-start;
    align-items: left;
    flex-direction: row;
}

.result-container{
    width: 100%;
    align-items: left;
}

.image-container {
    width: 100%;
}
table, th, td
{
    border: 1px solid black;
}
.tableArea{
    width: 100%;
    align-items: left;
}

#bodyResult td {
    border: 1px solid black;
}
</style>
