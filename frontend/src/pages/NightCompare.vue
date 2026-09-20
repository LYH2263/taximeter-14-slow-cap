<script setup>
import { ref } from 'vue'
import { postJSON } from '../api'
const distance_km = ref(18)
const slow_min = ref(12)
const c = ref(null)
const run = async () => { c.value = await postJSON('/api/compare', { distance_km: distance_km.value, slow_min: slow_min.value, persist: true }) }
</script>
<template>
  <div class="page"><h1>昼夜对比</h1>
    <button @click="run">对比</button>
    <div v-if="c" class="panel">
      <p>白天 ¥{{ c.day_total }}（低速截断：{{ c.day_slow_fee_truncated ? '是' : '否' }}） · 夜间 ¥{{ c.night_total }}（低速截断：{{ c.night_slow_fee_truncated ? '是' : '否' }}） · 差 ¥{{ c.delta }}</p>
      <p>夜间低速费先乘系数 {{ c.night.night_factor }} 再封顶：截断前 ¥{{ c.night.slow_fee_before_cap }} → 截断后 ¥{{ c.night.slow_fee }}（上限 ¥{{ c.slow_fee_cap }}）</p>
    </div>
  </div>
</template>
