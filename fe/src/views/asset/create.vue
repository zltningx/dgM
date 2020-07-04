<template>
  <asset-detail :is-edit="false" />
</template>

<script>
import AssetDetail from './components/AssetDetail'

export default {
  name: 'CreateAssetDetail',
  components: { AssetDetail }
}
</script>