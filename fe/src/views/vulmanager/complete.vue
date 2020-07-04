<template>
  <vul-detail :is-edit="true" :completed="false" />
</template>

<script>
import VulDetail from './components/VulDetail'

export default {
  name: 'CompleteVulWorkflow',
  components: { VulDetail }
}
</script>