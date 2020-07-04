<template>
  <div class="app-container">
      <vul-table :status='status'></vul-table>
  </div>
</template>

<script>
  import VulTable from './components/VulTable'

  export default {
    name: 'VulListCreate',
    components: {
      VulTable
    },
    data() {
      return {
        status: 0
      }
    },
    created () {
      this.status = 0
    }
  }
</script>
