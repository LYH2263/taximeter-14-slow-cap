<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const cap = ref('')
const msg = ref('')
const err = ref('')
const load = async () => {
  s.value = await getJSON('/api/settings')
  cap.value = Number(s.value.slow_fee_cap)
}
const save = async () => {
  msg.value = ''; err.value = ''
  const v = Number(cap.value)
  if (!Number.isFinite(v) || v <= 0) {
    err.value = '低速费上限必须为正数，未保存'
    await load()
    return
  }
  try {
    const r = await putJSON('/api/settings/slow-fee-cap', { slow_fee_cap: v })
    msg.value = `已保存，低速费上限 ¥${r.slow_fee_cap}`
  } catch (e) {
    err.value = '保存失败，上限未修改，仍为原值'
  }
  await load()
}
onMounted(load)
</script>
<template>
  <div class="page"><h1>设置</h1>
    <div class="panel">
      <label>低速费上限 <input type="number" v-model.number="cap" min="0.01" step="0.01" /></label>
      <button @click="save">保存</button>
      <p v-if="msg" class="ok">{{ msg }}</p>
      <p v-if="err" class="err">{{ err }}</p>
    </div>
    <pre>{{ s }}</pre>
  </div>
</template>
