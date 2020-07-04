<template>
  <vul-detail :is-edit="false" />
</template>

<script>
import VulDetail from './components/VulDetail'

export default {
  name: 'CreateVulWorkflow',
  components: { VulDetail }
}
</script>