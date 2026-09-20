<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const distance_km = ref(8)
const slow_min = ref(3)
const night = ref(false)
const out = ref(null)
const run = async () => { out.value = await postJSON('/api/fare', { distance_km: distance_km.value, slow_min: slow_min.value, night: night.value, persist: true }) }
</script>
<template>
  <div class="page"><h1>打表试算</h1>
    <div class="panel">
      <label>公里 <input type="number" v-model.number="distance_km" /></label>
      <label>低速分钟 <input type="number" v-model.number="slow_min" /></label>
      <label><input type="checkbox" v-model="night" /> 夜间</label>
      <button @click="run">计算</button>
    </div>
    <template v-if="out">
      <p class="hero-num">¥{{ out.total }}</p>
      <div class="panel">
        <p>起步 {{ out.start }} · 里程 {{ out.mileage }} · 低速 {{ out.slow_fee }}</p>
        <p v-if="out.slow_fee_truncated">低速费已截断：截断前 ¥{{ out.slow_fee_before_cap }} → 截断后 ¥{{ out.slow_fee }}（上限 ¥{{ out.slow_fee_cap }}）</p>
        <p v-else>低速费未截断（上限 ¥{{ out.slow_fee_cap }}）</p>
      </div>
    </template>
  </div>
</template>
