<script setup>
import { ref } from 'vue'
import { postJSON, errText } from '../api'
const distance_km = ref(8)
const slow_min = ref(3)
const night = ref(false)
const out = ref(null)
const err = ref('')

const calc = async (persist) => {
  err.value = ''
  try {
    out.value = await postJSON('/api/fare', {
      distance_km: distance_km.value, slow_min: slow_min.value, night: night.value, persist,
    })
  } catch (e) {
    err.value = errText(e)
  }
}
</script>
<template>
  <div class="page"><h1>打表试算</h1>
    <div class="panel">
      <label>公里 <input type="number" v-model.number="distance_km" /></label>
      <label>低速分钟 <input type="number" v-model.number="slow_min" /></label>
      <label><input type="checkbox" v-model="night" /> 夜间</label>
      <div>
        <button @click="calc(false)">试算</button>
        <button @click="calc(true)" style="margin-left:.5rem">结算</button>
      </div>
      <p v-if="err" class="form-msg err">{{ err }}</p>
    </div>
    <div v-if="out" class="panel">
      <p class="hero-num">¥{{ out.total }}</p>
      <p class="fee-row">起步 {{ out.start }} · 里程 {{ out.mileage }} ·
        低速 {{ out.slow_fee }}
        <span v-if="out.slow_fee_capped" class="badge badge-capped"
          >已按上限 ¥{{ out.slow_fee_cap }} 截断（原价 ¥{{ out.slow_fee_before }}）</span>
      </p>
      <p v-if="out.run_id" class="hint">
        结算单号 <router-link :to="'/history/' + out.run_id">#{{ out.run_id }}</router-link>
      </p>
      <p v-else class="hint">只读试算，未写入记录</p>
    </div>
  </div>
</template>
