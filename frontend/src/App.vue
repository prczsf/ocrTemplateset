<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->
    <div class="wrapper">
      <nav>
        <RouterLink to="/">首页</RouterLink>
        <RouterLink to="/rectareamanage">识别模板管理</RouterLink>
        <RouterLink to="/tablerecgonize">基于模板识别表格</RouterLink>
        <!-- <RouterLink to="/tablercalibration">手工调整表格</RouterLink> -->
        <RouterLink to="/reportgeneration">报告生成</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    display: flex; /* 启用 Flexbox 布局 */
    justify-content: space-between; /* 水平方向上平均分配剩余空间 */
    align-items: center; /* 垂直居中对齐 */
  }

  /* 如果需要，可以添加额外的样式，例如间距 */
  nav a {
    padding: 20px;
    font-size: large;
  }
  /* nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  } */
}
</style>
