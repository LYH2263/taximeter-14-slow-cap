<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getJSON, postJSON, errText } from '../api'
const route = useRoute()
const trip = ref(null)
const live = ref(null)   // 无历史快照时的实时试算结果
const err = ref('')

// 优先展示写入时的结算快照；无快照才实时试算
const fare = computed(() => trip.value?.fare ?? live.value)
const fromSnapshot = computed(() => !!(trip.value && trip.value.fare))

const load = async () => {
  trip.value = null
  live.value = null
  err.value = ''
  try {
    trip.value = await getJSON(`/api/trips/${route.params.id}`)
    if (!trip.value.fare) {
      live.value = await postJSON('/api/fare', {
        distance_km: trip.value.distance_km, slow_min: trip.value.slow_min,
        night: !!trip.value.night, trip_id: trip.value.id, persist: false,
      })
    }
  } catch (e) {
    err.value = errText(e)
  }
}
onMounted(load); watch(() => route.params.id, load)
</script>
<template>
  <div class="page" v-if="trip">
    <h1>{{ trip.label }}</h1>
    <p class="hint">
      <template v-if="fromSnapshot">结算时快照（写入上限 ¥{{ fare.slow_fee_cap ?? '—' }}），
        <router-link :to="'/history/' + trip.fare_run_id">查看记录 #{{ trip.fare_run_id }}</router-link>
      </template>
      <template v-else>无历史快照，以下为按当前上限的实时试算（不落记录）</template>
    </p>
    <p class="hero-num">¥{{ fare?.total }}</p>
    <p class="fee-row">起步 {{ fare?.start }} · 里程 {{ fare?.mileage }} ·
      低速 {{ fare?.slow_fee }}
      <span v-if="fare?.slow_fee_capped" class="badge badge-capped"
        >已截断（截断前 ¥{{ fare.slow_fee_before }}，上限 ¥{{ fare.slow_fee_cap ?? '—' }}）</span>
    </p>
    <p v-if="err" class="form-msg err">{{ err }}</p>
  </div>
  <div class="page" v-else-if="err"><h1>行程</h1><p class="form-msg err">{{ err }}</p></div>
</template>
