<template>
  <form>
    <v-file-upload v-model="formData" />
  </form>
  <pre>{{ formData?.length }}</pre>
</template>

<script setup lang="ts">
import { ref } from "vue"
import VFileUpload from "./VFileUpload.vue"

const formData = ref<FileList>()
</script>

<style lang="postcss"></style>
