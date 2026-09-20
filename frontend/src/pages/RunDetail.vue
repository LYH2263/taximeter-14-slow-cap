<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, errText } from '../api'
const route = useRoute()
const run = ref(null)
const err = ref('')
const load = async () => {
  run.value = null
  err.value = ''
  try {
    run.value = await getJSON(`/api/history/${route.params.id}`)
  } catch (e) {
    err.value = errText(e)
  }
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template>
  <div class="page" v-if="run">
    <h1>记录 #{{ run.id }}</h1>
    <p class="hint">类型 {{ run.kind }} · 行程 {{ run.trip_id ?? '—' }} · {{ run.created_at }}</p>
    <template v-if="run.kind === 'compare'">
      <div class="panel" v-for="b in [['白天', run.result.day], ['夜间', run.result.night]]" :key="b[0]">
        <strong>{{ b[0] }}</strong>
        <p class="hero-num">¥{{ b[1].total }}</p>
        <p class="fee-row">起步 {{ b[1].start }} · 里程 {{ b[1].mileage }} · 低速 {{ b[1].slow_fee }}
          <span v-if="b[1].slow_fee_capped" class="badge badge-capped"
            >已截断（截断前 ¥{{ b[1].slow_fee_before }}，写入上限 ¥{{ b[1].slow_fee_cap ?? '—' }}）</span>
        </p>
      </div>
    </template>
    <div class="panel" v-else>
      <p class="hero-num">¥{{ run.result.total }}</p>
      <p class="fee-row">起步 {{ run.result.start }} · 里程 {{ run.result.mileage }} · 低速 {{ run.result.slow_fee }}
        <span v-if="run.result.slow_fee_capped" class="badge badge-capped"
          >已截断（截断前 ¥{{ run.result.slow_fee_before }}，写入上限 ¥{{ run.result.slow_fee_cap ?? '—' }}）</span>
      </p>
    </div>
    <p class="hint">以上为写入时快照，不随后续上限调整变化。</p>
  </div>
  <div class="page" v-else-if="err"><h1>记录</h1><p class="form-msg err">记录不存在（{{ err }}）</p></div>
</template>
