import store from '@/store'

export default {
  inserted(el, binding, vnode) {
    const { value } = binding
    const role = store.getters && store.getters.role

    if (value && value instanceof Array && value.length > 0) {
      const permissionRoles = value

      const hasPermission = permissionRoles.includes(role)
      console.warn(hasPermission)

      if (!hasPermission) {
        el.parentNode && el.parentNode.removeChild(el)
        console.warn(23232)
      }
    } else {
      throw new Error(`need roles! Like v-permission="['admin','editor']"`)
    }
  }
}
