<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const detail = ref(null)
const err = ref('')
const open = async (id) => {
  err.value = ''
  try { detail.value = await getJSON(`/api/history/${id}`) }
  catch (e) { detail.value = null; err.value = `记录 #${id} 不存在` }
}
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template>
  <div class="page"><h1>记录</h1>
    <table><tr v-for="h in items" :key="h.id" @click="open(h.id)"><td>#{{ h.id }}</td><td>{{ h.kind }}</td></tr></table>
    <p v-if="err" class="err">{{ err }}</p>
    <div v-if="detail" class="panel">
      <h2>#{{ detail.id }} {{ detail.kind }}</h2>
      <template v-if="detail.kind === 'compare'">
        <p>写入时上限：¥{{ detail.result.slow_fee_cap ?? '—' }}</p>
        <p>白天低速截断：{{ detail.result.day_slow_fee_truncated ? '是' : '否' }} · 夜间低速截断：{{ detail.result.night_slow_fee_truncated ? '是' : '否' }}</p>
      </template>
      <template v-else>
        <p>写入时上限：¥{{ detail.result.slow_fee_cap ?? '—' }} · 低速截断：{{ detail.result.slow_fee_truncated ? '是' : '否' }}</p>
        <p v-if="detail.result.slow_fee_before_cap !== undefined">截断前 ¥{{ detail.result.slow_fee_before_cap }} → 截断后 ¥{{ detail.result.slow_fee }}</p>
      </template>
      <p>应付 ¥{{ detail.result.total ?? detail.result.night_total }}</p>
    </div>
  </div>
</template>
