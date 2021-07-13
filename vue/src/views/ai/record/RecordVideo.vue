<template>
  <v-title title="Video Analysis"></v-title>
  <img src="" alt="stream" ref="imgRef" class="rounded-2xl" />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import VTitle from '~/components/base/VTitle.vue'
import { useSocketService } from '~/composable/useSocketService'

const imgRef = ref() as Ref<HTMLImageElement>

const socketService = useSocketService()

socketService.readVideo(imgRef)
</script>

<style lang="postcss" scoped></style>
