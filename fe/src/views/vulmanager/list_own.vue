<template>
  <div class="app-container">
      <vul-table :own="true"></vul-table>
  </div>
</template>

<script>
  import VulTable from './components/VulTable'

  export default {
    name: 'VulListOwn',
    components: {
      VulTable
    }
  }
</script>
