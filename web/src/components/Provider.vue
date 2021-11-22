<script setup lang="ts">
import { NConfigProvider, NLoadingBarProvider, darkTheme } from 'naive-ui'
import { isDark } from '~/composables'
</script>

<template>
  <n-config-provider :theme="isDark ? darkTheme : undefined">
    <n-loading-bar-provider>
      <slot></slot>
    </n-loading-bar-provider>
  </n-config-provider>
</template>
