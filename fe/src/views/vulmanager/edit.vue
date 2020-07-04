<template>
  <vul-detail :is-edit="true" />
</template>

<script>
import VulDetail from './components/VulDetail'

export default {
  name: 'EditVulWorkflow',
  components: { VulDetail }
}
</script>