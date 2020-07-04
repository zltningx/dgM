<template>
  <asset-detail :is-edit="true" />
</template>

<script>
import AssetDetail from './components/AssetDetail'

export default {
  name: 'EditAssetDetail',
  components: { AssetDetail }
}
</script>