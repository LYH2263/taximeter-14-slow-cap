<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON, errText } from '../api'
const s = ref({})
const capInput = ref(null)
const savedCap = ref(null)
const msg = ref('')
const msgType = ref('')

onMounted(async () => {
  s.value = await getJSON('/api/settings')
  capInput.value = s.value.slow_fee_cap
  savedCap.value = s.value.slow_fee_cap
})

const save = async () => {
  const v = Number(capInput.value)
  // 前端正数预校验：非法直接拒绝，不发请求
  if (!Number.isFinite(v) || v <= 0) {
    msg.value = '请输入正数上限（大于 0）'
    msgType.value = 'err'
    capInput.value = savedCap.value
    return
  }
  try {
    const r = await putJSON('/api/settings', { slow_fee_cap: v })
    savedCap.value = r.slow_fee_cap
    capInput.value = r.slow_fee_cap
    s.value = r
    msg.value = '已保存'
    msgType.value = 'ok'
  } catch (e) {
    // 保存失败：原值不变，输入框回填服务器当前值
    msg.value = '保存失败：' + errText(e)
    msgType.value = 'err'
    capInput.value = savedCap.value
  }
}
</script>
<template>
  <div class="page">
    <h1>设置</h1>
    <div class="panel">
      <p class="hint">计价货币：{{ s.currency }}</p>
      <label>低速费上限（元，正数）
        <input type="number" min="0" step="0.01" v-model.number="capInput" />
      </label>
      <div><button @click="save">保存</button></div>
      <p v-if="msg" class="form-msg" :class="msgType">{{ msg }}</p>
    </div>
  </div>
</template>
