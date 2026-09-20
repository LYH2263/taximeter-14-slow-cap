<script setup>
import { ref } from 'vue'
import { postJSON, errText } from '../api'
const distance_km = ref(18)
const slow_min = ref(12)
const c = ref(null)
const err = ref('')
const run = async () => {
  err.value = ''
  try {
    // 对比为分析功能：只读试算，不写记录
    c.value = await postJSON('/api/compare', { distance_km: distance_km.value, slow_min: slow_min.value, persist: false })
  } catch (e) {
    err.value = errText(e)
  }
}
const block = (t, f) => ({ t, f })
</script>
<template>
  <div class="page"><h1>昼夜对比</h1>
    <div class="panel">
      <label>公里 <input type="number" v-model.number="distance_km" /></label>
      <label>低速分钟 <input type="number" v-model.number="slow_min" /></label>
      <div><button @click="run">对比</button></div>
    </div>
    <div v-if="c" class="panel">
      <p>白天 ¥{{ c.day_total }} · 夜间 ¥{{ c.night_total }} · 差 ¥{{ c.delta }}</p>
      <div v-for="b in [block('白天', c.day), block('夜间', c.night)]" :key="b.t" class="detail-block">
        <strong>{{ b.t }}</strong>（系数 {{ b.f.night_factor }}）
        <p class="fee-row">起步 {{ b.f.start }} · 里程 {{ b.f.mileage }} · 低速 {{ b.f.slow_fee }}
          <span v-if="b.f.slow_fee_capped" class="badge badge-capped"
            >已截断（截断前 ¥{{ b.f.slow_fee_before }}，上限 ¥{{ b.f.slow_fee_cap }}）</span>
          <span v-else class="badge">未截断</span>
        </p>
      </div>
    </div>
    <p v-if="err" class="form-msg err">{{ err }}</p>
  </div>
</template>
