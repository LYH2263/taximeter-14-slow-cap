export async function getJSON(path) {
  const r = await fetch(path)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}
export async function postJSON(path, body) {
  const r = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}
export async function putJSON(path, body) {
  const r = await fetch(path, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

// 从后端错误体提取可展示信息（422 为 {"detail":[{"msg":...}]}，其余可能是纯文本）
export function errText(e) {
  try {
    const j = JSON.parse(e.message)
    if (Array.isArray(j.detail) && j.detail[0]?.msg) return j.detail[0].msg
    return e.message
  } catch {
    return e.message
  }
}
