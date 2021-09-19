<template>
  <div class="mb-8">
    <BaseTitle title="Quick Start with Artificial Intelligence" />
  </div>
  <p>Start by trying out some models or take a look at the video stream.</p>
  <div class="flex flex-col mt-6 xs:flex-row">
    <BaseButton
      type="primary"
      class="px-4 py-2 font-semibold rounded-md"
      @click="router.push({ name: 'record' })"
    >
      Manage Models
    </BaseButton>
    <BaseButton
      type="secondary"
      class="px-4 py-2 mt-4 font-semibold rounded-md xs:mt-0 xs:ml-4"
      @click="router.push({ name: 'video-analysis' })"
    >
      Video Stream
    </BaseButton>
  </div>
</template>

<script lang="ts" setup>
import BaseTitle from '~/components/base/BaseTitle.vue'
import BaseButton from '~/components/base/BaseButton.vue'
import { useRouter } from 'vue-router'
const x: number = ''
const router = useRouter()
</script>

<style lang="scss"></style>
