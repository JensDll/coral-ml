<template>
  <div v-if="state.loading">Loading</div>
  <div v-else-if="state.responseOk">
    <div v-for="model in state.data?.data">{{ model.modelName }}</div>
  </div>
</template>

<script setup lang="ts">
import type { EnumerableEnvelope, TFLiteModel } from "../../api/types"
import { useFetch } from "../../composition/useFetch"

const state = useFetch<EnumerableEnvelope<TFLiteModel>>("/model")
  .get()
  .json(true)
</script>

<style lang=""></style>
