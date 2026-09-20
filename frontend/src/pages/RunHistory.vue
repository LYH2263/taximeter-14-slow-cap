<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/history')).items })
</script>
<template>
  <div class="page"><h1>记录</h1>
    <table>
      <tr><th>编号</th><th>类型</th><th>行程</th><th>时间</th></tr>
      <tr v-for="h in items" :key="h.id">
        <td><router-link :to="'/history/' + h.id">#{{ h.id }}</router-link></td>
        <td>{{ h.kind }}</td>
        <td>{{ h.trip_id ?? '—' }}</td>
        <td>{{ h.created_at }}</td>
      </tr>
    </table>
  </div>
</template>
