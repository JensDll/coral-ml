<template>
  <h1>Stream</h1>
  <img alt="stream" :src="src" />
  <img alt="stream" :src="src" />
  <img alt="stream" :src="src" />
  <img alt="stream" :src="src" />
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  data() {
    return {
      src: "http://localhost:8001/video",
    };
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
