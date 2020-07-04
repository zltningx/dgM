<template>
  <div class="app-container">
      <asset-table></asset-table>
  </div>
</template>

<script>
  import AssetTable from './components/AssetTable'

  export default {
    name: 'AssetListAll',
    components: {
      AssetTable
    }
  }
</script>
